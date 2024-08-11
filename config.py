import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Load environment variables from .flaskenv file
load_dotenv('.flaskenv')

def create_app():
    app = Flask(__name__)

    # Load configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Import and register blueprints or routes
    with app.app_context():
        from . import auth, models

    return app

# Create an instance of the app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
