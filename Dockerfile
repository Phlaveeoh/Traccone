# Dockerfile
# Utilizza un'immagine base di Python
FROM python:3.10-alpine

# Imposta la cartella di lavoro nel container
WORKDIR /app

# Copia i requisiti e installa le dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia l'intero progetto nella cartella di lavoro
COPY . .

# Sposta la cartella di lavoro nella sottocartella 'src'
# in cui è stato spostato il file app.py
WORKDIR /app/src

# Esegui il server Flask. Il percorso è ora corretto
CMD ["python", "app.py"]
