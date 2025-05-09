from flask import Flask, redirect
from dotenv import load_dotenv
import os
from .auth import auth
from .bookmarks import bookmarks
from .config import Config
from .database import db, Bookmark
from .http_status_codes import *
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)


    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
      db.create_all()

    jwt = JWTManager()
    jwt.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    
    API_URL = '/static/api.yaml' 
    SWAGGER_URL = '/api/docs'

    swaggerui_blueprint = get_swaggerui_blueprint(
      SWAGGER_URL,
      API_URL, 
      config={ 
         "app_name": "RPS"
      }
   )

    app.register_blueprint(swaggerui_blueprint)

    @app.get('/<short_url>')
    def redirect_to_url(short_url):
       bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()

       if bookmark:
          bookmark.visits += 1
          db.session.commit()

          return redirect(bookmark.url )
       
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
       return {
          "error" : "Not found"
       }, HTTP_404_NOT_FOUND
    
    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
       return {
          "error" : "Something went wrong please try again"
       }, HTTP_500_INTERNAL_SERVER_ERROR
    
    
    return app
