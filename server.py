from flask import Flask, render_template, redirect, url_for, flash, request, session,abort
import datetime
import os
import psycopg2 as db
import random
import login,books

from dbinit import db_initialize,init_tables

#Venv\Scripts\activate

app = Flask(__name__)
app.config['SECRET_KEY'] = '9ioJbIGGH6ndzWOi3vEW'
GOOGLE_API_KEY = "AIzaSyDGkEHbMHzjlk4PsJ0ud_1S7ZfyPHI0btg"

DEBUG = False
if(DEBUG == False):
	url = os.getenv("DATABASE_URL")
else:
	url = "dbname='lovenletter' user='postgres' host='localhost' password='45581222'"
	#initialize(url)
	flag = db_initialize()
	if flag:
		init_tables()
	# drop_table(url)



@app.route("/")
@app.route("/home")
def home_page():
	try:
		log = session['logged_in']
	except:
		session['logged_in'] = False
		log = session['logged_in']
	return render_template('home_page.html',login=log)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
	return login.login(url)

@app.route("/logout")
def logout_page():
	return login.logout()

@app.route("/search",methods=['GET', 'POST'])
def search_page():
	return books.search()

@app.route("/search/results/<search_term>")
@app.route("/search/results/<search_term>/<page>")
def search_results_page(search_term,page=0):
	return books.results(search_term,int(page))


if __name__ == "__main__":
	if(DEBUG):
		app.run(debug='True')
	else:
		app.run()