
verifier_mdp

| Input 'mdp_saisi' | État '_mdp' de l’utilisateur | Output attendu | Situation / commentaire |
|------------------|-----------------------------|----------------|------------------------|
| '"abcd"'          | '"abcd"'                     | True           | Mot de passe correct |
| '"wrong"'         | '"abcd"'                     | False          | Mot de passe incorrect |
| '""'              | '"abcd"'                     | False          | Mot de passe vide |

---

email setter

| Input 'new_email'         | Output attendu | Situation |
|---------------------------|----------------|-----------|
| '"alice@mail.com"'        | email modifié  | Email valide |
| '"mauvais_email"'         | Exception levée | Email invalide |
| '"bob@example.org"'       | email modifié  | Email valide |


Fonction 'str'

| Input | Output attendu | Situation |
|-------|----------------|-----------|
| Utilisateur("Carla","Lopez","carla@mail.com","pass","admin") | '"Carla Lopez - carla@mail.com - admin"' | Vérifie le format de sortie pour affichage |


---

Changement nom via setter ('valeurNom')

| Input | Output attendu | Situation |
|-------|----------------|-----------|
| '"Durand"' | 'nom = "Durand"' | Vérifie la mise à jour du nom via le setter |


---

Connexion réussie

| Input email / mdp | État initial | Output attendu | Situation |
|------------------|--------------|----------------|-----------|
| '"test@mail.com"' / '"1234"' | Utilisateur existant dans Main.liste_utilisateurs | 'app_gui.utilisateur' mis à jour, menu affiché | Vérifie le processus de connexion dans la GUI |

---

Création compte champs vides

| Inputs champs | Output attendu | Situation |
|---------------|----------------|-----------|
| nom, prenom, email vides | Message d'erreur via messagebox | Vérifie la validation des champs obligatoires dans la GUI |

---

Transformation emails en majuscules (map + lambda)

| Input | Output attendu | Situation |
|-------|----------------|-----------|
| '[Utilisateur(email="a@mail.com"), Utilisateur(email="b@mail.com")]' | '['A@MAIL.COM','B@MAIL.COM']' | Vérifie la transformation des emails en majuscules avec map/lambda |

