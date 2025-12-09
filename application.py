from Reservations import Reservation
import sqlite3

DB_PATH = "Gaston_db.sqlite"

class Application:

    def __init__(self, utilisateurConnecte):
        self.utilisateur = utilisateurConnecte

    def run(self):
        print(f"\nConnexion réussie pour {self.utilisateur.nom} !\n")
        self.menu_principal()

    def menu_principal(self):
        while True:
            print("\n--- MENU ---")
            print("1. Voir mes réservations")
            print("2. Ajouter une réservation")
            print("3. Supprimer une réservation")
            print("4. Voir les tables disponibles")
            print("5. Se déconnecter")

            choix = input("Choisissez une option [1-5] >> ")

            if choix == "1":
                self.voirReservation()
            elif choix == "2":
                self.saisirReservation()
            elif choix == "3":
                self.supprimerReservation()
            elif choix == "4":
                self.voirTables()
            elif choix == "5":
                self.deconnecterUtilisateur()
                break
            else:
                print("Option invalide. Veuillez réessayer.")

    def saisirReservation(self):
        self.voirTables()
        id_table = input("Entrez l'ID de la table que vous souhaitez réserver >> ")
        date = input("Entrez la date de la réservation (YYYY-MM-DD) >> ")
        heure = input("Entrez l'heure de la réservation (HH:MM) >> ")
        nbr_pers = input("Nombre de personnes >> ")
        pref = input("Préférences du client >> ")
        self.ajouterReservation(id_table, date, heure, nbr_pers, pref)

    def ajouterReservation(self, id_table, date, heure, nbr_pers, pref):
        try:
            connexion = sqlite3.connect(DB_PATH)
            curseur = connexion.cursor()
            curseur.execute("""
                INSERT INTO reservations (id_util, id_table, date, heure, nbr_pers, pref)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.utilisateur.id_util, id_table, date, heure, nbr_pers, pref))
            connexion.commit()
            id_resa = curseur.lastrowid
            nouvelle_resa = Reservation(id_resa, self.utilisateur.id_util, id_table, date, heure, nbr_pers, pref)
            connexion.close()
            print(f"Réservation ajoutée : {nouvelle_resa}")
        except Exception as e:
            print("Erreur lors de l'ajout de réservation :", e)

    def voirReservation(self):
        try:
            connexion = sqlite3.connect(DB_PATH)
            curseur = connexion.cursor()
            curseur.execute("SELECT * FROM reservations WHERE id_util = ?", (self.utilisateur.id_util,))
            lignes = curseur.fetchall()
            if not lignes:
                print("Vous n'avez aucune réservation.")
            else:
                for ligne in lignes:
                    resa = Reservation(*ligne)
                    print(resa)
            connexion.close()
        except Exception as e:
            print("Erreur lors de la lecture des réservations :", e)

    def supprimerReservation(self):
        id_resa = input("Entrez l'ID de la réservation à supprimer >> ")
        try:
            connexion = sqlite3.connect(DB_PATH)
            curseur = connexion.cursor()
            curseur.execute("SELECT * FROM reservations WHERE id_resa = ? AND id_util = ?", 
                            (id_resa, self.utilisateur.id_util))
            ligne = curseur.fetchone()
            if ligne:
                curseur.execute("DELETE FROM reservations WHERE id_resa = ?", (id_resa,))
                connexion.commit()
                print(f"Réservation {id_resa} supprimée.")
            else:
                print("Aucune réservation correspondante.")
            connexion.close()
        except Exception as e:
            print("Erreur lors de la suppression :", e)

    def voirTables(self):
        try:
            connexion = sqlite3.connect(DB_PATH)
            curseur = connexion.cursor()
            curseur.execute("SELECT * FROM tabless")
            lignes = curseur.fetchall()
            if not lignes:
                print("Aucune table disponible.")
            else:
                print("\n--- Tables disponibles ---")
                for ligne in lignes:
                    print(f"ID: {ligne[0]}, Capacité: {ligne[1]}, Salle: {ligne[2]}")
            connexion.close()
        except Exception as e:
            print("Erreur lors de la lecture des tables :", e)

    @staticmethod
    def deconnecterUtilisateur():
        from main import Main
        Main.utilisateurConnecte = None
        print("Vous êtes maintenant déconnecté.")
