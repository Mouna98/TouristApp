from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import VisitForm
import json
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Visit


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

        itinerario_citta = itinerari_data.get(place.lower(), {})
        giorni_itinerario = {}
        domande_vero_falso = []


        # Ottieni l'itinerario per la città e il numero di giorni
        for i in range(1, int(duration) + 1):
            giorno_key = f'giorno {i}'
            giorno_data = itinerario_citta.get(giorno_key, {})

            # Ottieni solo le informazioni necessarie per ogni attività del giorno
            attivita_giorno = [{
                'luogo': attivita.get('luogo', ''),
                'orario': attivita.get('orario', ''),
                'descrizione': attivita.get('descrizione', '')
            } for attivita in giorno_data.get('attività', [])]

            giorni_itinerario[giorno_key] = attivita_giorno

        # Ottieni le domande vero/falso per la città
        domande_vero_falso = itinerari_data.get(place.lower(), {}).get('domande_vero_falso', [])

        return render(request, 'myapp/itinerario.html', {'name': name, 'place': place, 'duration': duration, 'giorni_itinerario': giorni_itinerario, 'domande_vero_falso': domande_vero_falso})
    except FileNotFoundError:
        return HttpResponseNotFound("File JSON non trovato")
    except Exception as e:
        return HttpResponseServerError("Si è verificato un errore durante il recupero dell'itinerario: {}".format(str(e)))


def is_risposta_corretta(place, indice, risposta):
    try:
        # Leggi il file JSON degli itinerari
        with open('myapp/itinerari.json') as file:
            itinerari_data = json.load(file)

        # Trova il luogo nel file JSON
        itinerario_citta = itinerari_data.get(place.lower(), {})
        domande_vero_falso = itinerario_citta.get('domande_vero_falso', [])

        # Verifica se la chiave 'domande_vero_falso' è presente nel dizionario
        if domande_vero_falso:
            print("Chiave 'domande_vero_falso' trovata")
            if 0 <= indice < len(domande_vero_falso):
                print("Indice valido:", indice)
                # Confronta direttamente le stringhe delle risposte
                if domande_vero_falso[indice]["risposta"].lower() == risposta['risposta'].lower():
                    print(f"Domanda {indice} risposta corretta: {risposta['risposta']}")
                    return True
                else:
                    print(f"Domanda {indice} risposta errata: {risposta['risposta']}")
            else:
                print("Indice non valido")
        else:
            print("Chiave 'domande_vero_falso' non trovata per il luogo specificato")

    except FileNotFoundError:
        print("File JSON non trovato")
    except Exception as e:
        print("Errore durante il caricamento del file JSON:", e)

    return False


def calcola_punteggio(place, risposte_utente):
    punteggio = 0
    for indice, risposta in risposte_utente.items():
        if is_risposta_corretta(place, int(indice), risposta):
            punteggio += 1
    return punteggio

def rispondi_domanda(request,place):
    print("Inizio vista rispondi_domanda")

    if request.method == 'POST':
        risposte_utente = {}
        try:
            for key, value in request.POST.items():
                if key.startswith('risposte'):
                    index = key.split('[')[1].split(']')[0]
                    campo = key.split('[')[2].split(']')[0]
                    if index not in risposte_utente:
                        risposte_utente[index] = {}
                    risposte_utente[index][campo] = value

            print("Risposte dell'utente:", risposte_utente)

            punteggio = calcola_punteggio(place, risposte_utente)
            print("Punteggio:", punteggio)

            print("Tipo di punteggio:", type(punteggio))
            print("Valore di punteggio:", punteggio)
            context = {'punteggio': punteggio}

            return render(request, 'myapp/domanda.html', context)
        except Exception as e:
            print(f"Errore durante la gestione delle risposte dell'utente: {e}")

    return JsonResponse({'error': 'Metodo non consentito'}, status=405)

def pagina_punteggio(request, punteggio):

      # Ottieni il punteggio dalla query string dell'URL, se presente
    print("Punteggio attuale:", punteggio)

    return render(request, 'myapp/domanda.html', {'punteggio': punteggio})



