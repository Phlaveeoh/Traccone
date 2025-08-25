// Variabili globali per la mappa e i layer
let map;
let currentPathLayer;
let realtimeMarker;

// Funzione per inizializzare la mappa
function loadMap() {
    map = L.map('map').setView([41.9028, 12.4964], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Inizializza il marcatore per la posizione in tempo reale.
    // Usiamo una posizione iniziale fittizia.
    realtimeMarker = L.marker([0, 0], {
        icon: L.icon({
            iconUrl: 'https://leafletjs.com/examples/custom-icons/leaf-red.png',
            iconSize: [38, 95],
            iconAnchor: [22, 94],
            popupAnchor: [-3, -76]
        })
    }).addTo(map);
}

function createLineStringFromFeatures(featureCollection) {
    // Verifica che i dati siano una FeatureCollection valida con feature
    if (!featureCollection || !featureCollection.features || !Array.isArray(featureCollection.features)) {
        return null;
    }

    const coordinates = [];
    // Itera su ogni feature e aggiungi le sue coordinate all'array della linea
    featureCollection.features.forEach(feature => {
        // Assicurati che la feature abbia una geometria valida di tipo Point
        if (feature.geometry && feature.geometry.type === 'Point' && feature.geometry.coordinates) {
            coordinates.push(feature.geometry.coordinates);
        }
    });

    // Restituisci il nuovo oggetto GeoJSON LineString
    return {
        type: 'Feature',
        geometry: {
            type: 'LineString',
            coordinates: coordinates
        },
        properties: {} // Proprietà opzionali
    };
}

// Funzione per disegnare un percorso GeoJSON sulla mappa
function drawPath(geoJsonData) {
    // Rimuovi il layer del percorso precedente, se esiste
    if (currentPathLayer) {
        map.removeLayer(currentPathLayer);
    }

    // Verifica che l'array di coordinate non sia vuoto
    if (!geoJsonData || !geoJsonData.geometry || geoJsonData.geometry.coordinates.length === 0) {
        return;
    }

    // Crea un nuovo layer dal GeoJSON (LineString) e aggiungilo alla mappa
    currentPathLayer = L.geoJSON(geoJsonData, {
        style: {
            color: '#3498db',
            weight: 5,
            opacity: 0.8
        }
    }).addTo(map);

    // Adatta la vista della mappa per mostrare tutto il percorso
    map.fitBounds(currentPathLayer.getBounds());
}

// Funzione per aggiornare la posizione in tempo reale
async function updateRealtimeLocation() {
    let user_id = localStorage.getItem('user_id');
    let token = localStorage.getItem('jwt_token');

    const url = `/api/posizioni/${user_id}/lastPosition`;

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}` // Invia il token nell'header
            }
        });
        const data = await response.json();

        const newLatLng = [data.latitudine, data.longitudine];

        // Aggiorna la posizione del marker e il suo popup
        realtimeMarker.setLatLng(newLatLng).bindPopup("Posizione attuale").openPopup();

    } catch (error) {
        console.error('Errore durante l\'aggiornamento della posizione in tempo reale:', error);
    }
}

// Aggiungi un listener per il pulsante di filtro
document.getElementById('filterBtn').addEventListener('click', async () => {
    let user_id = localStorage.getItem('user_id');
    let token = localStorage.getItem('jwt_token');
    const data = document.getElementById('dateInput').value;

    if (!data) {
        alert('Per favore, seleziona una data.');
        return;
    }

    const url = `/api/posizioni/${user_id}?data=${data}`;

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}` // Invia il token nell'header
            }
        });

        if (!response.ok) {
            // Se la risposta non è 'ok', lancia un errore
            throw new Error(`Errore del server: ${response.status} - ${response.statusText}`);
        }

        const geoJsonData = await response.json();

        // Disegna il percorso sulla mappa
        const lineString = createLineStringFromFeatures(geoJsonData);
        if (lineString) {
            drawPath(lineString);
        }

    } catch (error) {
        console.error('Si è verificato un errore durante la fetch:', error);
        alert('Impossibile caricare le posizioni. Controlla la console per i dettagli.');
    }
});

// Inizializza la mappa e avvia l'aggiornamento in tempo reale quando la pagina è completamente caricata
window.onload = () => {
    loadMap();
    updateRealtimeLocation(); // Chiamata iniziale
    setInterval(updateRealtimeLocation, 5000); // Aggiorna ogni 5 secondi
};