import re
import requests


def hack_tar(self,dir):
    url = "https://api.hackertarget.com/hostsearch//"
    res = requests.get(url=url,params={"q":f"{self.target}"})
    subs=re.findall(f'\w.*{self.target}',res.text)
    subs = list(set(subs))