from flask import Flask,redirect,url_for,session
from flask import render_template
from flask import request
from flask_apscheduler import APScheduler
from datetime import timedelta
from mysql_db import *
import json
from config import *
from ip_address import *
app = Flask(__name__)
app.config.from_object('flask_config')
app.config['SECRET_KEY']=os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=7)
sched = APScheduler()
sched.init_app(app)
sched.start()

@app.route('/')
def index():
	session.permanent=True
	return render_template("login.html")


@app.route('/api/',methods=['GET'])
def api():
	try:
		# num = request.args.get('num') if request.args.get('num') != None else 1
		# ip_type = request.args.get('type') if request.args.get('type') != None else 'http'
		page = request.args.get('page') if request.args.get('page') != None else 0
		try:
			page = int(page)
		except:
			page = 0
		# page = 0
		# https = 1 if ip_type == 'https' else 0
		sql = 'select host,port,city,country,https from proxy where `using` = 0 and `is_alive` = 1 order by pid limit '+str(page*10)+",10;"
		db = MysqlDB({
			'host': 'localhost',
			'port': 3306,
			'user': 'root',
			'passwd': 'root',
			'database': 'proxypool',
		})
		sqlres = db.execute(sql)
		# return str(sql)
		data = {}
		if len(sqlres) == 0:
			data['status'] = 'false'
			return json.dumps(data)
		data['status'] = 'true'
		data['data'] = []
		for ip in sqlres:
			data['data'].append(ip)
		return json.dumps(data)
	except Exception as e:
		return str(e)

def checkuser(username,password):
	sql = 'select * from `user` where uname = "'+username+'" and upwd = "' +password+'";'
	# print(sql)
	ures = db.execute(sql)
	if len(ures)==0:
		return False
	return True

@app.route('/jobs',methods=['POST','GET'])
def jobs():
	job_list = sched.get_jobs()
	job_data_list = []
	for job in job_list:
		job_data_list.append(job.__getstate__())
	if session.get('is_login') != None:
		return render_template('jobs.html',job_list = job_data_list)
	if request.method != "POST":
		return ''
	try:
		if checkuser(request.form['username'],request.form['password']) == False:# != 'admin' or request.form['password']!='admin':
			return ''
	except:
		pass
	session['is_login'] = request.form['username']
	return render_template('jobs.html',job_list = job_data_list)


@app.route('/test')
def ht_test():
	return str(sched.get_jobs())


@app.route('/stop',methods=['GET','POST'])
def stop_job():
	try:
		jid = request.form['jid']
		if jid == None:
			return str({'state':'false'})
		job = sched.get_job(jid)
		if job == None:
			return str({'state':'false'})
		job.pause()
		return str({'state':'success'})
	except Exception as e:
		print(e)
		return str({'state':'false'})

@app.route('/resume',methods=['GET','POST'])
def resume_job():
	try:
		jid = request.form['jid']
		if jid == None:
			return str({'state':'false'})
		job = sched.get_job(jid)
		if job == None:
			return str({'state':'false'})
		job.resume()
		return str({'state':'success'})
	except Exception as e:
		print(e)
		return str({'state':'false'})


@app.route('/remove',methods=['GET','POST'])
def remove_job():
	db.update('jobs',{'is_run':0},'jname', request.form['jid'])
	try:
		jid = request.form['jid']
		if jid == None:
			return str({'state':'false'})
		job = sched.get_job(jid)
		if job == None:
			return str({'state':'false'})
		job.pause()
		job.remove()
		return str({'state':'success'})
	except Exception as e:
		print(e)
		return str({'state':'false'})

@app.route('/add')
def add_job():
	return render_template('add.html')
@app.route('/add_script',methods=['POST'])
def add_script():
	jname = request.form['jname']
	args = request.form['args']
	func = request.form['func']
	seconds = request.form['seconds']
	try:
		seconds = int(seconds)
	except:
		return 'cant int seconds'
	try:
		funcpg = str(func).split(":")
		if len(funcpg)<2:
			return 'func:package error'
		mymod = __import__(funcpg[0])
		fun = getattr(mymod,funcpg[1])
		if fun == None:
			return "No such function"
		sched.add_job(func=fun,args=args,id=jname,trigger='interval',seconds=seconds)
		db.insert('jobs',{'args':args,'jname':jname,'seconds':seconds,'func':func,'trigger':'interval','is_run':1})
		return redirect(url_for('jobs'))
	except Exception as e:
		return str(e)
		return 'func error'
	return args+jname+func+seconds


def htss():
	# print(sched.get_jobs())
	print(sched.get_job('ip_spider_free_ip').__getstate__())
	print(type(sched.get_job('asd').__getstate__()))


if __name__ == '__main__':
	# sched.add_job(func=eval('flask_config:test'),id="asd",trigger='cron',second='*/5')
	# sched.get_job('asd').pause()
	# sched.add_job(func=htss,id="asd2",trigger='cron',second='*/5')
	app.run(debug=True)


