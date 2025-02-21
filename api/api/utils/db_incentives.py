import logging

from api.middleware.mongo import get_mongo
from api.models.incentive_cache import IncentiveCache

logger = logging.getLogger(__name__)


def init_incentives_collection():
    """Initialize the incentives collection with proper indexes"""
    try:
        mongo = get_mongo()
        collection = mongo.db[IncentiveCache.Config.collection]

        # Drop existing indexes
        collection.drop_indexes()

        # Create indexes
        collection.create_index("last_updated")
        collection.create_index([("id", 1), ("user_id", 1)], unique=True, name="unique_id_per_user")

        logger.info(f"Initialized {IncentiveCache.Config.collection} collection with indexes")
    except Exception as e:
        logger.error(f"Error initializing incentives collection: {str(e)}", exc_info=True)
        raise
