import subprocess


def check_active(subdoms):
    active =[]
    subdoms = ','.join(subdoms)
    proc = subprocess.Popen(['httpx','-status-code','-u',subdoms,'grep',"200 OK"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    for domain in out.decode().split('\n'):
        domain = domain.split(" ")[0]
        print(domain)
        active.append(domain)
    return active

# subdoms =  ['www.google.com','anchore.staging.enova.com', 'dreamcast11a.oak.enova.com', 'odi.enova.com', 'leafblower-frontend.enova.com', 'astro.enova.com', 'ir.enova.com', 'portal.staging.decisions.enova.com', 'uk-gdpr.enova.com', 'password.enova']

# print(check_active(subdoms))