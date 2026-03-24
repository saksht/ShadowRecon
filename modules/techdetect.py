import requests
import re

def run(target):
    if not target.startswith("http"):
        target = "http://" + target

    print(f"    [*] Analyzing: {target}\n")

    found = []

    try:
        r = requests.get(target, timeout=10, verify=False)
    except Exception as e:
        print(f"    \033[91m[-] Could not reach target: {e}\033[0m")
        return found

    headers = r.headers
    body = r.text.lower()

    # Server header
    if "Server" in headers:
        info = f"Server: {headers['Server']}"
        print(f"    \033[92m[+] {info}\033[0m")
        found.append(info)

    # Powered-By header
    if "X-Powered-By" in headers:
        info = f"X-Powered-By: {headers['X-Powered-By']}"
        print(f"    \033[92m[+] {info}\033[0m")
        found.append(info)

    # Cookies
    if "Set-Cookie" in headers:
        cookie = headers["Set-Cookie"]
        if "phpsessid" in cookie.lower():
            print(f"    \033[92m[+] Language: PHP\033[0m")
            found.append("Language: PHP")
        if "jsessionid" in cookie.lower():
            print(f"    \033[92m[+] Language: Java\033[0m")
            found.append("Language: Java")
        if "asp.net_sessionid" in cookie.lower():
            print(f"    \033[92m[+] Language: ASP.NET\033[0m")
            found.append("Language: ASP.NET")

    # CMS Detection
    cms_signatures = {
        "WordPress": ["wp-content", "wp-includes", "wordpress"],
        "Joomla": ["joomla", "/components/com_"],
        "Drupal": ["drupal", "sites/default/files"],
        "Django": ["csrfmiddlewaretoken", "django"],
        "Laravel": ["laravel_session"],
    }

    for cms, sigs in cms_signatures.items():
        if any(sig in body for sig in sigs):
            print(f"    \033[92m[+] CMS: {cms}\033[0m")
            found.append(f"CMS: {cms}")

    # JS Frameworks
    js_signatures = {
        "React": ["react.js", "react.min.js", "_react", "reactdom"],
        "Vue.js": ["vue.js", "vue.min.js", "__vue__"],
        "Angular": ["angular.js", "ng-version", "angular.min.js"],
        "jQuery": ["jquery.js", "jquery.min.js"],
        "Bootstrap": ["bootstrap.css", "bootstrap.min.css"],
    }

    for fw, sigs in js_signatures.items():
        if any(sig in body for sig in sigs):
            print(f"    \033[92m[+] JS Framework: {fw}\033[0m")
            found.append(f"JS Framework: {fw}")

    # Security Headers check
    security_headers = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
    ]

    print()
    for h in security_headers:
        if h in headers:
            print(f"    \033[92m[+] Security Header Present: {h}\033[0m")
            found.append(f"Security Header: {h}")
        else:
            print(f"    \033[91m[-] Missing Security Header: {h}\033[0m")
            found.append(f"Missing Header: {h}")

    if not found:
        print("    [-] No technologies detected")

    return found
