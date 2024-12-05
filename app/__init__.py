from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy() 

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'spotify.db')}"
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app

