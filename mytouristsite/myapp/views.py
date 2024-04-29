from django.shortcuts import render, redirect
from .forms import VisitForm
import json
from django.http import HttpResponseNotFound, HttpResponseServerError


def home(request):
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            form.save()
            # Ottieni i dati dal modulo per passarli alla vista mostra_itinerario
            name = form.cleaned_data['name']
            place = form.cleaned_data['place']
            duration = form.cleaned_data['duration']
            # Reindirizza alla vista mostra_itinerario con i dati del modulo
            return redirect('mostra_itinerario', name=name, place=place, duration=duration)
    else:
        form = VisitForm()
    return render(request, 'myapp/home.html', {'form': form})


def mostra_itinerario(request, name, place, duration):
    try:
        # Leggi il file JSON
        with open('myapp/itinerari.json') as file:
            itinerari_data = json.load(file)

           # print(itinerari_data)

        itinerario_citta = itinerari_data.get(place.lower(), {})
        giorni_itinerario = {}

        # Ottieni l'itinerario per la città e il numero di giorni
        for i in range(1, int(duration) + 1):
            giorno_key = f'giorno {i}'
            giorno_data = itinerario_citta.get(giorno_key, {})
            #print("Giorno data:", giorno_data)
            #for attivita in giorno_data.get("attività", []):
                #print("Attività:", attivita)

            # Ottieni solo le informazioni necessarie per ogni attività del giorno
            attivita_giorno = [{
                'luogo': attivita.get('luogo', ''),
                'orario': attivita.get('orario', ''),
                'descrizione': attivita.get('descrizione', '')
            } for attivita in giorno_data.get('attività', [])]

            giorni_itinerario[giorno_key] = attivita_giorno




        #print(giorni_itinerario)

        return render(request, 'myapp/itinerario.html', {'name': name, 'place': place, 'duration': duration, 'giorni_itinerario': giorni_itinerario})
    except FileNotFoundError:
        return HttpResponseNotFound("File JSON non trovato")
    except Exception as e:
        return HttpResponseServerError("Si è verificato un errore durante il recupero dell'itinerario: {}".format(str(e)))