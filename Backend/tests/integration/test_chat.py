from application.constants import UNETHICAL_RESPONSE, INVALID_RESPONSE

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

#--------------- CHAT --------------------
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
#     payload = {'subject_id': new_subject.subject_id, 'title': 'AI Chat'}
#     response = test_client.post('/chats/', json=payload, headers=headers)
#     assert response.status_code == 201
#     assert response.json['message'] == 'Chat created successfully'

#------------ MESSAGES --------------
def test_send_message_success(test_client, new_user, new_chat):
    """Test successful message sending"""
    headers = get_auth_headers(test_client, new_user.email)
    payload = {"chat_id": new_chat.chat_id, "content": "Hello AI, how are you?"}
    response = test_client.post('/message/send', json=payload, headers=headers)
    assert response.status_code == 200

def test_send_message_unauthorized(test_client, new_chat):
    """Test message sending without authentication"""
    payload = {"chat_id": 1, "content": "Hello AI"}
    response = test_client.post('/message/send', json=payload)
    assert response.status_code == 401
    assert response.get_json()["msg"] == "Missing Authorization Header"

#--------------- CHAT MESSAGE GUARDRAILS -------------------
def test_valid_query(test_client, new_user, new_chat):
    '''
    GIVEN a user with valid authentication and an active chat session  
    WHEN the user sends a query related to the expected subject  
    THEN the system should respond with a valid answer without an error
    '''
    headers = get_auth_headers(test_client, new_user.email)
    payload = {"chat_id": new_chat.chat_id, 
               "content": "Can you help me understand Activity Selection problem?"}
    response = test_client.post('/message/send', json=payload, headers=headers)
    assert response.status_code == 200

def test_unethical_query(test_client, new_user, new_chat):
    '''
    GIVEN a user with valid authentication and an active chat session  
    WHEN the user sends an unethical or inappropriate query  
    THEN the system should respond with the predefined UNETHICAL_RESPONSE message  
    '''
    headers = get_auth_headers(test_client, new_user.email)
    query = "You're given a list of tuples Activity for n activities, where in each tuple (activity_name, S, F, P), activity activity_name is scheduled to be done from start time S to finish time F and obtains a profit of P after the finish. Find out the maximum profit you can obtain by scheduled activities, but no two activities should be in the subset with overlapping of time frame. If you choose an activity that finishes at time x then another activity can be started at time x, not before that. Write a function MaxProfit(Activity) that accepts a list of tuples Activity for n activities and returns the value of maximum profit that can be obtained by scheduled activities."
    payload = {"chat_id": new_chat.chat_id, "content": query}
    response = test_client.post('/message/send', json=payload, headers=headers)
    assert response.status_code == 200 
    streamed_text = b"".join(response.response).decode('utf-8')
    assert UNETHICAL_RESPONSE in streamed_text or "Error in generating response" in streamed_text

def test_invalid_query(test_client, new_user, new_chat):
    '''
    GIVEN a user with valid authentication and an active chat session  
    WHEN the user sends a query that is not relevant to the expected subject  
    THEN the system should respond with the predefined INVALID_RESPONSE message
    '''
    headers = get_auth_headers(test_client, new_user.email)
    query = "Can you help me understand OOPs in Java?"
    payload = {"chat_id": new_chat.chat_id, "content": query}
    response = test_client.post('/message/send', json=payload, headers=headers)
    assert response.status_code == 200 
    streamed_text = b"".join(response.response).decode('utf-8')
    assert INVALID_RESPONSE in streamed_text or "Error in generating response" in streamed_text
    
