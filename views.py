import flask
from flask import render_template, request, url_for, redirect, session, flash, Markup
from app import app, db, login_manager,s,mail
from models import User
from forms import LoginForm, RegisterForm, EmailForm, PasswordForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from itsdangerous import SignatureExpired, BadTimeSignature
from flask_mail import Message

@login_manager.user_loader #handling with user login
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/',methods=['GET','POST'])
@login_required
def index():
    if current_user.confirm:
        if flask.request.method == 'POST':
            tasks = request.get_json()
            current_user.tasks = tasks
            db.session.commit()
            return tasks
        else:
            return render_template('index.html')
    else:
        return render_template('usernotconfirmed.html')


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated: #checar antes de logar se o cliente já nao está logado
        flash("Already logged in","loggedin")
        return redirect(url_for('index'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password,form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))
            else:
                flash("Wrong Password", "userorpassword")
                return redirect(url_for('login'))
        else:
            flash("User does not exist", "userorpassword")
            return redirect(url_for('login'))



    return render_template('login.html', form=form)

@app.route('/register',methods=['GET','POST'])
def register():

    if current_user.is_authenticated: #checar antes de logar se o cliente já nao está logado
        flash("Please log out to register a new user","loggedin")
        return redirect(url_for('index'))


    form = RegisterForm()
    if form.validate_on_submit():
        try:
            hashed_password = generate_password_hash(form.password.data,method='sha256')
            new_user = User(name=form.name.data, email=form.email.data,password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            email = form.email.data
            name = form.name.data
            token = s.dumps(email, salt='email-confirm')

            link = url_for('confirm_email',token=token, _external=True)
            email_sender(email,link,name,"register")
            login_user(new_user)
            flash("Token has been sent to your email address. Please validate it.","token_success")
            print(link)
            return redirect(url_for('index'))
        except:
            flash("We had a problem when saving information. Please try again", "internalerror")
            return redirect(url_for('index'))

    form = RegisterForm(request.form)
    return render_template('signup.html',form=form)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm',max_age=300)
        print(token)
    except SignatureExpired:
        flash(Markup('Token has expired. It expires in 5 minutes. Please <a href="/login" class="alert-link">Log In</a> to resend token'),"token_expired")
        return redirect(url_for('index'))
    except BadTimeSignature:

        flash(Markup('Wrong Token. Please <a href="/login" class="alert-link">Log In</a> to resend token'),"token_expired")
    user = User.query.filter_by(email=email).first_or_404()

    if user.confirm:
        flash("Account already confirmed. Please enjoy", "token_success")
        return redirect(url_for('index'))
    user.confirm = True
    db.session.commit()
    print(user.email,user.confirm)
    flash("Registration finished", "token_success")
    return redirect(url_for('index'))


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

@app.route('/users') #function to send user information to react
@login_required
def users():
    return {"name": current_user.name.split(" ")[0], "tasks": current_user.tasks}


@app.route('/delete/<int:id>') #simples function to delete users on interface
@login_required
def delete(id):
    if current_user.email=="admin@admin.com":
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('specialadmin'))
    else:
        return redirect(url_for('index'))

@app.route('/specialadmin') #function to display all users
@login_required
def specialadmin():
    if current_user.email == "admin@admin.com":
        users = User.query.all()
        return render_template("admin.html", users=users)
    else:
        return redirect(url_for('index'))

@app.route('/resend')
@login_required
def resend():
    token = s.dumps(current_user.email, salt='email-confirm')
    link = url_for('confirm_email', token=token, _external=True)
    email_sender(current_user.email, link, current_user.name,'Token')
    flash("Token has been sent to your email address again. Please validate it.", "token_success")
    print(link)
    return render_template("usernotconfirmed.html", users=users)

@app.route('/forget', methods=['GET','POST'])
def forget():
    form = EmailForm()
    if form.validate_on_submit():

        email = form.email.data

        user = User.query.filter_by(email=email).first()
        if user:
            token = s.dumps(user.email, salt='forget-password')

            link = url_for('forget_password', token=token, _external=True)
            email_sender(user.email, link, user.name, 'Password')

            flash("Token has been sent to your email address. Please check it to redefine password.",
                  "password_success")

            return redirect(url_for('login'))
        flash("User does not exist.", "password_unsuccess")
        return render_template('forgetpassword.html', form=form)
    return render_template('forgetpassword.html', form=form)

@app.route('/forget_password/<token>')
def forget_password(token):
    try:
        email = s.loads(token, salt='forget-password',max_age=300)
        print(token)
    except SignatureExpired:
        flash('Token has expired. It expires in 5 minutes. Try it again',"token_expired")
        return redirect(url_for('index'))
    except BadTimeSignature:
        flash('Token not valid',"token_expired")

    user = User.query.filter_by(email=email).first_or_404()

    if current_user.is_authenticated:
        flash("You are logged in. Please enjoy", "token_success")
        return redirect(url_for('index'))

    login_user(user)
    user.verification='0' #easy way to allow access only for those who forgot password
    db.session.commit()
    return redirect(url_for('redefine_password'))

@app.route('/redefine_password', methods=['GET','POST'])
@login_required
def redefine_password():
    if current_user.verification=='0':
        form = PasswordForm()
        print('2')
        if form.validate_on_submit():
            print('3')
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            current_user.password = hashed_password
            current_user.verification='1'
            db.session.commit()
            flash("Password updated", "password_success")
            print('1')
            return redirect(url_for('index'))
        return render_template('redefinepassword.html', form=form)


    return redirect(url_for('index'))

#function to send email, method differs if it's to confirm email or redefine password
def email_sender(email,link,name,method):
    if method != 'Password':
        msg = Message('Confirm E-mail', sender='trackpricedjango@gmail.com',recipients=[email])
        msg.body = "Dear, {}.\n\n Welcome to the Special To-do List. \n\n Your link is {}. \n\nThis link will expire in 5 minutes".format(name,link)
        mail.send(msg)
    else:
        msg = Message('Redefine Password', sender='trackpricedjango@gmail.com', recipients=[email])
        msg.body = "Dear, {}.\n\n Click below to proceed with password redefinition. \n\n Link: {}. \n\nThis link will expire in 5 minutes".format(name, link)
        mail.send(msg)