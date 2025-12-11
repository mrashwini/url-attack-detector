# backend/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class AttackRecord(Base):
    __tablename__ = "attack_records"

    id = Column(Integer, primary_key=True, index=True)
    src_ip = Column(String, index=True)
    dst_ip = Column(String, index=True)
    method = Column(String, index=True)
    url = Column(String, index=True)
    attack_type = Column(String, index=True)
    is_successful = Column(Boolean, default=False)
    raw_request = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
