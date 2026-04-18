"""
Unit tests for the Mergington High School API

Tests for activity viewing and signup endpoints using AAA pattern
"""

from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self):
        """Should return all activities from the database"""
        # Arrange - No special setup needed, activities are pre-loaded
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert "Chess Club" in data
        
    def test_activity_has_required_fields(self):
        """Each activity should have required fields"""
        # Arrange - No special setup needed
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_for_activity(self):
        """Should successfully sign up a student for an activity"""
        # Arrange
        test_email = "test@mergington.edu"
        activity_name = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert "Signed up" in response_data["message"]
        assert test_email in response_data["message"]
        
    def test_signup_duplicate_student(self):
        """Should prevent duplicate signup"""
        # Arrange
        test_email = "duplicate@mergington.edu"
        activity_name = "Chess Club"
        
        # Act - First signup (should succeed)
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        
        # Act - Second signup (should fail)
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        
        # Assert
        assert response.status_code == 400
        response_data = response.json()
        assert "already signed up" in response_data["detail"]
        
    def test_signup_nonexistent_activity(self):
        """Should return 404 for nonexistent activity"""
        # Arrange
        test_email = "test@mergington.edu"
        nonexistent_activity = "Nonexistent Club"
        
        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": test_email}
        )
        
        # Assert
        assert response.status_code == 404
        response_data = response.json()
        assert "not found" in response_data["detail"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/signup endpoint"""
    
    def test_unregister_from_activity(self):
        """Should successfully unregister a student from an activity"""
        # Arrange
        test_email = "unregister@mergington.edu"
        activity_name = "Basketball Team"
        
        # Pre-condition: Sign up first
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert "Unregistered" in response_data["message"]
        assert test_email in response_data["message"]
        
    def test_unregister_not_signed_up(self):
        """Should return 400 when trying to unregister a student who is not signed up"""
        # Arrange
        test_email = "notregistered@mergington.edu"
        activity_name = "Soccer Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        
        # Assert
        assert response.status_code == 400
        response_data = response.json()
        assert "not signed up" in response_data["detail"]
