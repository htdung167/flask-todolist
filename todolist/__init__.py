from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")
DB_NAME = os.environ.get("DB_NAME")


def create_database(app):
    if not os.path.exists('todolist/' + DB_NAME):
        db.create_all(app=app)
        print("Created DB!")


def create_app():
    app = Flask(__name__)
    from todolist.user import user
    from todolist.views import views
    from todolist.models import User, Note

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    create_database(app)

    app.register_blueprint(user)
    app.register_blueprint(views)
    return app
