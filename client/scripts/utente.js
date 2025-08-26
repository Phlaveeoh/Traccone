async function getUtente() {
    let user_id = localStorage.getItem('user_id');
    let token = localStorage.getItem('jwt_token');

    const url = `/api/utenti/${user_id}`;

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}` // Invia il token nell'header
            }
        });
        const data = await response.json();

        // Popola il form con i dati dell'utente
        document.getElementById("username").innerText = data.username;
        document.getElementById("telefono").value = data.telefono;
        document.getElementById("nome").value = data.nome;
        document.getElementById("cognome").value = data.cognome;
    } catch (error) {
        document.getElementById("message").innerText = "Errore nel recupero dei dati utente:" + error;
    }
}

document.getElementById('updateUserBtn').addEventListener('click', async () => {
    const user_id = localStorage.getItem('user_id');
    const token = localStorage.getItem('jwt_token');

    const url = `/api/utenti/${user_id}/update`;

    const formData = {
        telefono: document.getElementById("telefono").value,
        nome: document.getElementById("nome").value,
        cognome: document.getElementById("cognome").value
    };

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            document.getElementById("message").innerText = "Informazioni utente aggiornate con successo.";
            getUtente();
        } else {
            document.getElementById("message").innerText = "Errore nell'aggiornamento delle informazioni utente";
        }
    } catch (error) {
        console.error("Errore nella richiesta:", error);
    }
});

document.getElementById('bCambiaPass').addEventListener('click', async () => {
    const user_id = localStorage.getItem('user_id');
    const token = localStorage.getItem('jwt_token');

    const url = `/api/utenti/${user_id}/cambiaPassword`;

    const formData = {
        vecchia_password: document.getElementById("vecchia_password").value,
        nuova_password: document.getElementById("nuova_password").value,
    };
    let confermaPass =  document.getElementById("conferma_password")

    if (confermaPass != formData.nuova_password) {
        document.getElementById("message").innerText("le 2 password non coincidono!")
        return;
    }

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            document.getElementById("message").innerText = "Password utente aggiornate con successo.";
            getUtente();
        } else {
            document.getElementById("message").innerText = "Errore nell'aggiornamento della password utente";
        }
    } catch (error) {
        console.error("Errore nella richiesta:", error);
    }
});



//Appena carico la finestra stampo nel form i dati dell'utente
window.onload = () => {
    getUtente();
};