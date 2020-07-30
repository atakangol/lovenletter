from flask import Flask, render_template, redirect, url_for, flash, request, session,abort
import datetime
import os
import psycopg2 as db
import random

from flask_wtf import FlaskForm
from wtforms import SelectField,StringField, PasswordField, SubmitField, BooleanField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

GOOGLE_API_KEY = "AIzaSyDGkEHbMHzjlk4PsJ0ud_1S7ZfyPHI0btg"

class LoginForm(FlaskForm):
    user_name = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    full_name = StringField("Your Name",validators=[DataRequired()])
    username = StringField("Username",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    birth_year = IntegerField("Birth Year", validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')


def login(url):
	if session.get('logged_in'):
		return redirect(url_for('home_page'))
	else:
		login_form = LoginForm()
		signup_form = SignupForm()
		if login_form.validate_on_submit():
			user_name = login_form.user_name.data
			pw = login_form.password.data
			try:
				connection = db.connect(url)
				cursor = connection.cursor()

				statement = "SELECT id FROM USERS WHERE SCREEN_NAME = '{}'  AND pass=crypt('{}',pass) ".format(user_name,pw )

				cursor.execute(statement)
				result = cursor.fetchone()
				#print(result)
				
				if result ==None:
					flash('Login Unsuccessful. Please check username and password', 'danger')
				else:

					id = result[0]

				
					
					flash('You have been logged in!', 'success')
					session['logged_in'] = True
					session['id'] = id
					return redirect(url_for('home_page'))
			
			except db.DatabaseError:
				connection.rollback()
				flash('Login Unsuccessful. Please check username and password', 'danger')
			finally:
				connection.close()
		
		elif signup_form.validate_on_submit():
			user_name = signup_form.username.data
			full_name = signup_form.full_name.data
			email = signup_form.email.data
			pw =signup_form.password.data
			birth_year = signup_form.birth_year.data

			try:
				connection = db.connect(url)
				cursor = connection.cursor()

				statement = "SELECT screen_name FROM USERS "
				cursor.execute(statement)
				names = cursor.fetchall()
				statement = "SELECT email FROM USERS "
				cursor.execute(statement)
				emails = cursor.fetchall()
				statement = "SELECT id FROM USERS "
				cursor.execute(statement)
				ids = cursor.fetchall()
				#print(names,emails,ids)

				if (user_name,) in names:
					flash("Name taken","danger")
				
				elif (email,) in emails:
					flash("Email already registered","danger")

				else:
					user_count = len(ids)
					new_id = random.randint(1,user_count*100)
					while new_id in ids:
						
						new_id = random.randint(1,user_count*100)


					statement = "INSERT INTO public.users (id, pass, full_name, screen_name, email,created_at,birth_year) VALUES ({id},crypt('{pw}', gen_salt('bf')),'{full_name}','{screen_name}','{email}','{date}',{birth}) returning id;"
					today = datetime.date.today()
					statement = statement.format(id=new_id,pw=pw,full_name=full_name,screen_name=user_name,email=email,date=str(today),birth=birth_year)
					cursor.execute(statement)
					#print(statement)
					#feedback = cursor.fetchall()
					#print(feedback)
					#print("succes??")
					connection.commit()
					cursor.close()
					flash('You have been logged in!', 'success')
					session['logged_in'] = True
					session['id'] = new_id
					return redirect(url_for('home_page'))


				
			except db.DatabaseError:
				#print(statement)
				#print(feedback)
				connection.rollback()
			finally:
				connection.close()



		return render_template('login_page.html', title='Login', login_form=login_form,signup_form=signup_form)

def logout():
	session.pop('id', None)
	session['logged_in'] = False
	return redirect(url_for('home_page'))

def user_books(url):
	user_id = session["id"]
	connection = db.connect(url)
	cursor = connection.cursor()
	statement = "select * from reviews where user_id={}".fromat(user_id)
	cursor.execute(statement)
	all_reviews = cursor.fetchall() #user_id,rating,date,book_id




	pass
