from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from .forms import VisitForm
import requests
import json
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse, HttpResponseRedirect, JsonResponse
import wikipediaapi
import openai
import re


# Configura la chiave API di OpenAI
#SECRET_API_OPENAI

def prima_pagina(request):
    return render(request, 'myapp/prima_pagina.html')


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

    # Ottieni il punteggio dalla query string dell'URL
    punteggio = request.GET.get('punteggio')

    # Inizializza punteggio a None nel contesto se non presente nella query string
    context = {'form': form, 'punteggio': punteggio}

    return render(request, 'myapp/home.html', context)

def mostra_itinerario(request, name, place, duration):
    try:
        # Richiesta di creazione dell'itinerario tramite GPT-4
        prompt_itinerary = f"""
            Crea un itinerario di viaggio per {place} per {duration} giorni. Includi il nome dei luoghi da visitare, l'orario e una breve descrizione per ogni luogo.
            Fornisci l'output nel seguente formato JSON:
            {{
                "{place}": {{
                    "giorno 1": {{
                        "data": "YYYY-MM-DD",
                        "attività": [
                            {{
                                "luogo": "Nome del luogo",
                                "orario": "Orario di inizio - Orario di fine",
                                "descrizione": "Descrizione del luogo",
                                "latitudine": "Latitudine",
                                "longitudine": "Longitudine"
                            }},
                            ...
                        ]
                    }},
                    ...
                    "domande_vero_falso": [
                        {{
                            "indice": 0,
                            "domanda": "Domanda vero/falso sull'itinerario",
                            "risposta": "true/false",
                            "descrizione": "Spiegazione della risposta"
                        }},
                        ...
                    ]
                }}
            }}
            """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sei un assistente di viaggio."},
                {"role": "user", "content": prompt_itinerary}
            ]
        )

        # Estraiamo i dati dell'itinerario dalla risposta
        itinerary_data = response.choices[0].message['content']
        itinerary = json.loads(itinerary_data)

        # Costruiamo la struttura dati dell'itinerario come richiesto
        giorni_itinerario = {}
        for i in range(1, int(duration) + 1):
            giorno_key = f'giorno {i}'
            giorno_data = itinerary.get(place, {}).get(giorno_key, {})
            attivita_giorno = []
            for attivita in giorno_data.get('attività', []):
                luogo = attivita.get('luogo', '')
                orario = attivita.get('orario', '')
                descrizione = attivita.get('descrizione', '')
                latitudine = attivita.get('latitudine', '')
                longitudine = attivita.get('longitudine', '')

                # Ottieni l'URL dell'immagine da Wikipedia per il luogo
                image_url = get_wikipedia_image_url(luogo)

                attivita_giorno.append({
                    'luogo': luogo,
                    'orario': orario,
                    'descrizione': descrizione,
                    'latitudine': latitudine,
                    'longitudine': longitudine,
                     'image_url': image_url
                })
            giorni_itinerario[giorno_key] = attivita_giorno

        domande_vero_falso = itinerary.get(place, {}).get("domande_vero_falso", [])

        # Salviamo l'itinerario e le domande nella sessione
        request.session['itinerario'] = giorni_itinerario
        request.session['domande_vero_falso'] = domande_vero_falso

        context = {
            'name': name,
            'place': place,
            'duration': duration,
            'giorni_itinerario': giorni_itinerario,
            'domande_vero_falso': domande_vero_falso,
            'punteggio': None
        }

        # Renderizziamo il template itinerario.html con i dati dell'itinerario
        return render(request, 'myapp/itinerario.html', context)

    except Exception as e:
        return render(request, 'myapp/itinerario.html', {'error': str(e)})

def is_risposta_corretta(place, indice, risposta_utente, risposte_corrette):
    try:
        # Recupera la risposta corretta dal JSON
        risposta_corretta = None
        for domanda in risposte_corrette:
            if domanda['indice'] == indice:
                risposta_corretta = domanda['risposta'].strip().lower()
                break

        if risposta_corretta is None:
            print(f"Nessuna risposta trovata per l'indice: {indice}")
            return False

        # Confronta la risposta dell'utente con quella corretta
        risposta_utente = risposta_utente['risposta'].strip().lower()
        is_correct = (risposta_corretta == risposta_utente or
                      (risposta_corretta == 'true' and risposta_utente in ['true', 'sì']) or
                      (risposta_corretta == 'false' and risposta_utente in ['false', 'no']))

        print(
            f"Risposta corretta per indice {indice}: {risposta_corretta}, Risposta utente: {risposta_utente}, Esito: {is_correct}")

        return is_correct
    except Exception as e:
        print(f"Errore durante la verifica della risposta: {e}")
        return False


def calcola_punteggio(place, risposte_utente, risposte_corrette):
    try:
        punteggio = 0
        for index, risposta in risposte_utente.items():
            indice = int(risposta['indice'])
            if is_risposta_corretta(place, indice, risposta, risposte_corrette):
                punteggio += 1
        print(f"Punteggio totale calcolato: {punteggio}")
        return punteggio
    except Exception as e:
        print(f"Errore durante il calcolo del punteggio: {e}")
        return 0  # Restituisci 0 se si verifica un errore

def rispondi_domanda(request, name, place, duration):
    if request.method == 'POST':
        try:
            risposte_utente = {}
            for key, value in request.POST.items():
                if key.startswith('risposte'):
                    index = key.split('[')[1].split(']')[0]
                    campo = key.split('[')[2].split(']')[0]
                    if index not in risposte_utente:
                        risposte_utente[index] = {}
                    risposte_utente[index][campo] = value

            # Recupera l'itinerario e le domande dalla sessione
            itinerario = request.session.get('itinerario', {})
            domande = request.session.get('domande_vero_falso', [])

            # Calcola il punteggio
            punteggio = calcola_punteggio(place, risposte_utente, domande)

            # Aggiungi il punteggio, l'itinerario e le domande al contesto
            context = {
                'name': name,
                'place': place,
                'duration': duration,
                'giorni_itinerario': itinerario,
                'domande_vero_falso': domande,
                'punteggio': punteggio
            }

            # Renderizza il template punteggio.html con il contesto
            return render(request, 'myapp/punteggio.html', context)
        except Exception as e:
            print(f"Errore durante la gestione delle risposte dell'utente: {e}")
            return HttpResponseServerError("Si è verificato un errore durante la gestione delle risposte dell'utente.")
    else:
        return HttpResponseNotFound("La pagina richiesta non è stata trovata.")

def ottieni_domande_itinerario(name, place, duration):
    try:
        prompt_itinerary = f"""
            Create a travel itinerary for {place} for {duration} days. Include the name of the places to visit, the time and a brief description for each place.
            Provide the output in the following JSON format:
            {{
                "{place}": {{
                    "giorno 1": {{
                        "date": "YYYY-MM-DD",
                        "attività": [
                            {{
                                "luogo": "Place name",
                                "orario": "Start time - End time",
                                "descrizione": "Description of the place",
                                "latitudine": "Latitude",
                                "longitudine": "Longitude"
                            }},
                            ...
                        ]
                    }},
                    ...
                    "domande_vero_falso": [
                        {{
                            "indice": 0,
                            "domanda": "True/false question about the itinerary",
                            "risposta": "true/false",
                            "descrizione": "Explanation about the answer"
                        }},
                        ...
                    ]
                }}
            }}
            """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a travel assistant."},
                {"role": "user", "content": prompt_itinerary}
            ]
        )

        itinerary_data = response.choices[0].message['content']
        itinerary = json.loads(itinerary_data)

        giorni_itinerario = {}
        for i in range(1, int(duration) + 1):
            giorno_key = f'giorno {i}'
            giorno_data = itinerary.get(place, {}).get(giorno_key, {})
            attivita_giorno = []
            for attivita in giorno_data.get('attività', []):
                luogo = attivita.get('luogo', '')
                orario = attivita.get('orario', '')
                descrizione = attivita.get('descrizione', '')
                latitudine = attivita.get('latitudine', '')
                longitudine = attivita.get('longitudine', '')
                attivita_giorno.append({
                    'luogo': luogo,
                    'orario': orario,
                    'descrizione': descrizione,
                    'latitudine': latitudine,
                    'longitudine': longitudine
                })
            giorni_itinerario[giorno_key] = attivita_giorno

        domande_vero_falso = itinerary.get(place, {}).get("domande_vero_falso", [])

        return giorni_itinerario, domande_vero_falso
    except json.JSONDecodeError:
        print("Errore durante il parsing del JSON.")
        return {}, []
    except Exception as e:
        print(f"Errore durante il recupero dell'itinerario e delle domande: {e}")
        return {}, []

def livello_due(request, name, place, duration):
    itinerario = request.session.get('itinerario', {})
    try:
        prompt_livello_due = f"""
            Fornisci domande di livello due per {place} nel seguente formato JSON:
            {{
                "domande_livello_due": [
                    {{
                        "indice": 0,
                        "domanda": "Domanda di livello due",
                        "risposta": "true/false",
                        "descrizione": "Spiegazione della risposta"
                    }},
                    ...
                ]
            }}
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sei un assistente quiz di viaggio."},
                {"role": "user", "content": prompt_livello_due}
            ]
        )

        domande_livello_due_data = response.choices[0].message['content']
        domande_livello_due = json.loads(domande_livello_due_data).get('domande_livello_due', [])

        # Memorizza le nuove domande nella sessione
        request.session['domande_livello_due'] = domande_livello_due

        punteggio = None

        if request.method == 'POST':
            risposte_utente = {}
            for key, value in request.POST.items():
                if key.startswith('risposte'):
                    index = key.split('[')[1].split(']')[0]
                    campo = key.split('[')[2].split(']')[0]
                    if index not in risposte_utente:
                        risposte_utente[index] = {}
                    risposte_utente[index][campo] = value

            if risposte_utente:
                # Recupera le domande di livello due dalla sessione
                domande_livello_due = request.session.get('domande_livello_due', [])
                punteggio = calcola_punteggio_livello_due(place, risposte_utente, domande_livello_due)

                # Debug: stampa il contenuto della sessione
                print("Contenuto della sessione:")
                print(request.session)

            # Recupera l'itinerario dalla sessione
            itinerario = request.session.get('itinerario', {})

            # Debug: stampa l'itinerario recuperato
            print("Itinerario recuperato dalla sessione:")
            print(itinerario)

        context = {
            'name': name,
            'place': place,
            'duration': duration,
            'giorni_itinerario': itinerario,
            'domande': domande_livello_due,
            'punteggio': punteggio
        }
        return render(request, 'myapp/domande_livello_due.html', context)
    except Exception as e:
        # Debug: stampa l'errore
        print(f"Errore nella vista livello_due: {e}")
        return HttpResponseServerError(f"Si è verificato un errore durante il recupero delle domande di livello due: {str(e)}")

def calcola_punteggio_livello_due(place, risposte_utente, risposte_corrette):
    try:
        punteggio = 0
        for index, risposta in risposte_utente.items():
            indice = int(risposta['indice'])
            if is_risposta_corretta_livello_due(place, indice, risposta, risposte_corrette):
                punteggio += 1
        print(f"Punteggio totale calcolato: {punteggio}")
        return punteggio
    except Exception as e:
        print(f"Errore durante il calcolo del punteggio: {e}")
        return 0  # Restituisci 0 se si verifica un errore

def is_risposta_corretta_livello_due(place, indice, risposta_utente, risposte_corrette):
        try:
            # Recupera la risposta corretta dal JSON
            risposta_corretta = None
            for domanda in risposte_corrette:
                if domanda['indice'] == indice:
                    risposta_corretta = domanda['risposta'].strip().lower()
                    break

            if risposta_corretta is None:
                print(f"Nessuna risposta trovata per l'indice: {indice}")
                return False

            # Confronta la risposta dell'utente con quella corretta
            risposta_utente = risposta_utente['risposta'].strip().lower()
            is_correct = (risposta_corretta == risposta_utente or
                          (risposta_corretta == 'true' and risposta_utente in ['true', 'sì']) or
                          (risposta_corretta == 'false' and risposta_utente in ['false', 'no']))

            print(
                f"Risposta corretta per indice {indice}: {risposta_corretta}, Risposta utente: {risposta_utente}, Esito: {is_correct}")

            return is_correct
        except Exception as e:
            print(f"Errore durante la verifica della risposta: {e}")
            return False



def get_wikipedia_image_url(title):
    response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}")
    if response.status_code == 200:
        page_data = response.json()
        thumbnail_url = page_data.get('thumbnail', {}).get('source')
        return thumbnail_url
    else:
        return None

