import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from main import Main
from application import Application
import sqlite3
from Utilisateur import Utilisateur
from Menu import get_menu_du_jour

COULEUR_FOND = "#f4e9d8"       # Beige chaleureux
COULEUR_ACCENT = "#c97b5b"     # Terracotta
COULEUR_BOUTON = "#d89c81"     # Brun clair

DB_PATH = "Gaston_db.sqlite"


class FenetreConnexion(tk.Frame):
    def __init__(self, root, app_gui):
        super().__init__(root, bg=COULEUR_FOND)
        self.app_gui = app_gui

        tk.Label(self, text="Connexion", font=("Arial", 22, "bold"),
                 bg=COULEUR_FOND, fg=COULEUR_ACCENT).pack(pady=20)

        # Champs email + mot de passe
        self.email = tk.Entry(self, width=30)
        self.mdp = tk.Entry(self, width=30, show="*")

        tk.Label(self, text="Email :", bg=COULEUR_FOND).pack()
        self.email.pack()

        tk.Label(self, text="Mot de passe :", bg=COULEUR_FOND).pack()
        self.mdp.pack()

        # Boutons
        tk.Button(self, text="Se connecter",
                  bg=COULEUR_BOUTON, command=self.connexion).pack(pady=15)

        tk.Button(self, text="Créer un compte",
                  bg=COULEUR_BOUTON, command=self.goto_creation).pack()

    def connexion(self):
        Main.chargerUtilisateurs()
        email = self.email.get().strip()
        mdp = self.mdp.get().strip()

        for u in Main.liste_utilisateurs:
            if u.email == email and u.verifier_mdp(mdp):
                self.app_gui.utilisateur = u
                self.app_gui.afficher_menu()
                return

        messagebox.showerror("Erreur", "Email ou mot de passe incorrect.")

    def goto_creation(self):
        self.pack_forget()
        self.app_gui.afficher_creation()


class FenetreCreationCompte(tk.Frame):
    def __init__(self, root, app_gui):
        super().__init__(root, bg=COULEUR_FOND)
        self.app_gui = app_gui

        tk.Label(self, text="Créer un compte",
                 font=("Arial", 22, "bold"),
                 bg=COULEUR_FOND, fg=COULEUR_ACCENT).pack(pady=20)

        self.nom = tk.Entry(self, width=30)
        self.prenom = tk.Entry(self, width=30)
        self.email = tk.Entry(self, width=30)
        self.mdp = tk.Entry(self, width=30)
        self.role = tk.Entry(self, width=30)

        for label, field in [("Nom", self.nom),
                             ("Prénom", self.prenom),
                             ("Email", self.email),
                             ("Mot de passe", self.mdp),
                             ("Rôle (admin/client)", self.role)]:
            tk.Label(self, text=label, bg=COULEUR_FOND).pack()
            field.pack()

        tk.Button(self, text="Créer",
                  bg=COULEUR_BOUTON, command=self.creer_compte).pack(pady=15)

        tk.Button(self, text="Retour",
                  bg=COULEUR_BOUTON,
                  command=self.retour).pack()

    def creer_compte(self):
        nom = self.nom.get().strip()
        prenom = self.prenom.get().strip()
        email = self.email.get().strip()
        mdp = self.mdp.get().strip()
        role = self.role.get().strip()

        if nom == "" or prenom == "" or email == "":
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        try:
            # 1. On crée un objet "temporaire" juste pour tester si l'email est valide
            # Si l'email est mauvais, ça plante ICI et ça va direct au 'except ValueError'
            test_validite = Utilisateur(nom, prenom, email, mdp, role)

            # 2. Si on arrive ici, c'est que l'email est bon. On peut insérer en BDD.
            Main.curseur.execute(
                "INSERT INTO utilisateurs (nom, prenom, email, mdp, role) VALUES (?, ?, ?, ?, ?)",
                (nom, prenom, email, mdp, role)
            )
            Main.connexion.commit()
            
            # 3. On recharge la liste
            Main.chargerUtilisateurs()
            
            messagebox.showinfo("Succès", "Compte créé ! Vous pouvez vous connecter.")
            self.retour()

        except ValueError as e:
            messagebox.showerror("Format Invalide", str(e))

        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Cette adresse email est déjà utilisée.")
            
        except Exception as e:
            messagebox.showerror("Erreur DB", f"Impossible de créer le compte : {e}")

    def retour(self):
        self.pack_forget()
        self.app_gui.afficher_connexion()


class FenetreMenu(tk.Frame):
    def __init__(self, root, app_gui):
        super().__init__(root, bg=COULEUR_FOND)
        self.app_gui = app_gui

        tk.Label(self, text="Menu principal",
                 font=("Arial", 22, "bold"),
                 bg=COULEUR_FOND, fg=COULEUR_ACCENT).pack(pady=20)

        for texte, action in [
            ("Voir la Carte 🍽️", self.app_gui.voir_la_carte),
            ("Voir mes réservations", self.app_gui.afficher_reservations),
            ("Ajouter une réservation", self.app_gui.afficher_ajout_resa),
            ("Supprimer une réservation", self.app_gui.afficher_suppr_resa),
            ("Voir les tables", self.app_gui.afficher_tables),
            ("Se déconnecter", self.app_gui.deconnexion)
        ]:
            tk.Button(self, text=texte, bg=COULEUR_BOUTON,
                      width=30, command=action).pack(pady=8)


class InterfaceGraphique:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gaston - Réservations Restaurant")
        self.root.geometry("980x520")
        self.root.config(bg=COULEUR_FOND)

        self.utilisateur = None
        self.frame = None

        self.afficher_connexion()

    # -----------------------
    # NOUVELLE MÉTHODE : Voir la Carte
    # -----------------------
    def voir_la_carte(self):
        # Création de la fenêtre Pop-up
        fenetre_menu = tk.Toplevel(self.root)
        fenetre_menu.title("Le Menu de Gaston")
        fenetre_menu.geometry("450x600")
        fenetre_menu.configure(bg="#2c3e50") # Fond sombre externe

        # --- Cadre style "Feuille de papier" ---
        feuille = tk.Frame(fenetre_menu, bg="#fffaf0", bd=10, relief="ridge")
        feuille.pack(expand=True, fill="both", padx=20, pady=20)

        # Titre sur la feuille
        lbl_titre = tk.Label(feuille, text="Menu du Jour", 
                             font=("Times New Roman", 26, "bold"), 
                             bg="#fffaf0", fg="#8b4513")
        lbl_titre.pack(pady=(15, 20))

        # Récupération des données depuis Menu.py (Utilisation)
        liste_plats = get_menu_du_jour()

        # Affichage des plats
        for plat in liste_plats:
            ligne = tk.Frame(feuille, bg="#fffaf0")
            ligne.pack(fill='x', pady=6, padx=15)
            
            # Nom du plat (gauche)
            tk.Label(ligne, text=f"• {plat.nom}", font=("Garamond", 13, "bold"), 
                     bg="#fffaf0", fg="#333").pack(side="left")
            
            # Prix (droite)
            tk.Label(ligne, text=f"{plat.prix:.2f} €", font=("Garamond", 13, "bold"), 
                     bg="#fffaf0", fg="#c0392b").pack(side="right")
            
            # Catégorie (petit en dessous)
            tk.Label(feuille, text=f"   ({plat.categorie})", font=("Arial", 9, "italic"), 
                     bg="#fffaf0", fg="#7f8c8d", anchor="w").pack(fill='x', padx=35, pady=(0, 2))

        # Bouton fermer en bas
        tk.Button(feuille, text="Fermer", command=fenetre_menu.destroy, 
                  bg="#dcdcdc", font=("Arial", 10)).pack(side="bottom", pady=20)

    # -----------------------
    # Plan interactif (version A, fidèle au croquis)
    # -----------------------
    def afficher_plan_resto(self, callback, date_init="", heure_init=""):
        """
        Ouvre une fenêtre avec le plan du restaurant (fidèle au croquis).
        - callback(id_table) est appelé lorsqu'une table disponible est sélectionnée.
        - date_init, heure_init : valeurs initiales optionnelles pour vérifier les réservations.
        """
        plan = tk.Toplevel(self.root)
        plan.title("Plan du restaurant - Choisissez une table")
        plan.geometry("1000x520")
        plan.config(bg=COULEUR_FOND)

        # Barre de contrôle (date / heure / vérifier)
        ctrl = tk.Frame(plan, bg=COULEUR_FOND)
        ctrl.pack(fill="x", padx=10, pady=6)

        tk.Label(ctrl, text="Date (YYYY-MM-DD) :", bg=COULEUR_FOND).pack(side="left")
        entry_date = tk.Entry(ctrl, width=12)
        entry_date.pack(side="left", padx=(4, 12))
        entry_date.insert(0, date_init)

        tk.Label(ctrl, text="Heure (HH:MM) :", bg=COULEUR_FOND).pack(side="left")
        entry_heure = tk.Entry(ctrl, width=8)
        entry_heure.pack(side="left", padx=(4, 12))
        entry_heure.insert(0, heure_init)

        info_label = tk.Label(ctrl, text="Cliquez sur une table libre pour la sélectionner.", bg=COULEUR_FOND)
        info_label.pack(side="left", padx=6)

        canvas = tk.Canvas(plan, width=980, height=420, bg="#000000", highlightthickness=0)  # noir fond comme croquis
        canvas.pack(padx=10, pady=(0, 10))

        # Définition des tables (id, x, y, w, h, forme) - positions approximatives fidèles au dessin
        tables = [
            # grande salle droite - top row rectangulaire (IDs 11,10,9,8,7)
            (11, 280, 60, 90, 50, "rect"),
            (10, 390, 60, 90, 50, "rect"),
            (9,  500, 60, 90, 50, "rect"),
            (8,  610, 60, 90, 50, "rect"),
            (7,  720, 60, 90, 50, "rect"),

            # middle right small squares column (IDs 5,6,3,4 from top to bottom)
            (5,  720, 150, 40, 40, "rect"),
            (6,  720, 210, 40, 40, "rect"),
            (3,  720, 270, 40, 40, "rect"),
            (4,  720, 330, 40, 40, "rect"),

            # round tables center bottom (IDs 1,2)
            (1,  320, 220, 130, 130, "oval"),
            (2,  480, 220, 130, 130, "oval"),

            # middle row rectangles (IDs 12,13,14 left-mid column)
            (12, 100, 100, 50, 80, "rect"),
            (13, 100, 220, 50, 80, "rect"),
            (14, 100, 330, 40, 40, "rect"),

            # left long vertical zone (IDs 15,16,17,18) - stacked small tables
            (15, 20, 320, 40, 40, "rect"),
            (16, 20, 240, 40, 40, "rect"),
            (17, 20, 160, 40, 40, "rect"),
            (18, 20, 50, 50, 80, "rect"),
        ]

        # mapping: canvas object id -> table id
        objets = {}
        label_objects = {}

        COLOR_AVAILABLE_FILL = "#f4e0cf"
        COLOR_RESERVED_FILL = "#e05858"  # red for reserved
        OUTLINE = "#ffffff"

        # Dessiner salles / murs (cadre et séparation) pour ressembler au croquis
        canvas.create_rectangle(10, 10, 970, 410, outline=OUTLINE, width=4)   # cadre général
        canvas.create_rectangle(10, 10, 200, 410, outline=OUTLINE, width=3)   # séparation gauche
        

        # Fonction pour dessiner toutes les tables (selon état réservé)
        def dessiner_tables(reserve_ids=set()):
            # supprimer anciens objets de tables (mais garder cadre)
            for obj in list(objets.keys()):
                try:
                    canvas.delete(obj)
                except:
                    pass
            objets.clear()
            for lbl in list(label_objects.keys()):
                try:
                    canvas.delete(label_objects[lbl])
                except:
                    pass
            label_objects.clear()

            for tid, x, y, w, h, shape in tables:
                fill_color = COLOR_RESERVED_FILL if tid in reserve_ids else COLOR_AVAILABLE_FILL
                if shape == "rect":
                    obj = canvas.create_rectangle(x, y, x + w, y + h, fill=fill_color, outline=OUTLINE, width=3)
                else:
                    obj = canvas.create_oval(x, y, x + w, y + h, fill=fill_color, outline=OUTLINE, width=3)
                # numéro au centre
                txt = canvas.create_text(x + w / 2, y + h / 2, text=str(tid), font=("Arial", 14, "bold"), fill="black")
                objets[obj] = tid
                label_objects[tid] = txt

        # Interroger la DB pour réservations à la date/heure donnée
        def get_reserved_tables(date_str, heure_str):
            reserved = set()
            if not date_str or not heure_str:
                return reserved
            try:
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute(
                    "SELECT id_table FROM reservations WHERE date = ? AND heure = ?",
                    (date_str, heure_str)
                )
                rows = cur.fetchall()
                reserved = {int(r[0]) for r in rows}
                conn.close()
            except Exception as e:
                messagebox.showerror("Erreur DB", f"Impossible de lire les réservations : {e}")
            return reserved

        # action du bouton "Vérifier"
        def verifier_action():
            date_val = entry_date.get().strip()
            heure_val = entry_heure.get().strip()
            if date_val == "" or heure_val == "":
                messagebox.showwarning("Champs vides", "Veuillez saisir la date et l'heure pour vérifier les réservations.")
                return
            reserved = get_reserved_tables(date_val, heure_val)
            dessiner_tables(reserved)

        # gestion du clic : si table réservée => avertir, sinon callback et fermer
        def on_clic(event):
            # récupérer l'objet le plus proche du clic
            found = canvas.find_closest(event.x, event.y)
            if not found:
                return
            obj = found[0]
            if obj not in objets:
                return
            tid = objets[obj]
            date_val = entry_date.get().strip()
            heure_val = entry_heure.get().strip()
            reserved = get_reserved_tables(date_val, heure_val) if date_val and heure_val else set()
            if tid in reserved:
                messagebox.showinfo("Table réservée", f"La table {tid} est déjà réservée à cette date/heure.")
                return
            # marque visuelle brève (pour confirmation)
            try:
                canvas.itemconfig(obj, fill="#8fd17f")  # vert temporaire
            except:
                pass
            # Appel du callback et fermeture
            callback(tid)
            plan.destroy()

        # lier le clic
        canvas.bind("<Button-1>", on_clic)

        # bouton vérifier
        btn_check = tk.Button(ctrl, text="Vérifier disponibilités", bg=COULEUR_BOUTON, command=verifier_action)
        btn_check.pack(side="right", padx=6)

        # Dessin initial : si date/heure fournis, on colore les réservées
        initial_reserved = get_reserved_tables(entry_date.get().strip(), entry_heure.get().strip())
        dessiner_tables(initial_reserved)

    # -----------------------
    # Fonctions d'affichage / actions
    # -----------------------
    def afficher_connexion(self):
        if self.frame:
            self.frame.pack_forget()
        self.frame = FenetreConnexion(self.root, self)
        self.frame.pack(fill="both", expand=True)

    def afficher_creation(self):
        if self.frame:
            self.frame.pack_forget()
        self.frame = FenetreCreationCompte(self.root, self)
        self.frame.pack(fill="both", expand=True)

    def afficher_menu(self):
        if self.frame:
            self.frame.pack_forget()
        self.frame = FenetreMenu(self.root, self)
        self.frame.pack(fill="both", expand=True)

    def afficher_tables(self):
        win = tk.Toplevel(self.root)
        win.title("Tables disponibles")
        win.config(bg=COULEUR_FOND)

        tree = ttk.Treeview(win, columns=("id", "cap", "salle"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("cap", text="Capacité")
        tree.heading("salle", text="Salle")
        tree.pack(fill="both", expand=True, padx=8, pady=8)

        connexion = sqlite3.connect(DB_PATH)
        curseur = connexion.cursor()
        try:
            curseur.execute("SELECT id_table, capacite, salle FROM tabless")
        except Exception:
            # fallback si colonnes différentes
            try:
                curseur.execute("SELECT * FROM tabless")
            except Exception as e:
                messagebox.showerror("Erreur DB", f"Impossible de lire les tables : {e}")
                connexion.close()
                return
        for t in curseur.fetchall():
            # afficher en fonction du nombre de colonnes récupérées
            if len(t) >= 3:
                tree.insert("", tk.END, values=(t[0], t[1], t[2]))
            elif len(t) == 2:
                tree.insert("", tk.END, values=(t[0], t[1], ""))
            else:
                tree.insert("", tk.END, values=(t[0], "", ""))
        connexion.close()

    def afficher_reservations(self):
        win = tk.Toplevel(self.root)
        win.title("Mes réservations")
        win.config(bg=COULEUR_FOND)

        tree = ttk.Treeview(win, columns=("id_table", "date", "heure", "id_resa"), show="headings")
        tree.heading("id_resa", text="ID Réservation")
        tree.heading("id_table", text="Table")
        tree.heading("date", text="Date")
        tree.heading("heure", text="Heure")
        tree.pack(fill="both", expand=True, padx=8, pady=8)

        connexion = sqlite3.connect(DB_PATH)
        curseur = connexion.cursor()
        try:
            curseur.execute("SELECT id_resa, id_table, date, heure FROM reservations WHERE id_util = ?", (self.utilisateur.id_util,))
            for row in curseur.fetchall():
                tree.insert("", tk.END, values=(row[1], row[2], row[3], row[0]))
        except Exception as e:
            messagebox.showerror("Erreur DB", f"Impossible de lire les réservations : {e}")
        connexion.close()

    def afficher_ajout_resa(self):
        win = tk.Toplevel(self.root)
        win.title("Ajouter réservation")
        win.geometry("420x420")
        win.config(bg=COULEUR_FOND)

        # Champs
        tk.Label(win, text="Date (YYYY-MM-DD)", bg=COULEUR_FOND).pack(pady=(10, 0))
        date_entry = tk.Entry(win)
        date_entry.pack()

        tk.Label(win, text="Heure (HH:MM)", bg=COULEUR_FOND).pack(pady=(8, 0))
        heure_entry = tk.Entry(win)
        heure_entry.pack()

        selected_table_var = tk.StringVar(value="Aucune")

        def ouvrir_plan():
            d = date_entry.get().strip()
            h = heure_entry.get().strip()

            def callback_choose(tid):
                selected_table_var.set(str(tid))
                bouton_table.config(text=f"Table choisie : {tid}")

            # ouverture du plan avec date/heure préremplis
            self.afficher_plan_resto(callback_choose, date_init=d, heure_init=h)

        bouton_table = tk.Button(win, text="Ouvrir le plan pour choisir une table",
                                 bg=COULEUR_BOUTON, command=ouvrir_plan)
        bouton_table.pack(pady=12)

        tk.Label(win, text="Table sélectionnée :", bg=COULEUR_FOND).pack()
        tk.Label(win, textvariable=selected_table_var, bg=COULEUR_FOND, font=("Arial", 12, "bold")).pack(pady=(0, 8))

        # autres champs
        tk.Label(win, text="Nombre de personnes", bg=COULEUR_FOND).pack()
        nbr_entry = tk.Entry(win)
        nbr_entry.pack()

        tk.Label(win, text="Préférences", bg=COULEUR_FOND).pack()
        pref_entry = tk.Entry(win)
        pref_entry.pack()

        def ajouter():
            id_table = selected_table_var.get()
            date_val = date_entry.get().strip()
            heure_val = heure_entry.get().strip()
            nbr = nbr_entry.get().strip()
            pref = pref_entry.get().strip()

            if id_table in ("", "Aucune"):
                messagebox.showerror("Erreur", "Veuillez choisir une table depuis le plan.")
                return
            if date_val == "" or heure_val == "":
                messagebox.showerror("Erreur", "Veuillez renseigner la date et l'heure.")
                return

            # Appel à ta logique (Application.ajouterReservation)
            try:
                app = Application(self.utilisateur)
                app.ajouterReservation(id_table, date_val, heure_val, nbr, pref)
                messagebox.showinfo("Succès", f"Réservation ajoutée pour la table {id_table}.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ajouter la réservation : {e}")

        tk.Button(win, text="Ajouter la réservation", bg=COULEUR_BOUTON, command=ajouter).pack(pady=16)

    def afficher_suppr_resa(self):
        win = tk.Toplevel(self.root)
        win.title("Supprimer réservation")
        win.config(bg=COULEUR_FOND)

        tk.Label(win, text="ID Réservation", bg=COULEUR_FOND).pack()
        champ = tk.Entry(win)
        champ.pack()

        def supprimer():
            id_resa = champ.get().strip()
            try:
                connexion = sqlite3.connect(DB_PATH)
                curseur = connexion.cursor()
                curseur.execute("DELETE FROM reservations WHERE id_resa = ? AND id_util = ?", (id_resa, self.utilisateur.id_util))
                connexion.commit()
                connexion.close()
                messagebox.showinfo("OK", "Réservation supprimée.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Erreur DB", f"Impossible de supprimer : {e}")

        tk.Button(win, text="Supprimer", bg=COULEUR_BOUTON, command=supprimer).pack(pady=10)

    def deconnexion(self):
        self.utilisateur = None
        if self.frame:
            self.frame.pack_forget()
        self.afficher_connexion()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    InterfaceGraphique().run()
