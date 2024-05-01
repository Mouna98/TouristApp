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
            // Se la risposta è stata inviata correttamente, mostra le descrizioni delle domande
            var descrizioni = document.querySelectorAll('.descrizione');
            descrizioni.forEach(function(descrizione) {
                descrizione.style.display = 'block';
            });
            // Mostra il pulsante "Visualizza punteggio"
            var visualizzaPunteggioBtn = document.getElementById('visualizza_punteggio');
            visualizzaPunteggioBtn.style.display = 'inline-block';


        } else {
            console.error('Error sending answers');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});


function showAllDescriptions() {
    var descrizioni = document.querySelectorAll('.descrizione');
    descrizioni.forEach(function(descrizione) {
        descrizione.style.display = 'block';
    });
}