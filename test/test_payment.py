# test_members.py
import pytest
from app import create_app
from models import db

@pytest.fixture
def test_app():
    app = create_app('testing')  # Initialize app with the testing configuration
    with app.app_context():
        db.create_all()  # Create in-memory database for testing
        yield app  # Yield the app to the test
        db.session.remove()
        db.drop_all()  # Cleanup after tests


@pytest.fixture
def client(test_app):
    return test_app.test_client()  # Return the test client for making HTTP requests


def test_add_member(client):
    # Test adding a new member
    response = client.post('/members', json={
        'f_name': 'John',
        'l_name': 'Doe',
        'phone_number': '0710855840',
        'email': 'john.doe@gmail.com'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'New member added successfully'


def test_duplicate_member(client):
    # Test adding a member with duplicate phone number or email
    client.post('/members', json={
        'f_name': 'John',
        'l_name': 'Doe',
        'phone_number': '1234567890',
        'email': 'john.doe@example.com'
    })
    response = client.post('/members', json={
        'f_name': 'Jane',
        'l_name': 'Smith',
        'phone_number': '1234567890',  # Duplicate phone number
        'email': 'jane.smith@example.com'
    })
    assert response.status_code == 422
    assert response.json['message'] == 'Phone number already exists'
