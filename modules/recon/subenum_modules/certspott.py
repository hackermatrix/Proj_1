import requests

def san_extract(domain):
    url = f"https://api.certspotter.com/v1/issuances?domain={domain}&expand=dns_names&include_subdomains=true"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        subdomains = {dns_name for cert in data for dns_name in cert['dns_names'] if dns_name.endswith(f".{domain}")}
        print(f"[+] Certispotter found {len(subdomains)} subdomains !!")
        return subdomains
    else:
        print(f"Failed to fetch subdomains: {response.text}")
        return set()


