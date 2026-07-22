# La nostra prima chiamata a un LLM, con la libreria ufficiale di OpenAI.
# Idea da passare: con l'SDK, parlare col modello è una sola funzione.

import os
from dotenv import load_dotenv
from openai import OpenAI

# load_dotenv legge il file .env e mette OPENAI_API_KEY tra le variabili d'ambiente.
# Diciamo all'aula: la chiave NON si scrive nel codice, sta nel .env (che non va su Git).
load_dotenv()

# OpenAI() prende da solo la chiave da OPENAI_API_KEY. Il client è il nostro "telefono" verso il modello.
client = OpenAI()

# Il modello: gpt-4.1-mini è piccolo ed economico, perfetto per imparare.
modello = "gpt-4.1-mini"

# La chiamata più semplice: gli diciamo quale modello vogliamo e cosa gli chiediamo (input).
risposta = client.responses.create(
    model=modello,
    input="Spiega in una frase cos'è un'API.",
)

# Il testo della risposta sta in output_text.
print(risposta.output_text)

print("-" * 40)

# Ora aggiungiamo un ruolo. instructions sono le istruzioni di sistema: il "system prompt" di giovedi.
# Riprendiamo il ticket che a parole chiave classificavamo male: "il collo che non arriva".
ticket = "Non mi è mai arrivato il collo."

risposta = client.responses.create(
    model=modello,
    instructions="Sei un classificatore di ticket. Rispondi con una sola parola tra: tecnico, fatturazione, spedizione, generale.",
    input=ticket,
)

print(ticket, "->", risposta.output_text)
