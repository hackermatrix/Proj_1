import requests
import re

def wayback(url):
    wayback_url = f"https://web.archive.org/cdx/search/cdx?url={url}&matchType=domain&fl=original&collapse=urlkey&output=json&fl=original&collapse=urlkey"
    response = requests.get(wayback_url)
    subdomains = set()

    if response.ok:
        data = response.json()
        #print(data)
        urls = [d[0] for d in data[1:]]
        for url in urls:
            subdomain = re.match(r'https?://([^/]+)\..+', url)
            if subdomain:
                subdomains.add(subdomain.group(1))
    print(f"[+] waybackURLs found {len(subdomains)} subdomains !!")
    return subdomains


