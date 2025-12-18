class Plat:
    def __init__(self, nom, prix, categorie):
        self.nom = nom
        self.prix = prix
        self.categorie = categorie

    def __str__(self):
        return f"[{self.categorie}] {self.nom} : {self.prix}€"

def get_menu_du_jour():
    """Crée et retourne la liste des plats du jour."""
    liste_plats = [
        Plat("Croquettes de Crevettes", 12.00, "Entrée"),
        Plat("Carpaccio de Bœuf", 14.50, "Entrée"),
        Plat("Carbonnade Flamande", 18.50, "Plat"),
        Plat("Pavé de Saumon", 19.50, "Plat"),
        Plat("Dame Blanche", 8.50, "Dessert"),
        Plat("Mousse au Chocolat", 6.00, "Dessert"),
        Plat("Jupiler", 3.00, "Boisson"),
        Plat("Coca-Cola", 2.50, "Boisson")
    ]
    return liste_plats