import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_returns_all_activities(self, client, clean_activities):
        # Arrange
        expected_activities = ["Chess Club", "Programming Class"]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert list(activities.keys()) == expected_activities

    def test_activity_has_required_fields(self, client, clean_activities):
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_data in activities.values():
            for field in required_fields:
                assert field in activity_data


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_successful_signup(self, client, clean_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]

    def test_signup_with_nonexistent_activity(self, client, clean_activities):
        # Arrange
        activity_name = "NonExistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_duplicate_signup_rejected(self, client, clean_activities):
        # Arrange
        activity_name = "Programming Class"
        email = "existing@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_increases_participant_count(self, client, clean_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        initial_count = len(
            client.get("/activities").json()[activity_name]["participants"]
        )

        # Act
        client.post(f"/activities/{activity_name}/signup?email={email}")
        updated_response = client.get("/activities")

        # Assert
        updated_count = len(
            updated_response.json()[activity_name]["participants"]
        )
        assert updated_count == initial_count + 1

    def test_new_participant_appears_in_list(self, client, clean_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        client.post(f"/activities/{activity_name}/signup?email={email}")
        response = client.get("/activities")

        # Assert
        participants = response.json()[activity_name]["participants"]
        assert email in participants
