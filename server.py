from flask import Flask, render_template, redirect, url_for, flash, request, session,abort
import datetime
import os
import psycopg2 as db
import random
import user,books

from dbinit import db_initialize,init_tables

#Venv\Scripts\activate

app = Flask(__name__)
app.config['SECRET_KEY'] = '9ioJbIGGH6ndzWOi3vEW'
GOOGLE_API_KEY = "AIzaSyDGkEHbMHzjlk4PsJ0ud_1S7ZfyPHI0btg"

DEBUG = True
if(DEBUG == False):
	url = os.getenv("DATABASE_URL")
else:
	url = "dbname='lovenletter' user='postgres' host='localhost' password='45581222'"
	#initialize(url)
	flag = db_initialize()
	if flag:
		init_tables()
	# drop_table(url)

def check_login():
	try:
		log = session['logged_in']
	except:
		session['logged_in'] = False
		log = session['logged_in']
	return log

@app.route("/")
@app.route("/home")
def home_page():
	log = check_login()
	return render_template('home_page.html',login=log)

#user pages
@app.route("/login", methods=['GET', 'POST'])
def login_page():
	return user.login(url)

@app.route("/logout")
def logout_page():
	return user.logout()

@app.route("/user_ratings")
def user_ratings_ratings():
	log = check_login()
	if log == False:
		return redirect(url_for('home_page'))
	else:
		return user.user_books()

#book pages
@app.route("/search",methods=['GET', 'POST'])
def search_page():
	log = check_login()
	return books.search(log=log)

@app.route("/search/results/<search_term>")
@app.route("/search/results/<search_term>/<page>")
def search_results_page(search_term,page=0):
	log = check_login()
	return books.results(search_term,int(page),log=log)

@app.route("/book/<id>",methods=['GET', 'POST'])
def book_details(id):
	log = check_login()
	return books.details(id=id,log=log,url=url)

if __name__ == "__main__":
	if(DEBUG):
		app.run(debug='True')
	else:
		app.run()