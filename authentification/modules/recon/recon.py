from ip_add import get_ips
from dirbrute import godir
from tech import get_tech_stack
from subenum import sub_enum


target = "enova.com"
subs =[]
ips ={}

# Get subdomains:

subs = sub_enum(target)

print("[+] Subs!!!!!!!!:")

print(subs)

#Get ip addresses of each active subdomain

ips = get_ips(subs)

print(ips)


