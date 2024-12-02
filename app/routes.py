from flask import Blueprint, jsonify, request
from .spotify_api import spotify_request
from .models import db, User
from bcrypt import hashpw, gensalt, checkpw

routes_bp = Blueprint('routes', __name__)

# Health Check Route
@routes_bp.route('/health-check', methods=['GET'])
def health_check():
    """Verify the app is running."""
    return jsonify({"status": "running"}), 200

# Create Account Route
@routes_bp.route('/create-account', methods=['POST'])
def create_account():
    """Create a new user account."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password cannot be null"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    salt = gensalt()
    password_hash = hashpw(password.encode('utf-8'), salt).decode('utf-8')

    new_user = User(username=username, salt=salt.decode('utf-8'), password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Account created successfully"}), 201

# Login Route
@routes_bp.route('/login', methods=['POST'])
def login():
    """Log in an existing user."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password cannot be null"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Username not registered"}), 401

    if checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Incorrect password"}), 401

# Update Password Route
@routes_bp.route('/update-password', methods=['PUT'])
def update_password():
    """Update an existing user's password."""
    data = request.json
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not username or not old_password or not new_password:
        return jsonify({"error": "All fields are required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Username not registered"}), 401

    if not checkpw(old_password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({"error": "Incorrect old password"}), 401

    salt = gensalt()
    new_password_hash = hashpw(new_password.encode('utf-8'), salt).decode('utf-8')

    user.salt = salt.decode('utf-8')
    user.password_hash = new_password_hash
    db.session.commit()

    return jsonify({"message": "Password updated successfully"}), 200

# Spotify Search Track Route
@routes_bp.route('/search-track', methods=['GET'])
def search_track():
    """Search for a track by name using Spotify API."""
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    data = spotify_request("search", {"q": query, "type": "track", "limit": 1})
    if not data['tracks']['items']:
        return jsonify({"error": "No tracks found"}), 404

    track = data['tracks']['items'][0]
    return jsonify({
        "id": track['id'],
        "name": track['name'],
        "artist": track['artists'][0]['name'],
        "album": track['album']['name']
    })

# Spotify Get Track Details Route
@routes_bp.route('/track/<track_id>', methods=['GET'])
def get_track_details(track_id):
    """Get detailed information about a specific track."""
    data = spotify_request(f"tracks/{track_id}")
    return jsonify({
        "id": data['id'],
        "name": data['name'],
        "artist": data['artists'][0]['name'],
        "album": data['album']['name'],
        "popularity": data['popularity']
    })

# Spotify Get Artist Details Route
@routes_bp.route('/artist/<artist_id>', methods=['GET'])
def get_artist_details(artist_id):
    """Get detailed information about an artist."""
    data = spotify_request(f"artists/{artist_id}")
    return jsonify({
        "id": data['id'],
        "name": data['name'],
        "followers": data['followers']['total'],
        "genres": data['genres']
    })

