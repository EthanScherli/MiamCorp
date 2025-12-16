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
        return self._mdp == mdp


def test_connexion_reussie():
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
def test_email_valide_et_invalide():
    u = Utilisateur("Alice", "Dupont", "alice@mail.com", "1234", "admin")
    assert u.email == "alice@mail.com"

    with pytest.raises(ValueError):
        u.email = "mauvais_email"

def test_verifier_mdp():
    u = Utilisateur("Bob", "Martin", "bob@mail.com", "abcd", "client")
    assert u.verifier_mdp("abcd") is True
    assert u.verifier_mdp("wrong") is False

def test_email_valide_et_invalide():
    u = Utilisateur("Alice", "Dupont", "alice@mail.com", "1234", "admin")
    assert u.email == "alice@mail.com"
    with pytest.raises(ValueError):
        u.email = "mauvais_email"

def test_verifier_mdp():
    u = Utilisateur("Bob", "Martin", "bob@mail.com", "abcd", "client")
    assert u.verifier_mdp("abcd") is True
    assert u.verifier_mdp("wrong") is False

def test_str_utilisateur():
    u = Utilisateur("Carla", "Lopez", "carla@mail.com", "pass", "admin")
    result = str(u)
    assert "Carla Lopez" in result
    assert "carla@mail.com" in result
    assert "admin" in result

def test_changement_nom():
    u = Utilisateur("David", "Martin", "david@mail.com", "pass", "client")
    u.valeurNom = "Durand" 
    assert u.nom == "Durand"