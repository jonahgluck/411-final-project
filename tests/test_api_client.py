import pytest
from unittest.mock import patch
from app.api_client import SpotifyAPI

@pytest.fixture
def mock_api_key(monkeypatch):
    """Mocks the Spotify API key environment variable for testing.

        Temporarily sets the 'SPOTIFY_API_KEY' environment variable to a mock value to
        simulate API authentication during tests.

        Args:
            monkeypatch (MonkeyPatch): A pytest utility for modifying environment variables
            and attributes in the test environment.

        Returns:
            None
    """
    monkeypatch.setenv("SPOTIFY_API_KEY", "mock_api_key")

@patch("requests.get")
def test_search_tracks(mock_get, mock_api_key):
    """Tests successful track search functionality of the SpotifyAPI.

        Mocks the response from Spotify's API for a track search query and ensures that the
        'search_tracks' method processes and returns the data correctly.

        Args:
            mock_get (MagicMock): Mocked 'requests.get' to simulate API behavior.
            mock_api_key (fixture): Fixture providing a mock Spotify API key.

        Asserts: 
            - The track name, artist, and album are accurately parsed from the mock response.
            - The 'requests.get' method is called with the correct URL, headers, and query parameters.   
    """
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
    """Tests error handing in the SpotifyAPI's search_tracks method.

        Simulates an error response from Spotify's API and verifies that the 
        method correctly captures and returns the error message.

        Args:
            mock_get (MagicMock): Mocked 'requests.get' to simulate API behavior.
            mock_api_key (fixture): Fixture providing a mock Spotify API key.

        Asserts: 
            - The response contains an error field.
            - The error message matches the mocked API response.
    """
    mock_get.return_value.status_code = 401
    mock_get.return_value.json.return_value = {"error": "Unauthorized"}

    result = SpotifyAPI.search_tracks("test query")
    assert "error" in result
    assert result["error"] == "Unauthorized"

