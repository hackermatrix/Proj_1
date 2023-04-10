import subprocess

target = "https://public-firing-range.appspot.com"

def nikto_scan(target):
    print(f"Scanning target {target}...")

    params = {'ssl': 1, 'maxtime': 600, 'Plugins': 'apacheusers'}

    args = ['nikto', '-host', target]
    for key, value in params.items():
        args.append(f'-{key}')
        if value is not None:
            args.append(str(value))
    
    args += ['-o', f'{target.split("//")[-1]}.xml', '-Format', 'xml', '-Display','V']
    

    nikto_process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output, error = nikto_process.communicate()

    print(f"Scan of target {target} finished.")

    if error:
        print(f"Error while scanning target {target}:")
        print(error.decode())

    for line in output.decode().split('\n'):
        print(line)


nikto_scan(target)