# Usa un'immagine ufficiale di Python
FROM python:3.10-alpine

# Imposta la directory di lavoro all'interno del container
WORKDIR /usr/src/app

# Copia il file delle dipendenze e installale
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice della tua applicazione
COPY . .

# Espone la porta che l'app userà
EXPOSE 5000

# Comando per avviare l'applicazione usando Gunicorn o Eventlet
CMD ["python", "app.py"]