import pymysql,os
import sys,time,urllib,hashlib
import traceback
def array_join(arr, c):
    t = ''
    for a in arr:
        t += "'%s'" % str(a).replace("'","\\\'") + c
    return t[:-len(c)]

class MysqlDB(object):

    def __init__(self, conf):
        self.conf = conf
        config = {
            'host': conf['host'],
            'port': conf['port'],
            'user': conf['user'],           
            'passwd': conf['passwd'],
            'charset':'utf8mb4', # 支持1-4个字节字符
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.conn = pymysql.connect(**config)
        self.conn.autocommit(1)
        self.conn.select_db(conf['database'])
        self.execute("SET NAMES utf8mb4");

    def select_count_table(self,table):
        sql = "select count(*) from "+table
        return self.execute(sql)

    def saveexception(self,info):
        if info.find('generic exception:') >= 0 or info.find('Traceback') >= 0 or info.find('mysql异常') >= 0:
            hashstr = hashlib.md5(info.encode("utf8")).hexdigest()
            result = self.select('voice_log', 'hash', hashstr)
            if len(result) > 0:
                return
            content = info.replace('generic exception:', '')
            data = {}
            data['content'] = urllib.parse.quote(content)
            data['type'] = 'exception'
            data['hash']=hashstr
            data['time'] = time.time()
            self.insert('voice_log', data)
        else:
            print(info)

    def exitwithid(self, table, idkey, value):

        result = self.select(table, idkey, value)
        if len(result) > 0:
            return result[0][idkey]
        return 0
    def lastinsertid(self):
        return self.execute(sql='SELECT  LAST_INSERT_ID() as fid')
    def show_tables(self):
        c = self.conn.cursor()
        sql = 'SHOW TABLES'
        c.execute(sql)
        return [r['Tables_in_'+self.conf['database']] for r in c.fetchall()]
    def insert(self, table, modal):
        try:
            listkey = ["`"+r+"`" for r in modal.keys()]
            listvalues = ["\""+str(r)+"\""  for r in modal.values()]
            sql = 'INSERT INTO %s(%s) VALUES (%s)' % (table, ','.join(listkey), ','.join(listvalues))
            return self.execute(sql=sql)

        except:
            print('sql insert except')
            self.saveexception(traceback.format_exc())
            self.saveexception(sql)
            return 0

    def selectbrandname(self):#获取采集过公众号
        sql='select brandname  from brand_file GROUP BY brandname'
        return self.execute(sql=sql)
    def update(self,table,modal,field='', condition=''):
        try:
            sql = 'update  %s set ' % table
            for key, value in modal.items():
                sql = sql +"`"+ key+"`" + '=\"' + str(value) + '\",'
            sql=sql.rstrip(',')
            if field and condition:
                sql += " WHERE %s='%s'" % (field, condition)
            return self.execute(sql=sql)
        except Exception:
            print('sql update except')
            self.saveexception(traceback.format_exc())
            self.saveexception(sql)
            return 0

        #UPDATE persondata SET ageage=age*2, ageage=age+1;

    def select(self, table, field='', condition=''):
        """
        @brief      select all result from table
        @param      table  String
        @param      field  String
        @param      condition  String
        @return     result  Tuple
        """
        sql = "SELECT * FROM %s" % table
        if field and condition:
            sql += " WHERE %s='%s' limit 1" % (field, condition)

        return self.execute(sql)


    def execute(self, sql):
        """
        @brief      execute sql commands, return result if it has
        @param      sql  String
        @param      value  Tuple
        @return     result  Array
        """
        c = self.conn.cursor()
        hasReturn = sql.lstrip().upper().startswith("SELECT")
        success=1
        result = []
        try:

            c.execute(sql)

            if hasReturn:
                result = c.fetchall()

        except Exception:
            self.saveexception('mysql异常:'+sql)
            self.saveexception(traceback.format_exc())
            self.conn.rollback()
            success=0
        finally:
            if hasReturn:
                return result
            else:
                return success