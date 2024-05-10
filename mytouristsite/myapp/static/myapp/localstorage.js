// Quando il documento è pronto
document.addEventListener('DOMContentLoaded', function() {
    // Controlla se ci sono risposte salvate in localStorage
    var risposteSalvate = localStorage.getItem('risposte_utente');
    if (risposteSalvate) {
        // Ripristina le risposte salvate nei campi del modulo
        var risposte = JSON.parse(risposteSalvate);
        risposte.forEach(function(risposta) {
            var input = document.getElementById(risposta.inputId);
            if (input) {
                input.checked = true;
            }
        });
    }
});

// Quando il modulo delle risposte viene inviato
document.getElementById('risposte_form').addEventListener('submit', function() {
    // Salva le risposte dell'utente in localStorage
    var risposte = [];
    document.querySelectorAll('input[name^="risposte"]').forEach(function(input) {
        var indice = input.getAttribute('name').match(/\d+/)[0];
        var valore = input.value;
        if (input.checked) {
            risposte.push({indice: indice, valore: valore, inputId: input.id});
        }
    });
    localStorage.setItem('risposte_utente', JSON.stringify(risposte));
});
