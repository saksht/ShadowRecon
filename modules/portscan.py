import socket
import concurrent.futures

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 8888: "HTTP-Alt", 27017: "MongoDB"
}

def run(target):
    domain = target.replace("https://", "").replace("http://", "").strip("/").split(":")[0]

    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        print(f"    \033[91m[-] Could not resolve {domain}\033[0m")
        return []

    print(f"    [*] Target: {domain} ({ip})")
    print(f"    [*] Scanning {len(COMMON_PORTS)} common ports...\n")

    found = []

    def scan(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            sock.close()
            if result == 0:
                service = COMMON_PORTS.get(port, "Unknown")
                print(f"    \033[92m[+] {port}/tcp open  {service}\033[0m")
                return {"port": port, "service": service, "state": "open"}
        except:
            pass
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(scan, COMMON_PORTS.keys())

    found = [r for r in results if r]

    if not found:
        print("    [-] No open ports found")

    return found
