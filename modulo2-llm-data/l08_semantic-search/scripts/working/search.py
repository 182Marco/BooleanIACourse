"""search.py — la ricerca semantica sul corpus Lumen di Modulo 2 · Lezione 7, a mano.

carica_corpus() è già scritta (si legge insieme, col docente); le due
funzioni di ricerca (TODO 1-2) le scrivete voi e le provate sulle query
del main, variando K e LAMBDA:

    python working/search.py
"""
import json
import sys

from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from aikit.embeddings import embed, cosine_similarity  # noqa: E402 — il toolkit di Modulo 2 · Lezione 7

DATASET = SCRIPTS / "dataset"


# ------------------------------------------- già scritta: si legge insieme 🎤
def carica_corpus():
    """Riapre il corpus di Modulo 2 · Lezione 7: restituisce (docs, vectors, backend).

    docs[i] è il dict {"id", "tipo", "testo"} del vettore vectors[i];
    backend dice con che cosa è stato embeddato il corpus (corpus_meta.json).
    """
    vectors = np.load(DATASET / "corpus_embeddings.npz")["vectors"]
    meta = json.loads((DATASET / "corpus_meta.json").read_text(encoding="utf-8"))

    per_id = {}
    for riga in (DATASET / "corpus_lumen.jsonl").read_text(encoding="utf-8").splitlines():
        if riga.strip():
            doc = json.loads(riga)
            per_id[doc["id"]] = doc

    # i testi nell'ORDINE dei vettori: la riga i del npz è il doc di ids[i]
    docs = [per_id[doc_id] for doc_id in meta["ids"]]
    return docs, vectors, meta["backend"]


# ----------------------------------------------------------- TODO 1 · voi ⌨️
def search(query, k):
    """I k testi più simili alla query, dal più simile in giù.

    Ogni risultato è un dict {"id", "tipo", "testo", "score"}. Il corpus si
    apre chiamando carica_corpus(); la query va embeddata col backend del
    corpus; la similarità è la cosine di Modulo 2 · Lezione 7.

    TODO 1.
    """
    raise NotImplementedError("TODO 1: search")


# ----------------------------------------------------------- TODO 2 · voi ⌨️
def search_mmr(query, k, lambda_):
    """Come search(), ma i k risultati li sceglie MMR.

    A ogni giro vince il candidato che massimizza
    lambda_ * sim(candidato, query) - (1-lambda_) * max sim(candidato, già scelti).
    Il primo scelto è il più rilevante (senza già-scelti la
    penalità non esiste ancora). Con lambda_=1.0 deve uscire esattamente il
    top-k di search().
    (Il parametro è lambda_ con l'underscore: "lambda" da sola è una parola
    riservata di Python.)

    TODO 2 — dopo search: se il tempo stringe, search è quello che serve
    alla prossima lezione; MMR si completa insieme al debrief.
    """
    raise NotImplementedError("TODO 2: search_mmr")


if __name__ == "__main__":
    QUERY_FACILE = "Quanto costa la spedizione?"
    QUERY_GENERICA = "informazioni sulla scrivania"
    QUERY_DOPPIONI = "problemi con il motore della scrivania"
    K = 3
    LAMBDA = 0.5

    docs, vectors, backend = carica_corpus()
    print(f"corpus: {len(docs)} testi, vettori {vectors.shape}, backend={backend}")

    # Provate ogni query con le due funzioni, variando K e LAMBDA:
    # cosa cambia tra le due liste?
    for query in (QUERY_FACILE, QUERY_GENERICA, QUERY_DOPPIONI):
        print(f"\n=== {query!r} · k={K} · lambda={LAMBDA}")
        try:
            print("top-k:")
            for r in search(query, K):
                print(f"  {r['score']:.3f}  [{r['tipo']:<10}] {r['id']:<8} {r['testo'][:52]}…")
        except NotImplementedError as err:
            print(f"  [--] ancora da scrivere — {err}")
            break
        try:
            print("MMR:")
            for r in search_mmr(query, K, LAMBDA):
                print(f"  {r['score']:.3f}  [{r['tipo']:<10}] {r['id']:<8} {r['testo'][:52]}…")
        except NotImplementedError as err:
            print(f"  [--] ancora da scrivere — {err}")
