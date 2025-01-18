import argparse
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_subdomain(subdomain, domain):
    """Try to resolve the subdomain and return results if successful."""
    url = f"{subdomain}.{domain}"
    try:
        # Resolve DNS
        ip = socket.gethostbyname(url)
        return f"{url} -> {ip}"
    except socket.gaierror:
        # If DNS resolution fails, return None
        return None

def main():
    parser = argparse.ArgumentParser(description="Subdomain enumeration script with multithreading")
    parser.add_argument("domain", type=str, help="The target domain for subdomain enumeration")
    parser.add_argument("-w", "--wordlist", type=str, required=True, help="Path to the wordlist file")
    parser.add_argument("-o", "--output", type=str, help="Path to save the output results")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads to use (default: 10)")
    
    args = parser.parse_args()
    domain = args.domain
    wordlist_path = args.wordlist
    output_file = args.output
    threads = args.threads

    # Read the wordlist and start enumeration
    try:
        with open(wordlist_path, "r") as wordlist:
            subdomains = [line.strip() for line in wordlist if line.strip()]
    except FileNotFoundError:
        print(f"Wordlist file {wordlist_path} not found.")
        return

    found_subdomains = []
    print(f"Starting subdomain enumeration for {domain} with {threads} threads...")

    # Use ThreadPoolExecutor to run check_subdomain concurrently
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_subdomain = {executor.submit(check_subdomain, subdomain, domain): subdomain for subdomain in subdomains}
        for future in as_completed(future_to_subdomain):
            result = future.result()
            if result:
                print(f"Found: {result}")
                found_subdomains.append(result)
            else:
                print("NA")

    # Output results
    if output_file:
        with open(output_file, "w") as f:
            for sub in found_subdomains:
                f.write(sub + "\n")
        print(f"Results saved to {output_file}")
    else:
        print("Subdomains found:")
        for sub in found_subdomains:
            print(sub)

if __name__ == "__main__":
    main()