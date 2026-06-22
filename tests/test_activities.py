"""Tests for the GET /activities endpoint."""

import pytest


def test_get_all_activities(client):
    """Test retrieving all activities from the API."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Verify we get a dictionary of activities
    assert isinstance(activities, dict)
    assert len(activities) > 0


def test_activities_contain_expected_fields(client):
    """Test that each activity has required fields."""
    response = client.get("/activities")
    activities = response.json()
    
    # Check that each activity has required fields
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str)
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        
        # Verify types
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_activities_have_participants_list(client):
    """Test that activities have a list of participants."""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        participants = activity_data["participants"]
        assert isinstance(participants, list)
        
        # Each participant should be an email string
        for participant in participants:
            assert isinstance(participant, str)
            assert "@" in participant  # Basic email validation


def test_activities_response_includes_specific_activities(client):
    """Test that expected activities are in the response."""
    response = client.get("/activities")
    activities = response.json()
    
    # These are activities from the app's hardcoded data
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class"
    ]
    
    for activity in expected_activities:
        assert activity in activities
