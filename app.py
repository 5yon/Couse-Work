from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

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
   cur.execute("INSERT INTO USER(username,password,email,country_phone,mobile_number) VALUES (?,?,?,?,?)", (request.form['un'],request.form['pw'],request.form['em'],request.form['id'],request.form['ph']))
   con.commit()
   con.close()
   return 'insert'

@app.route('/create')
def create():
    con = sqlite3.connect('login.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE USER(
                    username VARCHAR(20) NOT NULL PRIMARY KEY,
                    password VARCHAR(20) NOT NULL,
                    mail VARCHAR(25) NOT NULL,
                    country_phone VARCHAR(20) NOT NULL,
                    mobile_number VARCHAR(20) NOT NULL
                    )
                 """)
    return 'created'

@app.route('/select')
def select():
    con = sqlite3.connect('login.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM user")
    rows = cur.fetchall()
    return str(rows)

@app.route('/insert')
def insert():
    con = sqlite3.connect('login.db')
    cur = con.cursor()
    cur.execute("""INSERT INTO user(username, password)
                    VALUES ("bob" , "123")
        """)
    con.commit()
    return 'insert!'

@app.route('/login', methods=['POST'])
def login():
    con = sqlite3.connect('login.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM User WHERE Username=? AND Password=?",
    (request.form['un'],request.form['pw']))
    match = len(cur.fetchall())
    if match == 0:
        return "Wrong username and password"
    else:
        return "Welcome " + request.form['un']

