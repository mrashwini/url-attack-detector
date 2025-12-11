# URL-Based Cyber Attack Detection System

Developed by Ashwini © 2025

A full-stack URL-based attack detection platform with:

FastAPI backend for detection

React dashboard for visualization

PCAP ingestion

Dataset generator + PCAP generator

Support for 11+ attack types (SQLi, XSS, LFI, XXE, SSRF, etc.)

Export CSV/JSON

Real-time statistics

Anime cyberpunk UI

🚀 Features

Detects multiple cyber-attacks via URL analysis

Parses PCAP files and extracts malicious requests

Large automatically generated dataset

Beautiful web dashboard

CSV/JSON export

IP range filtering

Successful vs. unsuccessful attack classification

🔧 Technologies

Python FastAPI

React + Vite

SQLite / SQLAlchemy

Scapy

Recharts

📂 Project Structure
backend/
frontend/
dataset_generator.py
pcap_generator.py

▶️ Running Backend
cd backend
uvicorn main:app --reload

▶️ Running Frontend
cd frontend
npm install
npm run dev