import pymysql
from cryptography.fernet import Fernet
import configparser
from datetime import datetime

class DBControl:
	def __init__(self, _dbname):
		key = b'JEfz5xn3zNlNJYdUK1UZsRzVGzcGV5tYl5MwXwnQlfg='
		self.config = configparser.RawConfigParser()
		self.config.read('info.properties')
		self.fernet = Fernet(key)

		_port = 3306
		_host = self.getInfo('db.url')
		_id = self.getInfo('db.id')
		_pw = self.getInfo('db.pwd')
		self.con = pymysql.connect(host=_host, port=_port, user=_id, password=_pw, database=_dbname, charset='utf8')
		self.cur = self.con.cursor(pymysql.cursors.DictCursor)
		self.cur.execute("set names utf8")
	def __del__(self):
		self.con.close()

	def getInfo(self, proKey) :
		return (self.fernet.decrypt(bytes(self.config.get('db', proKey), 'utf-8'))).decode("utf-8")
		
	##테이블생성
	def createTable(self, dllSql):		
		self.cur.execute(dllSql)
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
	def addData(self, tableName, tags, data):
		if len(tags) != len(data) and isinstance(tags, tuple):
			return False
			
		sql = "insert into " + tableName + " ("
		if not isinstance(tags, tuple):
			sql+=tags+","
		else :
			for i in tags:
				sql+=(i+",")
			
		sql=sql[:-1] + ") values ("
		if not isinstance(tags, tuple):
			sql+=("'%s'," % data)
		else:
			for i in data:
				if i == '':
					sql += ("NULL,")
				else:
					sql += ("'%s'," % i)
		sql=sql[:-1] + ") ;"
		self.cur.execute(sql)
		self.con.commit()
		return True
		