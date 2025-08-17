import secrets

def genera_chiave_segreta(lunghezza_byte):
    """
    Genera una stringa esadecimale sicura.
    Il risultato ha una lunghezza doppia rispetto ai byte specificati.
    Ad esempio, 32 byte generano una stringa di 64 caratteri.
    """
    return secrets.token_hex(lunghezza_byte)

# Lunghezza raccomandata per una chiave sicura (64 caratteri)
lunghezza_byte = 32

# Genera la chiave segreta
chiave_segreta = genera_chiave_segreta(lunghezza_byte)

# Stampa la chiave che puoi copiare e incollare nel tuo file .env
print("Copia questa chiave e incollala nel tuo file .env:")
print(chiave_segreta)
