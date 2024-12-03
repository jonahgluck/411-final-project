from flask import Blueprint, request, jsonify
from .models import User, Playlist, Track
from . import db
from werkzeug.security import check_password_hash
import requests
from .api_client import SpotifyAPI

main = Blueprint('main', __name__)

@main.route('/create-account', methods=['POST'])
def create_account():
    """Handles the user account creation.
        
        It accepts a username and password in the request payload, creates a new user, 
        hahes the password for security, and stores the user in the database.
        
        Returns: 
            Response: JSON with a success message and HTTP status code 201. 
    """
    data = request.json
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Account created successfully!"}), 201

@main.route('/login', methods=['POST'])
def login():
    """Authenticates a user by verifying their credentials.
       
       Checks the provided username and password against the stored hash.
       
       Returns:
           Response: JSON with a success message (200) if credentials are valid, or an error
           message (401) is invalid.
    """
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@main.route('/update-password', methods=['POST'])
def update_password():
    """Updates a user's password. 
    
        Validates the old password and updates it with a new hashed password.
        
        Returns: 
            Response: JSON with a success message (200) if the update is successful, or an error
           message (401) if validation fails.
    """
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['old_password']):
        user.set_password(data['new_password'])
        db.session.commit()
        return jsonify({"message": "Password updated successfully!"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@main.route('/health', methods=['GET'])
def health():
    """Checks if the application is running.
        Returns: 
            Response: JSON with a status message and HTTP status code 200.
    """
    return jsonify({"status": "Running"}), 200

@main.route('/playlists', methods=['POST'])
def create_playlist():
    """Creates a new playlist.
    
        Accepts playlist details in teh request payload, such as name and description,
        and stores the playlist in the database.
        
        Returns: 
            Response: JSON with a success message, playlist ID, and HTTP status code 201.
    """
    data = request.json
    playlist = Playlist(name=data['name'], description=data.get('description', ''))
    db.session.add(playlist)
    db.session.commit()
    return jsonify({"message": "Playlist created successfully!", "playlist_id": playlist.id}), 201

@main.route('/search-track', methods=['GET'])
def search_track():
    """Searches for tracks using the Spotify API. 

        Takes a query parameter 'q' to perform the search and retrieves results from Spotify's API. 

        Returns: 
            Response: JSON with the search results and HTTP status code 200.
    """
    query = request.args.get('q')
    results = SpotifyAPI.search_tracks(query)
    return jsonify(results), 200

@main.route('/playlist/<int:playlist_id>', methods=['GET'])
def get_playlist_details(playlist_id):
    """Fetches details of a specific playlist.

        Args: 
            playlist_id (int): ID of the playlist to retrieve.

        Returns: 
            Response: JSON with playlist details, including associated tracks (200), or
            an error message if the playlist if not found (404). 
    """
    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404

    tracks = [
        {"title": track.title, "artist": track.artist, "album": track.album}
        for track in playlist.tracks
    ]
    return jsonify({
        "id": playlist.id,
        "name": playlist.name,
        "description": playlist.description,
        "tracks": tracks
    }), 200


@main.route('/playlist/<int:playlist_id>/add-track', methods=['POST'])
def add_track_to_playlist(playlist_id):
    """Adds a new track to a playlist.

        Args:
            playlist_id (int): ID of the playlist to add the track to.

        Returns: 
            Response: JSON with a success message (201) if the track is added successfully,
            or an error message if the playlist is not found (404).
    """
    data = request.json
    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404

    new_track = Track(
        title=data["title"],
        artist=data["artist"],
        album=data.get("album", ""),
        playlist_id=playlist.id
    )
    db.session.add(new_track)
    db.session.commit()
    return jsonify({"message": "Track added successfully!"}), 201


@main.route('/playlist/<int:playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    """Deletes a playlist by ID. 

        Args:
            playlist_id (int): ID of the playlist to delete.

        Returns:
            Response: JSON with a success message (200) if the playlist is deleted successfully,
            or an error message if the playlist is not found (404). 
    """
    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404

    db.session.delete(playlist)
    db.session.commit()
    return jsonify({"message": f"Playlist {playlist.name} deleted successfully!"}), 200

