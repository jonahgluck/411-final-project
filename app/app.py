import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from routes import routes_bp
from models import db

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# App configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(routes_bp)

@app.before_first_request
def initialize_database():
    """Initialize the database before the first request."""
    db.create_all()

# Home route for testing
@app.route('/')
def home():
    """Home route to verify the app is running."""
    return "App Running Successfully!"

if __name__ == '__main__':
    app.run(debug=True)

