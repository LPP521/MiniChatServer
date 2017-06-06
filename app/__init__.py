from flask import Flask
from flask import request
from router import main

from models import db, User

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ctz1995429ctz@127.0.0.1/test'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.register_blueprint(main)
    db.app = app
    db.init_app(app)

    db.create_all()

    return app