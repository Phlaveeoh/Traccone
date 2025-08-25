//Appena carico la finestra stampo nel form i dati dell'utente
window.onload = () => {
    // Simulazione di recupero dati utente
    const userData = {
        username: "MarioRossi",
        telefono: "1234567890",
        nome: "Mario",
        cognome: "Rossi"
    };

    // Popola il form con i dati dell'utente
    document.getElementById("username").innerText = userData.username;
    document.getElementById("telefono").value = userData.telefono;
    document.getElementById("nome").value = userData.nome;
    document.getElementById("cognome").value = userData.cognome;
};