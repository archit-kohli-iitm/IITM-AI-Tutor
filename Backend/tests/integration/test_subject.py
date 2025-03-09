def get_auth_headers(test_client, user_email, password="TestPwd"):
    """Logs in the user and returns authorization headers with a valid access token."""
    response = test_client.post('/auth/login', json={
        'email': user_email,
        'password': password
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    return {'Authorization': f'Bearer {data["access_token"]}'}

def test_get_all_subjects_admin(test_client, new_user, new_subject):
    """Test GET /subject/ as an admin user"""
    new_user.utype = "tpadmin"  # Set user as admin
    headers = get_auth_headers(test_client, new_user.email)
    
    response = test_client.get('/subjects/', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(subject['name'] == new_subject.name for subject in data)

def test_get_all_subjects_non_admin(test_client, new_user):
    """Test GET /subject/ as a non-admin user"""
    headers = get_auth_headers(test_client, new_user.email)
    response = test_client.get('/subjects/', headers=headers)
    assert response.status_code == 403
    assert response.get_json()['message'] == "Admin privileges required"

def test_create_subject_admin(test_client, new_user, db_session):
    """Test POST /subject/ as an admin user"""
    new_user.utype = "tpadmin"
    headers = get_auth_headers(test_client, new_user.email)
    data = {'name': 'Machine Learning'}
    response = test_client.post('/subjects/', headers=headers, json=data)
    assert response.status_code == 201
    assert response.get_json()['message'] == "Subject created successfully"

def test_create_subject_non_admin(test_client, new_user):
    """Test POST /subject/ as a non-admin user"""
    headers = get_auth_headers(test_client, new_user.email)
    data = {'name': 'Data Science'}
    response = test_client.post('/subjects/', headers=headers, json=data)
    assert response.status_code == 403
    assert response.get_json()['message'] == "Admin privileges required"

def test_delete_subject_admin(test_client, new_user, new_subject, db_session):
    """Test DELETE /subject/ as an admin user"""
    new_user.utype = "tpadmin"
    headers = get_auth_headers(test_client, new_user.email)
    data = {'name': new_subject.name}
    response = test_client.delete('/subjects/', headers=headers, json=data)
    assert response.status_code == 200
    assert response.get_json()['message'] == "Subject deleted successfully"

def test_delete_subject_non_admin(test_client, new_user, new_subject):
    """Test DELETE /subject/ as a non-admin user"""
    headers = get_auth_headers(test_client, new_user.email)
    data = {'name': new_subject.name}
    response = test_client.delete('/subjects/', headers=headers, json=data)
    assert response.status_code == 403
    assert response.get_json()['message'] == "Admin privileges required"

def test_list_all_subject_chats(test_client, new_user, new_chat):
    """Test GET /subject/list to fetch subjects and chats of a user"""
    headers = get_auth_headers(test_client, new_user.email)
    response = test_client.get('/subjects/list', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(chat['chat_id'] == new_chat.chat_id for chat in data)