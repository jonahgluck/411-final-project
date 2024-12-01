import requests
import os
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"
ACCESS_TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN")

def search_track(query):
    """Search for a track using Spotify API."""
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {"q": query, "type": "track", "limit": 1}
    response = requests.get(f"{SPOTIFY_API_BASE_URL}/search", headers=headers, params=params)
    response.raise_for_status()
    return response.json()

