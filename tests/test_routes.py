import pytest
from app import create_app, db

@pytest.fixture
def client():
    """Prepares a test client for the Flask application.

        Configures the application in testing mode, sets up an in-memory SQLite database
        for isolated tests, and provides a client to send HTTP requests.

        Yields:
            FlaskClient: A client for sending requests to the application during tests.
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
    yield app.test_client()
    with app.app_context():
        db.drop_all()

def test_health(client):
    """Validates the health check endpoint.

        Sends a GET request to the '/health/' endpoint and checks that the response matches 
        the expected status message.

        Args: 
            client (FlaskClient): The test client used to simulate HTTP requestes.

        Asserts: 
            - The response contains a JSON object with '{"status": "Running"}'.
    """
    response = client.get('/health-check')
    assert response.json == {"status": "running"}

