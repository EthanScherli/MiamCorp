from Reservations import Reservation
from main import Main

class Application : #construction de base de la classe application

    listeReservation=[]

    def __init__(self,utilisateurConnecte):
        self.__utilisateur = utilisateurConnecte 

    @property
    def utilisateur(self):
        return self.__utilisateur

    @staticmethod
    def deconnecterUtilisateur():
        Main.utilisateurConnecte=None
        print("vous êtes maintenant déconnecter")
        Main.application()

    @staticmethod
    def ajouterReservation():
        pass

    @staticmethod
    def voirReservation():
        pass


    