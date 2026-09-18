"""assistente.py — un assistente con due tool: i documenti e il database.

Fin qui il sistema faceva una cosa sola: il RAG rispondeva dai sei documenti
Lumen (Modulo 3 · Lezione 2-6), il giro del tool calling dal database degli
ordini (Modulo 3 · Lezione 7-8). Oggi un assistente unico riceve la domanda
e SCEGLIE: cerca nei documenti, interroga il database, o tutti e due. E
quando nessuno dei due ha la risposta, lo dice invece di inventare.

Il file, dall'alto in basso:

  costanti             MODELLO, K (quanti chunk rimanda cerca_documenti),
                       MAX_CHIAMATE; DOMANDE (una per strada, più una senza
                       risposta), LAB2 (True: il main fa anche le domande di
                       working/domande_lab2.py), LE_MIE_DOMANDE, SOLO
  TODO 2 (Lab 1b)      CercaDocumenti + cerca_documenti(domanda): il RAG come
                       tool. Sta SOPRA il TODO 1 perché TOOLS ha bisogno
                       della classe, ma si scrive dopo.
  TODO 1 (Lab 1a)      TOOLS, la lista che il modello vede, e i rami di
                       esegui(): prima query_db (Lab 1a), poi cerca_documenti
                       (Lab 1b)
  TODO 3 (Lab 1c)      ISTRUZIONI: quando usare quale tool, le citazioni, il
                       rifiuto
  chiedi(domanda)      il giro di Modulo 3 · Lezione 7-8, con dentro il
                       TODO 1 (Lab 1a): eseguire le function_call e rimandare
                       i risultati al modello
  dato                 strada(usati), gli helper di stampa, il main, che in
                       fondo stampa la tabella strada attesa / strada presa

Nel Lab 2 si mette LAB2 = True (le domande sono in working/domande_lab2.py,
le vostre in LE_MIE_DOMANDE), ogni esito va in working/griglia.md, e si
sistema con due leve:
le ISTRUZIONI e la descrizione di cerca_documenti. La consegna completa è in
CONSEGNA.md.

Uso (dalla cartella scripts/):
    python working/assistente.py
"""
import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))   # il solito prologo del modulo: rende importabile aikit/
sys.path.insert(0, str(SCRIPTS / "working"))       # e working/: domande_lab2.py, le domande del Lab 2

from dotenv import load_dotenv                   # noqa: E402
from openai import OpenAI                        # noqa: E402
from pydantic import BaseModel                   # noqa: E402 — Modulo 2 · Lezione 13

from aikit import rag                            # noqa: E402 — Modulo 3 · Lezione 2: recupera()
from aikit import vectorstore                    # noqa: E402 — Modulo 2 · Lezione 9: la collection
from aikit.llm_client import cost_usd            # noqa: E402 — Modulo 2 · Lezione 3
from aikit.tools import QueryDb, query_db, definisci_tool   # noqa: E402 — Modulo 3 · Lezione 8, promosso oggi
from domande_lab2 import DOMANDE_LAB2               # noqa: E402 — working/domande_lab2.py: le domande del Lab 2

load_dotenv(SCRIPTS / ".env")                    # OPENAI_API_KEY
client = OpenAI()

MODELLO = "gpt-5.6-luna"                         # è in PRICING di llm_client: cost_usd sa quanto costa. Nell'output arrivano anche item "reasoning": tornano nell'input con il resto
K = 4                                            # quanti chunk cerca_documenti rimanda al modello (la baseline di rag.py)
MAX_CHIAMATE = 6                                 # il tetto al giro, come a Modulo 3 · Lezione 8

# Le domande del main, ognuna con la STRADA ATTESA: "documenti", "dati",
# "documenti+dati" quando servono tutti e due, "nessuna" quando la risposta
# non sta da nessuna parte e l'assistente deve dirlo.
DOMANDE = [
    ("Entro quanti giorni posso restituire un prodotto comprato online?", "documenti"),
    ("Quanti ordini ha fatto Giulia Moretti?", "dati"),
    ("Lorenzo Rossi può montare il braccio LMX-4400 sulle scrivanie che ha ordinato?", "documenti+dati"),
    ("Che tempo fa oggi a Padova?", "nessuna"),
]
LAB2 = False             # Lab 2: True, e il main fa anche le DOMANDE_LAB2 di working/domande_lab2.py
LE_MIE_DOMANDE = [       # Lab 2: le domande vostre, nella stessa forma (domanda, strada attesa)
]
SOLO = None              # una domanda sola al posto delle altre: SOLO = "Quanti ordini ha fatto Giulia Moretti?"


# ------------------------------------------- TODO 2 (Lab 1b) · il RAG come tool · ⌨️
class CercaDocumenti(BaseModel):                 # la docstring è la descrizione che il modello legge
    """TODO 2: riscrivi questa riga, il modello la legge così com'è: cosa cerca il tool, in quali documenti, cosa ritorna."""
    domanda: str


def cerca_documenti(domanda):
    """Il RAG come tool: i K chunk più pertinenti per la domanda
    (rag.recupera(domanda, K): dict con id, testo, score, source),
    restituiti come UN testo in cui ogni chunk ha davanti il suo id tra
    parentesi quadre, così il modello può citarlo. Ritorna una stringa."""
    raise NotImplementedError("TODO 2: cerca_documenti()")


# ------------------------------------ TODO 1 (Lab 1a) · la lista dei tool e i rami · ⌨️
# La lista che il modello vede a ogni chiamata, con definisci_tool(schema,
# nome): nel Lab 1a solo query_db (schema e funzione arrivano da
# aikit/tools.py), nel Lab 1b anche cerca_documenti.
TOOLS = [
    # TODO 1: query_db (Lab 1a), poi cerca_documenti (Lab 1b)
]


def esegui(nome, argomenti):
    """Esegue il tool che il modello ha chiesto: nome come in TOOLS,
    argomenti già convertiti in dict. Un ramo per tool, come a Modulo 3 ·
    Lezione 8. Ritorna il risultato."""
    # TODO 1: un ramo per tool
    raise ValueError(f"tool sconosciuto: {nome}")


# ------------------------------------------- TODO 3 (Lab 1c) · le istruzioni · ⌨️
# Valgono a ogni chiamata del giro. Dicono al modello quando usare quale
# tool, come citare i documenti e cosa fare quando la risposta non c'è: le
# regole di citazione e di rifiuto di rag.py ora stanno qui.
ISTRUZIONI = """Rispondi in italiano, in una frase."""   # TODO 3: le istruzioni dell'assistente (queste sono quelle di Modulo 3 · Lezione 7)


# ------------------------------- il giro, con dentro il TODO 1 (Lab 1a)
def chiedi(domanda):
    """Il giro del tool calling di Modulo 3 · Lezione 7-8, con una cosa in
    più: registra i tool chiamati (usati) e li ritorna insieme alla
    risposta, così il main può dire quale STRADA ha preso il modello.
    Chiama il modello con la domanda, le ISTRUZIONI e la lista dei tool;
    se nell'output ci sono item function_call, esegue ognuno e rimanda il
    risultato come function_call_output con lo stesso call_id; ripete
    finché il modello risponde con testo, o fino a MAX_CHIAMATE.
    Ritorna (risposta, usati)."""
    storia = [{"role": "user", "content": domanda}]   # la conversazione: la domanda, poi ciò che si aggiunge a ogni giro
    usati = []                                   # i tool chiamati, in ordine: il log della strada
    n_chiamate = 0
    costo = 0.0
    while True:
        if n_chiamate == MAX_CHIAMATE:           # il tetto al giro
            stampa_costo(n_chiamate, costo)
            return f"(mi fermo: {MAX_CHIAMATE} chiamate senza una risposta)", usati
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
            return r.output_text, usati

        # ---- TODO 1 (Lab 1a) · eseguire le function_call e rimandare i risultati · ⌨️
        # Per ogni chiamata: gli argomenti (chiamata.arguments è una STRINGA
        # JSON), il risultato con esegui(), il nome nel log, la stampa, e il
        # risultato in storia come function_call_output con lo stesso call_id.
        for chiamata in chiamate:                # può chiederne più d'uno nella stessa risposta
            raise NotImplementedError("TODO 1: eseguire la function_call e rimandare il risultato")


# ------------------------------------------------------ dato · la strada
def strada(usati):
    """Dai tool chiamati alla STRADA della risposta: "documenti" se ha
    usato cerca_documenti, "dati" se query_db, "documenti+dati" se tutti
    e due, "nessuna" se non ha chiamato nessun tool."""
    documenti = "cerca_documenti" in usati
    dati = "query_db" in usati
    if documenti and dati:
        return "documenti+dati"
    if documenti:
        return "documenti"
    if dati:
        return "dati"
    return "nessuna"


# ------------------------------------------------- helper di stampa (dati)
# Producono le righe «chiamata 1  [512 token in, 27 out] …» che si vedono a schermo.
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
    """Il risultato di un tool può essere lungo (i chunk, le righe di una
    query): se ne stampano al massimo sei righe, il modello riceve tutto."""
    righe = str(risultato).split("\n")
    print(f"      eseguo {nome}: " + righe[0])
    for riga in righe[1:6]:
        print("         " + riga)
    if len(righe) > 6:
        print(f"         … altre {len(righe) - 6} righe")


def stampa_costo(n, costo):
    print(f"   {n} chiamat{'a' if n == 1 else 'e'} · ${costo:.5f}")


def stampa_tabella(esiti):
    """La tabella del giro: una riga per domanda con la strada attesa e
    quella presa. esiti è una lista di (domanda, attesa, presa). È la
    tabella che si confronta prima e dopo una leva (Lab 2)."""
    print("\n\n" + "#" * 78)
    print(f"# RIASSUNTO · K {K} · strada attesa / strada presa")
    print("#" * 78)
    print(f"  {'domanda':<46} {'attesa':<15} {'presa':<15} uguale?")
    uguali = 0
    for domanda, attesa, presa in esiti:
        uguali += attesa == presa
        print(f"  {domanda[:46]:<46} {attesa:<15} {presa:<15} {'sì' if attesa == presa else 'NO'}")
    print(f"\n  strada giusta: {uguali}/{len(esiti)}")


if __name__ == "__main__":
    # La collection del modulo: si indicizza solo se manca (la prima volta:
    # 82 chunk, un paio di minuti, meno di un centesimo).
    if vectorstore.apri_collection(rag.CONFIG["collection"]).count() == 0:
        rag.indicizza()

    domande = [(SOLO, None)] if SOLO else DOMANDE + (DOMANDE_LAB2 if LAB2 else []) + LE_MIE_DOMANDE
    esiti = []
    for domanda, attesa in domande:
        print("\n" + "=" * 78)
        print(f"D: {domanda}")
        try:
            risposta, usati = chiedi(domanda)
        except NotImplementedError as e:
            raise SystemExit(f"ancora da scrivere: {e}")
        except ValueError as e:
            raise SystemExit(f"{e}: il tool è in TOOLS ma manca il ramo in esegui(), o il nome è scritto diverso")
        print(f"→ {risposta}")
        print(f"   strada: {strada(usati)}  (tool: {' → '.join(usati) if usati else 'nessuno'})")
        esiti.append((domanda, attesa, strada(usati)))
    if not SOLO:
        stampa_tabella(esiti)
