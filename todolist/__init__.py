from flask import Flask
import os
from dotenv import load_dotenv
from todolist.user import user
from todolist.views import views


load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")
DB_NAME = os.environ.get("DB_NAME")


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.register_blueprint(user)
    app.register_blueprint(views)
    return app
