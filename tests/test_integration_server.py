import pytest
from ..server import app, loadClubs, loadCompetitions
from flask import url_for

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_clubs_details_display(client):
    response = client.get('/clubsDetails')
    assert response.status_code == 200
    for club in loadClubs():
        assert club['name'] in response.get_data(as_text=True)
        assert str(club['points']) in response.get_data(as_text=True)



def test_logout_process(client):
    response = client.get('/logout')
    assert response.status_code == 302


def test_booking_flow(client):
    # Étape 1 : Envoyer un email valide pour afficher le résumé
    valid_email = 'john@simplylift.co'
    response = client.post('/showSummary', data={'email': valid_email})
    assert response.status_code == 200
    assert 'Summer Festival' in response.get_data(as_text=True)

    # Étape 2 : Récupérer les données pour l'étape suivante
    clubs = loadClubs()
    valid_club_name = next(club['name'] for club in clubs if club['email'] == valid_email)
    competitions = loadCompetitions()
    summer_festival = next(comp for comp in competitions if comp['name'] == 'Summer Festival')

    # Étape 3 : Aller à la page de réservation pour "Summer Festival"
    response = client.get(f'/book/{summer_festival["name"]}/{valid_club_name}')
    assert response.status_code == 200
    # Vérifiez que le bouton de réservation est présent sur la page
    assert 'type="submit">Book</button>' in response.get_data(as_text=True)

