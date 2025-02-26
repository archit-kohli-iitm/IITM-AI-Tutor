
def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password, and utype (role) fields are defined correctly
    """
    assert new_user.email == 'testuser79@gmail.com'
    assert new_user.password == 'TestPwd'
    assert new_user.utype == 'user'
