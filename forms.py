from wtforms import StringField,PasswordField, BooleanField, EmailField
from wtforms.validators import InputRequired, Email, Length, email_validator, EqualTo
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])
    email = EmailField('E-mail', validators=[InputRequired(), Email(message='Invalid E-mail'), Length(max=50)])
    remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[InputRequired(), Length(min=4,max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=200), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    email = EmailField('E-mail', validators=[InputRequired(), Email(message='Invalid E-mail'), Length(max=50)])