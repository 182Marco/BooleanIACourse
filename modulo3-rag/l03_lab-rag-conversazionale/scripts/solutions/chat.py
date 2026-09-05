"""chat.py — il RAG della lezione scorsa regge una conversazione.

rag.py (Modulo 3 · Lezione 2, da oggi in aikit/) risponde a UNA domanda
alla volta: dentro recupera() entra la domanda così com'è, e «E per il
secondo caso?» non contiene nessuna delle parole che servono a ritrovare
il chunk giusto. Qui la pipeline diventa conversazionale in tre passi:

  Lab 1  la STORIA dei messaggi davanti al prompt RAG — la porta
         rag.genera(chunks, domanda, storia), scritta nel live coding di
         apertura — col troncamento per budget di token di Modulo 2 ·
         Lezione 3 (estratto dalla classe Chatbot in funzioni piatte);
  Lab 2  la QUERY CONDENSATION: la domanda di follow-up viene riscritta
         dal modello, usando la storia, in una domanda che sta in piedi da
         sola — ed è QUELLA che va al retrieval e alla generazione;
  Lab 3  la SUMMARY MEMORY (la parte vecchia della storia diventa un
         riassunto invece di sparire) e le SESSIONI su file JSON.

In storia vanno solo domanda e risposta di ogni turno, MAI i chunk: i
documenti recuperati entrano nel prompt del turno e basta, altrimenti la
storia esplode in pochi turni.

Dopo il live coding rag.py non si tocca più: qui si chiamano
rag.recupera() e rag.genera(). La riscrittura della domanda, il riassunto
e le sessioni sono cose della conversazione, non della pipeline: stanno
in questo file. La consegna dei tre lab, con il criterio di "fatto" di
ogni TODO, è in CONSEGNA.md. Se all'avvio esce AttributeError su
rag.genera, il live coding su scaffolding/aikit/rag.py è rimasto
indietro: si copia solutions/aikit/rag.py al suo posto.

Uso (dalla cartella scripts/):
    python solutions/chat.py
"""
import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

import tiktoken                              # noqa: E402 — Modulo 2 · Lezione 2-3
from dotenv import load_dotenv               # noqa: E402
from openai import OpenAI                    # noqa: E402

from aikit import rag                        # noqa: E402 — Modulo 3 · Lezione 2-3

load_dotenv()

client = OpenAI()

# ---------------------------------------- le manopole della conversazione
# Quelle della pipeline (corpus, k, modello) restano in rag.CONFIG.
CONFIG = {
    "budget_token": 350,                # quanta storia rispediamo al massimo (stretto apposta)
    "memoria": "buffer",                # "buffer" (Lab 1) o "riassunto" (Lab 3)
    "sessioni_dir": SCRIPTS / "sessioni",   # un file JSON per sessione (Lab 3)
}

_encoder = tiktoken.get_encoding("o200k_base")


def conta_token(storia):
    """I token della storia: quelli che rispediamo al modello a ogni turno."""
    return sum(len(_encoder.encode(m["content"])) for m in storia)


# ------------------------------------------------------------- TODO 1 · ⌨️
def tronca(storia):
    """Buffer memory (Modulo 2 · Lezione 3): toglie i messaggi più vecchi
    finché la storia sta in CONFIG["budget_token"]. Modifica la lista sul
    posto e ritorna quanti messaggi ha tolto."""
    tolti = 0
    while len(storia) > 2 and conta_token(storia) > CONFIG["budget_token"]:
        storia.pop(0)
        tolti += 1
    return tolti


# ------------------------------------------------------------- TODO 2 · ⌨️
def rispondi_in_chat(storia, domanda):
    """Un turno di conversazione sopra rag.recupera() e rag.genera().

    Riscrive la domanda con la storia (Lab 2), recupera i chunk, genera la
    risposta con la storia davanti al prompt (rag.genera), e aggiunge alla
    storia la domanda com'era e la risposta (senza i chunk). Alla fine
    tiene la storia nel budget: tronca() o riassumi(), secondo
    CONFIG["memoria"]. Ritorna (risposta, chunks, domanda_cercata).
    """
    # Lab 2: la domanda che va al retrieval è quella riscritta con la storia.
    if storia:
        domanda_cercata = condensa(storia, domanda)
    else:
        domanda_cercata = domanda

    chunks = rag.recupera(domanda_cercata)
    # Alla generazione vanno la domanda riscritta (coerente coi chunk) e la
    # storia: rag.genera() la mette davanti al messaggio del turno.
    risposta = rag.genera(chunks, domanda_cercata, storia)

    # In storia vanno domanda e risposta, MAI i chunk.
    storia.append({"role": "user", "content": domanda})
    storia.append({"role": "assistant", "content": risposta})

    # Lab 1: la storia resta nel budget, turno dopo turno (Lab 3: o si
    # riassume). Quello che sopravvive qui è tutto ciò che il prossimo
    # turno saprà del passato.
    if CONFIG["memoria"] == "riassunto":
        riassumi(storia)
    else:
        tronca(storia)
    return risposta, chunks, domanda_cercata


# ------------------------------------------------------------- TODO 3 · ⌨️
def condensa(storia, domanda):
    """Query condensation: riscrive la domanda usando la storia, così che
    stia in piedi da sola (nomi al posto dei pronomi, il tema della
    conversazione dentro la domanda). Una chiamata al modello; ritorna la
    domanda riscritta, come stringa. Se la domanda è già autonoma, il
    modello la lascia com'è."""
    conversazione = ""
    for m in storia:
        chi = "Utente" if m["role"] == "user" else "Assistente"
        conversazione += f"{chi}: {m['content']}\n"

    prompt = f"""Qui sotto c'è una conversazione e una nuova domanda dell'utente.
Riscrivi la nuova domanda in modo che sia comprensibile DA SOLA, senza la
conversazione: sostituisci pronomi e riferimenti ("quello", "il secondo
caso", "e per la wide?") con ciò a cui si riferiscono. Se la domanda è già
autonoma, ricopiala uguale. Rispondi SOLO con la domanda riscritta.

<conversazione>
{conversazione}</conversazione>

<nuova_domanda>
{domanda}
</nuova_domanda>"""

    r = client.responses.create(
        model=rag.CONFIG["modello"],
        input=[{"role": "user", "content": prompt}],
    )
    return r.output_text.strip()


# ------------------------------------------------------------- TODO 4 · ⌨️
def riassumi(storia):
    """Summary memory: se la storia sfora CONFIG["budget_token"], tutti i
    messaggi tranne gli ultimi due (l'ultimo turno) vengono sostituiti da
    UN messaggio di riassunto scritto dal modello — un messaggio "user"
    che inizia con «Riassunto della conversazione finora: …», seguito da un
    "assistant" di presa d'atto per tenere l'alternanza. Un riassunto
    precedente, se c'è, viene assorbito nel nuovo. Modifica la lista sul
    posto e ritorna il riassunto (o None se non serviva)."""
    if conta_token(storia) <= CONFIG["budget_token"] or len(storia) <= 2:
        return None

    vecchi, ultimo_turno = storia[:-2], storia[-2:]
    conversazione = ""
    for m in vecchi:
        chi = "Utente" if m["role"] == "user" else "Assistente"
        conversazione += f"{chi}: {m['content']}\n"

    prompt = f"""Riassumi la conversazione qui sotto in poche righe, in italiano,
conservando ogni fatto concreto emerso (prodotti, codici, cifre, tempi,
condizioni) e le fonti citate tra parentesi quadre. Niente premesse:
solo il riassunto.

<conversazione>
{conversazione}</conversazione>"""

    r = client.responses.create(
        model=rag.CONFIG["modello"],
        input=[{"role": "user", "content": prompt}],
    )
    riassunto = r.output_text.strip()
    storia[:] = [{"role": "user", "content": f"Riassunto della conversazione finora: {riassunto}"},
                 {"role": "assistant", "content": "D'accordo, ne tengo conto."}] + ultimo_turno
    return riassunto


# ------------------------------------------------------------- TODO 5 · ⌨️
def salva_sessione(nome, storia):
    """Scrive la storia in CONFIG["sessioni_dir"]/<nome>.json (la cartella
    si crea se manca)."""
    cartella = CONFIG["sessioni_dir"]
    cartella.mkdir(exist_ok=True)
    with open(cartella / f"{nome}.json", "w", encoding="utf-8") as f:
        json.dump(storia, f, ensure_ascii=False, indent=2)


def carica_sessione(nome):
    """Ritorna la storia salvata con quel nome, o una lista vuota se la
    sessione non esiste ancora."""
    percorso = CONFIG["sessioni_dir"] / f"{nome}.json"
    if not percorso.exists():
        return []
    with open(percorso, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------- il loop (dato)
if __name__ == "__main__":
    # La collection del modulo: si indicizza solo se è vuota (come a
    # Modulo 3 · Lezione 2, costa meno di un centesimo).
    if rag.vectorstore.apri_collection(rag.CONFIG["collection"]).count() == 0:
        rag.indicizza()

    nome = input("Nome della sessione (invio per non salvare): ").strip()
    storia = []
    if nome:
        try:
            storia = carica_sessione(nome)
            print(f"sessione '{nome}': {len(storia)} messaggi ripresi")
        except NotImplementedError:
            print("carica_sessione(): ancora da scrivere, si parte da zero")

    print(f"Chat sul corpus Lumen — memoria: {CONFIG['memoria']}, "
          f"budget {CONFIG['budget_token']} token. 'exit' per uscire.\n")
    while True:
        testo = input("Tu> ").strip()
        if testo.lower() in {"exit", "quit"}:
            break
        if not testo:
            continue
        prima = len(storia)
        try:
            risposta, chunks, cercata = rispondi_in_chat(storia, testo)
        except NotImplementedError as e:
            raise SystemExit("c'è ancora un TODO da scrivere: "
                             "il main si ferma qui.") from e
        except AttributeError as e:
            if "genera" not in str(e):
                raise
            raise SystemExit("rag.genera() non c'è: il live coding su "
                             "scaffolding/aikit/rag.py è rimasto indietro. "
                             "Copia solutions/aikit/rag.py al suo posto.") from e
        if cercata != testo:
            print(f"   ↳ cercato: {cercata}")
        rag.stampa_chunks(chunks)
        print(f"\nBot> {risposta}")
        print(f"   [storia: {len(storia)} messaggi, {conta_token(storia)}/"
              f"{CONFIG['budget_token']} token]")
        if len(storia) < prima + 2:          # la memoria ha fatto spazio
            if CONFIG["memoria"] == "riassunto":
                print(f"   [riassunto] {storia[0]['content']}")
            else:
                print(f"   [buffer] tolti i {prima + 2 - len(storia)} messaggi più vecchi")
        print()
        if nome:
            try:
                salva_sessione(nome, storia)
            except NotImplementedError:
                pass
