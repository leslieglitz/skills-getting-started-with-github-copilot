"""Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint."""

import pytest
from urllib.parse import quote


def test_successful_participant_removal(client):
    """Test successfully removing a participant from an activity."""
    # First, verify the participant exists
    activities_before = client.get("/activities").json()
    initial_participants = activities_before["Chess Club"]["participants"].copy()
    
    if initial_participants:
        email_to_remove = initial_participants[0]
        
        # Remove the participant
        response = client.delete(
            f"/activities/Chess%20Club/participants/{email_to_remove}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "Removed" in data["message"]
        assert email_to_remove in data["message"]


def test_removal_updates_activity_list(client):
    """Test that removing a participant updates the activity participant list."""
    # Get initial state
    activities_before = client.get("/activities").json()
    initial_participants = activities_before["Programming Class"]["participants"].copy()
    initial_count = len(initial_participants)
    
    if initial_participants:
        email_to_remove = initial_participants[0]
        
        # Remove the participant
        client.delete(
            f"/activities/Programming%20Class/participants/{email_to_remove}"
        )
        
        # Verify participant was removed
        activities_after = client.get("/activities").json()
        final_participants = activities_after["Programming Class"]["participants"]
        
        assert email_to_remove not in final_participants
        assert len(final_participants) == initial_count - 1


def test_remove_nonexistent_participant(client):
    """Test removing a participant that doesn't exist in an activity."""
    response = client.delete(
        "/activities/Gym%20Class/participants/nonexistent@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_remove_from_nonexistent_activity(client):
    """Test removing a participant from an activity that doesn't exist."""
    response = client.delete(
        "/activities/Nonexistent%20Activity/participants/student@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_remove_participant_with_special_characters_in_email(client):
    """Test removing a participant with special characters in email (URL encoded)."""
    # First, sign up a participant with a special character email
    email = "student+special@mergington.edu"
    signup_response = client.post(
        f"/activities/Gym%20Class/signup?email={quote(email)}"
    )
    
    if signup_response.status_code == 200:
        # Now try to remove them using proper URL encoding
        response = client.delete(
            f"/activities/Gym%20Class/participants/{quote(email)}"
        )
        
        assert response.status_code == 200


def test_integration_signup_then_remove(client):
    """Integration test: sign up a student then remove them."""
    email = "integration.test@mergington.edu"
    
    # Sign up
    signup_response = client.post(
        f"/activities/Gym%20Class/signup?email={email}"
    )
    assert signup_response.status_code == 200
    
    # Verify they're in the list
    activities = client.get("/activities").json()
    assert email in activities["Gym Class"]["participants"]
    
    # Remove them
    remove_response = client.delete(
        f"/activities/Gym%20Class/participants/{email}"
    )
    assert remove_response.status_code == 200
    
    # Verify they're no longer in the list
    activities_after = client.get("/activities").json()
    assert email not in activities_after["Gym Class"]["participants"]
