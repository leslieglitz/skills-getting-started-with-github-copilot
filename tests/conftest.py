"""Shared pytest fixtures for FastAPI tests."""

import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client(sample_activities):
    """Provide a TestClient instance for testing the FastAPI app."""
    app_module.activities = copy.deepcopy(sample_activities)
    return TestClient(app_module.app)

@pytest.fixture
def sample_activities():
    """Provide a fresh copy of sample activities data for each test.
    
    This fixture ensures test isolation by providing a clean copy of activities
    for each test, preventing data pollution from other tests.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
