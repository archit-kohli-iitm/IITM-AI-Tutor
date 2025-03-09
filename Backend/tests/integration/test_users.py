from flask_jwt_extended import decode_token

def test_home_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/default/health')
    assert response.status_code == 200

def test_signup(test_client, db_session):
    """Test user signup"""
    response = test_client.post('/auth/signup', json={
        'email': 'testuser@example.com',
        'password': 'TestPwd123',
        'name': 'Test User',
        'phone': '1234567890',
        'dob': '1990-01-01',
        'utype': 'tpstudent'
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'User registered successfully'
    assert 'access_token' in data
    
    # Decode token to verify correct identity
    decoded_token = decode_token(data['access_token'])
    assert decoded_token['sub'] == 'testuser@example.com'

def test_signup_existing_user(test_client, new_user):
    """Test signup with existing user"""
    response = test_client.post('/auth/signup', json={
        'email': new_user.email,
        'password': 'TestPwd123',
        'name': 'Another User'
    })
    
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User already exists'

def test_login(test_client, new_user):
    """Test user login"""
    response = test_client.post('/auth/login', json={
        'email': new_user.email,
        'password': 'TestPwd'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Login successful'
    assert 'access_token' in data

def test_login_invalid_credentials(test_client):
    """Test login with invalid credentials"""
    response = test_client.post('/auth/login', json={
        'email': 'invalid@example.com',
        'password': 'WrongPassword'
    })
    
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Invalid email or password'

def test_logout(test_client, new_user):
    """Test user logout"""
    # Obtain a valid access token
    login_response = test_client.post('/auth/login', json={
        'email': new_user.email,
        'password': 'TestPwd'
    })
    access_token = login_response.get_json()['access_token']
    
    # Perform logout
    response = test_client.post('/auth/logout', headers={
        'Authorization': f'Bearer {access_token}'
    })
    
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Logout successful'