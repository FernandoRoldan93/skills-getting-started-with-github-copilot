from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange
    expected_activity_keys = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Swimming Club",
        "Drama Club",
        "Music Ensemble",
        "Science Olympiad",
        "Debate Team",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert set(activities.keys()) == expected_activity_keys
    assert all("participants" in activity for activity in activities.values())


def test_signup_adds_participant_to_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    # Verify the participant was added
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_duplicate_signup_returns_400():
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant():
    # Arrange
    activity_name = "Gym Class"
    email = "olivia@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_nonexistent_participant_returns_404():
    # Arrange
    activity_name = "Chess Club"
    email = "missing@student.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
