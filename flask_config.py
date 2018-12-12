from config import *
JOBS = []



def job_list_init():
	sql = "select * from jobs where is_run = 1;"
	jobres = db.execute(sql)
	if len(jobres) == 0:
		return []
	result = []
	for job in jobres:
		item = {}
		item['id'] = job['jname']
		item['func'] = job['func']
		item['args'] = job['args']
		item['trigger'] = job['trigger']
		item['seconds'] = job['seconds']
		result.append(item)
	return result
JOBS = job_list_init()
# print(JOBS)

def test():
	print('asdsad')