# backend/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ------------------ MAIN ATTACK RECORD SCHEMAS ------------------

class AttackRecordBase(BaseModel):
    src_ip: str
    dst_ip: str
    method: str
    url: str
    attack_type: str
    is_successful: bool = False
    raw_request: Optional[str] = None


class AttackRecordCreate(AttackRecordBase):
    pass


class AttackRecordRead(AttackRecordBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True   # (Pydantic V2 equivalent of orm_mode)


# ------------------ QUERY MODEL ------------------

class AttackQuery(BaseModel):
    attack_type: Optional[str] = None
    src_ip: Optional[str] = None
    dst_ip: Optional[str] = None
    ip_range: Optional[str] = None  # e.g., "192.168.0.0/24"
    successful_only: Optional[bool] = None


# ------------------ STATISTICS MODELS ------------------

class AttackTypeCount(BaseModel):
    attack_type: str
    count: int


class IpCount(BaseModel):
    ip: str
    count: int


class TimelinePoint(BaseModel):
    date: str   # YYYY-MM-DD
    count: int


class AttackStats(BaseModel):
    by_attack_type: List[AttackTypeCount]
    by_src_ip: List[IpCount]
    by_day: List[TimelinePoint]
