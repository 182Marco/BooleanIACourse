# Il finale: diamo all'Help Desk del progetto il "cervello" di un LLM.
# Classifichiamo i ticket prima uno alla volta, poi tutti in parallelo.

import os
import json
import time
import asyncio
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
from pydantic import BaseModel

load_dotenv()
client = OpenAI()
modello = "gpt-4.1-mini"

istruzioni = "Classifica il ticket con una sola parola: tecnico, fatturazione, spedizione, generale."


# Lo stesso modello dati del vostro progetto: un ticket ha un id e un messaggio.
class Ticket(BaseModel):
    id: int
    messaggio: str


# Carichiamo i ticket dal file e li trasformiamo in oggetti Ticket (Pydantic li valida).
def carica_ticket():
    with open("tickets.json", encoding="utf-8") as f:
        dati = json.load(f)
    return [Ticket(**d) for d in dati]


# Classifica un singolo ticket chiamando il modello.
def classifica(ticket):
    risposta = client.responses.create(
        model=modello,
        instructions=istruzioni,
        input=ticket.messaggio,
        temperature=0,
    )
    return risposta.output_text.strip().lower()


# Versione asincrona della stessa cosa: serve per lanciarne tante in parallelo.
async def classifica_async(client_async, ticket):
    risposta = await client_async.responses.create(
        model=modello,
        instructions=istruzioni,
        input=ticket.messaggio,
        temperature=0,
    )
    return risposta.output_text.strip().lower()


async def in_parallelo(ticket):
    client_async = AsyncOpenAI()
    # asyncio.gather lancia tutte le chiamate insieme e aspetta che finiscano.
    return await asyncio.gather(*[classifica_async(client_async, t) for t in ticket])


ticket = carica_ticket()

# Uno alla volta: sommiamo i tempi di ogni chiamata.
inizio = time.time()
risultati = [classifica(t) for t in ticket]
print("seriale:  ", risultati, "  in", round(time.time() - inizio, 1), "s")

# Tutti insieme: il tempo è quello della chiamata più lenta.
inizio = time.time()
risultati = asyncio.run(in_parallelo(ticket))
print("parallelo:", risultati, "  in", round(time.time() - inizio, 1), "s")
