import os
import subprocess
import time
from django.http import StreamingHttpResponse
import re
import json

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

def start_nuclei_scan(url):
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
                    json_data = json.dumps(data)
                    event = "{\"data\": "+f"{json_data}"+"}"
                    yield event
                    time.sleep(0.5)

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

    return StreamingHttpResponse(generate_events(), content_type='text/event-stream')
