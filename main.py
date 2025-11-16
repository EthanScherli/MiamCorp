from application import Application
from Utilisateur import Utilisateur

liste_utilisateurs = []
utilisateurConnecte=None
choixCorrect=False

def creerCompteUtilisateur():
    nom=input("veuillez entrez votre nom")
    prenom=input("veuillez entrez votre prenom")
    mdp=input("veuillez entrez un mot de passe")
    idUtilisateur=input("veuillez entrez un identifiant")
    
    user = Utilisateur(nom, prenom, mdp, idUtilisateur)
    liste_utilisateurs.append(user)
    
    return user

def connecterUtilisateur():
    pass

def application():
    choix=None
    while choixCorrect ==  False:
        choix=input("Voulez vous vous connecter ou créer un comptre [co/cr]")
        if choix =="co":
            connecterUtilisateur()
            choixCorrect == True
        elif choix =="cr":
            creerCompteUtilisateur() 
            choixCorrect ==True
        else:
            print("---ERREUR--- Veuillez entrez une valeur correct")
