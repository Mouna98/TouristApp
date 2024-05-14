document.getElementById('mostra_descrizioni').addEventListener('click', function() {
    // Mostra le descrizioni delle domande quando si fa clic sul pulsante
    var descrizioni = document.querySelectorAll('.descrizione');
    descrizioni.forEach(function(descrizione) {
        descrizione.style.display = 'block';
    });
});
