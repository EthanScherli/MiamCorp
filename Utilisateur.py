import hashlib #pour hasher le mdp
class Utilisateur:
    def __init__(self, nomUtilisateur, prenomUtilisateur, mdpUtilisateur, idUtilisateur):
        self.__nom = nomUtilisateur
        self.__prenom = prenomUtilisateur
        self.__mdp = mdpUtilisateur
        self.__mdp_hash = self._hasher_mdp(mdpUtilisateur)
        self.__id = idUtilisateur
        self.__permission = "user"
        
    def _hasher_mdp(self, mdp):
        # Hashage simple (SHA-256)
        return hashlib.sha256(mdp.encode()).hexdigest()

    def verifier_mdp(self, mdp_a_verifier):
        # On hash l'entrée et on compare avec le hash stocké
        return self._hasher_mdp(mdp_a_verifier) == self.__mdp_hash
        
    @property
    def permission(self):
        return self.__permission

    @property 
    def mdp(self):
        return self.__mdp

    @property
    def id(self):
        return self.__id
