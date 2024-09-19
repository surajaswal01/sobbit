# Sobbit
To build a more comprehensive subdomain finder tool with an interactive help menu,multi-threading, and various features , we  can use python's command line argument parsing,dns python for Dns resolution, requests for HTTP checks, and threading for performance.

This script include:
DNS resolution to find subdomains.
HTTP request checks to verify if subdomains are live.
Multi-threading for faster execution.
An intractive help menu using argparse.


# Run the script with diffrent options. 
for example:-
bash
python sobbit.py -d example.com -w wordlist.txt --check-http -t 20
DNS Resolution: Uses dnspython to resolve DNS records and find existing subdomains.
HTTP Check: Optionally checks if the subdomain is live via an HTTP request (--check-http flag).
Multi-threading: Uses multi-threading to speed up the enumeration process (-t or --threads option).
Help Menu: Uses argparse to provide a command-line interface with options.
Command-Line Options
-d or --domain: Specify the target domain (required).
-w or --wordlist: Specify the path to the wordlist file (required).
-t or --threads: Number of threads to use (default is 10).
--check-http: Use this flag to make an HTTP request to see if the subdomain is live.
Example Usage
bash
# Basic usage without HTTP checks
python subdomain_finder.py -d example.com -w subdomains.txt

# Using more threads and HTTP checks
python subdomain_finder.py -d example.com -w subdomains.txt --check-http -t 20
Requirements
Python 3.x
Install the necessary libraries:
bash
Copy code
pip install dnspython requests
Notes
Legality: Always ensure you have permission to scan a target domain.
Wordlist: Use a comprehensive wordlist to improve subdomain discovery.
Performance: Adjust the number of threads based on your network conditions and wordlist size.
This script provides a full-featured subdomain finder with a flexible and user-friendly command-line interface.
