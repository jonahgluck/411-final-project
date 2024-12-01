from flask import Blueprint, jsonify, request
from .spotify_api import search_track
from .models import SpotifyData, db

bp = Blueprint('routes', __name__)

@bp.route('/api/search-track', methods=['GET'])
def api_search_track():
    """
    Search for a track by name using the Spotify API.

    Query Parameters:
    - `query` (str): The track name to search for.

    Response:
    - JSON with track details (id, name, artist, album).
    """
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    data = search_track(query)
    if not data['tracks']['items']:
        return jsonify({"error": "No results found"}), 404

    track = data['tracks']['items'][0]
    return jsonify({
        "id": track['id'],
        "name": track['name'],
        "artist": track['artists'][0]['name'],
        "album": track['album']['name']
    })

@bp.route('/api/tracks', methods=['GET'])
def api_get_tracks():
    """
    Retrieve all tracks stored in the database.

    Response:
    - List of JSON objects with track details.
    """
    tracks = SpotifyData.query.all()
    return jsonify([{
        "id": track.track_id,
        "name": track.track_name,
        "artist": track.artist_name,
        "album": track.album_name
    } for track in tracks])

@bp.route('/api/save-track', methods=['POST'])
def api_save_track():
    """
    Save a track to the database.

    Request Body:
    - JSON object with track details (id, name, artist, album).

    Response:
    - Confirmation message.
    """
    data = request.get_json()
    required_fields = ['id', 'name', 'artist', 'album']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_track = SpotifyData(
        track_id=data['id'],
        track_name=data['name'],
        artist_name=data['artist'],
        album_name=data['album']
    )
    db.session.add(new_track)
    db.session.commit()

    return jsonify({"message": "Track saved successfully"}), 201

@bp.route('/api/delete-track/<track_id>', methods=['DELETE'])
def api_delete_track(track_id):
    """
    Delete a track from the database by track ID.

    Path Parameter:
    - `track_id` (str): The ID of the track to delete.

    Response:
    - Confirmation message.
    """
    track = SpotifyData.query.filter_by(track_id=track_id).first()
    if not track:
        return jsonify({"error": "Track not found"}), 404

    db.session.delete(track)
    db.session.commit()

    return jsonify({"message": f"Track {track_id} deleted successfully"}), 200

@bp.route('/api/update-track/<track_id>', methods=['PUT'])
def api_update_track(track_id):
    """
    Update track information in the database.

    Path Parameter:
    - `track_id` (str): The ID of the track to update.

    Request Body:
    - JSON object with updated track details (name, artist, album).

    Response:
    - Confirmation message.
    """
    track = SpotifyData.query.filter_by(track_id=track_id).first()
    if not track:
        return jsonify({"error": "Track not found"}), 404

    data = request.get_json()
    track.track_name = data.get('name', track.track_name)
    track.artist_name = data.get('artist', track.artist_name)
    track.album_name = data.get('album', track.album_name)

    db.session.commit()
    return jsonify({"message": f"Track {track_id} updated successfully"}), 200

@bp.route('/create-account', methods=['POST'])
def create_account():
    """
    Route for creating a new user account.

    Expected Request Format:
    {
        "username": "string",
        "password": "string"
    }

    Response Format:
    {
        "message": "string"
    }
    """
    # TODO: Implement account creation logic
    return jsonify({"message": "Not implemented yet"}), 501


@bp.route('/login', methods=['POST'])
def login():
    """
    Route for logging in an existing user.

    Expected Request Format:
    {
        "username": "string",
        "password": "string"
    }

    Response Format:
    {
        "message": "string"
    }
    """
    # TODO: Implement login logic
    return jsonify({"message": "Not implemented yet"}), 501


@bp.route('/update-password', methods=['PUT'])
def update_password():
    """
    Route for updating a user's password.

    Expected Request Format:
    {
        "username": "string",
        "old_password": "string",
        "new_password": "string"
    }

    Response Format:
    {
        "message": "string"
    }
    """
    # TODO: Implement password update logic
    return jsonify({"message": "Not implemented yet"}), 501

