from sqlalchemy_utils import EmailType, PasswordType
from app import db
from flask_login import UserMixin



class User(UserMixin, db.Model):

    #defini o controle de usuários repetidos a partir do email
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    email = db.Column(EmailType(50), unique=True)
    password = db.Column(db.String(200))
    tasks = db.Column(db.ARRAY(db.String))
    verification = db.Column(db.String(6))

    def __init__(self,name,email,password,verification='1'):
        self.name = name
        self.email = email
        self.password = password
        self.tasks = []
        self.verification = verification
