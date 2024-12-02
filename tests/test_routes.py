import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
    yield app.test_client()
    with app.app_context():
        db.drop_all()

def test_health(client):
    response = client.get('/health')
    assert response.json == {"status": "Running"}

