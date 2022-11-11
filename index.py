#arquivo pra chamar todos os arquivos em sequencia e evitar erro do flask de referência circular

import app
from models import Torcedor
import views
from app import app, db

#criar tudo no banco, caso não tenha sido criado..

#rodar aplicação
if __name__ == '__main__':
    db.create_all()
    app.run()

