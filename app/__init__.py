from flask import Flask
import os
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "dev_secret")

    from app.routes import main
    app.register_blueprint(main)

    return app