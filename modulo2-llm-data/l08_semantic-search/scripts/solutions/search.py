"""search.py — la ricerca semantica sul corpus Lumen di Modulo 2 · Lezione 7, a mano.

Versione COMPLETA (riferimento docente) di working/search.py: stessi nomi,
stessi import. Negli esercizi il come sta agli studenti.
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
    """I k testi più simili alla query, dal più simile in giù."""
    docs, vectors, backend = carica_corpus()
    q = embed([query], backend=backend)[0]        # lo STESSO spazio del corpus
    scores = [cosine_similarity(q, v) for v in vectors]
    risultati = [{**docs[i], "score": scores[i]} for i in range(len(docs))]
    risultati.sort(key=lambda r: r["score"], reverse=True)
    return risultati[:k]


# ----------------------------------------------------------- TODO 2 · voi ⌨️
def search_mmr(query, k, lambda_):
    """Come search(), ma i k risultati li sceglie MMR."""
    docs, vectors, backend = carica_corpus()
    q = embed([query], backend=backend)[0]
    sim_query = [cosine_similarity(v, q) for v in vectors]

    scelti = [int(np.argmax(sim_query))]          # il primo è il più rilevante
    while len(scelti) < min(k, len(vectors)):
        migliore = None
        punteggio_migliore = None
        for c in range(len(vectors)):
            if c in scelti:
                continue
            # quanto il candidato assomiglia ai già scelti: il max è il suo
            # "peggior doppione" — è quello che MMR penalizza
            somiglianza_scelti = max(
                cosine_similarity(vectors[c], vectors[s]) for s in scelti
            )
            punteggio = lambda_ * sim_query[c] - (1 - lambda_) * somiglianza_scelti
            if punteggio_migliore is None or punteggio > punteggio_migliore:
                migliore = c
                punteggio_migliore = punteggio
        scelti.append(migliore)

    return [{**docs[i], "score": sim_query[i]} for i in scelti]


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
