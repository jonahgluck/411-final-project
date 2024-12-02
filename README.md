# Spotify Web API Application

## Overview

This Flask-based web application integrates with the Spotify API to provide account management and music discovery features. Users can create accounts, log in, search for tracks, and retrieve detailed information about tracks and artists.

## Features

- **User Account Management**
  - Create new user accounts
  - Secure login with password validation
  - Password update functionality

- **Spotify API Integration**
  - Search for music tracks by name
  - Retrieve detailed track information
  - Fetch artist details

- **Additional Capabilities**
  - Health check endpoint
  - SQLite database for user management

## Prerequisites

- Python 3.10 or later
- Spotify API credentials

## Installation

1. Clone the repository:
```bash
git clone <repository_url>
cd <repository_folder>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with the following contents:
```
SPOTIFY_ACCESS_TOKEN=your_spotify_access_token
SECRET_KEY=your_flask_secret_key
```

4. Initialize the database:
```bash
flask shell
>>> from app import db
>>> db.create_all()
```

5. Run the application:
```bash
python app.py
```

Access the app at `http://localhost:5000`

## API Endpoints

### Account Management
- `POST /create-account`: Create a new user account
- `POST /login`: Log in to an existing account
- `PUT /update-password`: Update user password

### Music Discovery
- `GET /search-track?query=<track_name>`: Search for tracks
- `GET /track/<track_id>`: Get track details
- `GET /artist/<artist_id>`: Get artist information

### System
- `GET /health-check`: Verify application status

## Testing

Run unit tests:
```bash
pytest
```

Check code coverage:
```bash
pytest --cov=.
```

## Project Structure
```
project/
├── app.py
├── routes.py
├── models.py
├── spotify_api.py
├── .env
├── requirements.txt
├── README.md
├── users.db
```

## Technologies Used
- Flask
- SQLite
- Spotify API
- Bcrypt for password security

