from scapy.all import Ether, IP, TCP, Raw, wrpcap
import json
import random
from datetime import datetime, timedelta

# Input dataset file
DATASET_FILE = "attacks_full_dataset.json"

# Output PCAP
OUTPUT_FILE = "attacks_dataset.pcap"

# Load dataset
with open(DATASET_FILE, "r", encoding="utf-8") as f:
    attacks = json.load(f)

packets = []

print(f"Generating PCAP with {len(attacks)} attacks...")

# Base timestamp
base_time = datetime.now()

for i, entry in enumerate(attacks):
    src = entry["src_ip"]
    dst = entry["dst_ip"]
    url = entry["url"]

    # Convert timestamp into scapy-friendly format
    ts = base_time + timedelta(seconds=i)

    # ---- Create HTTP Request Packet ----
    payload = f"GET {url} HTTP/1.1\r\nHost: victim.com\r\nUser-Agent: {entry['user_agent']}\r\n\r\n"

    ether = Ether()
    ip = IP(src=src, dst=dst)
    tcp = TCP(sport=random.randint(1024, 65535), dport=80, flags="PA", seq=1000+i, ack=1)

    pkt = ether / ip / tcp / Raw(load=payload)
    pkt.time = ts.timestamp()

    packets.append(pkt)

# Save PCAP
wrpcap(OUTPUT_FILE, packets)

print(f"✓ PCAP generated successfully: {OUTPUT_FILE}")
