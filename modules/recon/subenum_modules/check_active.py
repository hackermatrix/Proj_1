import subprocess


def check_active(subdoms):

    print(subdoms)
    proc = subprocess.Popen(['httpx',subdoms], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    print(out)

with open("sample.txt","r") as subs:
    subdoms = subs.read()
    print(check_active(subdoms))
