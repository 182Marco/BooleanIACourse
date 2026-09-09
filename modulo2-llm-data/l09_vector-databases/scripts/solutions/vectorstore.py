"""vectorstore.py — il punto di partenza DOPO il quick start col docente.

È la copia di working/vectorstore.py con la parte del docente già dentro:
TODO 1 (apri_collection) e il quick start nel main sono FATTI. Restano a
voi il Lab 1 (TODO 2-3: carica_corpus_nel_db, search), il Lab 2 (TODO 4-5:
search_filtrata e le prove CRUD in coda al main) e l'eventuale TODO 6.

Serve a chi è rimasto indietro durante il live coding: si riparte da qui,
senza la soluzione degli esercizi. Si lancia come il vostro:

    python working/vectorstore.py
"""
import json
import sys

from pathlib import Path

import chromadb
import numpy as np

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from aikit.embeddings import embed          # noqa: E402 — il toolkit di Modulo 2 · Lezione 7
from aikit import search as bruteforce      # noqa: E402 — il brute-force di Modulo 2 · Lezione 8

DATASET = SCRIPTS / "dataset"
CHROMA_DIR = SCRIPTS / "chroma"             # qui il DB vive su disco


# ------------------------------------------ TODO 1 · fatto col docente 🎤 ✔
def apri_collection():
    """La collection 'lumen' su disco: la crea la prima volta, poi la riapre."""
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(
        "lumen",
        metadata={"hnsw:space": "cosine"},   # la metrica di Modulo 2 · Lezione 7-8: gli score restano confrontabili
    )


# ----------------------------------------------------------- TODO 2 · voi ⌨️
def carica_corpus_nel_db(collection):
    """Upsert dei 48 doc di Modulo 2 · Lezione 7: id, testo, embedding dall'npz, metadata tipo.

    Gli embedding sono quelli GIÀ CALCOLATI di corpus_embeddings.npz, passati
    espliciti (mai l'embedder di default del DB); l'ordine giusto è in
    corpus_meta.json → "ids" (del meta qui servono solo "ids" e "backend";
    il tipo di ogni doc sta nel jsonl). I tre file di dataset/ rileggeteli
    QUI dentro: la funzione si basta da sola, come search(). Restituisce il
    backend del corpus, che serve per embeddare le query nello stesso spazio.
    """
    raise NotImplementedError("TODO 2: carica_corpus_nel_db")


# ----------------------------------------------------------- TODO 3 · voi ⌨️
def search(query, k):
    """I k doc più simili alla query, chiesti al DB. Risultati come a Modulo 2 · Lezione 8.

    Ogni risultato è un dict {"id", "tipo", "testo", "score"}: la query va
    embeddata col backend del corpus. Collection e backend qui dentro non
    arrivano dai parametri: potete riaprirli/rileggerli DENTRO la funzione
    (apri_collection() e corpus_meta.json — è quello che fa anche il vostro
    search.py di Modulo 2 · Lezione 8 col corpus). Il DB risponde in DISTANZE (cosine): lo
    score di Modulo 2 · Lezione 8 è 1 - distanza.
    """
    raise NotImplementedError("TODO 3: search")


# ----------------------------------------------------------- TODO 4 · voi ⌨️
def search_filtrata(query, k, tipo):
    """Come search(), ma solo tra i doc di quel tipo.

    Il filtro sui metadata è un parametro di collection.query:
    where={"tipo": ...}.
    """
    raise NotImplementedError("TODO 4: search_filtrata")


# ------------------------------------------------- già scritta: la stampa 🖨
def stampa(risultati):
    """Una riga per risultato: score, tipo, id, inizio del testo."""
    for r in risultati:
        print(f"  {r['score']:.3f}  [{r['tipo']:<10}] {r['id']:<8} {r['testo'][:52]}…")


if __name__ == "__main__":
    QUERY_FACILE = "Quanto costa la spedizione?"
    QUERY_GENERICA = "informazioni sulla scrivania"
    QUERY_DOPPIONI = "problemi con il motore della scrivania"
    K = 3

    # Il corpus com'è arrivato da Modulo 2 · Lezione 7: tre file da tenere
    # allineati a mano (npz + meta + testi). Stamattina entra in un DB.
    vectors = np.load(DATASET / "corpus_embeddings.npz")["vectors"]
    meta = json.loads((DATASET / "corpus_meta.json").read_text(encoding="utf-8"))
    per_id = {}
    for riga in (DATASET / "corpus_lumen.jsonl").read_text(encoding="utf-8").splitlines():
        if riga.strip():
            doc = json.loads(riga)
            per_id[doc["id"]] = doc
    print(f"corpus: {len(meta['ids'])} testi, vettori {vectors.shape}, backend={meta['backend']}")

    collection = apri_collection()
    print(f"collection 'lumen': {collection.count()} documenti su disco")

    # — Quick start (🎤 col docente) · l'upsert dei primi 3 doc e una query
    #   di prova. Rilanciando lo script i documenti sono ancora lì, e il
    #   count qui sopra non raddoppia (upsert).
    primi = meta["ids"][:3]                            # faq-01, faq-02, faq-03
    collection.upsert(
        ids=primi,
        documents=[per_id[i]["testo"] for i in primi],
        embeddings=vectors[:3],                        # espliciti, dall'npz di Modulo 2 · Lezione 7
        metadatas=[{"tipo": per_id[i]["tipo"]} for i in primi],
    )
    print(f"quick start: upsert dei primi {len(primi)} doc → count {collection.count()}")

    # query di prova: parla di uno dei 3 doc appena caricati (faq-01, la
    # garanzia) con parole diverse dal testo — deve uscire lui in testa
    q = embed(["Quanto dura la garanzia?"], backend=meta["backend"])[0]
    prova = collection.query(query_embeddings=[q], n_results=2)
    for i in range(len(prova["ids"][0])):
        print(f"  {1 - prova['distances'][0][i]:.3f}  {prova['ids'][0][i]:<8} "
              f"{prova['documents'][0][i][:52]}…")

    # — Lab 1 · TODO 2-3: il corpus completo nel DB, poi le tre query fianco
    #   a fianco col brute-force di Modulo 2 · Lezione 8.
    try:
        backend = carica_corpus_nel_db(collection)
    except NotImplementedError as err:
        print(f"[--] ancora da scrivere — {err}")
        raise SystemExit(0)
    print(f"caricato tutto il corpus: {collection.count()} documenti (backend={backend})")

    for query in (QUERY_FACILE, QUERY_GENERICA, QUERY_DOPPIONI):
        print(f"\n=== {query!r} · k={K}")
        try:
            print("dal DB:")
            stampa(search(query, K))
        except NotImplementedError as err:
            print(f"  [--] ancora da scrivere — {err}")
            break
        print("brute-force di Modulo 2 · Lezione 8 (aikit):")
        stampa(bruteforce.search(query, K))

    # — Lab 2 · TODO 4: la stessa query, con e senza filtro
    print(f"\n=== con e senza filtro · {QUERY_DOPPIONI!r}")
    try:
        print("senza filtro:")
        stampa(search(QUERY_DOPPIONI, K))
        for tipo in ("faq", "ticket", "recensione"):
            print(f"solo {tipo}:")
            stampa(search_filtrata(QUERY_DOPPIONI, K, tipo))
    except NotImplementedError as err:
        print(f"  [--] ancora da scrivere — {err}")

    # — Lab 2 · TODO 5, le prove CRUD: da qui in giù scrivete VOI.
    #   delete di un doc che sta in top-3 — collection.delete(ids=[...]) —
    #   poi ri-query: sparito? Quindi l'update fatto bene: nuovo testo,
    #   ri-embed con embed(), upsert con lo STESSO id.

    # — Esercizio extra (SOLO se il docente lo lancia) · il 49° documento:
    #   una voce nuova del corpus scritta da voi — embed + upsert con un id
    #   nuovo e il tipo giusto; la vostra query la trova? il filtro la rispetta?
