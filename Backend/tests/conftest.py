# Fixtures initialize tests to a known state to run tests in a predictable and repeatable manner.

# The @pytest.fixture decorator specifies that this function is a fixture with module-level scope. 
# In other words, this fixture will be called one per test module.
# import sys
# import os
# # Add the path to folder1 to the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

#from flask import current_app as myapp
from main import create_app
from application.config import TestConfig
from application.models import User
import pytest


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(TestConfig)[0]
    # print(flask_app)
    # print("URL MAP:-")
    # print(flask_app.url_map)
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client

@pytest.fixture(scope='module')
def new_user():
    user = User(email='testuser79@gmail.com', password='TestPwd', utype='user')
    return user