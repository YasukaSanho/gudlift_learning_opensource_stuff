import pytest
from server import app, loadClubs, loadCompetitions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_email_introuvable(client):
    response = client.post('/showSummary', data={'email': 'emailinexistant@example.com'})
    assert response.status_code == 200
    assert 'email introuvable' in response.data.decode('utf-8')
