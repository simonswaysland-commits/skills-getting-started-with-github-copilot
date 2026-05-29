from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_root_redirects_to_static_index():
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_list():
    response = client.get("/activities")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()
    assert "Programming Class" in response.json()
    assert "Gym Class" in response.json()


def test_signup_for_activity_adds_participant():
    email = "newstudent@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for Chess Club"
    }
    assert email in client.get("/activities").json()["Chess Club"]["participants"]


def test_signup_for_missing_activity_returns_404():
    response = client.post("/activities/Unknown Club/signup", params={"email": "test@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
