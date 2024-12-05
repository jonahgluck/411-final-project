import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"  # Adjust this to your app's running URL

def test_health():
    response = requests.get(f"{BASE_URL}/health-check")
    assert response.status_code == 200

def test_create_account():
    payload = {
        "username": "testuser",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/create_account", json=payload)
    assert response.status_code == 200

def test_login():
    payload = {
        "username": "testuser",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/login", json=payload)
    assert response.status_code == 200

def test_update_password():
    payload = {
        "username": "testuser",
        "old_password": "password123",
        "new_password": "newpassword456"
    }
    response = requests.post(f"{BASE_URL}/update_password", json=payload)
    assert response.status_code == 200

