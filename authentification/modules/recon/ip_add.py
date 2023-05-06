import socket
import urllib.parse

def get_ips(domain):
    if("http" in domain):
        parsed_url = urllib.parse.urlparse(domain)
        base_url = f"{parsed_url.netloc}"
    else:
        base_url = domain

    result = socket.gethostbyname(base_url)
    return result

# eg = ["google.com","www.yahoo.com","innovation.enova.com"]

# print(get_ips("https://testphp.vulnweb.com"))

