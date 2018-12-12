#coding:utf-8

import requests
import ssl,json
from config import *
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()
from ip_address import *

if hasattr(ssl,'_create_unverified_context'):
	ssl._create_default_https_context = ssl._create_unverified_context





import threading
class spider(object):
    url_list = ["https://free-proxy-list.net/","https://www.us-proxy.org/","https://www.socks-proxy.net/"]
    def __init__(self):
        self.sess = requests.Session()
        self.sess.headers = ipheaders
        self.sess.verify = False
        self.look = threading.Lock()

    def run(self):
    	self.works = []
    	for url in self.url_list:
    		t = threading.Thread(target = self.run_threading,args=(url,))
    		t.start()
    	for t in self.works:
    		t.join()
    	# self.run_threading(url = self.url_list[1])

    def run_threading(self,url = url_list[0]):
    	ipres = self.sess.get(url)
    	savelog(url,":",ipres)
    	ipres_soup = BeautifulSoup(ipres.content,"html.parser")
    	tr_list = ipres_soup.find_all("tr")
    	for tr in tr_list:
    		td_list = tr.find_all("td")
    		if len(td_list)!=8:
    			continue
    		ipitem = {}
    		ipitem['host'] = td_list[0].get_text().replace("\n","").replace(" ","")
    		ipitem['port'] = td_list[1].get_text().replace("\n","").replace(" ","")
    		savelog(ipitem['host'])
    		self.look.acquire()
    		if db.exitwithid("proxy","host",ipitem['host'])!=0:
    			self.look.release()
    			continue
    		self.look.release()
    		if check_ip(ipitem['host'],ipitem['port']) == False:
    			continue
    		ip_info=get_ip_info(ipitem['host'])
    		if ip_info != None:
	    		ipitem['country'] = ip_info['country_code']
	    		ipitem['city'] = ip_info['city']
	    	else:
	    		ipitem['country'] =''
	    		ipitem['city'] = ''
    		ipitem['https'] = 0 if "no" in td_list[-2].get_text() else 1
    		ipitem['weight'] = 0
    		ipitem['is_alive'] = 1
    		ipitem['use_num'] = 0
    		ipitem['using'] = 0
    		savelog(ipitem)
    		self.look.acquire()
    		db.insert('proxy', ipitem)
    		self.look.release()


def free_proxy_job():
    s = spider()
    s.run()


if __name__ =="__main__":
	free_proxy_job()