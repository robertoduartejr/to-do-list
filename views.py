from flask import render_template, request, url_for, redirect
from app import app, db
from models import User
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password,form.password.data):
                return redirect(url_for('register'))
            else:
                return 'wrong password'
        else:
            return "user does not exist"


    return render_template('login.html', form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data,method='sha256')
        new_user = User(name=form.name.data, email=form.email.data,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>' + 'new user has been created' + '</h1>'
    return render_template('signup.html',form=form)