# Spotify Web App

## Description
A Flask web application that interacts with the Spotify API to search for tracks and save them to a database.

## Routes
### `/health-check` (GET)
- **Purpose**: Check if the application is running.
- **Response**: `{"status": "running"}`

### `/search-track` (GET)
- **Purpose**: Search for a track on Spotify by query and save to the database.
- **Request**: `?query=<track_name>`
- **Response**: JSON object with track details.

### `/tracks` (GET)
- **Purpose**: Fetch all tracks stored in the database.
- **Response**: List of JSON objects with track details.

