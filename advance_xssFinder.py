import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time

# Step 1: Take a base URL and wordlist path from user
base_url, wordlist_path = input("Enter the base URL and wordlist path separated by space: ").split()

# Step 2: Crawl the base URL
visited = set()
to_visit = [base_url]
while to_visit:
    url = to_visit.pop()
    if url in visited:
        continue
    visited.add(url)

    # Indicator that the script is running
    print("Crawling:", url)

    # Get the HTML content of the page
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        r = requests.get(url, headers=headers, allow_redirects=True)
        soup = BeautifulSoup(r.content, 'html.parser')
    except:
        continue

    # Find all links on the page
    for link in soup.find_all('a'):
        link = link.get('href')
        if not link:
            continue
        if link.startswith('http'):
            if urlparse(link).netloc == urlparse(base_url).netloc:
                to_visit.append(link)
        elif link.startswith('/'):
            to_visit.append(base_url + link)

# Step 3: Keep a note of every URL that do have parameters in it
param_urls = []
for url in visited:
    if '?' in url:
        param_urls.append(url)

# Step 4: Take a wordlist of XSS payload
payloads = []
with open(wordlist_path, 'r') as f:
    payloads = f.readlines()

# Step 5: Try every payload from the wordlist with every URL with parameters
vulnerable = []
for url in param_urls:
    for payload in payloads:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            r = requests.get(url + payload, headers=headers, allow_redirects=True)
            if payload in r.content:
                vulnerable.append(url)
                break
        except:
            pass
        time.sleep(1)

# Step 6: Print out every URL which are vulnerable to XSS
if vulnerable:
    print("The following URLs are vulnerable to XSS:")
    for url in vulnerable:
        print(url)
else:
    print("No XSS vulnerabilities found.")
