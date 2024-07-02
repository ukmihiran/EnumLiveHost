import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
import argparse
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# Banner Info
def print_banner():
    banner = """
========================================================================================================================
'########:'##::: ##:'##::::'##:'##::::'##:'##:::::::'####:'##::::'##:'########:'##::::'##::'#######:::'######::'########:
 ##.....:: ###:: ##: ##:::: ##: ###::'###: ##:::::::. ##:: ##:::: ##: ##.....:: ##:::: ##:'##.... ##:'##... ##:... ##..::
 ##::::::: ####: ##: ##:::: ##: ####'####: ##:::::::: ##:: ##:::: ##: ##::::::: ##:::: ##: ##:::: ##: ##:::..::::: ##::::
 ######::: ## ## ##: ##:::: ##: ## ### ##: ##:::::::: ##:: ##:::: ##: ######::: #########: ##:::: ##:. ######::::: ##::::
 ##...:::: ##. ####: ##:::: ##: ##. #: ##: ##:::::::: ##::. ##:: ##:: ##...:::: ##.... ##: ##:::: ##::..... ##:::: ##::::
 ##::::::: ##:. ###: ##:::: ##: ##:.:: ##: ##:::::::: ##:::. ## ##::: ##::::::: ##:::: ##: ##:::: ##:'##::: ##:::: ##::::
 ########: ##::. ##:. #######:: ##:::: ##: ########:'####:::. ###:::: ########: ##:::: ##:. #######::. ######::::: ##::::
........::..::::..:::.......:::..:::::..::........::....:::::...:::::........::..:::::..:::.......::::......::::::..:::::
----------------------EnumLiveHost by ukmihiran-----https://github.com/ukmihiran-----------------------------------------
=========================================================================================================================
    Usage: python enumlivehost.py -u urls.txt -o live_hosts.csv --http-timeout 5 --max-threads 10
=========================================================================================================================
    """
    print(banner)

# Read URL
def read_urls(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file]
        return urls
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

# Extract Hostnames (HTTP, HTTPS or add HTTP if no scame is provided)
def extract_hostnames(urls):
    hostnames = []
    for url in urls:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url  # Default to HTTP if no scheme is provided
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        if hostname:
            hostnames.append(hostname)
    return hostnames

# Check Live status with http and https probes
def check_live_status(hostname, timeout):
    protocols = ['http', 'https']
    for protocol in protocols:
        url = f"{protocol}://{hostname}"
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code in [200, 301, 404]:
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.title.string if soup.title else 'No Title'
                return hostname, 'Live', title, response.status_code
        except requests.RequestException:
            continue
    return hostname, 'Down', '', None

# Save Results as CSV format
def save_to_csv(data, file_path):
    df = pd.DataFrame(data, columns=['Hostname', 'Live Status', 'Host Title', 'Status Code'])
    df.to_csv(file_path, index=False)

def main(url_file, output_file, http_timeout, max_threads):
    print_banner()
    
    urls = read_urls(url_file)
    hostnames = extract_hostnames(urls)
    
    print("[*] Checking live status of hosts...")

    live_data = []
    total_urls = len(hostnames)

#  manage a pool of threads for concurrent execution
    try:
        with ThreadPoolExecutor(max_threads) as executor:
            future_to_url = {executor.submit(check_live_status, hostname, http_timeout): hostname for hostname in hostnames}
            for i, future in enumerate(as_completed(future_to_url), 1):
                hostname, status, title, status_code = future.result()
                live_data.append([hostname, status, title, status_code])
                print(f"[{i}/{total_urls}] {hostname} - {status} - {status_code}")
    except KeyboardInterrupt:
        print("\nScanning interrupted by user. Saving results to file...")
        save_to_csv(live_data, output_file)
        print(f"Partial results saved to {output_file}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    save_to_csv(live_data, output_file)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EnumLiveHost - Enumerate live hosts from a URL list.")
    parser.add_argument('-u', '--url_file', required=True, help="Path to the file containing URLs.")
    parser.add_argument('-o', '--output_file', required=True, help="Path to the output CSV file.")
    parser.add_argument('--http-timeout', type=int, default=5, help="Timeout for HTTP requests (seconds).")
    parser.add_argument('--max-threads', type=int, default=10, help="Maximum number of threads to use.")
    
    args = parser.parse_args()
    
    start_time = time.time()
    try:
        main(args.url_file, args.output_file, args.http_timeout, args.max_threads)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    end_time = time.time()
    print(f"Scanning completed in {end_time - start_time:.2f} seconds.")
