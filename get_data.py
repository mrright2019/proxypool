from config import *


sql = "select * from proxy where https=0 and is_alive=1;"
res = db.execute(sql)
for i in res:
	print(i)