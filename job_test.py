import random
def job_test():
	f = open('test','w')
	f.write(str(random.random()))
	f.close()