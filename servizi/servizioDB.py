import psycopg2
import os

def connetti_db():
    """
    Stabilisce una connessione con il database PostgreSQL.
    Le credenziali sono lette dalle variabili d'ambiente.
    """
    try:
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST'),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD')
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Errore di connessione al database: {e}")
        # In un'app reale, potresti voler sollevare un'eccezione o gestire l'errore in modo diverso
        return None