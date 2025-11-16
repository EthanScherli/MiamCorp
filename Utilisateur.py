class Utilisateur:
    def __init__(self, nomUtilisateur, prenomUtilisateur, mdpUtilisateur, idUtilisateur):
        self.__nom = nomUtilisateur
        self.__prenom = prenomUtilisateur
        self.__mdp = mdpUtilisateur
        self.__id = idUtilisateur
        self.__permission = "user"

    @property
    def permission(self):
        return self.__permission

    @property 
    def mdp(self):
        return self.__mdp

    @property
    def id(self):
        return self.__id
