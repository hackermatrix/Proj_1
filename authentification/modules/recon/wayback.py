import os
import subprocess
from urllib.parse import urlparse, parse_qs

# def find_endpoints(url):
#     print(url)
#     try:
        
#         count=100
#         # Run waybackurls command to fetch URLs from archive.org
#         cmd = f'waybackurls {url} | head -n {count}'
#         output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)

#         # Extract endpoints with parameters from output
#         endpoints = set()
#         for line in output.splitlines():
#             if '?' in line:
#                 endpoints.add(line)
#                 # if len(endpoints) >= 100:
#                 #       break


#         return (list(endpoints))
#     except subprocess.CalledProcessError:
#         return ({'error': 'Failed to run waybackurls command. Please make sure you have waybackurls installed.'})
    

def find_endpoints(url):
    print(url)
    try:
        count=500
        # Run waybackurls command to fetch URLs from archive.org
        cmd = f'waybackurls {url} | head -n {count}'
        output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)

        # Extract endpoints with parameters from output
        endpoints = set()
        for line in output.splitlines():
            if '?' in line:
                parsed_url = urlparse(line)
                base_url = parsed_url.scheme+"://"+parsed_url.netloc+parsed_url.path+"?"
                query_params = parse_qs(parsed_url.query)
                for i in query_params.keys():
                    base_url+=i.strip()+"="+"&"

                endpoints.add(base_url)

        return list(endpoints)
    except subprocess.CalledProcessError:
        return {'error': 'Failed to run waybackurls command. Please make sure you have waybackurls installed.'}



# target="http://testphp.vulnweb.com"
# print(find_endpoints(target))

