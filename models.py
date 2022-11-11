from sqlalchemy_utils import EmailType, PasswordType
from app import db


class User(db.Model):

    #defini o controle de usuários repetidos a partir do email
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    email = db.Column(EmailType, unique=True)
    password = db.Column(PasswordType)
    tasks = db.Column(db.ARRAY(db.String))

    def __init__(self,nome,email,password,tasks):
        self.nome = nome
        self.email = email
        self.password = password
        self.tasks = tasks