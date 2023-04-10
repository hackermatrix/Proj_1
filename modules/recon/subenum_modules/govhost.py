import subprocess
import os

wordlist_path = os.path.join(os.path.dirname(__file__), '../../../wordlists/DNS')
print(wordlist_path)

def govhost(target,mode=1):
    subdomains = []
    
    if(mode == 1):
        wordlist = os.path.join(wordlist_path,"small.txt")
    elif(mode==2):
        wordlist = os.path.join(wordlist_path,"medium.txt")
    else:
        wordlist = os.path.join(wordlist_path,"large.txt")

    gobuster_process = subprocess.Popen(
        ['gobuster', 'vhost', '-u', target, '-w', f'{wordlist}'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output, error = gobuster_process.communicate()
    if gobuster_process.returncode != 0:
        print(f"Error running Gobuster: {error}")
        return subdomains
    for line in output.decode().split('\n'):
        if line.startswith('\rFound: '):
            subdomain = line.split(' ')[1]
            subdomains.append(subdomain)
    print(f"[+] Gobuster found {len(subdomains)} subdomains by VHOST lookup !!")
    return subdomains
    
