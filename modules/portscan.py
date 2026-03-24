import socket
import concurrent.futures

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 8888: "HTTP-Alt", 27017: "MongoDB",
    3000: "Node/React", 5000: "Flask", 8000: "Django"
}

def run(target):
    raw = target.replace("https://", "").replace("http://", "").strip("/")
    domain = raw.split(":")[0]
    port_hint = int(raw.split(":")[1]) if ":" in raw else None

    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        print(f"    \033[91m[-] Could not resolve {domain}\033[0m")
        return []

    ports_to_scan = list(COMMON_PORTS.keys())
    if port_hint and port_hint not in ports_to_scan:
        ports_to_scan.append(port_hint)

    print(f"    [*] Target: {domain} ({ip})")
    print(f"    [*] Scanning {len(ports_to_scan)} ports...\n")

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
        results = executor.map(scan, ports_to_scan)

    found = [r for r in results if r]

    if not found:
        print("    [-] No open ports found")

    return found
