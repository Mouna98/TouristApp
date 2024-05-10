// File: myscript.js
// Aggiungi un event listener al pulsante "Mostra descrizioni"
document.getElementById('visualizza_punteggio').addEventListener('click', function() {
    // Ottieni il punteggio dal contenuto del div
    var punteggio = document.getElementById('punteggio_container').textContent.trim();
    // Visualizza direttamente il punteggio
    console.log("Il punteggio è:", punteggio);
});