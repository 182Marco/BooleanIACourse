"""app.py — Progetto Modulo 2: tutta la pipeline, sul vostro corpus.

Un solo file per tutta la giornata (Modulo 2 · Lezione 15). Non c'è niente di
concettualmente nuovo: ogni funzione qui sotto riusa una lezione già fatta.
Mettete i vostri documenti in dataset/mio_corpus/ (o copiate lì la riserva
Lumen, dataset/riserva_lumen/, se non avete nulla di pronto) e scrivete le
quattro funzioni sotto.

    python working/app.py
"""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from dotenv import load_dotenv             # noqa: E402
from openai import OpenAI                  # noqa: E402
from pydantic import BaseModel             # noqa: E402

from aikit.loaders import load             # noqa: E402 — Modulo 2 · Lezione 4
from aikit.clean import clean, pipeline_for  # noqa: E402 — Modulo 2 · Lezione 5
from aikit.chunk import chunk_recursive    # noqa: E402 — Modulo 2 · Lezione 10
from aikit.embeddings import embed         # noqa: E402 — Modulo 2 · Lezione 7
from aikit import vectorstore              # noqa: E402 — Modulo 2 · Lezione 9

load_dotenv()

MODELLO = "gpt-4o-mini"
client = OpenAI()

CORPUS_DIR = SCRIPTS / "dataset" / "mio_corpus"      # <- i vostri file (o la riserva Lumen)
COLLECTION_NAME = "progetto_finale"
CHUNK_SIZE = 500

FATTURE_DIR = SCRIPTS / "dataset" / "fatture_lumen"  # fisse, uguali per tutti


class RispostaRAG(BaseModel):
    """La risposta strutturata: testo, fonti citate, se è stata trovata nei documenti."""
    risposta: str
    fonti: list[str]
    trovato: bool


class RigaFattura(BaseModel):
    prodotto: str
    quantita: int
    prezzo_unitario: float


class Fattura(BaseModel):
    """Stesso schema di Modulo 2 · Lezione 14 — non si riscrive, si riusa."""
    numero: str
    data: str
    cliente: str
    righe: list[RigaFattura]
    imponibile: float
    iva: float
    sconto: float | None = None
    totale: float
    note: str | None = None


# --------------------------------------------------------------- TODO 1
def indicizza_corpus():
    """load + clean + chunk + embed + index su tutti i file di CORPUS_DIR.

    Per ogni file: aikit.loaders.load() (attenzione: restituisce list[Document]
    — solo i PDF multipagina ne restituiscono più di uno, unite i testi prima
    di pulire; gli altri formati ne restituiscono già uno solo, ma unire va
    bene comunque), poi aikit.clean.clean() con la pipeline di
    aikit.clean.pipeline_for(), poi aikit.chunk.chunk_recursive(), poi
    aikit.embeddings.embed(), infine upsert in una collection nuova con
    vectorstore.crea_collection() (che cancella e ricrea) +
    vectorstore.indicizza() (ids, testi, embeddings, metadatas).

    Fatto quando (osservabile): la funzione stampa quanti chunk ha
    indicizzato, un numero coerente col numero di file caricati.
    """
    raise NotImplementedError


# --------------------------------------------------------------- TODO 2
def cerca_chunk(query, k=4):
    """I k chunk più pertinenti dalla collection COLLECTION_NAME.

    Riuso quasi identico di Modulo 2 · Lezione 11 (vectorstore.apri_collection
    + vectorstore.search): cambia solo il nome della collection.
    """
    raise NotImplementedError


# --------------------------------------------------------------- TODO 3
def genera_risposta(query, chunks):
    """Il prompt RAG di Modulo 2 · Lezione 11 (non ri-spiegato: chunk marcati
    con la loro fonte, risposta chiesta SOLO sui documenti, rifiuto esplicito
    se l'informazione non c'è), chiamato con structured outputs (Modulo 2 ·
    Lezione 13, client.responses.parse con text_format) invece di restituire
    testo libero. Restituisce un oggetto RispostaRAG.

    Fatto quando: su una domanda nel corpus, `trovato=True` e `fonti` punta a
    un chunk esistente; su una domanda fuori corpus, `trovato=False` col
    rifiuto pulito, senza inventare.
    """
    raise NotImplementedError


# --------------------------------------------------------------- TODO 4
def estrai_fattura(path):
    """Schema Fattura di Modulo 2 · Lezione 14 (sopra), riusato tale e quale:
    lettura diretta del file + client.responses.parse(text_format=Fattura).

    Fatto quando: sulla fattura senza sconto, sconto/note tornano None, non
    un valore inventato.
    """
    raise NotImplementedError


if __name__ == "__main__":
    indicizza_corpus()

    QUERY_DI_PROVA = [
        # <- 2-3 domande sul vostro corpus
    ]
    K = 4
    for query in QUERY_DI_PROVA:
        chunks = cerca_chunk(query, K)
        risposta = genera_risposta(query, chunks)
        print(f"\n=== {query}")
        print(risposta)

    print("\n--- estrazione fatture Lumen ---")
    for percorso in sorted(FATTURE_DIR.glob("*.txt")):
        print(f"\n=== {percorso.name}")
        print(estrai_fattura(percorso))
