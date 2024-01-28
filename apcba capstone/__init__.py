from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

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

    from your_package import models  # Import your models here
    from your_package import app as app_blueprint
    app.register_blueprint(app_blueprint)

    return app