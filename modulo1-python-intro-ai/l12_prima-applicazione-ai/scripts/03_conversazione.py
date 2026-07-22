# Il modello non ha memoria: ogni chiamata riparte da zero.
# Per continuare un discorso, la conversazione la costruiamo NOI in una lista
# di messaggi e gliela ripassiamo tutta a ogni chiamata.

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()
modello = "gpt-4.1-mini"

# Immaginiamo questo scambio:
#   "Raccontami una barzelletta."  -> il bot ne dice una
#   "Spiegamela."                  -> dipende TUTTA dalla battuta di prima

# 1) SENZA memoria: mandiamo solo l'ultima frase. Il bot non sa di cosa parliamo.
risposta = client.responses.create(
    model=modello,
    input="Spiegamela.",
)
print("SENZA memoria:")
print(risposta.output_text)

# 2) CON memoria: gli passiamo l'intera conversazione, come lista di messaggi.
#    Ogni messaggio ha un ruolo: user siamo noi, assistant è il bot.
messaggi = [
    {"role": "user", "content": "Raccontami una barzelletta."},
    {"role": "assistant", "content": "Perché il libro di matematica era triste? Perché aveva troppi problemi."},
    {"role": "user", "content": "Spiegamela."},
]
risposta = client.responses.create(model=modello, input=messaggi)
print("\nCON memoria:")
print(risposta.output_text)
