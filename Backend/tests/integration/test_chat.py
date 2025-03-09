import json

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

def test_get_chat_success(test_client, new_user, new_chat):
    headers = get_auth_headers(test_client,new_user.email)
    response = test_client.get(f'/chats/{new_chat.chat_id}', headers=headers)
    assert response.status_code == 200
    assert response.json['chat_id'] == new_chat.chat_id

def test_get_chat_not_found(test_client, new_user):
    headers = get_auth_headers(test_client,new_user.email)
    response = test_client.get('/chats/9999', headers=headers)
    assert response.status_code == 404
    assert response.json['message'] == 'Chat not found'

def test_delete_chat_success(test_client, new_user, new_chat):
    headers = get_auth_headers(test_client,new_user.email)
    response = test_client.delete(f'/chats/{new_chat.chat_id}', headers=headers)
    assert response.status_code == 200
    assert response.json['message'] == 'Chat deleted successfully'

def test_delete_chat_not_found(test_client, new_user):
    headers = get_auth_headers(test_client,new_user.email)
    response = test_client.delete('/chats/9999', headers=headers)
    assert response.status_code == 404
    assert response.json['message'] == 'Chat not found'

# -------------- GETTING ERROR IN THIS, PLS CHECK ------------------
# def test_create_chat_success(test_client, new_user, new_subject):
#     headers = get_auth_headers(test_client,new_user.email)
#     data = {'subject_id': new_subject.subject_id, 'title': 'AI Chat'}
#     response = test_client.post('/chats/create', data=json.dumps(data), headers=headers, content_type='application/json')
#     assert response.status_code == 201
#     assert response.json['message'] == 'Chat created successfully'


def test_send_message_success(test_client, new_user, new_chat):
    """Test successful message sending with AI response streaming."""
    headers = get_auth_headers(test_client, new_user.email)
    payload = {"chat_id": new_chat.chat_id, "content": "Hello AI, how are you?"}
    response = test_client.post('/message/send', json=payload, headers=headers)
    assert response.status_code == 200
    # streamed_response = "".join([chunk.decode('utf-8') for chunk in response.iter_encoded()])
    # assert "Hello, this is AI response." in streamed_response

def test_send_message_unauthorized(test_client):
    """Test message sending without authentication (should return 401)."""
    payload = {"chat_id": 1, "content": "Hello AI"}
    response = test_client.post('/message/send', json=payload)
    assert response.status_code == 401
    assert response.get_json()["msg"] == "Missing Authorization Header"

# def test_send_message_streaming_failure(test_client, new_user, new_chat, mocker):
#     """Test AI response failure during streaming."""
#     headers = get_auth_headers(test_client, new_user.email)
#     payload = {"chat_id": new_chat.chat_id, "content": "Hello AI, how are you?"}

#     # Simulate an exception in getQueryResponse
#     mocker.patch("application.routes.getQueryResponse", side_effect=Exception("LLM Error"))

#     response = test_client.post('/message/send', json=payload, headers=headers, stream=True)
    
#     assert response.status_code == 200  # Streaming starts, but with error message
#     streamed_response = "".join([chunk.decode('utf-8') for chunk in response.iter_encoded()])
#     assert "Error: Failed to get response" in streamed_response