# Un piccolo chatbot: come ChatGPT, ma scritto da noi e pagato a consumo.
# Mette insieme: i ruoli, il contesto che teniamo noi, lo streaming e la gestione errori.

import os
from dotenv import load_dotenv
from openai import OpenAI
from openai import APIError

load_dotenv()
client = OpenAI()
modello = "gpt-4.1-mini"

# Qui dentro accumuliamo la conversazione, turno dopo turno.
messaggi = []

print("Scrivi un messaggio (oppure 'esci' per uscire).")
while True:
    testo = input("Tu: ")
    if testo == "esci":
        break

    # Aggiungiamo il messaggio dell'utente alla conversazione.
    messaggi.append({"role": "user", "content": testo})

    # Chiamiamo il modello in streaming, passandogli TUTTA la conversazione.
    print("Bot: ", end="", flush=True)
    risposta = ""
    try:
        stream = client.responses.create(
            model=modello,
            instructions="Sei un assistente conciso. Rispondi in italiano.",
            input=messaggi,
            stream=True,
        )
        for evento in stream:
            if evento.type == "response.output_text.delta":
                print(evento.delta, end="", flush=True)
                risposta += evento.delta
    except APIError as e:
        print("errore:", e)
    print()

    # Aggiungiamo la risposta del bot, così al giro dopo "ricorda" cosa ci siamo detti.
    messaggi.append({"role": "assistant", "content": risposta})
