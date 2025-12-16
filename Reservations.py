import sqlite3
from datetime import datetime

DB_PATH = "Gaston_db.sqlite"

class DateInvalideError(Exception):
    pass
    
class Reservation:
    def __init__(self, id_resa, id_util, id_table, date, heure, nbr_pers, pref):
        self.id_resa = id_resa
        self.id_util = id_util
        self.id_table = id_table
        self.date = date
        self.heure = heure
        self.nbr_pers = nbr_pers
        self.pref = pref
        
    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise DateInvalideError("Format de date invalide (attendu: YYYY-MM-DD)")

        if date_obj < datetime.now().date():
            raise DateInvalideError(f"Impossible de réserver dans le passé ({date_str})")
        
        self._date = date_str
    
    def suppr_resa(self):
        try:
            connexion = sqlite3.connect(DB_PATH)
            curseur = connexion.cursor()
            curseur.execute("DELETE FROM reservations WHERE id_resa = ?", (self.id_resa,))
            connexion.commit()
            connexion.close()
            print(f"Réservation {self.id_resa} supprimée.")
        except Exception as e:
            print("Erreur lors de la suppression:", e)

    def __str__(self):
        return (f"Réservation {self.id_resa} - Utilisateur: {self.id_util}, Table: {self.id_table}, "
                f"Date: {self.date}, Heure: {self.heure}, Pers: {self.nbr_pers}, Préf: {self.pref}")
