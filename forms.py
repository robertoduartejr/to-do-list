from wtforms import StringField,PasswordField, BooleanField, EmailField
from wtforms.validators import InputRequired, Email, Length
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    email = EmailField('E-mail', validators=[InputRequired()])
    remember = BooleanField('Remember me')
