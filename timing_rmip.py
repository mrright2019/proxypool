#coding:utf-8
from config import *
from mysql_db import *
import re
import threading

lock = threading.Lock()
count = 0
all_thread_num = 1
deal_num = 100


def setcount():
	global count,all_thread_num
	count = db.select_count_table("proxy")
	count = int(re.findall("[0-9]+",str(count))[0])
	all_thread_num = int(count/100+1 if count/100+1 > 5 else 5)

def thread_ch(thread_num):
	"""
	@return 0 还有下一页
	@return 1 没有下一页
	"""
	sql = "select * from `proxy` where is_alive=1 and pid >="+str(thread_num*100)+" and pid <"+ str((thread_num+1)*100)
	lock.acquire()
	sqlres = db.execute(sql)
	lock.release()
	if len(sqlres)==0 and thread_num>deal_num:
		return 1
	for item in sqlres:
		print(item['host'])
		if check_ip(item['host'],item['port'])==False:
			lock.acquire()
			db.update("proxy",{'is_alive':0},'host',item['host'])
			lock.release()
		else:
			lock.acquire()
			db.update("proxy",{'is_alive':1},'host',item['host'])
			lock.release()
	return 0


def thread_run(thread_num):
	rmres = thread_ch(thread_num)
	# print(thread_num)
	while thread_num < int(count/100):
		thread_num+=6
		print(thread_num)
		rmres = thread_ch(thread_num)

def rmip_job():
	setcount()
	works = []
	for num in range(all_thread_num):
		print(num)
		t = threading.Thread(target=thread_run,args=(num,))
		t.start()
		works.append(t)
	for t in works:
		t.join()

# thread_ch(3)
if __name__ =="__main__":
	rmip_job()