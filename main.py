from application import Application #import des objet pour pouvoir les utiliser dans cette classe
from Utilisateur import Utilisateur

liste_utilisateurs = []#liste des utilisateurs qui ont créer un compte
utilisateurConnecte=None
choixCorrect=False #variable permetant de savoir si le choix de l'utilisateur est correct

def creerCompteUtilisateur():#fonction permettant de créer un utilisateur 
    nom=input("veuillez entrez votre nom")
    prenom=input("veuillez entrez votre prenom")
    mdp=input("veuillez entrez un mot de passe")
    idUtilisateur=input("veuillez entrez un identifiant")
    
    user = Utilisateur(nom, prenom, mdp, idUtilisateur)
    liste_utilisateurs.append(user)
    
    return user

def connecterUtilisateur():#fonction permettant de connecter un utilisateur
    idOk=False
    mdpOk=False
    positionUtilisateur=0
    while idOk == False:#boucle permettant de voir si l'identifiant est disponible dans la liste des utilisateurs créer
        positionUtilisateur=0
        identifiant=input("entrez votre identifiant")
        for i in liste_utilisateurs:
            if i[3]==identifiant:
                print("identifiant trouvé")
                idOk=True
                break
            else:
                positionUtilisateur= positionUtilisateur+1
            
        if idOk==False:
            print("identifiant introuvable")
    
    while mdpOk == False:#boucle permettant de voir si le mdp correspond à l'identifiant utilisé
        mdp=input("entrez votre mot de passe")
        if mdp==liste_utilisateurs[positionUtilisateur][2]:
            print("connexion Réussie")
            return identifiant
        else:
            print("mot de passe incorrect")
        


def application():#fonction faisant tourner l'application 
    choix=None
    while choixCorrect ==  False:
        choix=input("Voulez vous vous connecter ou créer un comptre [co/cr]")
        if choix =="co":
            utilisateurConnecte=connecterUtilisateur()
            choixCorrect == True
        elif choix =="cr":
            creerCompteUtilisateur() 
            choixCorrect ==True
            application()
        else:
            print("---ERREUR--- Veuillez entrez une valeur correct")
