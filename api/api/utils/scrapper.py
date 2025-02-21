import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class Incentive(BaseModel):
    id: str
    title: str
    status: str
    categories: List[str]
    link: str
    open_date: Optional[str] = None
    close_date: Optional[str] = None
    granted_costs: List[str] = Field(default_factory=list)
    activity_sector: List[str] = Field(default_factory=list)
    support_form: List[str] = Field(default_factory=list)
    scopes: List[str] = Field(default_factory=list)
    regions: List[str] = Field(default_factory=list)
    full_data: Optional[Dict[str, Any]] = None
    bonus_data: Optional[List[Dict[str, Any]]] = Field(default=None, exclude=True)


class IncentivesScraper:
    BASE_URL = "https://incentivi.gov.it/it/catalogo"
    API_BASE_URL = "https://incentivi.gov.it/solr/coredrupal/select"

    def __init__(self):
        self._headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        self._session = requests.Session()
        self._session.headers.update(self._headers)
        self._session.mount(
            "https://",
            requests.adapters.HTTPAdapter(
                max_retries=requests.adapters.Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
            ),
        )

    def _split_string_list(self, value: Optional[str]) -> List[str]:
        if not value:
            return []
        return [v.strip() for v in value.split(",")]

    def _extract_incentive_data(self, incentive_div):
        data = {
            "title": None,
            "area": None,
            "status": "",
            "open_date": None,
            "close_date": None,
            "url": None,
            "notification_status": None,
        }

        try:
            data["title"] = incentive_div.select_one(".title .field--name-field-page-title").get_text(strip=True)
            data["area"] = incentive_div.select_one(".area .field--name-name").get_text(strip=True)
            data["url"] = incentive_div.select_one(".btn.url a")["href"]

            open_date_str = incentive_div.get("open-date")
            close_date_str = incentive_div.get("close-date")
            current_time = datetime.now(timezone.utc)

            if open_date_str and close_date_str:
                try:
                    open_date = datetime.fromisoformat(open_date_str.replace("Z", "+00:00"))
                    close_date = datetime.fromisoformat(close_date_str.replace("Z", "+00:00"))
                    data.update({"open_date": open_date_str, "close_date": close_date_str})

                    if current_time < open_date:
                        data["status"] = "scheduled"
                    elif open_date <= current_time <= close_date:
                        data["status"] = "active"
                    else:
                        data["status"] = "closed"
                except ValueError as e:
                    logging.warning(f"Date parsing error: {str(e)}")
                    data["status"] = self._fallback_status_check(incentive_div)

            else:
                data["status"] = self._fallback_status_check(incentive_div)

            notification_span = incentive_div.select_one(".notification-status span")
            if notification_span:
                data["notification_status"] = "active" if "active" in notification_span.get("class", []) else "inactive"

        except Exception as e:
            logging.error(f"Error extracting incentive data: {str(e)}", exc_info=True)

        return data

    def _fallback_status_check(self, element):
        status_map = {
            "tag.open:not(.d-none)": "active",
            "tag.closed:not(.d-none)": "closed",
            "tag.scheduled:not(.d-none)": "scheduled",
        }

        for selector, status in status_map.items():
            if element.select(selector):
                return status
        return "unknown"

    def _merge_bonus_data(self, incentives, bonus_data):
        bonus_lookup = {str(item["nid"]): item for item in bonus_data}
        merged_incentives = []
        for incentive in incentives:
            if incentive.id in bonus_lookup:
                bonus_item = bonus_lookup[incentive.id]
                # Update the incentive with bonus data
                incentive.granted_costs = self._split_string_list(bonus_item.get("granted_costs"))
                incentive.activity_sector = self._split_string_list(bonus_item.get("activity_sector"))
                incentive.support_form = self._split_string_list(bonus_item.get("support_form"))
                incentive.scopes = self._split_string_list(bonus_item.get("scopes"))
                incentive.regions = self._split_string_list(bonus_item.get("regions"))
                incentive.full_data = bonus_item
                incentive.open_date = bonus_item.get("open_date") or incentive.open_date
                incentive.close_date = bonus_item.get("close_date") or incentive.close_date
            merged_incentives.append(incentive)

        return merged_incentives

    def scrape_incentives(self) -> Tuple[List[Incentive], List[Dict[str, Any]]]:
        try:
            url = f"{self.BASE_URL}"

            try:
                response = self._session.get(url, timeout=30)
                response.raise_for_status()
            except requests.RequestException:
                alt_url = url.replace("https://incentivi", "https://www.incentivi")
                logger.info(f"Retrying with alternative URL: {alt_url}")
                response = self._session.get(alt_url, timeout=30)
                response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            incentive_cards = soup.find_all("div", class_="incentive")

            # Create list of Incentive objects
            incentives = []
            for incentive_div in incentive_cards:
                data = self._extract_incentive_data(incentive_div)
                if data is not None:
                    incentive = Incentive(
                        id=incentive_div.get("data-incentive-id"),
                        title=data["title"],
                        status=data["status"],
                        categories=[data["area"]],
                        link=data["url"],
                        open_date=data["open_date"],
                        close_date=data["close_date"],
                    )
                    incentives.append(incentive)

            # Process bonus data
            try:
                bonus_script = soup.find("script", id="bonus_rest")
                bonus_data = json.loads(bonus_script.string) if bonus_script else []
                incentives = self._merge_bonus_data(incentives, bonus_data)
            except Exception as e:
                logger.error(f"Error extracting bonus data: {str(e)}")
                bonus_data = []

            return incentives, bonus_data

        except requests.RequestException as e:
            logger.error(f"Error scraping data: {str(e)}")
            raise Exception(f"Failed to scrape incentives: {str(e)}")

    def scrape_webpage_text(self, url):
        try:
            response = self._session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            text_parts = []
            content_wrapper = soup.find(class_="content-wrapper")
            if content_wrapper:
                text_parts.append(content_wrapper.get_text(strip=True))
            main_infos = soup.find(class_="main-infos")
            if main_infos:
                text_parts.append(main_infos.get_text(strip=True))
            main_description = soup.find(class_="main-description")
            if main_description:
                text_parts.append(main_description.get_text(strip=True))
            return " ".join(text_parts)
        except requests.RequestException as e:
            logger.error(f"Error scraping webpage: {str(e)}")
            raise Exception(f"Failed to scrape webpage: {str(e)}")
