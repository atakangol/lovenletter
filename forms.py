from flask_wtf import FlaskForm
from wtforms import SelectField,StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, FloatField, SelectMultipleField,widgets,HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo

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