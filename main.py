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
    def chargerUtilisateurs():
        Main.curseur.execute("SELECT id_util, nom, prenom, email, mdp, role FROM utilisateurs")
        lignes = Main.curseur.fetchall()
        Main.liste_utilisateurs.clear()
        for id_util, nom, prenom, email, mdp, role in lignes:
            user = Utilisateur(nom, prenom, email, mdp, role, id_util=id_util)
            Main.liste_utilisateurs.append(user)

    @staticmethod
    def creerCompteUtilisateur():
        nom = input("veuillez entrez votre nom >> ")
        prenom = input("veuillez entrez votre prenom >> ")
        email = input("veuillez entrez votre email >> ")
        mdp = input("veuillez entrez un mot de passe >> ")
        role = input("role de l'utilisateur (admin/client/autre) >> ")

        Main.curseur.execute(
            "INSERT INTO utilisateurs (nom, prenom, email, mdp, role) VALUES (?, ?, ?, ?, ?)",
            (nom, prenom, email, mdp, role)
        )
        Main.connexion.commit()
        Main.chargerUtilisateurs()
        print("Utilisateur créé :")
        for i in Main.liste_utilisateurs:
            print(i)

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
