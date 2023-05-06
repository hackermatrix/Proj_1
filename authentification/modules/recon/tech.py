import builtwith

def get_tech_stack(url):
    
    print("[+] Collecting Technology Information")
    data ={}
    result = builtwith.builtwith(url)
    print("Technology stack used by the website:")
    for key, value in result.items():
        if(key=="cms"):
            data["cms"]=''.join(value)
        if(key=="programming-languages"):
            data["programminglanguages"]=''.join(value)
        if(key=="web-servers"):
            data["webservers"]=''.join(value)
      #  print(key + ": " + ", ".join(value))

    return (data)

# print(get_tech_stack("http://testphp.vulnweb.com"))
