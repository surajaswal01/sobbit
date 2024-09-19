import dns.resolver
import requests
import threading
from queue import Queue
import argparse

class SubdomainFinder:
    def __init__(self, domain, wordlist, threads=10, check_http=False):
        self.domain = domain
        self.wordlist = wordlist
        self.threads = threads
        self.check_http = check_http
        self.queue = Queue()
        self.found_subdomains = []

    def load_subdomains(self):
        # Load subdomains into the queue from the wordlist
        with open(self.wordlist, 'r') as file:
            subdomains = file.read().splitlines()
        for subdomain in subdomains:
            self.queue.put(subdomain)

    def resolve_subdomain(self):
        while not self.queue.empty():
            sub = self.queue.get()
            subdomain = f"{sub}.{self.domain}"
            try:
                # Resolve DNS
                dns.resolver.resolve(subdomain, 'A')
                if self.check_http:
                    # Optionally, check if the subdomain is live via HTTP request
                    if self.is_live(subdomain):
                        print(f"[LIVE] {subdomain}")
                        self.found_subdomains.append(subdomain)
                else:
                    print(f"[FOUND] {subdomain}")
                    self.found_subdomains.append(subdomain)
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
                pass
            finally:
                self.queue.task_done()

    def is_live(self, subdomain):
        try:
            # Make an HTTP request to verify if the subdomain is live
            response = requests.get(f"http://{subdomain}", timeout=3)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def run(self):
        # Load subdomains into the queue
        self.load_subdomains()
        
        # Create and start threads
        threads = []
        for _ in range(self.threads):
            thread = threading.Thread(target=self.resolve_subdomain)
            thread.start()
            threads.append(thread)

        # Wait for the queue to be empty
        self.queue.join()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Print the results
        if self.found_subdomains:
            print("\nSubdomains found:")
            for subdomain in self.found_subdomains:
                print(subdomain)
        else:
            print("No subdomains found.")

def main():
    # Argument parser for command-line options
    parser = argparse.ArgumentParser(description="Subdomain Finder Tool")
    parser.add_argument('-d', '--domain', required=True, help='Target domain (e.g., example.com)')
    parser.add_argument('-w', '--wordlist', required=True, help='Path to the wordlist file')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads to use (default: 10)')
    parser.add_argument('--check-http', action='store_true', help='Check if the subdomain is live via HTTP request')
    
    args = parser.parse_args()
    
    # Initialize and run the subdomain finder
    finder = SubdomainFinder(
        domain=args.domain, 
        wordlist=args.wordlist, 
        threads=args.threads, 
        check_http=args.check_http
    )
    finder.run()

if __name__ == "__main__":
    main()
