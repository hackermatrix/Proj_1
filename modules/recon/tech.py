import builtwith

def get_tech_stack(url):
    result = builtwith.builtwith(url)
    print("Technology stack used by the website:")
    for key, value in result.items():
        print(key + ": " + ", ".join(value))

get_tech_stack("http://www.enova.com")
