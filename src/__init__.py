from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.getenv('SECRET_KEY'),
        )
    else:
        app.config.from_mapping(test_config)
        

    @app.get('/')
    def index():
        return "nigga server"

    @app.get('/demo')
    def demo():
        return {
            "message" : "Nigga this server runnning to hot"
        }
    
    return app
