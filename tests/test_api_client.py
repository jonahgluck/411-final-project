import pytest
import requests
from unittest.mock import patch
from app.api_client import SpotifyAPI

@pytest.fixture
def mock_api_key(monkeypatch):
    """Mock the Spotify API key environment variable."""
    monkeypatch.setenv("SPOTIFY_API_KEY", "mock_api_key")

@patch("requests.get")
def test_search_tracks(mock_get, mock_api_key):
    """Test successful track search functionality."""
    # Mock Spotify API response
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

    # Perform the search
    result = SpotifyAPI.search_tracks("test query", api_key="mock_api_key")

    # Assertions
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
    """Test error handling in the track search functionality."""
    # Mock an error response from Spotify API
    mock_get.return_value.status_code = 401
    mock_get.return_value.json.return_value = {"error": "Unauthorized"}
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Client Error: Unauthorized for url")

    # Perform the search
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        SpotifyAPI.search_tracks("test query", api_key="mock_api_key")

    # Assertions
    assert "401 Client Error" in str(exc_info.value)


