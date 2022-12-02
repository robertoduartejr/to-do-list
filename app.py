from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

load_dotenv()
app = Flask(__name__, template_folder='./to-do-list/templates')
app.app_context().push() #chamada para evitar working outside of application context
SECRET_KEY = os.urandom(32) #creating random secret key to csrf
app.config['SECRET_KEY'] = os.getenv("MAIL_SERVER")

bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)
login_manager.login_view = 'login' #here's where I define which page go when not logged in

#app.config.from_pyfile('config.cfg') #for the email
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True


mail = Mail(app)

SECRET_KEY_2 = os.urandom(32) #for the URL
s = URLSafeTimedSerializer(SECRET_KEY_2)


db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_database = os.getenv("DB_DATABASE")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@{db_host}/{db_database}'
db = SQLAlchemy(app)


