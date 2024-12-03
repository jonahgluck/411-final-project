import pytest
from app import create_app, db
from app.models import User, Playlist, Track
from werkzeug.security import check_password_hash

@pytest.fixture
def test_app():
    """Sets up a test Flack application with an in-memory database.

        Creates a Flask app configured for testing and initializes an SQLite in-memory
        database. The database is prepared before running tests and cleared afterward.

        Yields:
            Flask: The configured test Flask application instance.
    """
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

def test_user_model(test_app):
    """Tests functionality of the User model.

        Validates that a user can be created, saved to the database, and retrieved with the 
        correct attributes. Also ensures that password hashing and validation work as expected.

        Args: 
            test_app (Flask): The test Flask application with an initialized database.

        Asserts: 
            - The user is successfully saved and retrieved from the database.
            - The username matches the expected value.
            - The hashed password validates the correct plain-text password.
    """
    with test_app.app_context():
        user = User(username="testuser")
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()

        retrieved_user = User.query.filter_by(username="testuser").first()
        assert retrieved_user is not None
        assert retrieved_user.username == "testuser"
        assert check_password_hash(retrieved_user.password_hash, "testpassword")

def test_playlist_model(test_app):
    """Tests functionality of the Playlist model.

        Confirms that a playlist can be created, saved to the database, and retrieved 
        with its attributes intact.

        Args: 
            test_app (Flask): The test Flask application with an initialized database.

        Asserts:
            - The playlist is successfully saved and retrieved from the database.
            - The name and description of the playlist match the expected values.
    """
    with test_app.app_context():
        playlist = Playlist(name="My Playlist", description="A sample playlist")
        db.session.add(playlist)
        db.session.commit()

        retrieved_playlist = Playlist.query.filter_by(name="My Playlist").first()
        assert retrieved_playlist is not None
        assert retrieved_playlist.name == "My Playlist"
        assert retrieved_playlist.description == "A sample playlist"

def test_track_model(test_app):
    """Tests functionality of the Track model.

        Ensures that a track can be created, linked to a playlist, and saved to the database, 
        with all attributes correctly stored and retrieved.

        Args:
            test_app (Flask): The test Flask application with an initialized database.

        Asserts: 
            - The track is successfully saved and retrieved from the database.
            - The title, artist, and album of the track match the expected values. 
            - The track is correctly associated with the playlist.
    """
    with test_app.app_context():
        playlist = Playlist(name="My Playlist")
        db.session.add(playlist)
        db.session.commit()

        track = Track(
            title="Sample Track",
            artist="Sample Artist",
            album="Sample Album",
            playlist_id=playlist.id,
        )
        db.session.add(track)
        db.session.commit()

        retrieved_track = Track.query.filter_by(title="Sample Track").first()
        assert retrieved_track is not None
        assert retrieved_track.title == "Sample Track"
        assert retrieved_track.artist == "Sample Artist"
        assert retrieved_track.album == "Sample Album"
        assert retrieved_track.playlist_id == playlist.id

