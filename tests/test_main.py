def test_main_bp(client):
    response = client.get('/')
    assert response.status_code == 200