import requests

API_KEY = '76725faf3fbd5abd33a88b559149e7c8fa82886752e8ed8de6dc03b8d0f61cfc'

def vtotal(domain,q):
    url = f'https://www.virustotal.com/vtapi/v2/domain/report?apikey={API_KEY}&domain={domain}'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        subdomains = data.get('subdomains', [])
    
        print(f'[+] Virus Total found {len(subdomains)} subdomains !!')

        q.put(subdomains)
    else:
        print('Error:', response.status_code)
