from . import db
from werkzeug.security import generate_password_hash

class User(db.Model):
    """Model representing a user of the application.
    Attributes: 
        id (int): The unique identifier for the user.
        username (str): A unique username chosen by the user.
        password_hash (str): The securely stored hashed password.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        """Hashes the user's password and stores it securely.
            Args:
                password (str): The plain-text password to be hashed.
            Returns:
                None
        """
        self.password_hash = generate_password_hash(password)
        

class Playlist(db.Model):
    """Model representing a playlist created by a user.

        Attributes:
            id (int): The unique identifier for the playlist.
            name (str): The name of the playlist.
            description (str, optional): A brief description of the playlist.
            tracks (list): A collection of 'Track' objects linked to this playlist.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    tracks = db.relationship('Track', backref='playlist', lazy=True)

class Track(db.Model):
    """Model representing a track added to a playlist.

        Attributes:
            id (int): The unique identifier for the track.
            title (str): The name of the track.
            artist (str): The artist performing the track.
            album (str, optional): The album the track is part of.
            playlist_id (int): The ID of the playlist this track belongs to.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    album = db.Column(db.String(100), nullable=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), nullable=False)

