from flask import Flask, render_template, request, session, redirect, url_for
import os
import sqlite3
from markupsafe import escape
from datetime import timedelta

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(16)
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=1)


@app.route('/')
def home():
        return render_template('homepage.html')

@app.route('/user')
def user():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/signup',methods=['POST'])
def signup():
    con = sqlite3.connect('login.db')
    cur = con.cursor()
    cur.execute("INSERT INTO USER(username,email,password,mobile) VALUES (?,?,?,?)", (request.form['username'],request.form['email'],request.form['password'],request.form['mobile']))
    con.commit()
    con.close()
    session.permanent = True
    session['username'] = request.form['username']
    return 'welcome ' + request.form['username']

@app.route('/create')
def create():
    con = sqlite3.connect('login.db')
    cur = con.cursor()
    cur.execute("""
                    CREATE TABLE USER(
                    username VARCHAR(20) NOT NULL PRIMARY KEY,
                    email VARCHAR(20) NOT NULL,
                    password VARCHAR(25) NOT NULL,
                    mobile VARCHAR(20) NOT NULL)
                """)
    return 'created'



@app.route('/select')
def select():
    con = sqlite3.connect('login.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM USER")
    rows = cur.fetchall()
    return render_template('table.html', rows=rows)


@app.route('/insert', methods=['POST'])
def insert():
	with sqlite3.connect('login.db') as db:
		cursor = db.cursor()
		cursor.execute(	"INSERT INTO Users (Username, Password) VALUES (?,?)",
			       		(request.form['username'],request.form['password']))
		db.commit()
	return request.form['username'] + ' added'




@app.route('/login', methods=['POST'])
def login():
    con = sqlite3.connect('login.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM USER WHERE Username=? AND Password=?",
    (request.form['username'],request.form['password']))
    match = len(cur.fetchall())
    if match == 0:
        return "Wrong email and password"
    else:
        session.permanent = True
        session['unam'] = request.form['username']
        return render_template('homepage.html') + "Welcome " + request.form['username']


@app.route('/un')
def un():
    if 'unam' in session:
        return 'Logged in as %s' % escape(session['unam'])
    return render_template('homepage.html') +  'You are not logged in'

@app.route('/logout')
def logout():
    session.pop('unam', None)
    return redirect(url_for('un'))

@app.route('/tetra')
def fish():
  connection = sqlite3.connect("ourfish.db")
  cursor = connection.cursor()

  sqlcommand = """


      CREATE TABLE IF NOT EXISTS tblfish
      (
          fishID       TEXT,
          fishName     TEXT,
          price        INTEGER,
          size         TEXT,
          tempRange    TEXT,
          pHRange      TEXT,
          rating       TEXT,
          primary key   (fishID)
      )"""

  cursor.execute(sqlcommand)
  print("tblfish table has been created in ourfish.db")
  tblTemps = [('001','Neon Tetra',1.45,'3cm','21–27°C','6.0–6.5',"***"),
              ('002','Serpae Tetra',2.50,'3cm','22-27°C','6.0–8.0',"****"),

              ]
  #cursor.executemany("INSERT INTO tblFISH1 VALUES (?,?,?,?,?,?,?)", (request.form['fishID'], request.form['fishName'], (request.form['price'], request.form['size'], request.form['tempRange'], request.form['pHRange'], (request.form['rating'])
  cursor.executemany("INSERT or REPLACE into tblfish VALUES (?,?,?,?,?,?,?)",tblTemps)
  print("\n To select and display only records whichs are of 'Action' and 'Animation category")
  for row1 in cursor.execute('SELECT * FROM tblfish WHERE rating = "***" '):
    print(row1)
  connection.commit()
  connection.close()
fish()



