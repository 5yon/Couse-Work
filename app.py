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
        session['uname'] = request.form['username']
        return 'welcome ' + request.form['username']


@app.route('/username')
def un():
	if 'uname' in session:
		return 'Logged in as %s' % escape(session['uname'])
	return 'You are not logged in'

@app.route('/logout')
def logout():
    session.pop('uname', None)
    return redirect(url_for('username'))


    


