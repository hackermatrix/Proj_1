import asyncio
import subprocess
import multiprocessing
from subenum_modules.wayback import wayback
from subenum_modules.crtsh_scrap import crtsh
from subenum_modules.certspott import san_extract
from subenum_modules.virustotal import vtotal
from subenum_modules.dork import gdork
from subenum_modules.godns import godns
from subenum_modules.govhost import govhost

findings = set() # stores all the subdomains
active = [] # stores all the active subdomains
url = "enova.com"


# Collects all the subdomains no matter active or Not.

def collect(domain):
    # findings.update(crtsh(domain))
    # findings.update(wayback(domain))
    # findings.update(san_extract(domain))
    # findings.update(vtotal(domain))
    # #findings.update(gdork(domain))
    # findings.update(godns(domain,1))
    # findings.update(govhost(domain,1))

    processes = []
    for i in [crtsh,wayback,san_extract,vtotal,godns,govhost]:
        p = multiprocessing.Process(target = i,args=(domain,))
        p.start()
        processes.append(p)
    
    # Joins all the processes 
    for p in processes:
        p.join()
 

#asyncio.run(collect(url))


# print("[+]ACTIVE DOMAINS:\n",active)

collect(url)