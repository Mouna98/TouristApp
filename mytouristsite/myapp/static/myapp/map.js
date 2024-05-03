document.addEventListener('DOMContentLoaded', function () {

    document.getElementById('mostra_mappa').addEventListener('click', function () {
        // Mostra l'elemento del contenitore della mappa
        document.getElementById('map-container').style.display = 'block';

        // Controlla se la mappa è già stata inizializzata per evitare la duplicazione
        if (!window.map) {
            // Inizializza la mappa Leaflet centrata sull'Europa
            window.map = L.map('map-container').setView([50, 10], 4); // Imposta posizione e livello di zoom per centrare l'Europa
            L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png').addTo(window.map); // Aggiungi layer della mappa

            // Aggiungi il controllo di ricerca
            var searchControl = L.Control.geocoder().addTo(window.map);

            // Aggiungi l'evento per gestire la ricerca
            searchControl.on('markgeocode', function (event) {
                var latlng = event.geocode.center;
                window.map.setView(latlng, 13); // Imposta la vista sulla posizione trovata con un livello di zoom appropriato
            });
        }
    });
});
