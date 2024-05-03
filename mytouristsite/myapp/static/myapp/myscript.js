// File: myscript.js
// Aggiungi un event listener al pulsante "Mostra descrizioni"
document.getElementById('mostra_descrizioni').addEventListener('click', function() {
    // Mostra le descrizioni delle domande quando si fa clic sul pulsante
    var descrizioni = document.querySelectorAll('.descrizione');
    descrizioni.forEach(function(descrizione) {
        descrizione.style.display = 'block';
    });
});

document.getElementById('visualizza_punteggio').addEventListener('click', function() {
    var form = document.getElementById('risposte_form');
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

       // Reindirizza l'utente alla pagina del punteggio
            var punteggioUrl = this.getAttribute('data-punteggio-url');
            window.location.href = punteggioUrl;
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


