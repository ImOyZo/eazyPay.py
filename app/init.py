from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')

    # Set configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '6969'


    # Initialize extensions
    db.init_app(app)

    # Register blueprints or routes
    with app.app_context():
        from .routes import bp
        app.register_blueprint(bp)
        db.create_all()

    return app
