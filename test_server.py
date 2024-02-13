import pytest
from server_learning import app, loadClubs, loadCompetitions

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

def test_purchase_more_max_places(client):
    club_name = "Simply Lift"
    competition_name = "Spring Festival"
    clubs = loadClubs()
    competitions = loadCompetitions()

    # Assurez-vous d'avoir suffisamment de places disponibles pour le test
    competition = [comp for comp in competitions if comp['name'] == competition_name][0]
    initial_number_of_places = int(competition['numberOfPlaces'])

    # Simulez l'envoi d'un formulaire avec une réservation de 13 places (plus que la limite de 12)
    response = client.post('/purchasePlaces', data={
        'club': club_name,
        'competition': competition_name,
        'places': 13
    })

    # Vérifiez que la transaction n'est pas autorisée et qu'un message d'erreur est affiché
    assert 'Impossible de réserver plus de 12 places' in response.get_data(as_text=True)

    # Vérifiez également que le nombre de places disponibles pour la compétition n'a pas été réduit
    updated_competition = [comp for comp in loadCompetitions() if comp['name'] == competition_name][0]
    assert int(updated_competition['numberOfPlaces']) == initial_number_of_places

def test_booking_past_competition(client):
    club_name = "Simply Lift"
    past_competition_name = "Spring Festival"

    response = client.get(f'/book/{past_competition_name}/{club_name}')
    assert "Cette compétition est déjà passée et ne peut pas être réservée." in response.get_data(as_text=True)


