import requests
import os

SPOTIFY_API_URL = "https://api.spotify.com/v1"
SPOTIFY_ACCESS_TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN")

def spotify_request(endpoint, params=None):
    """
    Make a request to the Spotify API.

    Args:
        endpoint (str): Spotify API endpoint (e.g., 'search', 'tracks/{id}').
        params (dict): Query parameters for the API request.

    Returns:
        dict: JSON response from the Spotify API.
    """
    headers = {"Authorization": f"Bearer {SPOTIFY_ACCESS_TOKEN}"}
    response = requests.get(f"{SPOTIFY_API_URL}/{endpoint}", headers=headers, params=params)
    response.raise_for_status()
    return response.json()

