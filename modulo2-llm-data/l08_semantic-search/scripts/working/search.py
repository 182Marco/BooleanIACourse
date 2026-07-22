"""search.py — la ricerca semantica sul corpus Lumen di L19, a mano.

Prima si riapre il corpus vettorizzato (col docente), poi scrivete voi le
due funzioni di ricerca e le provate sulle query del main, variando K e
LAMBDA:

    python working/search.py
"""
import json
import sys

from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from aikit.embeddings import embed, cosine_similarity  # noqa: E402 — il toolkit di L19

DATASET = SCRIPTS / "dataset"


# --------------------------------------------------- TODO 1 · col docente 🎤
def carica_corpus():
    """Riapre il corpus di L19: restituisce (docs, vectors, backend).

    docs[i] è il dict {"id", "tipo", "testo"} del vettore vectors[i];
    backend dice con che cosa è stato embeddato il corpus (corpus_meta.json).
    """
    raise NotImplementedError


# ----------------------------------------------------------- TODO 2 · voi ⌨️
def search(query, k):
    """I k testi più simili alla query, dal più simile in giù.

    Ogni risultato è un dict {"id", "tipo", "testo", "score"}. La query va
    embeddata col backend del corpus; la similarità è la cosine di L19.
    """
    raise NotImplementedError


# ----------------------------------------------------------- TODO 3 · voi ⌨️
def search_mmr(query, k, lambda_):
    """Come search(), ma i k risultati li sceglie MMR.

    A ogni giro vince il candidato che massimizza
    lambda_ * sim(candidato, query) - (1-lambda_) * max sim(candidato, già scelti).
    Con lambda_=1.0 deve uscire esattamente il top-k di search().
    """
    raise NotImplementedError


if __name__ == "__main__":
    QUERY_FACILE = "Quanto costa la spedizione?"
    QUERY_GENERICA = "informazioni sulla scrivania"
    QUERY_DOPPIONI = "problemi con il motore della scrivania"
    K = 3
    LAMBDA = 0.5

    # Provate ogni query con search() e con search_mmr(), variando K e
    # LAMBDA: cosa cambia tra le due liste? Stampate sempre gli SCORE
    # accanto ai risultati — senza, non si diagnostica nulla.
    # Da qui in giù scrivete voi.
