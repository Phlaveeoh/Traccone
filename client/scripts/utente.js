//Funzione asincrona per recuperare i dati dell'utente
async function getUtente() {
    //Recupera l'ID utente e il token JWT (JSON Web Token) dalla memoria locale del browser.
    let user_id = localStorage.getItem('user_id');
    let token = localStorage.getItem('jwt_token');

    const url = `/api/utenti/${user_id}`;

    try {
        //Invia una richiesta HTTP GET all'URL specificato.
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                //Inserisce il token JWT nell'header 'Authorization'
                'Authorization': `Bearer ${token}`
            }
        });
        //Attende la risposta e la analizza come JSON.
        const data = await response.json();

        //Popola i campi del form sulla pagina con i dati ricevuti dal server.
        document.getElementById("username").innerText = data.username;
        document.getElementById("telefono").value = data.telefono;
        document.getElementById("nome").value = data.nome;
        document.getElementById("cognome").value = data.cognome;
    } catch (error) {
        //Se la richiesta fallisce (es. errore di rete o server non disponibile),
        //mostra un messaggio di errore.
        document.getElementById("message").innerText = "Errore nel recupero dei dati utente: " + error;
    }
}

//Aggiunge un "ascoltatore di eventi" al pulsante per l'aggiornamento dei dati utente.
document.getElementById('updateUserBtn').addEventListener('click', async (event) => {
    //Previene il comportamento predefinito del form
    event.preventDefault();
    
    //Recupera l'ID utente e il token JWT.
    const user_id = localStorage.getItem('user_id');
    const token = localStorage.getItem('jwt_token');

    const url = `/api/utenti/${user_id}/update`;

    //Crea un oggetto con i dati da inviare al server.
    const formData = {
        telefono: document.getElementById("telefono").value,
        nome: document.getElementById("nome").value,
        cognome: document.getElementById("cognome").value
    };

    try {
        //Invia una richiesta HTTP PATCH per aggiornare parzialmente i dati dell'utente.
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                //Specifica che il corpo della richiesta è in formato JSON.
                'Content-Type': 'application/json',
                //Inserisce il token per l'autenticazione.
                'Authorization': `Bearer ${token}`
            },
            //Converte l'oggetto 'formData' in una stringa JSON.
            body: JSON.stringify(formData)
        });

        if (response.ok) { //Controlla se la risposta del server ha avuto successo
            document.getElementById("message").innerText = "Informazioni utente aggiornate con successo.";
            //Richiama la funzione 'getUtente' per ricaricare e visualizzare i dati aggiornati.
            getUtente();
        } else {
            document.getElementById("message").innerText = "Errore nell'aggiornamento delle informazioni utente";
        }
    } catch (error) {
        //Gestisce gli errori di rete.
        console.error("Errore nella richiesta:", error);
    }
});

//Aggiunge un "ascoltatore di eventi" al pulsante per il cambio password.
document.getElementById('bCambiaPass').addEventListener('click', async (event) => {
    //Previene il comportamento predefinito del form.
    event.preventDefault();
    
    //Recupera l'ID utente e il token JWT.
    const user_id = localStorage.getItem('user_id');
    const token = localStorage.getItem('jwt_token');

    //Recupera i valori dei campi per la nuova password.
    const nuovaPassword = document.getElementById("nuova_password").value;
    const confermaPassword = document.getElementById("conferma_password").value;

    //Esegue una validazione di base per verificare che le password coincidano.
    if (confermaPassword != nuovaPassword) {
        document.getElementById("message").innerText = "Le due password non coincidono!";
        return; // Interrompe l'esecuzione della funzione.
    }

    const url = `/api/utenti/${user_id}/cambiaPassword`;

    //Crea un oggetto con le password da inviare al server.
    const formData = {
        vecchia_password: document.getElementById("vecchia_password").value,
        nuova_password: document.getElementById("nuova_password").value,
    };

    try {
        //Invia una richiesta HTTP PATCH per aggiornare la password.
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            document.getElementById("message").innerText = "Password utente aggiornata con successo.";
            //Richiama la funzione 'getUtente' per aggiornare eventuali dati, se necessario.
            getUtente();
        } else {
            document.getElementById("message").innerText = "Errore nell'aggiornamento della password utente";
        }
    } catch (error) {
        console.error("Errore nella richiesta:", error);
    }
});


window.onload = () => {
    //Chiama la funzione per recuperare e visualizzare i dati dell'utente.
    getUtente();
};
