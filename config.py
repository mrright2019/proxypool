#coding:utf-8
import os,codecs,time
import requests
debug = True
from  mysql_db import *
def savelog(*args):
	logstr = ""
	for s in args:
		logstr += str(s)
	if debug:
	    print(logstr)
	else:
	    filename= str(os.getpid())+'.txt'
	    logtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
	    fd = codecs.open('log/'+filename, 'a+', encoding='utf8')
	    fd.write(logtime+'  '+logstr + '\n')
	    fd.close()

def check_ip(ip,port):
	try:
		proxy = {
			"http":ip+":"+str(port),
			"https":ip+":"+str(port)
		}
		requests.get("https://www.instagram.com/",proxies = proxy,timeout=5)
		return True
	except Exception as e:
		savelog(e)
		return False


ipheaders ={
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
}


ipinfoheaders = {
	'Host': 'ip-api.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
	'Accept': '*/*',
	'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
	'Accept-Encoding': 'gzip, deflate, br',
	'Connection': 'keep-alive',
	'TE': 'Trailers',
}


db = MysqlDB({
'host': 'localhost',
'port': 3306,
'user': 'root',
'passwd': 'root',
'database': 'proxypool',
})


from flask_config import *
class falsk_jobs_config(object):

	JOBS = JOBS

	def __init__(self):
		pass



