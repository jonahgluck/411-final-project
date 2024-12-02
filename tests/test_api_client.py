import pytest
from unittest.mock import patch
from app.api_client import SpotifyAPI

@pytest.fixture
def mock_api_key(monkeypatch):
    monkeypatch.setenv("SPOTIFY_API_KEY", "mock_api_key")

@patch("requests.get")
def test_search_tracks(mock_get, mock_api_key):
    mock_response = {
        "tracks": {
            "items": [
                {
                    "name": "Song Title",
                    "artists": [{"name": "Artist Name"}],
                    "album": {"name": "Album Name"},
                }
            ]
        }
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    result = SpotifyAPI.search_tracks("test query")
    assert result["tracks"]["items"][0]["name"] == "Song Title"
    assert result["tracks"]["items"][0]["artists"][0]["name"] == "Artist Name"
    assert result["tracks"]["items"][0]["album"]["name"] == "Album Name"
    mock_get.assert_called_once_with(
        f"{SpotifyAPI.BASE_URL}/search",
        headers={"Authorization": "Bearer mock_api_key"},
        params={"q": "test query", "type": "track"},
    )

@patch("requests.get")
def test_search_tracks_error(mock_get, mock_api_key):
    mock_get.return_value.status_code = 401
    mock_get.return_value.json.return_value = {"error": "Unauthorized"}

    result = SpotifyAPI.search_tracks("test query")
    assert "error" in result
    assert result["error"] == "Unauthorized"

