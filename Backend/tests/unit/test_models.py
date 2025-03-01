def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password, and utype (role) fields are defined correctly
    """
    assert new_user.name == 'Test User'
    assert new_user.email == 'testuser79@gmail.com'
    assert new_user.password == 'TestPwd'
    assert new_user.utype == 'user'
    #--- default values are correctly assigned or not ---
    assert new_user.active is False  
    assert new_user.phone == '0000000000'  
    assert new_user.dob == '1900-01-01'  
    assert new_user.flagged == 'N'  
    assert new_user.chats == []  # Should have no associated chats initially

def test_new_subject(new_subject):
    """
    GIVEN a Subject model
    WHEN a new Subject is created
    THEN check the name field is defined correctly
    """
    assert new_subject.name == 'Artificial Intelligence'
    assert new_subject.chats == []  # Should have no associated chats initially
    
def test_new_chat(new_chat, new_user, new_subject):
    """
    GIVEN a Chat model
    WHEN a new Chat is created
    THEN check if the user_id and subject_id are assigned correctly
    """
    assert new_chat.uid == new_user.uid
    assert new_chat.title == 'AI Discussion'
    assert new_chat.subject_id == new_subject.subject_id
    assert new_chat.messages == []  # Should have no messages initially

def test_new_message(new_message, new_chat):
    """
    GIVEN a Message model
    WHEN a new Message is created
    THEN check if the chat_id, content, and msg_type are correctly assigned
    """
    assert new_message.chat_id == new_chat.chat_id
    assert new_message.content == "Hello, this is a test message."
    assert new_message.msg_type == "user"
    assert new_message.context is None  # Default should be None