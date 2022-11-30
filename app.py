from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_bootstrap import Bootstrap
from flask_login import LoginManager


app = Flask(__name__, template_folder='./to-do-list/templates')
app.app_context().push() #chamada para evitar working outside of application context
SECRET_KEY = os.urandom(32) #creating random secret key to csrf
app.config['SECRET_KEY'] = SECRET_KEY
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' #here's where I define which page go when not logged in




load_dotenv()

db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_database = os.getenv("DB_DATABASE")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@{db_host}/{db_database}'
db = SQLAlchemy(app)


