from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spotify.db'
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)

    # Register Blueprint
    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app

