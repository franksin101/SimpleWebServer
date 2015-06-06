from flask import *
import os
import uuid
import myDb

app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route("/")
def index() :
	return redirect(url_for('login'))
	# return render_template('login.html')
	
@app.route("/login", methods = ['GET', 'POST'])
def login() :
	if request.method == 'POST' :
		username = request.form.get('username', '')
		password = request.form.get('password', '')
		
		if (username, password) in [('apple', 'apple')] :
			session['username'] = username
			session['csrf_token'] = uuid.uuid4().hex
			return redirect(url_for('RWDb'))
		else :
			if len(username) == 0 :
				error = 'Account is empty'
			else :
				error = 'Account or Password is Wrong'
			return render_template('login.html', username = username, error = error)
	return render_template('login.html')
	
@app.route("/RWDb", methods = ['GET', 'POST'])
def RWDb() :
	if not 'method'  in session :
		session['method'] = '1'
		
	if request.method == 'POST' :
		if not request.form.get('act', '') == None or not request.form.get('act', '') == '' :
			session['method'] = str(request.form.get('act', ''))
			
		if session['method'] == '1' : # name,type,primary key,not null, add col, del col
			return redirect(url_for('Create'))
			
		elif session['method'] == '2' : # go table, delete table
			return redirect(url_for('View'))

		elif session['method'] == '3' : # add data, view data, delete data, update data
			pass
			
		return render_template('myDb.html', method = session['method'])
		
	if request.method == 'GET' :
		if session['method'] == '1' :
			return redirect(url_for('Create'))
		elif session['method'] == '2' :
			return redirect(url_for('View'))
		elif session['method'] == '3' :
			return redirect(url_for('Datas'))
			
	return render_template('myDb.html')
	
@app.route('/Create', methods = ['GET', 'POST'])
def Create() :
	if not 'method' in session :
		return redirect(url_for('RWDb'))
			
	if request.method == 'POST' :
		if not request.form.get('act', '') == None and not session['method'] == request.form.get('act', ''):
			session['method'] = str(request.form.get('act', '')) 
			return redirect(url_for('RWDb'))
	
		add = 'err'
		maxIndex = -1
			
		if request.form.get('maxIndex', '') :
			maxIndex = int(request.form.get('maxIndex', ''))
		if request.form.get('add', '') :
			add = request.form.get('add', '')
			
		print(request.form)
		print('Create')
			
		tbName	= ""		
		oneData = []
		tmpData = []
		Pkey = -1
				
		if not request.form.get('Pkey', '') == None and not request.form.get('Pkey', '') == '' :
			Pkey = int(request.form.get('Pkey', ''))
				
		if not request.form.get('tbName', '') == None :
			tbName = request.form.get('tbName', '')
			if tbName.isdigit() :
				tbName = 'tb_' +  tbName
				
		for i in range(0, maxIndex) :
			tmpData = []
				
			if Pkey == i :
				tmpData.append(i)
			else :
				tmpData.append(-1)
			if not request.form.get('fName' + str(i), '') == None:
				tmpData .append(request.form.get('fName' + str(i), ''))
			if not request.form.get('fType' + str(i), '') == None:
				tmpData .append(request.form.get('fType' + str(i), ''))
			if not request.form.get('fNULL' + str(i), '') == None:
				if request.form.get('fNULL' + str(i), '') == 'on' :
					tmpData .append(1)
				else :
					tmpData .append(0)
			else :
				tmpData .append(0)
						
			oneData.append(tmpData)
			
		if add == '1' :
			return render_template('Create.html', method = session['method'], maxCount = maxIndex + 1, oneData = oneData, tbName = tbName)
		elif add == '2' :
			print(oneData)
			createS = dict()
			for e in oneData :
				if e[0] >= 0 :
					e[0]  = 'PRIMARY KEY'
				else :
					e[0] = ''
					
				if e[3] > 0 :
					e[3]  = 'NULL'
				else :
					e[3] = 'NOT NULL'	
					
				createS[e[1]] = str(e[2]) + " " + e[0] + " " + e[3]
					
			db = myDb.myDb()
				
			if maxIndex > 0 :
				print(db.create(request.form.get('tbName', ''), createS))
				
			tableInfo = db.tables()
			
			twoData = []
			
			for k in list(tableInfo.keys()) :
				twoData.append([k, tableInfo[k]])
			
			db.close()
			session['method'] = '2'
			return redirect(url_for('RWDb'))
	return render_template('Create.html', method = '1')
	
@app.route('/View', methods=['GET', 'POST'])
def View() :
	if not 'method' in session :
		return redirect(url_for('RWDb'))

	db = myDb.myDb()
			
	tableInfo = db.tables()
			
	twoData = []
			
	for k in list(tableInfo.keys()) :
		print(tableInfo[k])
		twoData.append([k, tableInfo[k]])
			
	db.close()			
		
	if request.method == 'POST' :
		if not request.form.get('act', '') == None and not session['method'] == request.form.get('act', ''):
			session['method'] = str(request.form.get('act', '')) 
			return redirect(url_for('RWDb'))
			
		return render_template('View.html', method = session['method'], twoData = twoData)
	if request.method == 'GET' :
		return render_template('View.html', method = session['method'], twoData = twoData)
	return render_template('View.html', method = '2', twoData = twoData)
 
if __name__ == "__main__" :
	#app.run('0.0.0.0', debug=True, port=8100, ssl_context='adhoc')
	app.run('0.0.0.0', debug=True, port=5000)