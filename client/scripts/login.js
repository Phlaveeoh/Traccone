//L'evento 'submit' viene attivato quando l'utente preme il pulsante di invio del form.
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    //Impedisce il comportamento predefinito del form, che sarebbe quello di ricaricare la pagina.
    e.preventDefault();

    //Recupera i valori inseriti nei campi 'username' e 'password' del form.
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    //Recupera l'elemento HTML dove verranno visualizzati i messaggi (es. successi o errori).
    const messageDiv = document.getElementById('message');

    //Nasconde il messaggio precedente prima di inviare una nuova richiesta.
    messageDiv.style.display = 'none';

    try {
        //Invia una richiesta HTTP POST al server per l'autenticazione.
        const response = await fetch('/api/auth/login', {
            method: 'POST', //Specifica il metodo della richiesta.
            headers: {
                //Indica al server che il corpo della richiesta è in formato JSON.
                'Content-Type': 'application/json'
            },
            //Converte i dati (username e password) in una stringa JSON
            body: JSON.stringify({ username, password })
        });
        
        //Attende la risposta del server e la analizza come JSON.
        const data = await response.json();

        //Mostra il div del messaggio per visualizzare l'esito della richiesta.
        messageDiv.style.display = 'block';
        if (response.ok) { // La proprietà 'ok' è true se il codice di stato HTTP è 200-299.
            //Se il login ha successo, salva il token JWT e l'ID dell'utente nella memoria locale del browser per le richieste successive.
            localStorage.setItem('jwt_token', data.token);
            localStorage.setItem('user_id', data.user_id);
            
            //Aggiorna il testo e la classe CSS del messaggio per mostrare il successo.
            messageDiv.textContent = 'Login riuscito!';
            messageDiv.className = 'success';

            //Dopo un breve ritardo, reindirizza l'utente alla dashboard.
            //Il ritardo consente al browser di salvare i dati prima del reindirizzamento.
            setTimeout(() => {
                window.location.href = '/dashboard.html';
            }, 500);
        } else {
            //Se la risposta non è 'ok', mostra un messaggio di errore
            messageDiv.textContent = 'Errore: ' + (data.error || 'Credenziali non valide');
            messageDiv.className = 'error';
        }

    } catch (error) {
        //Cattura eventuali errori di rete che impediscono la richiesta di arrivare al server.
        messageDiv.style.display = 'block';
        messageDiv.textContent = 'Errore di rete. Riprova più tardi.';
        messageDiv.className = 'error';
        console.error('Fetch error:', error);
    }
});
