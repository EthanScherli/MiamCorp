import re

class Utilisateur:
    def __init__(self, nom, prenom, email, mdp, role, id_util=None):
        self.id_util = id_util  # optionnel, récupéré depuis la DB
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mdp = mdp
        self.role = role

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email):
        new_email = new_email.strip()
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9-]{2,}$'
        if not re.match(regex, new_email):
            raise ValueError(f"Format d'email invalide : {new_email}")
        self._email = new_email

    @property
    def valeurNom(self):
        return self.nom
    
    @valeurNom.setter
    def valeurNom(self,newNom):
        self.nom=newNom

    def verifier_mdp(self, mdp_a_verifier):
        return self.mdp == mdp_a_verifier

    def __str__(self):
        try:
            return f"{self.nom} {self.prenom} ({self.email}) - role: {self.role}"
        except Exception as e:
            return f"Utilisateur invalide ({e})"