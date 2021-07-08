import pymysql
from cryptography.fernet import Fernet
import configparser
import os

class DBControl:
	def __init__(self, _dbname):
		key = b'JEfz5xn3zNlNJYdUK1UZsRzVGzcGV5tYl5MwXwnQlfg='
		self.config = configparser.RawConfigParser()
		self.config.read('info.properties')
		self.fernet = Fernet(key)

		self.port = 3306
		self.host = self.getInfo('db.url')
		self.id = self.getInfo('db.id')
		self.pw = self.getInfo('db.pwd')
		self.dbNm = _dbname
		self.con = pymysql.connect(host=self.host, port=self.port, user=self.id, password=self.pw, database=self.dbNm, charset='utf8')
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

	def getJoamData(self):
		self.cur.execute("SELECT ROUTE_ID, IS_ONEWAY, MID_STATION FROM route where IS_ONEWAY is not null;")
		answer = self.cur.fetchall()
		return list(answer)

	def setJoamData(self, dataList):
		dataList = [[row['IS_ONEWAY'],row['MID_STATION'],row['ROUTE_ID']] for row in dataList]
		self.cur.executemany("UPDATE route set IS_ONEWAY = %s, MID_STATION = %s WHERE ROUTE_ID = %s;", dataList)
		self.con.commit()

	def dumpdb(self, tableNm):
		command = []
		command.append("mysqldump")
		command.append("-h%s" % self.host)
		command.append("-u%s" % self.id)
		command.append("-p%s" % self.pw)
		command.append("%s" % self.dbNm)
		command.append("%s > ./%s.sql" % (tableNm, tableNm))
		command = " ".join(command)
		os.system(command)
	
	def restoredb(self, tableNm):
		command = []
		command.append("mysql")
		command.append("-h%s" % self.host)
		command.append("-u%s" % self.id)
		command.append("-p%s" % self.pw)
		command.append("%s" % self.dbNm)
		command.append("< ./%s.sql" % (tableNm))
		command = " ".join(command)
		os.system(command)
