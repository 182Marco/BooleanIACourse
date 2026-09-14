"""tools.py — il giro del tool calling, scritto a mano.

Il modello non esegue niente: non sa che giorno è, non fa i conti esatti,
non tocca dati. Senza tool a «Che giorno è oggi?» risponde «27 aprile
2024» e a «Quanto fa 849 diviso 1,22?» risponde 696,72 (giusto: 695,90).
Con i tool gli diamo una lista di funzioni NOSTRE: lui decide se e quale
chiamare, e con quali argomenti; noi la eseguiamo e gli rimandiamo il
risultato; lui risponde. Tutto il tool calling è questo giro, ripetuto.

Il file, dall'alto in basso:

  1 (codice spiegato)   Calcolatrice, lo schema Pydantic degli argomenti
                        (Modulo 2 · Lezione 13), e calcolatrice(), la
                        funzione che li esegue;
  TODO (esercizio)      il secondo tool: DataOggi + data_oggi(), la voce
                        in TOOLS, il ramo in esegui();
  2 (codice spiegato)   definisci_tool(): dallo schema alla definizione
                        che l'API si aspetta; TOOLS, la lista che il
                        modello vede;
  3 (codice spiegato)   esegui(nome, argomenti): il tool chiesto dal
                        modello, eseguito da noi;
  4 (codice spiegato)   chiedi(domanda): il giro — chiama il modello, se
                        nell'output ci sono function_call le esegue e
                        rimanda i risultati, ripete finché arriva testo.

Il main fa le quattro DOMANDE (solo calcolo, solo data, entrambe,
nessuna) e stampa ogni passo del giro con i token e il costo. La
consegna completa è in CONSEGNA.md.

Uso (dalla cartella scripts/):
    python working/tools.py
"""
import json
import sys
from datetime import date
from pathlib import Path
from typing import Literal

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))   # il solito prologo del modulo: rende importabile aikit/

from dotenv import load_dotenv                   # noqa: E402
from openai import OpenAI                        # noqa: E402
from pydantic import BaseModel                   # noqa: E402 — Modulo 2 · Lezione 13

from aikit.llm_client import cost_usd            # noqa: E402 — Modulo 2 · Lezione 3

load_dotenv(SCRIPTS / ".env")                    # OPENAI_API_KEY
client = OpenAI()

MODELLO = "gpt-4.1-mini"                         # è in PRICING di llm_client: cost_usd sa quanto costa
ISTRUZIONI = "Rispondi in italiano, in una frase, senza domande di cortesia."   # valgono a ogni chiamata del giro

# Le quattro domande del main: solo calcolo, solo data, entrambe, nessuna.
DOMANDE = [
    "Quanto fa 849 diviso 1,22?",
    "Che giorno è oggi?",
    "Che giorno è oggi, e quanto fa 849 per 7?",
    "Cos'è una scrivania regolabile in altezza?",
]
SOLO = None      # una domanda sola al posto delle quattro, per provare: SOLO = "Che giorno è oggi?"


# ------------------------ 1 · la calcolatrice · 🎤 codice spiegato, già scritta
class Calcolatrice(BaseModel):                   # la docstring qui sotto è la descrizione che il modello legge
    """Esegue un'operazione aritmetica tra due numeri e ritorna il risultato esatto."""
    a: float
    b: float
    operazione: Literal["+", "-", "*", "/"]      # nello schema diventa un enum: il modello non può inventarne altre


def calcolatrice(a, b, operazione):
    """La funzione vera: la eseguiamo NOI, il modello la chiede soltanto."""
    if operazione == "+":
        return a + b
    if operazione == "-":
        return a - b
    if operazione == "*":
        return a * b
    return a / b


# ------------------------------------------------- TODO · il secondo tool · ⌨️
# Lo schema DataOggi (una classe senza campi: il tool non ha argomenti, e la
# docstring è la descrizione) e la funzione data_oggi(), senza argomenti, che
# ritorna la data di oggi come stringa (date.today().isoformat()). Poi la
# voce in TOOLS e il ramo in esegui(), qui sotto: il nome "data_oggi" deve
# combaciare nei due punti.


# ---------------------- 2 · la definizione dei tool · 🎤 codice spiegato, già scritta
def definisci_tool(schema, nome):
    """Dallo schema Pydantic alla definizione che l'API si aspetta: un
    dict con il nome, la descrizione (la docstring dello schema) e i
    parametri in JSON Schema (model_json_schema()). È il testo che il
    modello legge per decidere SE e COME chiamare il tool."""
    return {
        "type": "function",
        "name": nome,
        "description": schema.__doc__,
        "parameters": schema.model_json_schema(),
        "strict": False,                         # la modalità strict vuole uno schema più rigido di questo: stasera non serve
    }


# La lista che il modello vede a ogni chiamata.
TOOLS = [
    definisci_tool(Calcolatrice, "calcolatrice"),
    # TODO: il secondo tool → definisci_tool(DataOggi, "data_oggi")
]


# ---------------------------- 3 · l'esecuzione · 🎤 codice spiegato, già scritta
def esegui(nome, argomenti):
    """Esegue il tool che il modello ha chiesto: nome come in TOOLS,
    argomenti già convertiti in dict. Ritorna il risultato."""
    if nome == "calcolatrice":
        return calcolatrice(argomenti["a"], argomenti["b"], argomenti["operazione"])
    # TODO: il ramo del secondo tool → if nome == "data_oggi": …
    raise ValueError(f"tool sconosciuto: {nome}")


# ------------------------------- 4 · il giro · 🎤 codice spiegato, già scritta
def chiedi(domanda):
    """Il giro del tool calling. Chiama il modello con la domanda e la
    lista dei tool; se nell'output ci sono item function_call, esegue
    ognuno e rimanda il risultato come function_call_output con lo
    stesso call_id; ripete finché il modello risponde con testo.
    Ritorna il testo della risposta."""
    storia = [{"role": "user", "content": domanda}]   # la conversazione: la domanda, poi ciò che si aggiunge a ogni giro
    n_chiamate = 0
    costo = 0.0
    while True:                                  # si ferma alla prima risposta in testo (stasera basta così)
        r = client.responses.create(
            model=MODELLO,
            instructions=ISTRUZIONI,
            input=storia,
            tools=TOOLS,
        )
        n_chiamate += 1
        costo += cost_usd(MODELLO, r.usage.input_tokens, r.usage.output_tokens)
        stampa_chiamata(n_chiamate, r)

        storia += r.output                       # TUTTO l'output torna nell'input, anche le function_call
        chiamate = [item for item in r.output if item.type == "function_call"]
        if not chiamate:                         # niente da eseguire: è la risposta
            stampa_costo(n_chiamate, costo)
            return r.output_text                 # il testo del message, già estratto dagli item

        for chiamata in chiamate:                # può chiederne più d'uno nella stessa risposta
            argomenti = json.loads(chiamata.arguments)   # arguments è una STRINGA JSON
            risultato = esegui(chiamata.name, argomenti)
            stampa_esecuzione(chiamata.name, argomenti, risultato)
            storia.append({
                "type": "function_call_output",
                "call_id": chiamata.call_id,     # lo stesso della richiesta: così il modello sa a cosa risponde
                "output": str(risultato),        # sempre una stringa
            })


# ------------------------------------------------- helper di stampa (dati)
# Producono le righe «chiamata 1  [137 token in, 27 out] …» che si vedono a schermo.
def stampa_chiamata(n, r):
    """Una riga per chiamata: i token e cosa c'è nell'output."""
    item = []
    for i in r.output:
        if i.type == "function_call":
            item.append(f"function_call {i.name}({i.arguments})")
        else:
            item.append(i.type)
    print(f"   chiamata {n}  [{r.usage.input_tokens} token in, {r.usage.output_tokens} out]  output: " + " · ".join(item))


def stampa_esecuzione(nome, argomenti, risultato):
    print(f"      eseguo {nome}({argomenti}) = {risultato}")


def stampa_costo(n, costo):
    print(f"   {n} chiamat{'a' if n == 1 else 'e'} · ${costo:.5f}")


if __name__ == "__main__":
    domande = [SOLO] if SOLO else DOMANDE
    for domanda in domande:
        print("\n" + "=" * 72)
        print(f"D: {domanda}")
        risposta = chiedi(domanda)
        print(f"→ {risposta}")
