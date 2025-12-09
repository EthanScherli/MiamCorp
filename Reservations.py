import sqlite3
from datetime import datetime

DB_PATH = "Gaston_db.sqlite"

class Reservation:
    def __init__(self, id_resa, id_util, id_table, date, heure, nbr_pers, pref):
        self.id_resa = id_resa
        self.id_util = id_util
        self.id_table = id_table
        self.date = date
        self.heure = heure
        self.nbr_pers = nbr_pers
        self.pref = pref

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
