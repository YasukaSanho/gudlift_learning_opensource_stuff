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


def test_redeem_more_points_than_available(client):
    club_name = "Iron Temple"
    competition_name = "Fall Classic"
    clubs = loadClubs()
    club = [c for c in clubs if c['name'] == club_name][0]
    initial_points = int(club['points'])
    points_to_redeem = initial_points + 10  # Un nombre supérieur aux points disponibles

    # Simulez l'envoi d'un formulaire avec plus de points que disponibles
    response = client.post('/purchasePlaces', data={
        'club': club_name,
        'competition': competition_name,
        'places': points_to_redeem
    })

    # Vérifie que le message d'erreur est affiché
    assert f'Vous n avez pas assez de points : seulement {initial_points} réservés.' in response.get_data(as_text=True)

    # Vérifiez que les points du club n'ont pas été déduits incorrectement
    updated_club = [c for c in loadClubs() if c['name'] == club_name][0]
    assert int(updated_club['points']) == initial_points
