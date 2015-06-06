import sqlite3
import os.path


class myDb:
	def __init__(self):
		# if not os.path.isfile('new.db')  :
		self.DB = sqlite3.connect('test.db')
		self.C = self.DB.cursor()
		self.T = dict()
		self.tables()
		
	# support basic SQL create table statement
	def tables(self) :
		self.C.execute("SELECT tbl_name FROM sqlite_master WHERE type='table';")
		dataT = self.C.fetchall()
		for e in dataT :
			self.C.execute("SELECT sql FROM sqlite_master WHERE type='table' AND tbl_name='" + e[0] +"';")
			dataSQL = self.C.fetchall()
			dataSQL = dataSQL[0][0]
			dataSQL = dataSQL.split(' ')
			dataSQL = '#'.join(dataSQL)
			dataSQL = dataSQL.split('(')
			dataSQL = '#'.join(dataSQL)
			dataSQL = dataSQL.split(')')
			dataSQL = '#'.join(dataSQL)
			dataSQL = dataSQL.split('#')
			dataSQL = [t for t in dataSQL if not t == ""]
			dataSQL = dataSQL[3:len(dataSQL)]
			dataSQL = ' '.join(dataSQL)
			dataSQL = dataSQL.split(',')
			
			typeF = dict()
			
			for t in dataSQL :
				t = t.split(' ')
				t = [tt for tt in t if not tt == ""]
				typeF[t[0]] = ' '.join(t[1:len(t)])
			
			self.T[e[0]] = typeF
		return self.T
		
	# show all datas	
	def datas(self, tableName) :
		if not tableName in  list(self.T.keys()) :
			return []
		
		F = self.T[tableName]
		cols = ','.join(F)
		
		preSQL = "SELECT " + cols + " FROM " + tableName + ";"
		self.C.execute(preSQL)
		
		dataS = self.C.fetchall()
		dataT = [list(F.keys())]
		
		for e in dataS :
			dataT.append(list(e))
			
		return dataT
		
	# support basic create table statement
	def create(self, tableName, structure = dict()) :
		preSQL = "CREATE TABLE IF NOT EXISTS " + tableName
		typeSQL = []
		for k in list(structure.keys()) :
			typeSQL.append(k + ' ' + structure[k])
		typeSQL = ', '.join(typeSQL)
		preSQL = preSQL + ' (' + typeSQL + ');'
		self.C.execute(preSQL)
		self.DB.commit()
		return preSQL
		
	def drop(self, tableName) :
		if not tableName in  list(self.T.keys()) :
			return "No this table"
			
		preSQL = "DROP TABLE " + tableName + ";"
		self.C.execute(preSQL)
		self.DB.commit()
		return preSQL
		
	# support insert one line
	def add(self, tableName, value = dict()) :
		if not tableName in  list(self.T.keys()) :
			return "No this table"
			
		F = list(self.T[tableName].keys())
		preSQL = 'INSERT INTO ' + tableName + ' (' + ','.join(F) + ') VALUES '
		valSQL = []
		valBindP = []
		for f in F :
			valSQL.append(str(value[f]))
			valBindP.append('?')
		valBindP = ','.join(valBindP)
		
		preSQL = preSQL + '(' + valBindP + ');'
		# preSQL = preSQL + '(' + ','.join(valSQL) + ')'
		try :
			self.C.execute(preSQL, tuple(valSQL)) # use list bind => (?, ?, ...)
			self.DB.commit()
		except sqlite3.IntegrityError as e :
			return str(e)
		return preSQL
		
	# support basic delete SQL, default delete one item
	def delete(self, tableName, where = dict()) :
		if not tableName in  list(self.T.keys()) :
			return "No this table"
			
		F = list(self.T[tableName].keys())
		preSQL = "DELETE FROM " + tableName + " WHERE "
		
		whereBindP = []
		for k in list(where.keys()) :
			if k in F :
				whereBindP.append(k + "=:" + k)
		
		whereBindP = ' and '.join(whereBindP)
		
		preSQL = preSQL + whereBindP + ";"
		
		self.C.execute(preSQL, where) # user dict bind => ID=:ID ...
		self.DB.commit()
		
		return preSQL
	
	# support only change on value
	def update(self, tableName, key, value, where = dict()) :
		if not tableName in  list(self.T.keys()) :
			return "No this table"
			
		F = list(self.T[tableName].keys())
		preSQL = "UPDATE " + tableName + " SET "
		
		if key in F :
			preSQL = preSQL + str(key) + "=" + str(value) + " WHERE "
		else :
			return "No this key"
		
		whereBindP = []
		for k in list(where.keys()) :
			if k in F :
				whereBindP.append(k + "=:" + k)
		
		whereBindP = ' and '.join(whereBindP)
		
		preSQL = preSQL + whereBindP + ";"
		
		print(preSQL)
		
		self.C.execute(preSQL, where) # user dict bind => ID=:ID ...
		self.DB.commit()
		
		return preSQL
		
	def close(self) :
		self.DB.close()
		pass
		