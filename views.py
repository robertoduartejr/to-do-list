from flask import render_template, request, url_for, redirect
from app import app, db
from models import User
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from forms import LoginForm



@app.route('/')
def login():
    form = LoginForm()
    return render_template('index.html', form=form)