from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app import app

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://apcba_user:jLcGVdHxOSHxZZ6OUGfLOGrxCmtZb3Uz@dpg-cmr6pamd3nmc73ef4vg0-a.oregon-postgres.render.com/apcba'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    from .models import db


    app.register_blueprint(app)

    with app.app_context():
        db.create_all()

    return app
