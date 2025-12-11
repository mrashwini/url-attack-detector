# backend/detection.py
import re
from typing import List, Tuple
from urllib.parse import urlparse, parse_qs

# Simple regex patterns for different attacks
PATTERNS = {
    "SQL_INJECTION": re.compile(
        r"(\bUNION\b|\bSELECT\b|\bINSERT\b|\bUPDATE\b|\bDELETE\b|\bDROP\b|--|\bOR\b\s+1=1)",
        re.IGNORECASE,
    ),
    "XSS": re.compile(
        r"(<script\b|onerror=|onload=|javascript:|alert\()",
        re.IGNORECASE,
    ),
    "DIRECTORY_TRAVERSAL": re.compile(r"(\.\./|\.\.\\)", re.IGNORECASE),
    "COMMAND_INJECTION": re.compile(r"(;|&&|\|\|)\s*(ls|cat|whoami|id|wget|curl)", re.IGNORECASE),
    "LFI_RFI": re.compile(
        r"(etc/passwd|boot.ini|proc/self/environ|file://|php://|http://|https://)",
        re.IGNORECASE,
    ),
    "SSRF": re.compile(r"(metadata\.google|169\.254\.169\.254|localhost|127\.0\.0\.1)", re.IGNORECASE),
    "PARAMETER_POLLUTION": re.compile(r"(\b\w+)=([^&]*)&\1=", re.IGNORECASE),
    "XML_XXE": re.compile(r"<!DOCTYPE\s+[^>]*ENTITY", re.IGNORECASE),
    "WEBSHELL_UPLOAD": re.compile(r"\.(jsp|asp|php|aspx|ashx)$", re.IGNORECASE),
    "TYPOSQUATTING": re.compile(
        r"(paypa1\.|faceb00k\.|g00gle\.|micros0ft\.)", re.IGNORECASE
    ),
    "CREDENTIAL_STUFFING": re.compile(r"(login|signin|auth)", re.IGNORECASE),
}

def detect_attack_types(url: str, method: str, raw_request: str = "") -> List[str]:
    """
    Returns a list of attack type strings detected in the URL / request.
    """
    detected = []

    # Path + query string
    parsed = urlparse(url)
    full = url + " " + raw_request

    # Check each pattern
    for attack_name, pattern in PATTERNS.items():
        if pattern.search(full):
            detected.append(attack_name)

    # Extra heuristic: brute-force / credential stuffing (many attempts logic
    # should be done at a higher layer using frequency over time)
    # Here we just tag login-like URLs as potential.
    return detected


def is_successful_attack(
    attack_type: str,
    raw_request: str = "",
    raw_response: str = "",
    status_code: int | None = None,
) -> bool:
    """
    Heuristically decide whether an attack was likely successful.

    You can improve/extend these rules based on your test cases.
    """
    text = f"{raw_request or ''} {raw_response or ''}".lower()

    # Generic: 5xx errors often indicate backend / SQL / LFI issues
    if status_code is not None and status_code >= 500:
        return True

    # --- SQL Injection success indicators ---
    if attack_type == "SQL_INJECTION":
        db_error_signatures = [
            "you have an error in your sql syntax",
            "warning: mysql",
            "mysql_fetch",
            "odbc sql server driver",
            "unclosed quotation mark after the character string",
            "sql syntax error",
            "ora-",
            "psql:",
            "sqlite error",
        ]
        for sig in db_error_signatures:
            if sig in text:
                return True

        # Sometimes successful SQLi leaks table/column names
        leaked_keywords = [
            "information_schema",
            "table_schema",
            "from users",
            "user_password",
        ]
        if any(k in text for k in leaked_keywords):
            return True

    # --- Directory Traversal / LFI / RFI ---
    if attack_type in ("DIRECTORY_TRAVERSAL", "LFI_RFI"):
        traversal_markers = [
            "root:x:0:0:",     # /etc/passwd content
            "[extensions]",    # php.ini
            "[boot loader]",   # boot.ini
            "daemon:x:",
        ]
        if any(m in text for m in traversal_markers):
            return True

    # --- Command Injection ---
    if attack_type == "COMMAND_INJECTION":
        cmd_out_signatures = [
            "uid=0(root)",
            "uid=",
            "gid=",
            "total ",          # from `ls`/`dir` output
            "volume serial number is",
            "windows ip configuration",
        ]
        if any(s in text for s in cmd_out_signatures):
            return True

    # --- Web shell upload success ---
    if attack_type == "WEBSHELL_UPLOAD":
        webshell_markers = [
            "cmd.php",
            "cmd.jsp",
            "backdoor.asp",
            "shell.php",
            "webshell",
        ]
        if any(m in text for m in webshell_markers):
            return True

    # --- Credential stuffing / brute force ---
    if attack_type == "CREDENTIAL_STUFFING":
        # Very naive: lots of "invalid password" without any "login successful"
        if "login successful" in text or "welcome" in text:
            return True

    # If none of the specific conditions hit, assume attempt only.
    return False
