from application import Application
from Utilisateur import Utilisateur

class Main:
    liste_utilisateurs = []
    utilisateurConnecte = None

    @staticmethod
    def creerCompteUtilisateur():
        nom = input("veuillez entrez votre nom >> ")
        prenom = input("veuillez entrez votre prenom >> ")
        mdp = input("veuillez entrez un mot de passe >> ")
        idUtilisateur = input("veuillez entrez un identifiant >> ")

        user = Utilisateur(nom, prenom, mdp, idUtilisateur)
        Main.liste_utilisateurs.append(user)
        print("Utilisateur créé")
        for i in Main.liste_utilisateurs:
            print(i)

        return user

    @staticmethod
    def connecterUtilisateur():
        idOk = False
        mdpOk = False
        positionUtilisateur = 0

        while idOk == False:
            positionUtilisateur = 0
            identifiant = input("entrez votre identifiant >> ")
            for i in Main.liste_utilisateurs:
                if i.id == identifiant:
                    print("identifiant trouvé")
                    idOk = True
                    break
                else:
                    positionUtilisateur = positionUtilisateur + 1

            if idOk == False:
                print("identifiant introuvable")

        while mdpOk == False:
            mdp = input("entrez votre mot de passe >> ")
            if mdp == Main.liste_utilisateurs[positionUtilisateur].mdp:
                print("connexion Réussie")
                Main.utilisateurConnecte = Main.liste_utilisateurs[positionUtilisateur]
                return identifiant
            else:
                print("mot de passe incorrect")

    @staticmethod
    def application():
        choixCorrect = False
        choix = None

        while choixCorrect == False:
            choix = input("Voulez vous vous connecter ou créer un comptre [co/cr] >> ")
            if choix == "co":
                app = Application(Main.connecterUtilisateur())
                choixCorrect = True

            elif choix == "cr":
                Main.creerCompteUtilisateur()
                choixCorrect = True
                Main.application()

            else:
                print("---ERREUR--- Veuillez entrez une valeur correct")

appli = Main()
appli.application()
