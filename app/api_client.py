import os
import requests

class SpotifyAPI:
    BASE_URL = "https://api.spotify.com/v1"

    @staticmethod
    def search_tracks(query, api_key=None):
        """
        Search for tracks using Spotify's API.
        
        Args:
            query (str): The search query (e.g., track name, artist).
            api_key (str, optional): The Spotify API key. If not provided, it defaults to the value from the environment.
        
        Returns:
            dict: JSON response from the Spotify API.
        """
        if api_key is None:
            api_key = os.getenv("SPOTIFY_API_KEY")
            if not api_key:
                raise ValueError("API key is missing. Provide it as an argument or set the SPOTIFY_API_KEY environment variable.")

        headers = {"Authorization": f"Bearer {api_key}"}
        params = {"q": query, "type": "track"}

        response = requests.get(f"{SpotifyAPI.BASE_URL}/search", headers=headers, params=params)
        response.raise_for_status()
        return response.json()

