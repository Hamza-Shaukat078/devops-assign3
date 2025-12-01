import os
import sys

# Ensure the project root (where app.py lives) is on the Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app  # type: ignore


def test_app_exists():
    """
    Basic sanity test:
    Ensures the Flask app instance is created correctly.
    """
    assert app is not None


def test_home_route_status_code():
    """
    Test that the home route returns HTTP 200.
    The route handles DB errors internally, so this should pass
    even if MySQL is not running.
    """
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_home_route_contains_title():
    """
    Check that the homepage contains the main heading text.
    Update the expected text if you change the template.
    """
    client = app.test_client()
    response = client.get("/")
    # This should match the <h1> in templates/index.html
    assert b"CI/CD Flask Task App" in response.data

