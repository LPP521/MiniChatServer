# coding=utf-8
from flask import Flask
from flask import request
from router import main
import ConfigParser
from models import db, User, login_manager

def create_app():
    app = Flask(__name__)
    
	cp = ConfigParser.SafeConfigParser()
	cp.read('server.conf')
	database = cp.get('mysql', 'databaseUrl')

    app.config['SQLALCHEMY_DATABASE_URI'] = database
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.register_blueprint(main)
    db.app = app
    db.init_app(app)
    login_manager.init_app(app)

    db.create_all()

    return app