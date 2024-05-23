document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('mostra_mappa').addEventListener('click', function () {
        document.getElementById('map-container').style.display = 'block';

        if (!window.map) {
            window.map = L.map('map-container');

            // Dati JSON integrati nel codice
            var data = {
                "firenze": {
                    "giorno 1": {
                        "date": "2024-04-10",
                        "attività": [
                            {
                                "luogo": "Duomo di Firenze",
                                "orario": "09:00 - 11:00",
                                "descrizione": "Visita al magnifico Duomo di Firenze, con la sua cupola di Brunelleschi e il campanile di Giotto.",
                                "latitudine": "43.7730556",
                                "longitudine": "11.255"
                            },
                            {
                                "luogo": "Museo dell'Accademia",
                                "orario": "11:30 - 13:30",
                                "descrizione": "Ammira la celebre statua di Michelangelo, il David, e altre opere d'arte rinascimentale.",
                                "latitudine": "43.7765",
                                "longitudine": "11.258"
                            },
                            {
                                "luogo": "Mercato Centrale",
                                "orario": "13:30 - 15:00",
                                "descrizione": "Sosta al Mercato Centrale per deliziarsi con specialità toscane come la bistecca fiorentina.",
                                "latitudine": "43.777",
                                "longitudine": "11.254"
                            },
                            {
                                "luogo": "Gallerie degli Uffizi",
                                "orario": "15:30 - 18:00",
                                "descrizione": "Esplora una delle più importanti collezioni d'arte del mondo, con opere di Leonardo da Vinci, Botticelli, e altri.",
                                "latitudine": "43.767",
                                "longitudine": "11.255"
                            },
                            {
                                "luogo": "Trattoria La Casalinga",
                                "orario": "19:30 - 21:30",
                                "descrizione": "Goditi una cena autentica toscana in un'atmosfera accogliente e familiare.",
                                "latitudine": "43.77",
                                "longitudine": "11.257"
                            }
                        ]
                    },
                    "giorno 2": {
                        "date": "2024-04-11",
                        "attività": [
                            {
                                "luogo": "Galleria Palatina e Giardino di Boboli",
                                "orario": "09:00 - 12:00",
                                "descrizione": "Visita la Galleria Palatina per ammirare dipinti rinascimentali e poi rilassati nei magnifici Giardini di Boboli.",
                                "latitudine": "43.764",
                                "longitudine": "11.248"
                            },
                            {
                                "luogo": "Ponte Vecchio e Palazzo Pitti",
                                "orario": "14:30 - 17:30",
                                "descrizione": "Attraversa il famoso Ponte Vecchio e visita il sontuoso Palazzo Pitti, residenza dei Medici.",
                                "latitudine": "43.767",
                                "longitudine": "11.253"
                            },
                            {
                                "luogo": "Osteria delle Tre Panche",
                                "orario": "19:30 - 21:30",
                                "descrizione": "Termina la giornata con una cena raffinata a base di piatti tipici toscani.",
                                "latitudine": "43.776",
                                "longitudine": "11.249"
                            }
                        ]
                    }
                }
            };

            // Funzione per caricare le attività nella mappa
            function caricaAttivita(attivita) {
                attivita.forEach(function (luogo) {
                    L.marker([parseFloat(luogo.latitudine), parseFloat(luogo.longitudine)]).addTo(window.map)
                        .bindPopup(luogo.luogo + "<br>" + luogo.orario + "<br>" + luogo.descrizione);
                });
            }

            // Carica i dati del primo giorno e del secondo giorno
            var primoGiornoAttivita = data.firenze["giorno 1"].attività[0];
            window.map.setView([parseFloat(primoGiornoAttivita.latitudine), parseFloat(primoGiornoAttivita.longitudine)], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png').addTo(window.map);
            caricaAttivita(data.firenze["giorno 1"].attività);
            caricaAttivita(data.firenze["giorno 2"].attività);
        }
    });
});
