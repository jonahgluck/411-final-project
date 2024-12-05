import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the health-check endpoint."""
    response = client.get('/health-check')
    assert response.status_code == 200
    assert response.json == {"status": "running"}

def test_home(client):
    """Test the home route."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == "App Running Successfully!"

def test_create_account(client):
    """Test the create-account endpoint."""
    response = client.post('/create-account', json={
        "username": "smoke_test_user",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.json == {"message": "Account created successfully"}

def test_login(client):
    """Test the login endpoint."""
    client.post('/create-account', json={
        "username": "smoke_test_user",
        "password": "password123"
    })
    response = client.post('/login', json={
        "username": "smoke_test_user",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json == {"message": "Login successful"}

def test_update_password(client):
    """Test the update-password endpoint."""
    client.post('/create-account', json={
        "username": "smoke_test_user",
        "password": "password123"
    })
    response = client.put('/update-password', json={
        "username": "smoke_test_user",
        "old_password": "password123",
        "new_password": "new_password123"
    })
    assert response.status_code == 200
    assert response.json == {"message": "Password updated successfully"}
