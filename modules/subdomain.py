import dns.resolver
import requests
import concurrent.futures

def run(target):
    # Strip protocol
    domain = target.replace("https://", "").replace("http://", "").strip("/")
    
    wordlist = [
        "www", "mail", "ftp", "admin", "api", "dev", "staging", "test",
        "blog", "shop", "portal", "vpn", "remote", "cdn", "static",
        "assets", "beta", "app", "dashboard", "login", "secure", "m"
    ]

    found = []
    print(f"    [*] Target domain: {domain}")
    print(f"    [*] Testing {len(wordlist)} subdomains...\n")

    def check(sub):
        subdomain = f"{sub}.{domain}"
        try:
            dns.resolver.resolve(subdomain, "A")
            print(f"    \033[92m[+] Found: {subdomain}\033[0m")
            return subdomain
        except:
            return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(check, wordlist)

    found = [r for r in results if r]

    if not found:
        print("    [-] No subdomains found")

    return found
