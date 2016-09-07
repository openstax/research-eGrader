def test_dashboard_status(test_client):
    response = test_client.get('/')
    assert response.status_code == 302


def test_home_title(test_client):
    response = test_client.get('/')
    response = response.follow()
    assert 'Openstax eGrader' in response

