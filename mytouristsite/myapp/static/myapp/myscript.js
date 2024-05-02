// File: myscript.js
document.getElementById('risposte_form').addEventListener('submit', function(event) {
    event.preventDefault(); // Impedisce il comportamento predefinito del form (il ricaricamento della pagina)

    var form = event.target;
    var formData = new FormData(form);
    var csrfToken = form.elements['csrfmiddlewaretoken'].value; // Recupera il token CSRF dal form

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken // Aggiungi il token CSRF alla richiesta
        }
    })
    .then(response => {
        if (response.ok) {
            // Mostra le descrizioni delle domande anche dopo l'invio delle risposte
            var descrizioni = document.querySelectorAll('.descrizione');
            descrizioni.forEach(function(descrizione) {
                descrizione.style.display = 'block';
            });

            // Mostra il pulsante "Visualizza punteggio"
            var visualizzaPunteggioBtn = document.getElementById('visualizza_punteggio');
            visualizzaPunteggioBtn.style.display = 'inline-block';
        } else {
            console.error('Errore durante l\'invio delle risposte');
        }
    })
    .catch(error => {
        console.error('Errore:', error);
    });
});

function visualizzaPunteggio() {
    // Recupera il punteggio dalla pagina
    var punteggio = document.getElementById('punteggio').textContent;

    // Costruisci l'URL base per la pagina in cui desideri visualizzare il punteggio
    var baseUrl = "/pagina_punteggio/";

    // Aggiungi il punteggio come parametro alla fine dell'URL
    var url = baseUrl + "?punteggio=" + punteggio;

    // Reindirizza l'utente alla nuova pagina
    window.location.href = url;
}

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
