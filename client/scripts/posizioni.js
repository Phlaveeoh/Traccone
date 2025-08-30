//Variabili globali per la mappa e i layer.
let map;
let currentPathLayer;
let realtimeMarker;

//Funzione per inizializzare la mappa Leaflet.
function loadMap() {
    // Inizializza la mappa nel div con id 'map', centrata su Roma con zoom 13.
    map = L.map('map').setView([41.9028, 12.4964], 13);
    
    // Aggiunge un layer di tile (le "immagini" della mappa) da OpenStreetMap.
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    //Inizializza il marcatore per la posizione in tempo reale con coordinate fittizie.
    //Definisce anche un'icona personalizzata per il marcatore.
    realtimeMarker = L.marker([0, 0], {
        icon: L.icon({
            iconUrl: 'https://leafletjs.com/examples/custom-icons/leaf-red.png',
            shadowUrl: 'https://leafletjs.com/examples/custom-icons/leaf-shadow.png',
            iconSize: [38, 95],
            iconAnchor: [22, 94],
            popupAnchor: [-3, -76]
        })
    }).addTo(map);
}

//Funzione per creare un oggetto GeoJSON di tipo LineString da una FeatureCollection di punti.
//Serve per convertire i dati dei punti ricevuti dall'API in un formato che Leaflet può disegnare come una linea.
function createLineStringFromFeatures(featureCollection) {

    //Verifica che l'input sia una GeoJSON FeatureCollection valida.
    if (!featureCollection || !featureCollection.features || !Array.isArray(featureCollection.features)) {
        console.error("Dati non validi: L'input non è una FeatureCollection.");
        return null;
    }

    const coordinates = [];
    //Itera su ogni feature della collezione.
    featureCollection.features.forEach(feature => {
        //Controlla che la feature abbia una geometria valida di tipo 'Point' e che contenga coordinate.
        if (feature.geometry && feature.geometry.type === 'Point' && feature.geometry.coordinates) {
            //Aggiunge l'array di coordinate (longitudine, latitudine) all'array 'coordinates'.
            coordinates.push(feature.geometry.coordinates);
        }
    });

    // Restituisce l'oggetto GeoJSON di tipo LineString appena creato.
    return {
        type: 'Feature',
        geometry: {
            type: 'LineString',
            coordinates: coordinates
        },
        properties: {}
    };
}

//Funzione per disegnare un percorso (LineString GeoJSON) sulla mappa.
function drawPath(geoJsonData) {
    //Se un percorso esiste già, lo rimuove dalla mappa per evitarne la sovrapposizione.
    if (currentPathLayer) {
        map.removeLayer(currentPathLayer);
    }

    //Controlla che ci siano dati da disegnare.
    if (!geoJsonData || !geoJsonData.geometry || geoJsonData.geometry.coordinates.length === 0) {
        console.warn('Dati GeoJSON vuoti, non è stato disegnato nessun percorso.');
        return;
    }

    //Crea un nuovo layer Leaflet da un oggetto GeoJSON e lo aggiunge alla mappa.
    currentPathLayer = L.geoJSON(geoJsonData, {
        style: {
            color: '#3498db',
            weight: 5,
            opacity: 0.8
        }
    }).addTo(map);

    //Adatta la vista della mappa per centrarla sul percorso disegnato e visualizzarlo interamente.
    map.fitBounds(currentPathLayer.getBounds());
}

//Funzione asincrona per aggiornare la posizione in tempo reale.
async function updateLocation() {
    //Recupera l'ID utente e il token JWT dalla memoria locale del browser.
    let user_id = localStorage.getItem('user_id');
    let token = localStorage.getItem('jwt_token');

    const url = `/api/posizioni/${user_id}/lastPosition`;

    try {
        //Invia una richiesta GET all'API.
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                //Inserisce il token JWT nell'header 'Authorization' per l'autenticazione.
                'Authorization': `Bearer ${token}`
            }
        });
        
        //Aspetta la risposta del server.
        const data = await response.json();

        //Prendo le coordinate dalla risposta.
        const newLatLng = [data.latitudine, data.longitudine];

        //Aggiorna la posizione del marcatore sulla mappa.
        realtimeMarker.setLatLng(newLatLng).bindPopup("Posizione attuale").openPopup();

    } catch (error) {
        //Gestisce eventuali errori di rete o di server.
        console.error('Errore durante l\'aggiornamento della posizione in tempo reale:', error);
    }
}

//Aggiunge un "ascoltatore di eventi" al pulsante di filtro.
document.getElementById('filterBtn').addEventListener('click', async () => {
    //Recupera l'ID utente e il token JWT.
    let user_id = localStorage.getItem('user_id');
    let token = localStorage.getItem('jwt_token');
    //Ottiene il valore del campo data.
    const data = document.getElementById('dateInput').value;

    //Se la data non è stata selezionata, mostra un messaggio di avviso e interrompe l'esecuzione.
    if (!data) {
        alert('Per favore, seleziona una data.');
        return;
    }

    const url = `/api/posizioni/${user_id}?data=${data}`;

    try {
        //Invia una richiesta GET all'API.
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                //Invia il token per l'autenticazione.
                'Authorization': `Bearer ${token}`
            }
        });

        //Controlla se la risposta non è andata a buon fine.
        if (!response.ok) {
            //Lancia un errore personalizzato che verrà catturato nel blocco 'catch'.
            throw new Error(`Errore del server: ${response.status} - ${response.statusText}`);
        }

        //Analizza la risposta JSON, che si presume sia una FeatureCollection.
        const geoJsonData = await response.json();

        //Chiama la funzione per convertire la collezione di punti in una singola LineString.
        const lineString = createLineStringFromFeatures(geoJsonData);
        //Se la linea è stata creata con successo, la disegna sulla mappa.
        if (lineString) {
            drawPath(lineString);
        }

    } catch (error) {
        //Gestisce gli errori durante la fetch, mostrando un avviso all'utente.
        console.error('Si è verificato un errore durante la fetch:', error);
        alert('Impossibile caricare le posizioni. Controlla la console per i dettagli.');
    }
});

//Funzione che viene eseguita quando la pagina è completamente caricata.
window.onload = () => {
    //Inizializza la mappa.
    loadMap();
    //Esegue l'aggiornamento della posizione in tempo reale per la prima volta.
    updateLocation();
    //Imposta un intervallo per chiamare la funzione 'updateRealtimeLocation' ogni 5 secondi
    setInterval(updateRealtimeLocation, 5000);
};
