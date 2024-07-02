# EnumLiveHost

EnumLiveHost is a Python script designed to enumerate live hosts from a list of URLs. The script checks each URL's live status by making HTTP/HTTPS requests and outputs the results to a CSV file. It also includes threading to handle a large number of URLs efficiently.

## Features

- Checks live status of URLs using HTTP and HTTPS
- Retrieves and records the HTTP status code and page title
- Handles large URL lists efficiently using threading
- Gracefully handles interruptions and saves partial results
- Outputs results in CSV format

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/enumlivehost.git
   cd enumlivehost
   ```
2. Install the required Python packages:
   ```bash
     pip install -r requirements.txt
   ```

## Usage
Run the script with the following command:
  ```bash
  python enumlivehost.py -u urls.txt -o live_hosts.csv --http-timeout 5 --max-threads 10
  ```
Arguments
-u, --url_file: Path to the file containing URLs (required).
-o, --output_file: Path to the output CSV file (required).
--http-timeout: Timeout for HTTP requests in seconds (default: 5).
--max-threads: Maximum number of threads to use (default: 10).

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Author
Created by ukmihiran
 
