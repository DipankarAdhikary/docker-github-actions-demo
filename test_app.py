from app import app

def test_health():
    test_client = app.test_client()
    response = test_client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}
