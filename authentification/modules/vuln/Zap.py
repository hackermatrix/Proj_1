import subprocess
import json
import time
from pprint import pprint
from zapv2 import ZAPv2
import urllib.parse





apiKey = '12345'

# By default ZAP API client will connect to port 8080
zap = ZAPv2(apikey=apiKey,proxies={'http':'http://127.0.0.1:8090'})


# Function to perform spidering
def perform_spidering(target):
    print('Spidering target {}'.format(target))
    # The scan returns a scan id to support concurrent scanning
    scanID = zap.spider.scan(target)
    while (int(zap.spider.status(scanID)) < 100):
        # Poll the status until it completes
        print('Spider progress %: {}'.format(zap.spider.status(scanID)))
        time.sleep(5)

    print('Spider has completed!')
    # Prints the URLs the spider has crawled
    return zap.spider.results(scanID)


def ajax_spider(target):
    print('Ajax Spider target {}'.format(target))
    scanID = zap.ajaxSpider.scan(target)

    timeout = time.time() + 60*2   # 2 minutes from now
    # Loop until the ajax spider has finished or the timeout has exceeded
    while zap.ajaxSpider.status == 'running':
        if time.time() > timeout:
            break
        print('Ajax Spider status' + zap.ajaxSpider.status)
        time.sleep(2)

    print('Ajax Spider completed')
    ajaxResults = zap.ajaxSpider.results(start=0, count=10)
    print(ajaxResults)




# Function to perform quick scan
def perform_quick_scan():
    while int(zap.pscan.records_to_scan) > 0:
        # Loop until the passive scan has finished
        print('Records to passive scan : ' + zap.pscan.records_to_scan)
        time.sleep(2)

    print('Passive Scan completed')

    # Print Passive scan results/alerts
    print('Hosts: {}'.format(', '.join(zap.core.hosts)))
    print('Alerts: ')
    pprint(zap.core.alerts())




# Function to perform active scan
def perform_active_scan(target):
    print('Active Scanning target {}'.format(target))
    scanID = zap.ascan.scan(target)
    while int(zap.ascan.status(scanID)) < 100:
        # Loop until the scanner has finished
        print('Scan progress %: {}'.format(zap.ascan.status(scanID)))
        time.sleep(5)

    print('Active Scan completed')
    # Print vulnerabilities found by the scanning
    print('Hosts: {}'.format(', '.join(zap.core.hosts)))

    # Getting the base url from the target url
    parsed_url = urllib.parse.urlparse(target)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    print('Alerts: ')
    return zap.core.alerts(baseurl=base_url)




# target="http://testphp.vulnweb.com/"

# perform_spidering(target)

# perform_active_scan(target)