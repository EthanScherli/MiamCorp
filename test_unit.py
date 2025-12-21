import pytest
from unittest.mock import MagicMock, patch
from interface import FenetreConnexion, FenetreCreationCompte
from Utilisateur import *

# Utilisation de mock pour imiter un utilisateur sans devoir ouvrir Tkinter
class UtilisateurTest:
    def __init__(self, email, mdp):
        self.email = email
        self._mdp = mdp

    def verifier_mdp(self, mdp):
        """
        PRE:
            - mdp est une chaîne
        POST:
            - retourne True si mdp correspond à _mdp
            - False sinon
        """
        return self._mdp == mdp


def test_connexion_reussie():
    
    """
    PRE:
        - FenetreConnexion initialisée avec root et app_gui mockés
        - UtilisateurTest simulant un utilisateur existant
    POST:
        - app_gui.utilisateur est mis à jour
        - app_gui.afficher_menu est appelé
    """
    
    root = MagicMock()
    app_gui = MagicMock()

    fenetre = FenetreConnexion(root, app_gui)

    # Simulation saisie utilisateur
    fenetre.email.get = MagicMock(return_value="test@mail.com")
    fenetre.mdp.get = MagicMock(return_value="1234")

    fake_user = UtilisateurTest("test@mail.com", "1234")

    # Mock de Main utilisé DANS interface.py
    with patch("interface.Main") as MockMain:
        MockMain.liste_utilisateurs = [fake_user]
        MockMain.chargerUtilisateurs = MagicMock()

        fenetre.connexion()

        # Assertions
        assert app_gui.utilisateur == fake_user
        app_gui.afficher_menu.assert_called_once()


def test_creation_compte_champs_vides():
    """
  PRE:
    - FenetreCreationCompte initialisée avec root et app_gui mockés
    - Tous les champs sauf mdp et role sont vides
  POST:
    - messagebox.showerror est appelé avec le bon message
    """
    root = MagicMock()
    app_gui = MagicMock()

    fenetre = FenetreCreationCompte(root, app_gui)

    # Champs simulés
    fenetre.nom.get = MagicMock(return_value="")
    fenetre.prenom.get = MagicMock(return_value="")
    fenetre.email.get = MagicMock(return_value="")
    fenetre.mdp.get = MagicMock(return_value="1234")
    fenetre.role.get = MagicMock(return_value="client")

    # Mock d'erreur
    with patch("interface.messagebox.showerror") as mock_error:
        fenetre.creer_compte()

        mock_error.assert_called_once_with(
            "Erreur", "Veuillez remplir tous les champs"
        )

def test_verifier_mdp():
    """
    PRE:
        - Utilisateur avec mdp stocké
        - mdp à tester
    POST:
        - retourne True si mdp correct
        - False sinon
    """
    u = Utilisateur("Bob", "Martin", "bob@mail.com", "abcd", "client")
    assert u.verifier_mdp("abcd") is True
    assert u.verifier_mdp("wrong") is False

def test_str_utilisateur():
    """
    PRE:
        - Utilisateur avec nom, prenom, email et role
    POST:
        - retourne une chaîne contenant nom, prenom, email et role
    """
    u = Utilisateur("Carla", "Lopez", "carla@mail.com", "pass", "admin")
    result = str(u)
    assert "Carla Lopez" in result
    assert "carla@mail.com" in result
    assert "admin" in result

def test_changement_nom():
    """
    PRE:
        - Utilisateur existant
        - nouvelle valeur pour nom
    POST:
        - nom de l'utilisateur mis à jour
    """
    u = Utilisateur("David", "Martin", "david@mail.com", "pass", "client")
    u.valeurNom = "Durand" 
    assert u.nom == "Durand"

def test_emails_majuscule():
    """
    PRE:
        - liste d'objets Utilisateur avec emails valides
    POST:
        - retourne une liste avec tous les emails en majuscules
        - aucun effet de bord sur les objets originaux
    """
    utilisateurs = [
        Utilisateur("Nom1", "Prenom1", "a@mail.com", "123", "client"),
        Utilisateur("Nom2", "Prenom2", "b@mail.com", "456", "admin")
    ]
    emails_upper = list(map(lambda u: u.email.upper(), utilisateurs))
    assert emails_upper == ["A@MAIL.COM", "B@MAIL.COM"]