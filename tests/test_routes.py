import pytest
from app import create_app, db
from app.models import SpotifyData

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_app_launch(client):
    response = client.get('/health-check')
    assert response.status_code == 200
    assert response.json == {"status": "running"}

def test_search_track(client, monkeypatch):
    def mock_search_track(query):
        return {
            "tracks": {
                "items": [{
                    "id": "123",
                    "name": "Imagine",
                    "artists": [{"name": "John Lennon"}],
                    "album": {"name": "Imagine"}
                }]
            }
        }
    monkeypatch.setattr('app.spotify_api.search_track', mock_search_track)
    response = client.get('/api/search-track?query=Imagine')
    assert response.status_code == 200
    assert response.json == {
        "id": "123",
        "name": "Imagine",
        "artist": "John Lennon",
        "album": "Imagine"
    }

def test_save_track(client, app):
    data = {
        "id": "123",
        "name": "Imagine",
        "artist": "John Lennon",
        "album": "Imagine"
    }
    response = client.post('/api/save-track', json=data)
    assert response.status_code == 201
    assert response.json == {"message": "Track saved successfully"}

    with app.app_context():
        track = SpotifyData.query.filter_by(track_id="123").first()
        assert track is not None
        assert track.track_name == "Imagine"
        assert track.artist_name == "John Lennon"
        assert track.album_name == "Imagine"

def test_get_tracks(client, app):
    with app.app_context():
        track = SpotifyData(
            track_id="123",
            track_name="Imagine",
            artist_name="John Lennon",
            album_name="Imagine"
        )
        db.session.add(track)
        db.session.commit()

    response = client.get('/api/tracks')
    assert response.status_code == 200
    assert response.json == [{
        "id": "123",
        "name": "Imagine",
        "artist": "John Lennon",
        "album": "Imagine"
    }]

def test_delete_track(client, app):
    with app.app_context():
        track = SpotifyData(
            track_id="123",
            track_name="Imagine",
            artist_name="John Lennon",
            album_name="Imagine"
        )
        db.session.add(track)
        db.session.commit()

    response = client.delete('/api/delete-track/123')
    assert response.status_code == 200
    assert response.json == {"message": "Track 123 deleted successfully"}

    with app.app_context():
        track = SpotifyData.query.filter_by(track_id="123").first()
        assert track is None

def test_update_track(client, app):
    with app.app_context():
        track = SpotifyData(
            track_id="123",
            track_name="Imagine",
            artist_name="John Lennon",
            album_name="Imagine"
        )
        db.session.add(track)
        db.session.commit()

    update_data = {
        "name": "Imagine (Remastered)",
        "artist": "John Lennon",
        "album": "Imagine Remastered"
    }
    response = client.put('/api/update-track/123', json=update_data)
    assert response.status_code == 200
    assert response.json == {"message": "Track 123 updated successfully"}

    with app.app_context():
        track = SpotifyData.query.filter_by(track_id="123").first()
        assert track.track_name == "Imagine (Remastered)"
        assert track.artist_name == "John Lennon"
        assert track.album_name == "Imagine Remastered"

