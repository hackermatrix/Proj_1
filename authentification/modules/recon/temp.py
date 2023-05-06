from urllib.parse import urlparse, parse_qs

url = "http://testhtml5.vulnweb.com:80/static/css/?"

parsed_url = urlparse(url)
base_url = parsed_url.scheme+"://"+parsed_url.netloc+parsed_url.path+"?"
query_params = parse_qs(parsed_url.query)
# for i in query_params.keys():
#     base_url+=i+"="+"&"
# endpoint = base_url
print(query_params)