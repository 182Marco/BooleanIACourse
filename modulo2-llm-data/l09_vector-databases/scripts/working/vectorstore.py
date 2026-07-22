"""vectorstore.py — il corpus Lumen dentro un vector DB (ChromaDB).

Prima il quick start col docente (la collection su disco, i primi doc, una
query); poi scrivete voi il caricamento completo e le due ricerche, e le
provate nel main confrontandole col vostro brute-force di giovedì:

    python working/vectorstore.py
"""
import json
import sys

from pathlib import Path

import chromadb
import numpy as np

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from aikit.embeddings import embed          # noqa: E402 — il toolkit di L19
from aikit import search as ricerca_l20     # noqa: E402 — il brute-force di L20

DATASET = SCRIPTS / "dataset"
CHROMA_DIR = SCRIPTS / "chroma"             # qui il DB vive su disco


# --------------------------------------------------- TODO 1 · col docente 🎤
def apri_collection():
    """La collection 'lumen' su disco: la crea la prima volta, poi la riapre.

    Client persistente su CHROMA_DIR; la collection usa la metrica cosine
    (la stessa di L19-L20).
    """
    raise NotImplementedError


# ----------------------------------------------------------- TODO 2 · voi ⌨️
def carica_corpus_nel_db(collection):
    """Upsert dei 48 doc di L19: id, testo, embedding dall'npz, metadata tipo.

    Gli embedding sono quelli GIÀ CALCOLATI di corpus_embeddings.npz, passati
    espliciti (mai l'embedder di default del DB); l'ordine giusto è in
    corpus_meta.json → "ids". Restituisce il backend del corpus (dal meta),
    che serve per embeddare le query nello stesso spazio.
    """
    raise NotImplementedError


# ----------------------------------------------------------- TODO 3 · voi ⌨️
def search(query, k):
    """I k doc più simili alla query, chiesti al DB. Risultati come a L20.

    Ogni risultato è un dict {"id", "tipo", "testo", "score"}: la query va
    embeddata col backend del corpus. Collection e backend qui dentro non
    arrivano dai parametri: potete riaprirli/rileggerli DENTRO la funzione
    (apri_collection() e corpus_meta.json — è quello che fa anche il vostro
    search.py di L20 col corpus). Il DB risponde in DISTANZE (cosine): lo
    score di L20 è 1 - distanza.
    """
    raise NotImplementedError


# ----------------------------------------------------------- TODO 4 · voi ⌨️
def search_filtrata(query, k, tipo):
    """Come search(), ma solo tra i doc di quel tipo (where sui metadata)."""
    raise NotImplementedError


if __name__ == "__main__":
    QUERY_FACILE = "Quanto costa la spedizione?"
    QUERY_GENERICA = "informazioni sulla scrivania"
    QUERY_DOPPIONI = "problemi con il motore della scrivania"
    K = 3

    # Quick start (🎤 col docente): apri_collection(), upsert dei primi 3 doc
    # del corpus con gli embedding dell'npz, una query di prova. Poi rilanciate
    # lo script: i documenti sono ancora lì.

    # Lab 1 (⌨️ da soli): il corpus completo nel DB, poi le tre query qui
    # sopra con la vostra search() fianco a fianco col brute-force di
    # giovedì (ricerca_l20.search): stessi documenti in testa?

    # Lab 2 (⌨️ da soli): le stesse query con search_filtrata() variando il
    # tipo, poi le prove CRUD: delete di un doc in top-3, update di un testo
    # (ri-embed + upsert con lo stesso id). Da qui in giù scrivete voi.

    # Esercizio extra (SOLO se il docente lo lancia): il 49° documento —
    # scrivete VOI una voce nuova del corpus (una FAQ che manca, un ticket
    # realistico), embed + upsert con un id nuovo e il tipo giusto; poi
    # dimostrate che la ricerca la trova e che il filtro la rispetta.
