# Project developed by Ashwini (Signature) © 2025
# backend/main.py
from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
import shutil
import os
import ipaddress
from typing import List

from pydantic import BaseModel

from .database import Base, engine, get_db
from .models import AttackRecord
from .schemas import (
    AttackRecordRead,
    AttackQuery,
    AttackRecordCreate,
    AttackStats,
    AttackTypeCount,
    IpCount,
    TimelinePoint,
)
from .pcap_parser import parse_pcap_to_attacks
from .detection import detect_attack_types, is_successful_attack

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Attack Detection API")

# ------------------ CORS ------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ Body Model for detect_url ------------------
class DetectUrlBody(BaseModel):
    src_ip: str
    dst_ip: str
    method: str
    url: str
    raw_request: str | None = None
    raw_response: str | None = None
    status_code: int | None = None


# ------------------ DB Utility ------------------
def create_attack_record(db: Session, record: AttackRecordCreate) -> AttackRecord:
    db_obj = AttackRecord(**record.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


# ------------------ Detect URL ------------------
@app.post("/detect_url", response_model=List[AttackRecordRead])
def detect_url(body: DetectUrlBody, db: Session = Depends(get_db)):
    attack_types = detect_attack_types(
        url=body.url,
        method=body.method,
        raw_request=body.raw_request or "",
    )

    results: List[AttackRecord] = []

    for a_type in attack_types:
        success = is_successful_attack(
            attack_type=a_type,
            raw_request=body.raw_request or "",
            raw_response=body.raw_response or "",
            status_code=body.status_code,
        )

        rec = AttackRecordCreate(
            src_ip=body.src_ip,
            dst_ip=body.dst_ip,
            method=body.method,
            url=body.url,
            attack_type=a_type,
            is_successful=success,
            raw_request=body.raw_request or "",
        )
        db_rec = create_attack_record(db, rec)
        results.append(db_rec)

    return results


# ------------------ PCAP Upload ------------------
@app.post("/upload_pcap", response_model=List[AttackRecordRead])
def upload_pcap(file: UploadFile = File(...), db: Session = Depends(get_db)):
    tmp_path = f"./tmp_{file.filename}"
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        attack_records = parse_pcap_to_attacks(tmp_path)
        db_results = [create_attack_record(db, r) for r in attack_records]
        return db_results
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


# ------------------ Query with IP range ------------------
@app.post("/attacks/query", response_model=List[AttackRecordRead])
def query_attacks(q: AttackQuery, db: Session = Depends(get_db)):
    query = db.query(AttackRecord)

    if q.attack_type:
        query = query.filter(AttackRecord.attack_type == q.attack_type)
    if q.src_ip:
        query = query.filter(AttackRecord.src_ip == q.src_ip)
    if q.dst_ip:
        query = query.filter(AttackRecord.dst_ip == q.dst_ip)
    if q.successful_only is not None:
        query = query.filter(AttackRecord.is_successful == q.successful_only)

    results = query.order_by(AttackRecord.timestamp.desc()).limit(2000).all()

    # CIDR filter (in Python)
    if q.ip_range:
        try:
            network = ipaddress.ip_network(q.ip_range, strict=False)
            filtered = []
            for r in results:
                try:
                    src = ipaddress.ip_address(r.src_ip)
                    dst = ipaddress.ip_address(r.dst_ip)
                    if src in network or dst in network:
                        filtered.append(r)
                except ValueError:
                    pass
            results = filtered
        except ValueError:
            pass

    return results


# ------------------ Statistics Endpoint ------------------
@app.get("/attacks/stats", response_model=AttackStats)
def get_attack_stats(db: Session = Depends(get_db)):
    # 1) Count by attack type
    type_rows = (
        db.query(AttackRecord.attack_type, func.count(AttackRecord.id))
        .group_by(AttackRecord.attack_type)
        .all()
    )
    by_attack_type = [
        AttackTypeCount(attack_type=row[0], count=row[1]) for row in type_rows
    ]

    # 2) Top source IPs
    src_rows = (
        db.query(AttackRecord.src_ip, func.count(AttackRecord.id))
        .group_by(AttackRecord.src_ip)
        .order_by(func.count(AttackRecord.id).desc())
        .limit(10)
        .all()
    )
    by_src_ip = [IpCount(ip=row[0], count=row[1]) for row in src_rows]

    # 3) Timeline per day
    day_rows = (
        db.query(func.date(AttackRecord.timestamp), func.count(AttackRecord.id))
        .group_by(func.date(AttackRecord.timestamp))
        .order_by(func.date(AttackRecord.timestamp))
        .all()
    )
    by_day = [TimelinePoint(date=str(row[0]), count=row[1]) for row in day_rows]

    return AttackStats(
        by_attack_type=by_attack_type,
        by_src_ip=by_src_ip,
        by_day=by_day,
    )


# ------------------ Export CSV ------------------
@app.get("/attacks/export/csv")
def export_csv(db: Session = Depends(get_db)):
    import csv
    from fastapi.responses import StreamingResponse
    from io import StringIO

    rows = db.query(AttackRecord).all()
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow([
        "id", "src_ip", "dst_ip", "method", "url",
        "attack_type", "is_successful", "timestamp"
    ])
    for r in rows:
        writer.writerow([
            r.id, r.src_ip, r.dst_ip, r.method, r.url,
            r.attack_type, r.is_successful, r.timestamp
        ])
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=attacks.csv"},
    )


# ------------------ Export JSON ------------------
@app.get("/attacks/export/json", response_model=List[AttackRecordRead])
def export_json(db: Session = Depends(get_db)):
    return db.query(AttackRecord).all()
