import subprocess

target = "http://testphp.vulnweb.com/"

def nikto_scan(target):
    print(f"Scanning target {target}...")

    #Adding custom parameters to NIKTO.
    params = {'ssl': 1, 'Plugins': 'apacheusers'}
    

    #If the application has a authentication page, and if the user and password are know, use these params
    user ='asdas'
    password = 'asdas'

    if(user and password):
        params["id"]=f"{user}:{password}"


    args = ['nikto', '-host', target]
    for key, value in params.items():
        args.append(f'-{key}')
        if value is not None:
            args.append(str(value))

    #appending the parameters as arguments to the args array.
    
    args += ['-o', f'{target.split("//")[-1]}.xml', '-Format', 'xml', '-Display','V']

    #appending file name to args array to save in the respective xml file.
    

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