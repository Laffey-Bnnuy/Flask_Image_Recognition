"""Shared pytest fixtures."""

import pytest
from app import app  # This imports the Flask app for testing

@pytest.fixture(name="client")
def fixture_client():
    """Flask test client."""
    with app.test_client() as client:
        yield client
