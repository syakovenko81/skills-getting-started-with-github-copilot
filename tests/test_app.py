import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

def test_signup_and_unregister():
    activity = next(iter(client.get("/activities").json().keys()))
    email = "testuser@example.com"
    # Signup
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    # Check participant added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]
    # Unregister
    unregister_resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert unregister_resp.status_code == 200
    # Check participant removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]
