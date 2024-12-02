import pytest
from app import create_app, db
from app.models import User, Playlist, Track
from werkzeug.security import check_password_hash

@pytest.fixture
def test_app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

def test_user_model(test_app):
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
    with test_app.app_context():
        playlist = Playlist(name="My Playlist", description="A sample playlist")
        db.session.add(playlist)
        db.session.commit()

        retrieved_playlist = Playlist.query.filter_by(name="My Playlist").first()
        assert retrieved_playlist is not None
        assert retrieved_playlist.name == "My Playlist"
        assert retrieved_playlist.description == "A sample playlist"

def test_track_model(test_app):
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

