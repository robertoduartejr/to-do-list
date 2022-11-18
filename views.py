from flask import render_template, request, url_for, redirect, session, flash
from app import app, db, login_manager
from models import User
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user


@login_manager.user_loader #handling with user login
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated: #checar antes de logar se o cliente já nao está logado
        flash("already logged in","loggedin")
        return redirect(url_for('todolist'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password,form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('todolist'))
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

@app.route('/todolist')
@login_required
def todolist():
    return render_template('todolist.html', name=current_user.name)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
