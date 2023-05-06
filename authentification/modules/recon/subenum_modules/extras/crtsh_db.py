import psycopg2
import sys
import os
# current = os.path.dirname(os.path.realpath(__file__))
# root = os.path.dirname(current)

# import subenum as parent




async def crtsh(hostname):
	try:
		conn = psycopg2.connect(
			host="crt.sh",
			database="certwatch",
			user="guest",
			port="5432"
		)
		conn.autocommit = True
		cur = conn.cursor()
		query = f"SELECT ci.NAME_VALUE NAME_VALUE FROM certificate_identity ci WHERE ci.NAME_TYPE = 'dNSName' AND reverse(lower(ci.NAME_VALUE)) LIKE reverse(lower('%.{hostname}'))"
		cur.execute(query)
		result = cur.fetchall()
		cur.close()
		conn.close()
		tmp_list = []	
		for url in result:
			tmp_list.append(url[0])
		print(f'[+]CRT.sh FOUND:{len(tmp_list)} subdomains!')
		return (set(tmp_list))
	except Exception as e:
		print(f'[-]crtsh Exception :{e}')