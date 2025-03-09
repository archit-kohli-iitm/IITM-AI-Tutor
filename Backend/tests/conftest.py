# Fixtures initialize tests to a known state to run tests in a predictable and repeatable manner.
# The @pytest.fixture decorator specifies that this function is a fixture with module/function-level scope. 
# In other words, this fixture will be called one per test module.

# import sys
# import os
# # Add the path to folder1 to the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
#from flask import current_app as myapp

import pytest
from main import create_app
from application.config import TestConfig
from application.models import User, Subject, Chat, Message, mydb
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='module')
def test_app():
    # Create a test Flask app with a test database
    flask_app = create_app(TestConfig)[0]
    with flask_app.app_context():
        mydb.create_all()  # Create tables in the test database
        yield flask_app
        mydb.session.remove()
        mydb.drop_all()  # Drop tables after tests to reset db

@pytest.fixture(scope='module')
def test_client(test_app):
    # Provide a test client for making requests
    return test_app.test_client()

@pytest.fixture(scope='function')
def db_session(test_app):
    # Create a new database session for each test and rollback afterward
    with test_app.app_context():
        session = mydb.session
        session.begin()  # Start transaction
        yield session
        session.rollback()  # Rollback changes to keep db clean
        session.close()  # Close session

@pytest.fixture(scope='function')
def new_user(db_session):
    # Create a new user and commit it to the test database
    pwd = generate_password_hash('TestPwd')
    user = User(name='Test User', email='testuser79@gmail.com', password=pwd, utype='user', active=False)
    db_session.add(user)
    db_session.commit()
    yield user
    # cleanup after test
    db_session.delete(user)  
    db_session.commit()

@pytest.fixture(scope='function')
def new_subject(db_session):
    # Create a new subject and commit it to the test database
    subject = Subject(name='Artificial Intelligence')
    db_session.add(subject)
    db_session.commit()
    yield subject
    db_session.delete(subject)  
    db_session.commit()

@pytest.fixture(scope='function')
def new_chat(db_session, new_user, new_subject):
    # Create a new chat associated with a user and a subject
    chat = Chat(uid=new_user.uid, title='AI Discussion', subject_id=new_subject.subject_id)
    db_session.add(chat)
    db_session.commit()
    yield chat
    db_session.delete(chat) 
    db_session.commit()

@pytest.fixture(scope='function')
def new_message(db_session, new_chat):
    # Create a new message linked to a chat
    message = Message(chat_id=new_chat.chat_id, content="Hello, this is a test message.", msg_type="user")
    db_session.add(message)
    db_session.commit()
    yield message
    db_session.delete(message) 
    db_session.commit()