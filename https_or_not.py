#coding:utf-8
import requests
from config import *
import json
url = "http://api.ip.data5u.com/api/get.shtml?order=aa096aa87bac8085956a8ed984917600&num=100&area=%E4%B8%AD%E5%9B%BD&carrier=0&protocol=1&an1=1&an2=2&an3=3&sp1=1&sp2=2&sp3=3&sort=1&system=1&distinct=0&rettype=0&seprator=%0D%0A"

url_res = requests.get(url)
res = json.loads(url_res.content.decode('utf-8'))['data']

# print(res)
# exit()
# print(res)

x = 0
y = 0
for ipinfo in res:
	proxy = {
		"http":ipinfo['ip']+":"+str(ipinfo['port']),
		"https":ipinfo['ip']+":"+str(ipinfo['port'])
	}
	try:
		ipres = requests.get("https://zengyonghua.xyz/index/spread/test2",proxies=proxy,timeout=2)
		result = ipres.content.decode('utf-8')
		print(result)
		jsondata = json.loads(result)
		if jsondata['ip1'] == ipinfo['ip'] and jsondata['ip2'] == ipinfo['ip'] and jsondata['HTTP_X_FORWARDED_FOR']==None:
			y+=1	# pri(ipinfo['host']))
	except:
		pass
	x+=1

	# exit()
print('x:',x)
print('y:',y)