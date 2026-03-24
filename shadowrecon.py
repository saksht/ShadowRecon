#!/usr/bin/env python3

import argparse
import sys
from modules import subdomain, portscan, techdetect, sqli, xss, idor, reporter

def banner():
    print("""
\033[91m
  ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗
  ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║
  ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║
  ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║
  ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝
  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝
       ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
       ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
       ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
       ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
       ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
       ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝╚═╝  ╚═══╝
\033[0m
    \033[93m[ Automated Web Recon & Vulnerability Framework ]\033[0m
    \033[90m            github.com/saksht\033[0m
    """)

def main():
    banner()

    parser = argparse.ArgumentParser(
        description="ShadowRecon - Automated Web Recon & Vuln Detection",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-t", "--target", required=True, help="Target URL or domain (e.g. http://target.com)")
    parser.add_argument("--subdomains", action="store_true", help="Run subdomain enumeration")
    parser.add_argument("--portscan", action="store_true", help="Run port/service scan")
    parser.add_argument("--tech", action="store_true", help="Detect web technologies")
    parser.add_argument("--sqli", action="store_true", help="Run SQLi detection")
    parser.add_argument("--xss", action="store_true", help="Run XSS detection")
    parser.add_argument("--idor", action="store_true", help="Run IDOR checks")
    parser.add_argument("--all", action="store_true", help="Run all modules")
    parser.add_argument("-o", "--output", default="report", help="Output report name (default: report)")

    args = parser.parse_args()

    results = {}

    if args.all or args.subdomains:
        print("\n\033[94m[*] Running Subdomain Enumeration...\033[0m")
        results["subdomains"] = subdomain.run(args.target)

    if args.all or args.portscan:
        print("\n\033[94m[*] Running Port Scan...\033[0m")
        results["portscan"] = portscan.run(args.target)

    if args.all or args.tech:
        print("\n\033[94m[*] Detecting Web Technologies...\033[0m")
        results["techdetect"] = techdetect.run(args.target)

    if args.all or args.sqli:
        print("\n\033[94m[*] Running SQLi Detection...\033[0m")
        results["sqli"] = sqli.run(args.target)

    if args.all or args.xss:
        print("\n\033[94m[*] Running XSS Detection...\033[0m")
        results["xss"] = xss.run(args.target)

    if args.all or args.idor:
        print("\n\033[94m[*] Running IDOR Checks...\033[0m")
        results["idor"] = idor.run(args.target)

    print("\n\033[92m[+] Generating Report...\033[0m")
    reporter.generate(results, args.output)
    print(f"\033[92m[+] Report saved: {args.output}.html & {args.output}.json\033[0m\n")

if __name__ == "__main__":
    main()
