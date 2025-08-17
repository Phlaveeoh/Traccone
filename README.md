
# Server Traccone

Il server è una **RESTful API** sviluppata in **Python** con il framework **Flask**. Utilizza un database **PostgreSQL** con l'estensione **PostGIS** e l'autenticazione è gestita tramite **JWT (JSON Web Tokens)**.

## Istruzioni per il Deploy

Il deploy è gestito tramite **Docker Compose**.

### 1. Creazione del Database

Per avviare il database PostgreSQL, usa il seguente comando:

```
docker-compose up -d db
```
Durante il primo avvio del database andranno create anche le tabelle che verranno utilizzate dall'applicazione.  
Per crearle è sufficiente connettersi al database da linea di comando o con qualsiasi client PostgreSQL e creare le seguenti tabelle:

```
CREATE EXTENSION postgis;
```

```
CREATE TABLE users (
    id SERIAL PRIMARY KEY NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    telefono VARCHAR(20) UNIQUE,
    nome VARCHAR(50),
    cognome VARCHAR(50),
);
```
```
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    coordinate GEOMETRY(Point, 4326),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```
```
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    group_name VARCHAR(100) UNIQUE NOT NULL,
    owner_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
);

```
```
CREATE TABLE user_groups (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    group_id INTEGER REFERENCES groups(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, group_id)
);
```

### 2. Creazione del File `.env`

Crea un file chiamato `.env` nella directory principale del progetto. Il file deve avere il seguente formato:

```
# Variabili per la connessione al database PostgreSQL
DB_HOST=db
DB_NAME=mydatabase
DB_USER=user
DB_PASSWORD=password

# Chiave segreta per la firma dei token JWT
JWT_SECRET_KEY=chiave_segreta
```
La chiave può essere generata utilizzando lo script `generaChiaveJWT.py` che si trova in questa repo

### 3. Avvio del Server

Una volta che il database è in esecuzione e il file `.env` è configurato, puoi avviare il server backend con questo comando:

```
docker-compose up --build backend
```

### 4. Avvio di Tutti i Servizi

Per avviare sia il database che il backend contemporaneamente:

```
docker-compose up --build
```

## Esempi di Rotte API

* **`POST /api/auth/login`**: Autentica un utente e restituisce un token JWT.

* **`GET /api/posizioni/<user_id>`**: Richiede lo storico delle posizioni di un utente specifico. Richiede un token JWT.

* **`POST /api/posizioni/save`**: Salva una nuova posizione per l'utente autenticato. Richiede un token JWT.

## Manutenzione

* **Arresto dei servizi**: Per fermare tutti i container, usa `docker-compose down`.

* **Pulizia**: Per rimuovere i container e i volumi, usa `docker-compose down -v`.
