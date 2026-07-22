"""structured.py — dalla frase al dato: Pydantic + Structured Outputs.

L'unico file della serata (L25). Le prime due tappe (TODO 1-2) si scrivono
COL DOCENTE — guardate e replicate. Nell'esercizio guidato (TODO 3, da soli)
applicate lo stesso pattern su un testo diverso, seguendo il metodo della
slide "Suggerimento: come costruire uno JSON Schema".

    python working/structured.py
"""
from enum import Enum

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError

load_dotenv()

MODELLO = "gpt-4o-mini"

client = OpenAI()

TESTO_GIULIA = (
    "Mi chiamo Giulia Bianchi, lavoro nel marketing, ma studio Python nel "
    "tempo libero e mi appassiona l'intelligenza artificiale; il weekend "
    "faccio spesso arrampicata."
)


# --------------------------------------------------- TODO 1 · col docente 🎤
class PersonaEstratta(BaseModel):
    """Nome, cognome e interessi — una LISTA, non una frase.

    TODO: aggiungere i campi (vedi slide "Lo JSON Schema, per intero").
    """


# --------------------------------------------------- TODO 1 · col docente 🎤
def estrai_persona(testo):
    """Chiede al modello un oggetto PersonaEstratta e lo restituisce già
    validato — non una stringa su cui fare il parsing."""
    raise NotImplementedError


# --------------------------------------------------- TODO 2 · col docente 🎤
def estrai_persona_con_retry(testo):
    """Come estrai_persona, ma con un secondo tentativo se qualcosa va
    storto (rete, timeout, un ValidationError inatteso) — UN retry solo,
    non un loop infinito."""
    raise NotImplementedError


def cerca_corsi(interesse):
    """Il payoff dell'esempio guida: non un vero motore di ricerca corsi,
    solo la query pulita che ora si può finalmente scrivere."""
    print(f"cerco corsi su: {interesse}")


# ---------------------------------------------------------------------------
# ESERCIZIO GUIDATO (⌨️ da soli) — TODO 3
#
# Applicate il metodo della slide "Suggerimento: come costruire uno JSON
# Schema" sul testo di un botanico: valori veri → tipi → enum dove i valori
# sono un insieme chiuso e ricorrente → ripetere sui nested object (le
# piante, una lista di oggetti).
# ---------------------------------------------------------------------------
TESTO_BOTANICO = (
    "Mi chiamo Marco Ferretti e lavoro come botanico da quindici anni, "
    "attualmente all'Orto Botanico di Padova. A casa ho un piccolo "
    "giardino con alcune piante a cui tengo particolarmente. C'è un Ficus "
    "lyrata che sta in salotto vicino alla finestra, in pieno sole, e che "
    "innaffio ogni sette giorni. Poi c'è una Monstera deliciosa, che "
    "invece preferisce la luce indiretta e va bagnata ogni dieci giorni. "
    "Ho anche un piccolo cactus, un Echinocactus grusonii, che vive in "
    "pieno sole e che innaffio molto di rado, più o meno ogni trenta "
    "giorni."
)


# TODO 3 · da soli
class EsposizioneLuce(str, Enum):
    """Insieme CHIUSO di valori — non testo libero: il modello non può
    inventarne un quarto.

    TODO: aggiungere i valori (pieno sole / luce indiretta / ombra).
    """


# TODO 3 · da soli
class Pianta(BaseModel):
    """Una pianta del giardino: nome, esposizione (enum), frequenza di
    annaffiatura in giorni.

    TODO: aggiungere i campi.
    """


# TODO 3 · da soli
class PersonaBotanica(BaseModel):
    """Il botanico e il suo giardino — piante come lista di oggetti
    annidati (Pianta).

    TODO: aggiungere i campi.
    """


# TODO 3 · da soli
def estrai_botanico(testo):
    """Stesso pattern di estrai_persona, sul nuovo schema PersonaBotanica."""
    raise NotImplementedError


if __name__ == "__main__":
    persona = estrai_persona_con_retry(TESTO_GIULIA)
    print(persona)
    print(persona.model_dump_json())

    print()
    for interesse in persona.interessi:
        cerca_corsi(interesse)

    print()
    botanico = estrai_botanico(TESTO_BOTANICO)
    print(botanico)
