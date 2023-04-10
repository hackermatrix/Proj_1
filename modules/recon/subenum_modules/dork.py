import re
from googlesearch import search




def gdork(target):
    query = f'site:".{target}"'
    num_results = 10

    # Fetch the search results using the googlesearch library
    results = list(search(query))

    # Extract the domain names from the search results
    subdomains = set()
    for result in results:
        match = re.search(r'(https?://)?([^/]+)', result)
        if match:
            subdomain = match.group(2)
            subdomains.add(subdomain)
    print(f"[+] Dorking found {len(subdomains)} subdomains!!")
    return subdomains
