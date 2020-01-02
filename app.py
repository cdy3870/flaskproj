from flask import Flask, render_template, url_for, redirect, request, session, flash, g
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

#key needed for session 
app.secret_key = 'secret'
app.database = "posts.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

#wrap used to prevent unwanted accesses
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('you need to login first')
			return redirect(url_for('login'))
	return wrap

@app.route('/')
@login_required
def home():
	#g stores temporary objects, specific to flask, storing connection
	#g.db = connect_db()
	#select query
	#cur = g.db.execute('select * from posts')
	#create dict/map, used list comprehension to store query results in dict
	#posts = [dict(title = row[0], description = row[1]) for row in cur.fetchall()]
	#g.db.close()
	posts = db.session.query(BlogPosts).all()
	return render_template('index.html', posts = posts)

@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'invalid credentials'
		else:
			#store session value as true to indicate login
			session['logged_in'] = True
			flash('you were just logged in')
			return redirect(url_for('home'))

	return render_template('login.html', error=error)

@login_required
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('you were just logged out')
	return redirect(url_for('welcome'))

#established connection with database
def connect_db():
	return sqlite3.connect(app.database)

if __name__ == '__main__':
	app.run(debug=True)