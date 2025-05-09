from flask import Flask, redirect
from dotenv import load_dotenv
import os
from .auth import auth
from .bookmarks import bookmarks
from .config import Config
from .database import db, Bookmark
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
      db.create_all()

    jwt = JWTManager()
    jwt.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    @app.get('<short_url>')
    def redirect_to_url(short_url):
       bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404())

       if bookmark:
          bookmark.visits += 1
          db.session.commit()

          return redirect(bookmark.url )

    return app
