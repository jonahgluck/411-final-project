from flask import Blueprint, request, jsonify
from .models import User, Playlist, Track
from . import db
from werkzeug.security import check_password_hash
import requests
from .api_client import SpotifyAPI

main = Blueprint('main', __name__)

@main.route('/create-account', methods=['POST'])
def create_account():
    data = request.json
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Account created successfully!"}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@main.route('/update-password', methods=['POST'])
def update_password():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['old_password']):
        user.set_password(data['new_password'])
        db.session.commit()
        return jsonify({"message": "Password updated successfully!"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@main.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "Running"}), 200

@main.route('/playlists', methods=['POST'])
def create_playlist():
    data = request.json
    playlist = Playlist(name=data['name'], description=data.get('description', ''))
    db.session.add(playlist)
    db.session.commit()
    return jsonify({"message": "Playlist created successfully!", "playlist_id": playlist.id}), 201

@main.route('/search-track', methods=['GET'])
def search_track():
    query = request.args.get('q')
    results = SpotifyAPI.search_tracks(query)
    return jsonify(results), 200

@main.route('/playlist/<int:playlist_id>', methods=['GET'])
def get_playlist_details(playlist_id):
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
    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404

    db.session.delete(playlist)
    db.session.commit()
    return jsonify({"message": f"Playlist {playlist.name} deleted successfully!"}), 200

