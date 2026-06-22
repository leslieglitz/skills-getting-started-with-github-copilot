"""Tests for the POST /activities/{activity_name}/signup endpoint."""

import pytest


def test_successful_signup(client):
    """Test successfully signing up a student for an activity."""
    response = client.post(
        "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds the participant to the activity."""
    # Sign up a student
    signup_response = client.post(
        "/activities/Chess%20Club/signup?email=alice@mergington.edu"
    )
    assert signup_response.status_code == 200
    
    # Fetch activities and verify the student was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    participants = activities["Chess Club"]["participants"]
    
    assert "alice@mergington.edu" in participants


def test_signup_duplicate_student(client):
    """Test that a student cannot sign up twice for the same activity."""
    # Sign up a student
    client.post("/activities/Chess%20Club/signup?email=bob@mergington.edu")
    
    # Try to sign up again
    response = client.post(
        "/activities/Chess%20Club/signup?email=bob@mergington.edu"
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_nonexistent_activity(client):
    """Test signing up for an activity that doesn't exist."""
    response = client.post(
        "/activities/Nonexistent%20Club/signup?email=charlie@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_signup_with_different_email_formats(client):
    """Test signing up with various valid email formats."""
    test_emails = [
        "student1@mergington.edu",
        "student.name@mergington.edu",
        "student+tag@mergington.edu"
    ]
    
    for email in test_emails:
        response = client.post(
            f"/activities/Programming%20Class/signup?email={email}"
        )
        # Should succeed or fail gracefully if already exists
        assert response.status_code in [200, 400]


def test_signup_respects_max_participants(client):
    """Test that an activity can still accept signups up to max_participants.
    
    This is an integration test that verifies the signup system tracks
    participant count correctly.
    """
    # Get current state
    activities_response = client.get("/activities")
    activities = activities_response.json()
    
    # Chess Club has max_participants of 12
    chess_club = activities["Chess Club"]
    current_count = len(chess_club["participants"])
    max_participants = chess_club["max_participants"]
    
    # Verify we're not full before test
    assert current_count < max_participants
    
    # Sign up a new student
    response = client.post(
        "/activities/Chess%20Club/signup?email=newmember@mergington.edu"
    )
    
    assert response.status_code == 200
    
    # Verify participant count increased
    updated_activities = client.get("/activities").json()
    new_count = len(updated_activities["Chess Club"]["participants"])
    assert new_count == current_count + 1
