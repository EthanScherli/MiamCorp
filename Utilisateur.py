class Utilisateur:
    def __init__(self, nom, prenom, email, mdp, role, id_util=None):
        self.id_util = id_util  # optionnel, récupéré depuis la DB
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mdp = mdp
        self.role = role

    def verifier_mdp(self, mdp_a_verifier):
        return self.mdp == mdp_a_verifier

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.email}) - role: {self.role}"
