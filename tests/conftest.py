import os
import sys

import pytest


@pytest.fixture(autouse=True, scope="session")
def base_config():
    sys.path = [os.path.join(os.path.dirname(__file__), "..")] + sys.path


@pytest.fixture()
def redirector_app(base_config):
    """Used for testing the Redirector flask app in the context of the unit tests."""
    from redirector.app import create_app

    app = create_app(
        configs={
            "TESTING": True,
            "DEBUG": True,
        }
    )

    with app.app_context():
        yield app


@pytest.fixture()
def redirector_client(redirector_app):
    """Used for making requests to the app in the context of the app tests."""
    with redirector_app.test_client() as client:
        yield client


@pytest.fixture()
def redirector_runner(redirector_app):
    """Used for running CLI commands in the context of the app tests."""
    return redirector_app.test_cli_runner()


@pytest.fixture()
def admin_app(base_config):
    """Used for testing the Admin flask app in the context of the unit tests."""
    from admin.app import create_app

    app = create_app(
        configs={
            "TESTING": True,
            "DEBUG": True,
        }
    )

    with app.app_context():
        yield app


@pytest.fixture()
def admin_client(admin_app):
    """Used for making requests to the Admin app in the context of the unit tests."""
    with admin_app.test_client() as client:
        yield client


@pytest.fixture()
def admin_runner(admin_app):
    """Used for running CLI commands in the context of the unit tests."""
    return admin_app.test_cli_runner()
