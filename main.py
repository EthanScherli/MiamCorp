from application import Application
from Utilisateur import Utilisateur
import sqlite3

DB_PATH = "Gaston_db.sqlite"

class Main:
    liste_utilisateurs = []
    utilisateurConnecte = None

    connexion = sqlite3.connect(DB_PATH)
    curseur = connexion.cursor()

    @staticmethod
    def initialiser_bdd():
        """Crée les tables si elles n'existent pas encore, au cas où"""
        # 1. Table Utilisateurs
        Main.curseur.execute("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id_util INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            prenom TEXT,
            email TEXT UNIQUE,
            mdp TEXT,
            role TEXT
        )
        """)
        
        # 2. Table Reservations
        Main.curseur.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id_resa INTEGER PRIMARY KEY AUTOINCREMENT,
            id_util INTEGER,
            id_table INTEGER,
            date TEXT,
            heure TEXT,
            nbr_pers INTEGER,
            pref TEXT
        )
        """)

        # 3. Table Tables (tabless)
        Main.curseur.execute("""
        CREATE TABLE IF NOT EXISTS tabless (
            id_table INTEGER PRIMARY KEY AUTOINCREMENT,
            capacite INTEGER,
            salle INTEGER
        )
        """)
        
        # On sauvegarde les changements
        Main.connexion.commit()

        # (Optionnel) On crée quelques tables de restaurant par défaut si la table est vide
        Main.curseur.execute("SELECT count(*) FROM tabless")
        if Main.curseur.fetchone()[0] == 0:
            print("Création des tables du restaurant par défaut...")
            tables_defaut = [
                (4, 1), (4, 1), (2, 1), (6, 2), (4, 2) 
            ]
            Main.curseur.executemany("INSERT INTO tabless (capacite, salle) VALUES (?, ?)", tables_defaut)
            Main.connexion.commit()


    @staticmethod
    def chargerUtilisateurs():
        try:
            Main.curseur.execute(
                "SELECT id_util, nom, prenom, email, mdp, role FROM utilisateurs"
            )
            lignes = Main.curseur.fetchall()
        except sqlite3.OperationalError:
            return

        Main.liste_utilisateurs.clear()

        for id_util, nom, prenom, email, mdp, role in lignes:
            try:
                #  CORRECTION ICI
                if role is None:
                    role = "client"

                user = Utilisateur(nom, prenom, email, mdp, role, id_util=id_util)
                Main.liste_utilisateurs.append(user)

            except ValueError:
                print(f"ATTENTION: Utilisateur ignoré (données invalides en BDD) : {email}")
                continue

    @staticmethod
    def creerCompteUtilisateur():
        nom = input("veuillez entrez votre nom >> ").strip()
        prenom = input("veuillez entrez votre prenom >> ").strip()
        email = input("veuillez entrez votre email >> ").strip()
        mdp = input("veuillez entrez un mot de passe >> ").strip()

        if not nom or not prenom or not email or not mdp:
            print("Erreur : Tous les champs doivent être remplis.")
            return

        #  rôle par défaut
        role = "client"

        #  création de l'objet Utilisateur
        utilisateur = Utilisateur(nom, prenom, email, mdp, role)

        try:
            Main.curseur.execute(
                "INSERT INTO utilisateurs (nom, prenom, email, mdp, role) VALUES (?, ?, ?, ?, ?)",
                (
                    utilisateur.nom,
                    utilisateur.prenom,
                    utilisateur.email,
                    utilisateur.mdp,
                    utilisateur.role
                )
            )

            Main.connexion.commit()
            Main.chargerUtilisateurs()

            print("Utilisateur créé avec succès (rôle : client).")

        except sqlite3.IntegrityError:
            print("Erreur : Cet email est déjà utilisé.")

        except Exception as e:
            print(f"Erreur inattendue : {e}")

    @staticmethod
    def connecterUtilisateur():
        idOk = False
        positionUtilisateur = 0

        while not idOk:
            email = input("entrez votre email >> ")
            for i in Main.liste_utilisateurs:
                if i.email == email:
                    print("email trouvé")
                    idOk = True
                    break
                positionUtilisateur += 1
            if not idOk:
                print("email introuvable")

        mdpOk = False
        while not mdpOk:
            mdp = input("entrez votre mot de passe >> ")
            if Main.liste_utilisateurs[positionUtilisateur].verifier_mdp(mdp):
                Main.utilisateurConnecte = Main.liste_utilisateurs[positionUtilisateur]
                return Main.utilisateurConnecte
            else:
                print("mot de passe incorrect")

    @staticmethod
    def application():
        Main.initialiser_bdd() # On crée les tables AVANT de charger quoi que ce soit !!!
        Main.chargerUtilisateurs()
        
        while True:
            choix = input("Voulez vous vous connecter ou créer un compte [co/cr] >> ")
            if choix == "co":
                app = Application(Main.connecterUtilisateur())
                app.run()
                break
            elif choix == "cr":
                Main.creerCompteUtilisateur()
            else:
                print("---ERREUR--- Veuillez entrer une valeur correcte")

if __name__ == "__main__":
    Main.application()
