# I parametri di generazione: oggi diventano argomenti della chiamata.
# Il più importante è la temperature.

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()
modello = "gpt-4.1-mini"

ticket = "Non mi è mai arrivato il collo."

# temperature = 0 -> risposta stabile e ripetibile.
# Diciamo: è quello che vuoi per un classificatore. Rilanciamo 3 volte: esce sempre uguale.
print("temperature = 0")
for _ in range(3):
    risposta = client.responses.create(
        model=modello,
        instructions="Classifica il ticket con una sola parola: tecnico, fatturazione, spedizione, generale.",
        input=ticket,
        temperature=0,
    )
    print("  ", risposta.output_text)

# temperature alta -> più varietà. La proviamo su un compito creativo.
# Rilanciamo 3 volte: ogni volta cambia.
print("temperature = 1.3")
for _ in range(3):
    risposta = client.responses.create(
        model=modello,
        instructions="Scrivi una breve frase di avviso per la squadra spedizioni su questo ticket.",
        input=ticket,
        temperature=1.3,
    )
    print("  ", risposta.output_text)

# max_output_tokens: mette un tetto alla lunghezza della risposta.
risposta = client.responses.create(
    model=modello,
    input="Riassumi la storia di Internet.",
    max_output_tokens=30,
)
print("max_output_tokens = 30 ->", risposta.output_text)
