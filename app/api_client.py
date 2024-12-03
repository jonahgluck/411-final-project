import requests
import os

class SpotifyAPI:
    """ This is a class to interact with the Spotify Web API. 
        This class provides provides functionality for searching tracks through Spotify's Search API. 
    """
    BASE_URL = "https://api.spotify.com/v1"
    API_KEY = os.getenv("SPOTIFY_API_KEY")

    @staticmethod
    def search_tracks(query):

    """Search for tracks on Spotify using a query. 
        Sends a GET request to Spotify's Search API to fetch track details based on the given query
        and returns the API's response in JSON format. 

        Args: 
            query (str): The search string to find matching tracks.
        Returns:
            dict: A dictionary containing the API's response. On success, this includes track details
            such as titles, artists, and album information. On failure, the dictionary contains an error message.
        Raises:
            requests.exceptions.RequestException: Raised if a network error occurs or the API request fails.
            
    """
        
        headers = {"Authorization": f"Bearer {SpotifyAPI.API_KEY}"}
        response = requests.get(f"{SpotifyAPI.BASE_URL}/search", headers=headers, params={"q": query, "type": "track"})
        return response.json()

