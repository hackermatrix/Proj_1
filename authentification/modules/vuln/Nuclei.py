import os
import subprocess
import time
from django.http import StreamingHttpResponse
import re
import json
import sys
# sys.path.insert(0,"/home/popeye/Documents/final_year_proj/code/backend/authentification/")
from authentification.models import Nucleiscan

def parse_nuclei_output(output):
    pattern = re.compile(r'\x1b[^m]*m')
    lines = output.replace("[","").replace("]","")
    parsed = pattern.sub('', lines)
    parsed = parsed.split(" ")

    # Format information as JSON object
    data = {
        "Vuln": parsed[0],
        "severity": parsed[2],
        "url": parsed[3]
    }
    return data

def start_nuclei_scan(url,subdomain,user):
    def generate_events():
        try:
            # Run nuclei command with real-time output capture
            cmd = ['nuclei', '-u', url]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            count=0
            while True:
                count+=1
                print(f"Generating output:{count}")
                output = process.stdout.readline().strip()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    # Parse output and send as SSE event
                    data = parse_nuclei_output(output)

                    # Preparing data to be entered into the database
                    vulnerability = data['Vuln']
                    severity = data['severity']
                    vulnerable_url = data['url']
                    endpoint_name = url
                    subdomain_name = subdomain

                    #Entering the data to the database
                    print("yes!!")
                    scan = Nucleiscan(endpoint_name=endpoint_name,
                           severity=severity,
                           vulnerability=vulnerability,
                           vulnerable_url=vulnerable_url,
                           subdomain_name=subdomain_name,
                           user = user)
                    scan.save()
                    


                    json_data = json.dumps(data)
                    event = "{\"data\": "+f"{json_data}"+"}"
                    yield event
                    time.sleep(0.1)

            # Capture stderr and return code
            process.stdout.close()
            process.stderr.close()
            return_code = process.returncode
            if return_code != 0:
                event = "{\"data\": "+f"ERROR: {return_code}"+"}"
                yield event
        
        except Exception as e:
            event = "{\"data\": "+f"ERROR: {e}"+"}"
            yield event


#
    def fetch_data():
        print("love from database")
        for entry in nuclei_scan:
            vulnerable_url = entry.vulnerable_url
            severity = entry.severity
            vulnerability = entry.vulnerability
            json_data = json.dumps({"Vuln":f"{vulnerability}","severity":f"{severity}","url":f"{vulnerable_url}"})
            event = "{\"data\": "+f"{json_data}"+"}"
            yield event
            time.sleep(0.5)


    
    nuclei_scan = Nucleiscan.objects.filter(endpoint_name=url,subdomain_name=subdomain,user=user)
    

    if(nuclei_scan.exists()):

        return StreamingHttpResponse(fetch_data(), content_type='text/event-stream')
    else:
        print("YEY")
        return StreamingHttpResponse(generate_events(), content_type='text/event-stream')
