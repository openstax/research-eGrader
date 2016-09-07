def test_successful_login(user, test_client):
    """Login successful!"""
    response = test_client.get('/login')
    form = response.form
    form['email'] = user.email
    form['password'] = 'iH3@r7P1zz@'
    response = form.submit()
    assert response.status_code == 200


def test_unsuccessful_login(user, test_client):
    """Login unsucessful"""
    response = test_client.get('/login')
    form = response.form
    form['email'] = user.email
    form['password'] = 'iH3@r7P@rsn1ps'
    response = form.submit()
    assert 'Invalid password' in response
