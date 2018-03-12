import pymysql
from datetime import datetime
class DBControl:
	def __init__(self, _host, _id, _pw, _dbname, _port=3306):
		#self.con = pymysql.connect(host, port, id, pw, dbname, charset='utf8')
		self.con = pymysql.connect(host=_host, port=_port, user=_id, password=_pw, database=_dbname, charset='utf8')
		self.cur = self.con.cursor(pymysql.cursors.DictCursor)
		self.cur.execute("set names utf8")
	def __del__(self):
		self.con.close()
		
	##테이블생성
	def createTable(self, tableName, tags, bytesOfTags):
		sql = "create table " + tableName + " ( id int(1) not null,"
		if not isinstance(tags, tuple):
			sql+=("%s varchar(%d) not null," % (tags, bytesOfTags))
		else:
			for i in range(len(tags)):
				sql+=("%s varchar(%d) not null," % (tags[i], bytesOfTags[i]))
		sql+="primary key(id) );"
		self.cur.execute(sql)
		self.con.commit()

	##테이블제거
	def removeTable(self, tableName):
		sql = "drop table " + tableName
		self.cur.execute(sql)
		self.con.commit()

	def emptyTable(self, tableName):
		sql = "truncate " + tableName
		self.cur.execute(sql)
		self.con.commit()
		
		
	##테이블확인
	def isThisTable(self, tableName):
		self.cur.execute("show tables like '%s'" % tableName)
		printstr =str(self.cur.fetchall())
		return tableName in printstr
	
	def getRowViaSql(self, tableName):
		self.cur.execute( "select count(*) from %s;" % tableName)
		answer = self.cur.fetchall()
		return list(answer[0].values())[0]
	
	##데이터추가
	def addData(self, tableName, tags, data, id):
		if len(tags) != len(data) and isinstance(tags, tuple):
			return False
			
		sql = "insert into " + tableName + " (id,"
		if not isinstance(tags, tuple):
			sql+=tags+","
		else :
			for i in tags:
				sql+=(i+",")
			
		sql=sql[:-1] + (") values ('%d'," % id)
		if not isinstance(tags, tuple):
			sql+=("'%s'," % data)
		else:
			for i in data:
				sql+=("'%s'," % i)
		sql=sql[:-1] + ") ;"
		self.cur.execute(sql)
		self.con.commit()
		return True
		
		