import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from flask import jsonify, request
from pymongo.errors import OperationFailure

from api.middleware.mongo import get_mongo
from api.models.incentive_cache import DataIncentiveCache, IncentiveCache
from api.utils.db_incentives import init_incentives_collection
from api.utils.openai import client
from api.utils.scrapper import IncentivesScraper
from api.utils.session import get_current_user

logger = logging.getLogger(__name__)
CACHE_DURATION = timedelta(hours=168)


def get_cached_incentives() -> Optional[Dict]:
    """Get cached incentives if they exist and are not expired"""
    try:
        mongo = get_mongo()
        cache_threshold = datetime.utcnow() - CACHE_DURATION
        cached_data = mongo.db[DataIncentiveCache.Config.collection].find_one(
            {"last_updated": {"$gt": cache_threshold}, "data_type": "cached"}, {"_id": 0}
        )
        return cached_data if cached_data else None
    except OperationFailure:
        logger.warning("Cache collection not initialized, initializing now...")
        init_incentives_collection()
        return None
    except Exception as e:
        logger.error(f"Error getting cached incentives: {str(e)}", exc_info=True)
        return None


def update_cache(incentives: List[IncentiveCache]):
    """Update the incentives cache"""
    try:
        mongo = get_mongo()
        collection = mongo.db[DataIncentiveCache.Config.collection]
        incentive_dicts = []
        for incentive in incentives:
            incentive_dict = incentive.dict()
            incentive_dict["data_type"] = "cached"
            incentive_dicts.append(incentive_dict)

        cache_entry = DataIncentiveCache(data=incentive_dicts, last_updated=datetime.utcnow(), data_type="cached")

        collection.delete_many({"data_type": "cached"})
        collection.insert_one(cache_entry.dict())

        logger.info(f"Cache updated successfully with {len(incentives)} incentives")
    except Exception as e:
        logger.error(f"Error updating incentives cache: {str(e)}", exc_info=True)


def scrapper_incentives_get(force_refresh: bool = False):
    try:
        if not force_refresh:
            logger.info("Checking cache")
            cached_data = get_cached_incentives()
            if cached_data:
                logger.info("Returning cached incentives data")
                return jsonify(
                    {
                        "success": True,
                        "data": cached_data["data"],
                        "last_updated": cached_data["last_updated"],
                        "cached": True,
                    }
                )

        logger.info("Fetching fresh data" if force_refresh else "No valid cache found, scraping new data")
        scraper = IncentivesScraper()
        incentives, bonus_data = scraper.scrape_incentives()

        update_cache(incentives)
        return jsonify(
            {
                "success": True,
                "data": [incentive.dict(exclude={"bonus_data"}) for incentive in incentives],
                "cached": False,
            }
        )

    except ValueError as e:
        logger.error(f"Invalid region provided: {str(e)}")
        return jsonify({"success": False, "error": f"Invalid region: {str(e)}"}), 400

    except Exception as e:
        logger.error(f"Error scraping incentives: {str(e)}", exc_info=True)
        return jsonify({"success": False, "error": f"Failed to scrape incentives: {str(e)}"}), 500


def scrapper_incentive_get(incentive_id: str):
    """Get a single incentive by ID"""
    try:
        current_user = get_current_user()
        mongo = get_mongo()

        incentive = mongo.db[IncentiveCache.Config.collection].find_one(
            {"id": incentive_id, "user_id": current_user.id}, {"_id": 0}
        )

        if not incentive:
            return jsonify({"success": False, "error": "Incentive not found or unauthorized"}), 404

        return jsonify({"success": True, "data": incentive})

    except Exception as e:
        logger.error(f"Error fetching incentive: {str(e)}", exc_info=True)
        return jsonify({"success": False, "error": f"Failed to fetch incentive: {str(e)}"}), 500


def scrapper_incentive_update(incentive_id: str):
    """Update a single incentive"""
    try:
        current_user = get_current_user()
        mongo = get_mongo()

        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        existing_incentive = mongo.db[IncentiveCache.Config.collection].find_one(
            {"id": incentive_id, "user_id": current_user.id}, {"_id": 0}
        )

        if not existing_incentive:
            return jsonify({"success": False, "error": "Incentive not found or unauthorized"}), 404

        data["data_type"] = existing_incentive.get("data_type", "user")
        data["user_id"] = current_user.id

        try:
            incentive = IncentiveCache(**data)
        except Exception as e:
            return jsonify({"success": False, "error": f"Invalid data format: {str(e)}"}), 400

        result = mongo.db[IncentiveCache.Config.collection].update_one(
            {"id": incentive_id, "user_id": current_user.id}, {"$set": incentive.dict()}
        )

        if result.matched_count == 0:
            return jsonify({"success": False, "error": "Incentive not found or unauthorized"}), 404

        # Convert user object to dict for JSON serialization
        user_dict = {"id": current_user.id, "username": current_user.username, "subscriber": current_user.subscriber}

        return jsonify({"success": True, "message": "Incentive updated successfully", "user": user_dict})

    except Exception as e:
        logger.error(f"Error updating incentive: {str(e)}", exc_info=True)
        return jsonify({"success": False, "error": f"Failed to update incentive: {str(e)}"}), 500


def scrapper_incentive_delete(incentive_id: str):
    try:
        current_user = get_current_user()
        mongo = get_mongo()
        result = mongo.db[IncentiveCache.Config.collection].delete_one({"id": incentive_id, "user_id": current_user.id})

        if result.deleted_count == 0:
            return jsonify({"success": False, "error": "Incentive not found or unauthorized"}), 404

        return jsonify({"success": True, "message": "Incentive deleted successfully"})

    except Exception as e:
        logger.error(f"Error deleting incentive: {str(e)}", exc_info=True)
        return jsonify({"success": False, "error": f"Failed to delete incentive: {str(e)}"}), 500


def scrapper_incentive_create_v2():
    try:
        current_user = get_current_user()
        mongo = get_mongo()

        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        data["user_id"] = current_user.id
        data["data_type"] = "user"

        if mongo.db[IncentiveCache.Config.collection].find_one({"id": data.get("id"), "user_id": current_user.id}):
            return (
                jsonify(
                    {"success": False, "error": f"Incentive with ID {data.get('id')} already exists for this user"}
                ),
                409,
            )

        try:
            incentive = IncentiveCache(**data)
        except Exception as e:
            return jsonify({"success": False, "error": f"Invalid data format: {str(e)}"}), 400

        incentive_dict = incentive.dict()
        mongo.db[IncentiveCache.Config.collection].insert_one(incentive_dict)

        # Convert user object to dict for JSON serialization
        user_dict = {"id": current_user.id, "username": current_user.username, "subscriber": current_user.subscriber}

        return jsonify(
            {"success": True, "message": "Incentive created successfully", "data": incentive_dict, "user": user_dict}
        )

    except Exception as e:
        logger.error(f"Error creating incentive: {str(e)}", exc_info=True)
        return jsonify({"success": False, "error": f"Failed to create incentive: {str(e)}"}), 500


def scrapper_incentives_all():
    try:
        current_user = get_current_user()
        mongo = get_mongo()

        incentives = list(mongo.db[IncentiveCache.Config.collection].find({"user_id": current_user.id}, {"_id": 0}))

        return jsonify(
            {
                "success": True,
                "data": incentives,
                "total": len(incentives),
            }
        )

    except Exception as e:
        logger.error(f"Error fetching user incentives: {str(e)}", exc_info=True)
        return jsonify({"success": False, "error": f"Failed to fetch incentives: {str(e)}"}), 500


def scrapper_analyze(body):
    try:
        if not body or "url" not in body:
            raise Exception("URL is required in request body")

        url = body["url"]
        mongo = get_mongo()
        cache_collection = mongo.db.scraper_cache

        cached_result = cache_collection.find_one(
            {"url": url, "timestamp": {"$gt": datetime.utcnow() - timedelta(hours=100)}}
        )

        if cached_result:
            logger.info(f"Cache hit for {url}")
            return jsonify({"success": True, "text": cached_result["content"], "cached": True})

        scraper = IncentivesScraper()
        try:
            text = scraper.scrape_webpage_text(url)
        except Exception as e:
            error_msg = str(e)
            if "timed out" in error_msg.lower():
                error_msg = "The webpage took too long to respond. Please try again later."
            return jsonify({"success": False, "error": error_msg}), 500

        try:
            cache_collection.update_one(
                {"url": url}, {"$set": {"content": text, "timestamp": datetime.utcnow()}}, upsert=True
            )
        except Exception as e:
            logger.error(f"Cache update error: {str(e)}")

        return jsonify({"success": True, "text": text, "cached": False})

    except Exception as e:
        logger.error(f"Error scraping text: {str(e)}", exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500


def scrapper_analyze_text():
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"success": False, "error": "Text is required in request body"}), 400

        text = data["text"]
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """

                    Analizza il bando e sviluppa un piano aziendale dettagliato. Utilizza questa struttura precisa:

                                1. SOMMARIO ESECUTIVO
                                - Sintesi del progetto
                                - Obiettivi principali
                                - Vantaggio competitivo

                                2. INFORMAZIONI SULL'IMPRESA
                                - Dati aziendali
                                - Struttura organizzativa
                                - Competenze chiave

                                3. STRATEGIA E MERCATO
                                - Piano operativo dettagliato
                                - Target di riferimento
                                - Analisi della concorrenza
                                - Opportunità di mercato
                                - Strategie di marketing

                                4. ASPETTI ECONOMICI
                                - Investimenti necessari
                                - Dettaglio dei costi
                                - Previsioni di fatturato
                                - ROI atteso
                                - Piano di sostenibilità

                                5. CONFORMITÀ E INNOVAZIONE
                                - Requisiti del bando soddisfatti
                                - Elementi innovativi
                                - Impatto ambientale/sociale
                                - Rischi e mitigazioni

                                Genera una risposta dettagliata in Markdown . but dont add ```markdown``` tags.
                                IMPORTANTE: Lascia VUOTI i campi del capitolo 2 (Informazioni sull'Impresa).""",
                },
                {"role": "user", "content": text},
            ],
            timeout=60,
            max_tokens=2000,
        )

        return jsonify({"success": True, "analysis": response.choices[0].message.content})

    except Exception as e:
        logger.error(f"Error analyzing text: {str(e)}", exc_info=True)
        return jsonify({"success": False, "error": f"Failed to analyze text: {str(e)}"}), 500
