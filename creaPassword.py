import bcrypt

def generate_hash(password):
    """
    Genera un hash bcrypt valido per una password.
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

# Sostituisci "password_di_prova" con la password che vuoi testare
password = "roba"

# Genera l'hash
valid_hash = generate_hash(password)

# Stampa l'hash che puoi usare nel tuo database
print("Ecco un hash valido per la tua password:")
print(valid_hash)