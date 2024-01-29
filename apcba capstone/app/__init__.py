from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://apcba_user:jLcGVdHxOSHxZZ6OUGfLOGrxCmtZb3Uz@dpg-cmr6pamd3nmc73ef4vg0-a.oregon-postgres.render.com/apcba'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Assuming your login route is in the 'auth' blueprint

    # Importing models here to avoid circular import
    from .models import db, User, Announcement, Certificate, user_account, Course, Subject, Section, Teacher, Student, Module, Enrollment, Enrollies, Grades, Schedule

    # Import and register routes from auth.py
    from .routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Creating tables
    with app.app_context():
        db.create_all()

    return app

