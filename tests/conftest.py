"""
Pytest configuration and fixtures for isolated testing

Provides fixtures to reset application state between tests
"""

import pytest
from copy import deepcopy
from src.app import activities


# Store the original activities state
ORIGINAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture to reset the in-memory activities data before each test
    
    This ensures test isolation by restoring the original state of the
    activities dictionary before every test function runs.
    """
    # Reset to original state before test
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    
    yield
    
    # Cleanup after test (optional, but good practice)
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
