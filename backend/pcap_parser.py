# backend/pcap_parser.py
from typing import List
import pyshark
from .detection import detect_attack_types, is_successful_attack
from .schemas import AttackRecordCreate

def parse_pcap_to_attacks(pcap_path: str) -> List[AttackRecordCreate]:
    """
    Reads a PCAP, extracts HTTP requests, runs detection, and returns attack records.
    """
    cap = pyshark.FileCapture(pcap_path, display_filter="http.request")
    records: List[AttackRecordCreate] = []

    for pkt in cap:
        try:
            http_layer = pkt.http
            src_ip = pkt.ip.src
            dst_ip = pkt.ip.dst
            method = http_layer.get_field_value("request_method")
            host = http_layer.get_field_value("host") or ""
            uri = http_layer.get_field_value("request_uri") or "/"
            url = f"http://{host}{uri}"

            raw_request = str(http_layer)

            attack_types = detect_attack_types(url=url, method=method, raw_request=raw_request)
            if not attack_types:
                continue

            # For now, mark all as attempts (is_successful can be refined)
            for a_type in attack_types:
                record = AttackRecordCreate(
                    src_ip=src_ip,
                    dst_ip=dst_ip,
                    method=method,
                    url=url,
                    attack_type=a_type,
                    is_successful=False,    # refine later
                    raw_request=raw_request,
                )
                records.append(record)
        except Exception:
            continue

    cap.close()
    return records
