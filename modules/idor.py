import requests
import urllib3
urllib3.disable_warnings()

def run(target):
    if not target.startswith("http"):
        target = "http://" + target

    print(f"    [*] Target: {target}")
    print(f"    [*] Testing IDOR on common endpoints...\n")

    found = []

    endpoints = [
        "/user?id=", "/profile?id=", "/account?id=",
        "/order?id=", "/invoice?id=", "/document?id=",
        "/api/user/", "/api/profile/", "/api/order/",
    ]

    ids = [1, 2, 3, 100, 101, 1000]

    baseline_codes = set()

    for endpoint in endpoints:
        url = f"{target}{endpoint}0"
        try:
            r = requests.get(url, timeout=5, verify=False)
            baseline_codes.add(r.status_code)
        except:
            pass

    for endpoint in endpoints:
        for id in ids:
            url = f"{target}{endpoint}{id}"
            try:
                r = requests.get(url, timeout=5, verify=False)
                if r.status_code == 200 and r.status_code not in baseline_codes:
                    result = {
                        "url": url,
                        "status": r.status_code,
                        "length": len(r.text)
                    }
                    print(f"    \033[92m[+] Potential IDOR!\033[0m")
                    print(f"        URL: {url}")
                    print(f"        Status: {r.status_code} | Length: {len(r.text)}\n")
                    found.append(result)
            except:
                pass

    if not found:
        print("    [-] No IDOR vulnerabilities detected")

    return found
