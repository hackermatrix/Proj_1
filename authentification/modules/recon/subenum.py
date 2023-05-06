import subprocess
import multiprocessing
from subenum_modules.wayback import wayback
from subenum_modules.crtsh_scrap import crtsh
from subenum_modules.certspott import san_extract
from subenum_modules.virustotal import vtotal
from subenum_modules.dork import gdork
from subenum_modules.godns import godns
from subenum_modules.govhost import govhost
from subenum_modules.httpx import check_active


active = [] # stores all the active subdomains

# Collects all the subdomains no matter active or Not.
# original [wayback,san_extract,vtotal,godns,govhost,crtsh]
def collect(domain):
    findings = set() # stores all the subdomains
    processes = []
    q = multiprocessing.Queue()

    
    # while not q.empty():
    #     print(f"queue initial content {q.get()}")
        

    for i in [wayback,san_extract,vtotal,godns,govhost,crtsh]:
        p = multiprocessing.Process(target = i,args=(domain,q))
        p.start()
        processes.append(p)
    
    # Joins all the processes 
    for p in processes:
        p.join()

    while q.empty() is False:
        findings.update(q.get())

    print(f"Findings:{findings}")
    return findings

# Firstly finding and then Checking for active subdomains found from  different sources

def sub_enum(target):
    findings = collect(target)
    print("+++++++++++++++++++++++++++++++++++++++++++=HTTPX_STARTED=++++++++++++++++++++++++++++++++++++++++++++")

    active = check_active(findings)

    return (active)

