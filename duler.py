#coding:utf-8
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import logging

m = 'job_test'
f = 'job_test'

mo =__import__(m)
func = getattr(mo,f)
func()