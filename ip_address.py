#coding:utf-8
import requests
import json
ipinfoheaders = {
	'Host': 'ip-api.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
	'Accept': '*/*',
	'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
	'Accept-Encoding': 'gzip, deflate, br',
	'Connection': 'keep-alive',
	'TE': 'Trailers',
}

def ipinfo_1(ip):
	try:
		ipres = requests.get("https://geoip-db.com/jsonp/"+ip,timeout = 10)
		jsondata = json.loads(ipres.content)
		item = {}
		item['ip'] = ip
		item['country_name'] = jsondata['country_name']
		item['country_code'] = jsondata['country_code']
		item['city'] = '' if jsondata['city'] == "Not Found." else jsondata['city']
		return item
	except Exception as e:
		# print(e)
		return None




def ipinfo_2(ip):
	try:
		url = "http://ip-api.com/json/"+ip+""
		ipres = requests.get(url,headers=ipinfoheaders,timeout=30)
		if ipres.status_code!=200:
			return None
		ipinfo = json.loads(ipres.content)
		item['ip'] = ip
		item['city'] = ipinfo['city']
		item['country_name'] = ipinfo['country']
		item['country_code'] = ipinfo['countryCode']
		return item
	except Exception as e:
		return None



def get_ip_info(ip):
	result = ipinfo_1(ip)
	if result != None:
		return result
	else:
		return ipinfo_2(ip)

if __name__ == "__main__":
	print(get_ip_info("22.33.44.6"))

