"""rag.py — la pipeline RAG del modulo: un file, tre funzioni, una CONFIG.

È il salto rispetto ad app.py del Progetto Modulo 2, ed è uno solo: là le
quattro funzioni erano scritte una dietro l'altra e i parametri (k, chunk
size, modello) stavano sparsi nel codice; qui i parametri vivono in un unico
punto di configurazione — il dizionario CONFIG qui sotto — e rispondi()
ritorna la risposta INSIEME ai chunk usati. Senza sapere cosa è stato
recuperato non si diagnostica niente: da stasera ogni lezione del modulo
lavora su questa pipeline.

Le tre funzioni sono le tre interfacce dell'architettura RAG
(Modulo 3 · Lezione 1):

    indicizza()            l'INGEST: corpus → chunk → embedding → collection
    recupera(query, k)     il RETRIEVE: domanda → i k chunk più pertinenti
    rispondi(query)        il GENERATE: domanda → (risposta, chunk usati)

TODO 1 (🎤 live coding): indicizza(), la scriviamo insieme.
TODO 2 e TODO 3 (⌨️ da soli): recupera() e rispondi().

Uso (dalla cartella scripts/):
    python working/rag.py
"""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from dotenv import load_dotenv               # noqa: E402
from openai import OpenAI                    # noqa: E402

from aikit.loaders import load               # noqa: E402 — Modulo 2 · Lezione 4
from aikit.clean import clean, pipeline_for  # noqa: E402 — Modulo 2 · Lezione 5
from aikit.chunk import chunk_recursive      # noqa: E402 — Modulo 2 · Lezione 10
from aikit.embeddings import embed           # noqa: E402 — Modulo 2 · Lezione 7
from aikit import vectorstore                # noqa: E402 — Modulo 2 · Lezione 9

load_dotenv()

client = OpenAI()

# ---------------------------------------- il punto unico di configurazione
# Tutto ciò che nel Progetto Modulo 2 stava sparso nel codice ora sta qui:
# per cambiare un parametro si tocca UNA riga, e si vede subito cosa c'è da
# tarare. Da Modulo 3 · Lezione 4 in poi le manopole si girano da qui.
CONFIG = {
    "corpus_dir": SCRIPTS / "dataset" / "lumen_m3",  # i sei documenti Lumen
    "collection": "lumen_m3",       # la collection del modulo, si indicizza una volta
    "chunk_size": 500,              # recursive, come nel Modulo 2
    "k": 4,                         # chunk recuperati per domanda
    "modello": "gpt-4o-mini",       # il generator
}

# Le domande di prova del main: una sui documenti storici, una sui documenti
# nuovi del corpus esteso, una FUORI corpus (deve uscire il rifiuto pulito).
DOMANDA_STORICA = "Quanto tempo ho per richiedere il contributo per la postazione di casa?"
DOMANDA_NUOVA = "Quanto costa il vassoio portacavi e come si fissa?"
DOMANDA_FUORI = "Posso pagare alla consegna, in contrassegno?"


# ------------------------------------------------------------- TODO 1 · 🎤
def indicizza():
    """L'ingest: load → clean → chunk → embed → upsert, su tutto il corpus.

    Ricrea la collection da ZERO (vectorstore.crea_collection): rilanciare
    non raddoppia i chunk. Stampa il conteggio per documento e ritorna il
    numero totale di chunk indicizzati. Id dei chunk: "<documento>-<numero>"
    (es. "manuale-lumadesk-007"), metadata {"source": nome del file}.
    """
    raise NotImplementedError  # TODO 1: la scriviamo insieme (live coding)


# ------------------------------------------------------------- TODO 2 · ⌨️
def recupera(query, k=None):
    """Il retrieve: i k chunk più pertinenti per la query, dal più simile.

    Ogni chunk è un dict {"id", "testo", "score", "source"}. Se k non è
    indicato vale quello di CONFIG. La collection si riapre qui dentro con
    vectorstore.apri_collection(CONFIG["collection"]).
    """
    raise NotImplementedError  # TODO 2


# ------------------------------------------------------------- TODO 3 · ⌨️
def rispondi(query):
    """Il generate: risposta con citazioni, insieme ai chunk usati.

    Il prompt è quello di Modulo 2 · Lezione 11 — sezioni marcate, risposta
    SOLO dai documenti, citazione della fonte tra parentesi quadre, rifiuto
    pulito quando la risposta non c'è. Ritorna (risposta, chunks): i chunk
    che hanno fatto da contesto sono lo strumento di debug del modulo.
    """
    raise NotImplementedError  # TODO 3


# ------------------------------------------------- helper di stampa (dati)
def stampa_chunks(chunks):
    """I chunk recuperati, uno per riga: posizione, id, score, anteprima."""
    for posizione, c in enumerate(chunks, start=1):
        anteprima = " ".join(c["testo"].split())[:58]
        print(f"   {posizione}. {c['id']}  score={c['score']:.3f}  {anteprima}…")


if __name__ == "__main__":
    # L'ingest si fa una volta: se la collection è già piena non si ripaga.
    # Per ricostruirla da zero (corpus cambiato): chiamare indicizza() a mano.
    try:
        collection = vectorstore.apri_collection(CONFIG["collection"])
        if collection.count() == 0:
            indicizza()
            # crea_collection ricrea da zero: il riferimento va riaperto
            collection = vectorstore.apri_collection(CONFIG["collection"])
        print(f"collection '{CONFIG['collection']}': {collection.count()} chunk")
    except NotImplementedError:
        raise SystemExit("indicizza() è ancora da scrivere: si parte da lì.")

    for domanda in (DOMANDA_STORICA, DOMANDA_NUOVA, DOMANDA_FUORI):
        print("\n" + "=" * 72)
        print(f"D: {domanda}")
        try:
            chunks = recupera(domanda)
        except NotImplementedError:
            print("   recupera(): ancora da scrivere")
            continue
        stampa_chunks(chunks)
        try:
            risposta, usati = rispondi(domanda)
        except NotImplementedError:
            print("   rispondi(): ancora da scrivere")
            continue
        print(f"→ {risposta}")
