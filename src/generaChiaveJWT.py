import secrets

#----------------------------------------------
# Script per generare una chiave segreta per JWT
#----------------------------------------------

def genera_chiave_segreta(lunghezza_byte):
    """
    Genera una stringa esadecimale sicura.
    Il risultato ha una lunghezza doppia rispetto ai byte specificati.
    Ad esempio, 32 byte generano una stringa di 64 caratteri.
    """
    return secrets.token_hex(lunghezza_byte)

lunghezza_byte = 32

chiave_segreta = genera_chiave_segreta(lunghezza_byte)

print("Copia questa chiave e incollala nel tuo file .env:")
print(chiave_segreta)
