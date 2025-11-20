from Reservation import Reservation

class Application : #construction de base de la classe application
    def __init__(self,utilisateurConnecte):
        self.__utilisateur = utilisateurConnecte 

    @property
    def utilisateur(self):
        return self.__utilisateur

    

    