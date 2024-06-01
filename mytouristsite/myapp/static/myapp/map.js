document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('mostra_mappa').addEventListener('click', function () {
        document.getElementById('map-container').style.display = 'block';

        if (!window.map) {
            window.map = L.map('map-container');

            // Richiedi i dati della sessione al server
            fetch('/get-session-data/')
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error('Errore:', data.error);
                        return;
                    }

                    var giorniItinerario = data.giorni_itinerario;

                    // Funzione per caricare le attività nella mappa
                    function caricaAttivita(attivita) {
                        attivita.forEach(function (luogo) {
                            L.marker([parseFloat(luogo.latitudine), parseFloat(luogo.longitudine)]).addTo(window.map)
                                .bindPopup(luogo.luogo + "<br>" + luogo.orario + "<br>" + luogo.descrizione);
                        });
                    }

                    // Carica i dati del primo giorno e del secondo giorno
                    var primoGiornoAttivita = giorniItinerario["giorno 1"][0];
                    window.map.setView([parseFloat(primoGiornoAttivita.latitudine), parseFloat(primoGiornoAttivita.longitudine)], 13);
                    L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png').addTo(window.map);
                    for (var giorno in giorniItinerario) {
                        caricaAttivita(giorniItinerario[giorno]);
                    }
                })
                .catch(error => {
                    console.error('Errore durante il recupero dei dati:', error);
                });
        }
    });
});
