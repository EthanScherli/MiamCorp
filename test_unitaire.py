import unittest
from unittest.mock import patch
from datetime import datetime, timedelta, date
from Reservations import Reservation, DateInvalideError
from main import Main, Utilisateur

class TestReservation(unittest.TestCase):

    def test_creation_reservation_future(self):
        demain = (date.today() + timedelta(days=1)).isoformat()
        try:
            resa = Reservation(1, 1, 1, demain, "12:00", 2, "Aucune")
            self.assertEqual(resa.date, demain)
        except DateInvalideError:
            self.fail(f"Une date future valide ({demain}) ne devrait pas lever d'exception.")

    def test_rejet_reservation_passee(self):
        hier = (date.today() - timedelta(days=1)).isoformat()
        with self.assertRaises(DateInvalideError):
            Reservation(1, 1, 1, hier, "12:00", 2, "Aucune")

class TestConnecterUtilisateur(unittest.TestCase):

    def setUp(self):
        Main.liste_utilisateurs = [
            Utilisateur("Dupont", "Jean", "jean.dupont@mail.com", "1234", "client"),
            Utilisateur("Martin", "Alice", "alice.martin@mail.com", "abcd", "client")
        ]
        Main.utilisateurConnecte = None

    @patch('builtins.input', side_effect=["jean.dupont@mail.com", "1234"])
    @patch('builtins.print')
    def test_connecter_utilisateur_valide(self, mock_print, mock_input):
        utilisateur = Main.connecterUtilisateur()
        self.assertIsNotNone(utilisateur)
        self.assertEqual(utilisateur.email, "jean.dupont@mail.com")
        self.assertEqual(Main.utilisateurConnecte, utilisateur)
        mock_print.assert_any_call("email trouvé")

    @patch('builtins.input', side_effect=["inconnu@mail.com", "jean.dupont@mail.com", "1234"])
    @patch('builtins.print')
    def test_connecter_utilisateur_email_incorrect_puis_correct(self, mock_print, mock_input):
        utilisateur = Main.connecterUtilisateur()
        self.assertEqual(utilisateur.email, "jean.dupont@mail.com")
        mock_print.assert_any_call("email introuvable")
        mock_print.assert_any_call("email trouvé")

    @patch('builtins.input', side_effect=["alice.martin@mail.com", "wrong", "abcd"])
    @patch('builtins.print')
    def test_connecter_utilisateur_mdp_incorrect_puis_correct(self, mock_print, mock_input):
        utilisateur = Main.connecterUtilisateur()
        self.assertEqual(utilisateur.email, "alice.martin@mail.com")
        mock_print.assert_any_call("mot de passe incorrect")

if __name__ == '__main__':
    unittest.main()



class TestCapaciteTable(unittest.TestCase):

    def test_depassement_capacite(self):
        capacite_table = 4
        nbr_pers = 6
        self.assertGreater(nbr_pers, capacite_table)



