from Reservations import Reservation, DateInvalideError
import sqlite3
import functools
import datetime
from Menu import get_menu_du_jour

DB_PATH = "Gaston_db.sqlite"

def recuperer_menu(self):
    return get_menu_du_jour()

def log_action(func):
    """Décorateur qui log l'exécution d'une méthode dans un fichier."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            # Si ok, on log le succès
            with open("logs_activite.txt", "a", encoding="utf-8") as f:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[LOG] {timestamp} - Action: {func.__name__} - Status: Succès\n")
            return result
        except Exception as e:
            # Si erreur, on log l'exception
            with open("logs_activite.txt", "a", encoding="utf-8") as f:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[LOG] {timestamp} - Action: {func.__name__} - Erreur: {e}\n")
            raise e # On relance l'erreur
    return wrapper

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

        try:
            self.ajouterReservation(id_table, date, heure, nbr_pers, pref)
        except DateInvalideError as e:
            print(f"--- ERREUR DATE : {e} ---")
        except Exception as e:
            print(f"--- ERREUR : {e} ---")

    @log_action
    def ajouterReservation(self, id_table, date, heure, nbr_pers, pref):
        try:
            # 1. On crée l'objet avec None pour l'ID (car on ne l'a pas encore).
            # C'est ici que la date est vérifiée. Si elle est passée, ça plante et s'arrête là.
            nouvelle_resa = Reservation(None, self.utilisateur.id_util, id_table, date, heure, nbr_pers, pref)

            connexion = sqlite3.connect(DB_PATH)
            curseur = connexion.cursor()
            
            # 2. Vérification disponibilité
            curseur.execute("""
                SELECT * FROM reservations
                WHERE id_table = ? AND date = ? AND heure = ?
            """, (id_table, date, heure))
            
            if curseur.fetchone():
                connexion.close()
                # On lève une erreur pour l'afficher dans l'interface
                raise Exception("Cette table est déjà réservée à ce créneau.")
            
            # 3. Insertion dans la base de données
            curseur.execute("""
                INSERT INTO reservations (id_util, id_table, date, heure, nbr_pers, pref)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.utilisateur.id_util, id_table, date, heure, nbr_pers, pref))
            
            connexion.commit()
            
            # 4. Maintenant on récupère le vrai ID généré par la base de données
            id_genere = curseur.lastrowid
            nouvelle_resa.id_resa = id_genere
            
            connexion.close()
            print(f"Réservation ajoutée avec succès : ID {id_genere}")

        # Gestion des erreurs
        except DateInvalideError as e:
            # On relance l'erreur pour que l'interface puisse afficher la pop-up
            raise e 
        except Exception as e:
            # Pareil
            raise e
        
    def voirReservation(self):
            try:
                connexion = sqlite3.connect(DB_PATH)
                curseur = connexion.cursor()
                if self.utilisateur.role == "admin":
                    curseur.execute("SELECT * FROM reservations")
                else:
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
        

    @log_action
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

    def get_tables_pour_capacite(self, nbr_personnes_min):
        """Retourne les tables ayant une capacité suffisante (utilisation de filter/lambda)."""
        try:
            connexion = sqlite3.connect(DB_PATH)
            curseur = connexion.cursor()
            curseur.execute("SELECT * FROM tabless")
            toutes_les_tables = curseur.fetchall()
            connexion.close()
            tables_ok = list(filter(lambda x: x[1] >= int(nbr_personnes_min), toutes_les_tables))
            return tables_ok
        except Exception as e:
            print(f"Erreur lors du filtrage des tables : {e}")
            return []

    @staticmethod
    def deconnecterUtilisateur():
        from main import Main
        Main.utilisateurConnecte = None
        print("Vous êtes maintenant déconnecté.")
