from fastapi.testclient import TestClient
from src.app import app
import urllib.parse

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data


def test_signup_and_unregister():
    activity = "Basketball Team"
    email = "testuser@example.com"

    # Ensure email is not already present
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    if email in participants:
        client.post(f"/activities/{urllib.parse.quote(activity)}/unregister?email={urllib.parse.quote(email)}")

    # Sign up the test user
    resp = client.post(f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json()["message"]

    # Verify user was added
    resp = client.get("/activities")
    assert email in resp.json()[activity]["participants"]

    # Unregister the test user
    resp = client.post(f"/activities/{urllib.parse.quote(activity)}/unregister?email={urllib.parse.quote(email)}")
    assert resp.status_code == 200
    assert "Unregistered" in resp.json()["message"]

    # Verify user was removed
    resp = client.get("/activities")
    assert email not in resp.json()[activity]["participants"]
