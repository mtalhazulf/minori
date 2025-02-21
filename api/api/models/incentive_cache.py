from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class IncentiveCache(BaseModel):
    id: str
    title: str
    status: Optional[str] = None
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
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None
    data_type: str = "user"  # Default to "user" for user-created incentives

    class Config:
        collection = "incentives_cache"


class DataIncentiveCache(BaseModel):
    data: List[IncentiveCache]
    data_type: str = "cached"
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        collection = "incentives_cache"
