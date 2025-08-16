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

# Espone la porta che l'app userà
EXPOSE 5000

# Esegui il server Flask.
CMD ["python", "app.py"]