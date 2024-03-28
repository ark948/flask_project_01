def test_auth_bp(client):
    response = client.get('/auth')
    assert response.status_code == 308