# Spotify-like Web Application

## Description
This is a Flask-based web application that provides Spotify-like functionality for managing user accounts, playlists, and interacting with Spotify's API to search for tracks. Users can create accounts, create playlists, add tracks, and search for songs using the Spotify API.

## Features
- **User Account Management**: Create accounts, login, and update passwords.
- **Playlist Management**: Create, view, update, and delete playlists.
- **Track Management**: Search tracks from Spotify's API and add them to playlists.

## Getting Started

### Prerequisites
- Python 3.9 or above
- Docker (Optional, for containerization)

### Installation

1. **Clone the Repository**:
   ```sh
   git clone <repo_url>
   cd spotify-like-app
   ```

2. **Set Up Environment**:
   * Install dependencies:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   * Create a `.env` file in the project root:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   SECRET_KEY=your_flask_secret_key
   DATABASE_URL=sqlite:///app.db
   ```

4. **Initialize Database**:
   ```sh
   flask db upgrade
   flask shell
   >>> from models import db
   >>> db.create_all()
   ```

5. **Run the Application**:
   ```sh
   flask run
   ```

### Running with Docker
1. Build the Docker image:
   ```sh
   docker build -t spotify-like-app .
   ```

2. Run the container:
   ```sh
   docker run -p 5000:5000 spotify-like-app
   ```

## API Endpoints

### User Management
- `POST /register`: Create a new user account
- `POST /login`: Authenticate user
- `PUT /profile`: Update user profile

### Playlist Management
- `POST /playlists`: Create a new playlist
- `GET /playlists`: Retrieve user's playlists
- `PUT /playlists/<playlist_id>`: Update a playlist
- `DELETE /playlists/<playlist_id>`: Delete a playlist

### Track Management
- `GET /tracks/search`: Search tracks using Spotify API
- `POST /playlists/<playlist_id>/tracks`: Add tracks to a playlist

## Testing
Run tests using pytest:
```sh
pytest
```

## Technologies
- Flask
- SQLAlchemy
- Spotify Web API
- Docker
- Pytest
