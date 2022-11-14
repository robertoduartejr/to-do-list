from wtforms import StringField,PasswordField, BooleanField, EmailField
from wtforms.validators import InputRequired, Email, Length
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    email = EmailField('email', validators=[InputRequired()])
    remember = BooleanField('remember me')
