import unittest
from Reservations import Reservation, DateInvalideError
from datetime import datetime, timedelta

class TestReservation(unittest.TestCase):

    def test_creation_reservation_future(self):
        """Test si une réservation future est bien acceptée."""
        # On prend la date de demain
        demain = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        try:
            # On essaie de créer une réservation
            resa = Reservation(1, 1, 1, demain, "12:00", 2, "Aucune")
            # On vérifie que la date a bien été enregistrée
            self.assertEqual(resa.date, demain)
        except DateInvalideError:
            self.fail(f"Une date future valide ({demain}) ne devrait pas lever d'exception.")

    def test_rejet_reservation_passee(self):
        """Test si une réservation passée lève bien l'erreur personnalisée."""
        # On prend la date d'hier
        hier = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # On s'attend à ce que le code lève l'erreur DateInvalideError
        with self.assertRaises(DateInvalideError):
            Reservation(1, 1, 1, hier, "12:00", 2, "Aucune")

if __name__ == '__main__':
    unittest.main()