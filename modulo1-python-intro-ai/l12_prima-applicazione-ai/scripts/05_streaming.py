# Streaming: invece di aspettare tutta la risposta, la stampiamo pezzo per pezzo
# mentre il modello la genera (come fa ChatGPT).

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()
modello = "gpt-4.1-mini"

# Con stream=True non riceviamo una risposta unica, ma tanti piccoli eventi.
stream = client.responses.create(
    model=modello,
    instructions="Rispondi in italiano.",
    input="Spiega in tre frasi perché lo streaming è utile per gli LLM.",
    stream=True,
)

# Scorriamo gli eventi: quelli che ci interessano portano un pezzetto di testo (delta).
# end="" e flush=True servono a stampare tutto sulla stessa riga, subito.
for evento in stream:
    if evento.type == "response.output_text.delta":
        print(evento.delta, end="", flush=True)

print()  # a capo finale
