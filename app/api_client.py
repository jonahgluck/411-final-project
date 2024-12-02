import requests
import os

class SpotifyAPI:
    BASE_URL = "https://api.spotify.com/v1"
    API_KEY = os.getenv("SPOTIFY_API_KEY")

    @staticmethod
    def search_tracks(query):
        headers = {"Authorization": f"Bearer {SpotifyAPI.API_KEY}"}
        response = requests.get(f"{SpotifyAPI.BASE_URL}/search", headers=headers, params={"q": query, "type": "track"})
        return response.json()

