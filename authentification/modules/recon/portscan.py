import nmap
import urllib.parse

def scan_ports(target_subdomain,scan_mode='quick'):
    

    if("http" in target_subdomain):
        parsed_url = urllib.parse.urlparse(target_subdomain)
        target_subdomain = f"{parsed_url.netloc}"
    else:
        target_subdomain = target_subdomain
    # create nmap object

    print("Port Scanning :",target_subdomain)
    nm = nmap.PortScanner()

    # set scanning arguments based on mode
    if scan_mode == 'quick':
        arguments = '-F'
    elif scan_mode == 'full':
        arguments = '-p-'
    # elif(scan_mode == 'custom'):
    #     arguments = '-p' + ",".join(cus_ports)

    # scan ports on target subdomain
    nm.scan(hosts=target_subdomain, arguments=arguments)

    # get open ports
    open_ports = []
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in lport:
                if nm[host][proto][port]['state'] == 'open':
                    open_ports.append(port)

    return open_ports

# print(scan_ports("http://testphp.vulnweb.com","quick"))