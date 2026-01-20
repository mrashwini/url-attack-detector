🚀 How to Run & Test the Project (Beginner Friendly)

This section explains how to run the project and how to check whether a URL is malicious or not, step by step.

🛠️ Prerequisites (Install First)

Make sure the following are installed on your system:

Python 3.10 or above

Node.js (LTS version)

Git

👉 No cybersecurity knowledge is required.

📥 Step 1: Clone the Project

Open terminal and run:

git clone https://github.com/mrashwini/url-attack-detector.git
cd url-attack-detector

▶️ Step 2: Run the Backend (FastAPI)


From the project root:

python -m pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --reload

✅ Backend running if you see:
Uvicorn running on http://127.0.0.1:8000


Open this in browser:

http://localhost:8000/docs


This opens an interactive API page (Swagger UI).

🔍 Check if Backend is Running

After starting the backend with:

uvicorn backend.main:app --reload


Open these links in your browser:

Backend Home (Health Check):
http://127.0.0.1:8000/
✅ Should return: "URL Attack Detection API is running"

Swagger API Docs (Recommended):
http://127.0.0.1:8000/docs
✅ You should see the interactive API dashboard

API Stats Endpoint:
http://127.0.0.1:8000/attacks/stats
✅ Should return JSON attack statistics

If you see 404 Not Found, ensure the backend server is running and the correct port is used.

▶️ Step 3: Run the Frontend (Dashboard)

Open a new terminal:

cd frontend
npm install
npm run dev

✅ Frontend running if you see:
Local: http://localhost:5173/


Open in browser:

http://localhost:5173


You will see the URL-based Attack Detection Dashboard.

🔍 How to Check Whether a URL is Malicious or Not

You can test URLs using the backend API.

🟢 Example 1: Normal (Non-Malicious) URL

This is a safe URL:

http://example.com/product?id=10


It only contains a normal numeric parameter and does not try to exploit anything.

How to test it:

Open

http://localhost:8000/docs


Click POST /detect_url

Paste this JSON:

{
  "src_ip": "192.168.1.10",
  "dst_ip": "192.168.1.20",
  "method": "GET",
  "url": "http://example.com/product?id=10",
  "status_code": 200
}


Click Execute

👉 Result:

Either no attack or logged as non-malicious

🔴 Example 2: Malicious URL (SQL Injection)

This is a malicious URL:

http://example.com/product?id=10 UNION SELECT username,password FROM users


It tries to steal database data using SQL Injection.

How to test it:

Open

http://localhost:8000/docs


Click POST /detect_url

Paste this JSON:

{
  "src_ip": "192.168.1.50",
  "dst_ip": "192.168.1.20",
  "method": "GET",
  "url": "http://example.com/product?id=10 UNION SELECT username,password FROM users",
  "status_code": 500
}


Click Execute

👉 Result:

Attack Type: SQL_INJECTION

Attack appears on the dashboard

🔴 Example 3: Malicious URL (XSS)

Another malicious example (Cross-Site Scripting):

http://example.com/search?q=<script>alert(1)</script>


Test using:

{
  "src_ip": "192.168.1.60",
  "dst_ip": "192.168.1.20",
  "method": "GET",
  "url": "http://example.com/search?q=<script>alert(1)</script>",
  "status_code": 200
}


👉 Result:

Attack Type: XSS

📊 Step 4: View Results on Dashboard

Open:

http://localhost:5173


You can now see:

Detected attacks

Attack type (SQLi, XSS, etc.)

Source IP

Successful / unsuccessful flag

Statistics & charts

🧠 How the System Decides if a URL is Malicious

The URL is analyzed for known attack patterns

Keywords like UNION SELECT, <script>, ../, cmd=, etc. are detected

Based on patterns and response codes, the attack is classified

Results are stored and visualized automatically