import subprocess 
import os
import whois
import requests
import json

#Setting Variables

base_dir = os.path.dirname(os.path.dirname(__file__))
xml_dir = os.path.join(base_dir,"xml")


# Passive Information Gathering Section:
class PassiveInformationGathering:
    def __init__(self, target):
        self.target = target

    def whois_lookup(self):
        result = whois.whois(self.target)
        print(result)
    
    def wappalyzer_lookup(self):
        api_key="BPRtOcpd0K6dIDdJnCTeR5aRg2xtst3V4tpb3wdx"
        wappalyzer_url = f"https://api.wappalyzer.com/v2/lookup?url={self.target}"
        response = requests.get(wappalyzer_url,headers={"x-api-key":api_key})
        if response.status_code == 200:
            result = json.loads(response.text)
            technologies = result["data"]
            print("Technologies used:")
            for technology in technologies:
                print(technology["name"])
        else:
            print("Error: API request failed.")
      
# Active Information Gathering Section:
class ActiveInformationGathering:
    def __init__(self, target):
        self.target = target

    def port_scanning(self):
        os.system("nmap -Pn " + self.target)

if __name__ == "__main__":
    target = input("Enter target: ")
    passive_information_gathering = PassiveInformationGathering(target)
    passive_information_gathering.whois_lookup()
    passive_information_gathering.wappalyzer_lookup()
    active_information_gathering = ActiveInformationGathering(target)
    active_information_gathering.port_scanning()
