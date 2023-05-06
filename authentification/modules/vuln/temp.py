# import re

# def parse_nuclei_output(output):
#     pattern = re.compile(r'\x1b[^m]*m')
#     lines = output.replace("[","").replace("]","")
#     parsed = pattern.sub('', lines)
#     parsed = parsed.split(" ")

#     # Format information as JSON object
#     data = {
#         "Vuln": parsed[0],
#         "severity": parsed[2],
#         "url": parsed[3]
#     }
#     return data

# eg = "[tech-detect:nginx] [http] [info] http://testphp.vulnweb.com/listproducts.php?cat=1"

# print(parse_nuclei_output(eg)['Vuln'])

from authentification.models import Nucleiscan

url="http://testphp.vulnweb.com/listproducts.php?cat=1"


nuclei_scan = Nucleiscan.objects.filter(endpoint_name=url)

print(nuclei_scan)
