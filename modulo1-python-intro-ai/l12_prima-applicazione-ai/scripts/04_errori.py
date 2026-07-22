# Le chiamate via rete a volte falliscono: chiave sbagliata, troppe richieste, rete giù.
# In un'app vera le gestiamo con try/except, così il programma non si pianta.

import os
from dotenv import load_dotenv
from openai import OpenAI
from openai import AuthenticationError, RateLimitError, APIError

load_dotenv()
client = OpenAI()
modello = "gpt-4.1-mini"

# Mettiamo la chiamata dentro un try. Se va storto, gestiamo l'errore invece di crashare.
def classifica(testo):
    try:
        risposta = client.responses.create(
            model=modello,
            instructions="Classifica con una parola: tecnico, fatturazione, spedizione, generale.",
            input=testo,
        )
        return risposta.output_text
    except AuthenticationError:
        return "errore: la chiave non è valida"
    except RateLimitError:
        return "errore: troppe richieste, riprova tra poco"
    except APIError as e:
        return f"errore lato OpenAI: {e}"

print(classifica("Non mi è mai arrivato il collo."))

# Per vedere un errore vero dal vivo, proviamo con una chiave finta.
# È il modo sicuro di far comparire un errore senza rompere niente.
client_finto = OpenAI(api_key="sk-chiave-finta")
try:
    client_finto.responses.create(model=modello, input="ciao")
except AuthenticationError:
    print("Ho catturato l'errore: chiave non valida.")

# Da dire: se l'errore è temporaneo (server occupato, rate limit) l'SDK riprova già da solo.
# Possiamo dire quante volte riprovare e quanto aspettare al massimo:
client_robusto = OpenAI(max_retries=4, timeout=20)
