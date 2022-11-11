from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.app_context().push() #chamada para evitar working outside of application context

load_dotenv()

db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_database = os.getenv("DB_DATABASE")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@{db_host}/{db_database}'
db = SQLAlchemy(app)