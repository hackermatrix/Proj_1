import socket

def get_ips(domains):
    results = {}
    for domain in domains:
        ips = []
           
        answers = socket.gethostbyname(domain)

        ips.append(answers)
        results[domain] = ips

    return results

eg = ["google.com","www.yahoo.com","innovation.enova.com"]

print(get_ips(eg))

