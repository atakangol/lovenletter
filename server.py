from flask import Flask, render_template, redirect, url_for, flash, request, session,abort
import datetime
import os
import psycopg2 as db
import random
import login

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
	#print(session['logged_in'])
	return render_template('home_page.html',login=session['logged_in'])

@app.route("/login", methods=['GET', 'POST'])
def login_page():
	return login.login(url)

@app.route("/logout")
def logout_page():
	return login.logout()




if __name__ == "__main__":
	if(DEBUG):
		app.run(debug='True')
	else:
		app.run()