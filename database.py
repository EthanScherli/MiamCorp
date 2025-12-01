import sqlite3

def initialiser_bdd():
    #Connexion à la DB/ crée le fichier s'il n'existe pas
    conn = sqlite3.connect("GastonGourmmet.db")
    cursor = conn.cursor()

    #Table Utilisateurs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        identifiant_connexion TEXT UNIQUE NOT NULL, 
        nom TEXT,
        prenom TEXT,
        mdp_hash TEXT,
        role TEXT DEFAULT 'user'
    )
    """)

    #Table Tables Restaurant
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tables_restaurant (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_table INTEGER UNIQUE,
        capacite INTEGER,
        emplacement TEXT
    )
    """)

    #Table Reservations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        utilisateur_id INTEGER,
        table_id INTEGER,
        date_heure TEXT,
        nombre_personnes INTEGER,
        statut TEXT DEFAULT 'confirmee',
        FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id),
        FOREIGN KEY(table_id) REFERENCES tables_restaurant(id)
    )
    """)

    conn.commit()
    conn.close()
    print("Base de données initialisée avec succès.")
    
if __name__ == "__main__":
    initialiser_bdd()