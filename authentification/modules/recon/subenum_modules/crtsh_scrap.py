import requests
def crtsh(url,q):
    sub = set()

    # Using Crt.sh
    response = requests.get(f"https://crt.sh?q={url}&output=json")

    if response.ok:
        data = response.json()
        for entry in data:
            sub.add(entry["common_name"])
    print(f"[+] Crt.sh found : {len(sub)} subdomains !!")
    q.put(sub)
