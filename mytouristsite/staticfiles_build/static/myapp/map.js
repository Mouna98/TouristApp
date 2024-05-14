document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('mostra_mappa').addEventListener('click', function () {
        // Mostra l'elemento del contenitore della mappa
        document.getElementById('map-container').style.display = 'block';

        // Controlla se la mappa è già stata inizializzata per evitare la duplicazione
        if (!window.map) {
            // Inizializza la mappa Leaflet
            window.map = L.map('map-container');

            // Carica il file JSON con i dati dei luoghi direttamente
            fetch('itinerari.json')
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    // Ottieni il primo giorno di attività per la città specificata
                    var primoGiornoAttivita = data.firenze["giorno 1"].attività[0];

                    // Inizializza la mappa Leaflet centrata sul primo luogo
                    window.map.setView([parseFloat(primoGiornoAttivita.latitudine), parseFloat(primoGiornoAttivita.longitudine)], 13);

                    // Aggiungi il layer della mappa
                    L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png').addTo(window.map);

                    // Aggiungi un marker per il primo luogo
                    L.marker([parseFloat(primoGiornoAttivita.latitudine), parseFloat(primoGiornoAttivita.longitudine)]).addTo(window.map)
                        .bindPopup(primoGiornoAttivita.luogo + "<br>" + primoGiornoAttivita.orario + "<br>" + primoGiornoAttivita.descrizione);

                    // Aggiungi marker per gli altri luoghi
                    var attivita = data.firenze["giorno 1"].attività;
                    for (var i = 1; i < attivita.length; i++) {
                        var luogo = attivita[i];
                        L.marker([parseFloat(luogo.latitudine), parseFloat(luogo.longitudine)]).addTo(window.map)
                            .bindPopup(luogo.luogo + "<br>" + luogo.orario + "<br>" + luogo.descrizione);
                    }
                })
                .catch(function (error) {
                    console.error('Errore durante il recupero dei dati:', error);
                });
        }
    });
});
