from flask import Flask
from dotenv import load_dotenv
import os
from .auth import auth
from .bookmarks import bookmarks
from .config import Config
from .database import db

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
      db.create_all()

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    return app
