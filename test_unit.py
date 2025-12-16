import pytest
from unittest.mock import MagicMock, patch
from interface import FenetreConnexion, FenetreCreationCompte

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

    # Mock de la popup d'erreur
    with patch("interface.messagebox.showerror") as mock_error:
        fenetre.creer_compte()

        mock_error.assert_called_once_with(
            "Erreur", "Veuillez remplir tous les champs"
        )
