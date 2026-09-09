"""vectorstore.py — il corpus Lumen dentro un vector DB (ChromaDB).

Versione COMPLETA (riferimento docente) di working/vectorstore.py: stessi
nomi, stessi import. Il main segue la giornata nell'ordine: quick start
(live coding), Lab 1, Lab 2. Negli esercizi il come sta agli studenti.
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


# --------------------------------------------------- TODO 1 · col docente 🎤
def apri_collection():
    """La collection 'lumen' su disco: la crea la prima volta, poi la riapre."""
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(
        "lumen",
        metadata={"hnsw:space": "cosine"},   # la metrica di Modulo 2 · Lezione 7-8: gli score restano confrontabili
    )


# ----------------------------------------------------------- TODO 2 · voi ⌨️
def carica_corpus_nel_db(collection):
    """Upsert dei 48 doc di Modulo 2 · Lezione 7 (id, testo, embedding dall'npz, metadata tipo).

    Restituisce il backend del corpus (corpus_meta.json), che serve per
    embeddare le query nello stesso spazio.
    """
    vectors = np.load(DATASET / "corpus_embeddings.npz")["vectors"]
    meta = json.loads((DATASET / "corpus_meta.json").read_text(encoding="utf-8"))

    per_id = {}
    for riga in (DATASET / "corpus_lumen.jsonl").read_text(encoding="utf-8").splitlines():
        if riga.strip():
            doc = json.loads(riga)
            per_id[doc["id"]] = doc
    docs = [per_id[doc_id] for doc_id in meta["ids"]]   # stesso ordine dei vettori

    collection.upsert(                                  # upsert = insert-o-sostituisci
        ids=[d["id"] for d in docs],
        documents=[d["testo"] for d in docs],
        embeddings=vectors,                             # espliciti: MAI l'embedder di default
        metadatas=[{"tipo": d["tipo"]} for d in docs],
    )
    return meta["backend"]


# ----------------------------------------------------------- TODO 3 · voi ⌨️
def search(query, k):
    """I k doc più simili alla query, chiesti al DB. Risultati come a Modulo 2 · Lezione 8."""
    collection = apri_collection()
    backend = json.loads((DATASET / "corpus_meta.json").read_text(encoding="utf-8"))["backend"]
    q = embed([query], backend=backend)[0]              # lo STESSO spazio del corpus
    ris = collection.query(query_embeddings=[q], n_results=k)
    # Chroma risponde per LISTE di query (se ne possono mandare più di una
    # insieme): ris["ids"][0] sono gli id della NOSTRA, unica, query —
    # da qui il [0] davanti a ogni [i].
    risultati = []
    for i in range(len(ris["ids"][0])):
        risultati.append({
            "id": ris["ids"][0][i],
            "tipo": ris["metadatas"][0][i]["tipo"],
            "testo": ris["documents"][0][i],
            "score": 1 - ris["distances"][0][i],        # il DB parla in DISTANZE
        })
    return risultati


# ----------------------------------------------------------- TODO 4 · voi ⌨️
def search_filtrata(query, k, tipo):
    """Come search(), ma solo tra i doc di quel tipo (where={"tipo": ...})."""
    collection = apri_collection()
    backend = json.loads((DATASET / "corpus_meta.json").read_text(encoding="utf-8"))["backend"]
    q = embed([query], backend=backend)[0]
    ris = collection.query(query_embeddings=[q], n_results=k, where={"tipo": tipo})
    risultati = []
    for i in range(len(ris["ids"][0])):                 # [0] = la nostra unica query
        risultati.append({
            "id": ris["ids"][0][i],
            "tipo": ris["metadatas"][0][i]["tipo"],
            "testo": ris["documents"][0][i],
            "score": 1 - ris["distances"][0][i],
        })
    return risultati


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
    backend = carica_corpus_nel_db(collection)
    print(f"caricato tutto il corpus: {collection.count()} documenti (backend={backend})")

    for query in (QUERY_FACILE, QUERY_GENERICA, QUERY_DOPPIONI):
        print(f"\n=== {query!r} · k={K}")
        print("dal DB:")
        stampa(search(query, K))
        print("brute-force di Modulo 2 · Lezione 8 (aikit):")
        stampa(bruteforce.search(query, K))

    # — Lab 2 · TODO 4: la stessa query, con e senza filtro
    print(f"\n=== con e senza filtro · {QUERY_DOPPIONI!r}")
    print("senza filtro:")
    stampa(search(QUERY_DOPPIONI, K))
    for tipo in ("faq", "ticket", "recensione"):
        print(f"solo {tipo}:")
        stampa(search_filtrata(QUERY_DOPPIONI, K, tipo))

    # — Lab 2 · TODO 5, le prove CRUD: delete, poi l'update fatto bene
    print(f"\n=== delete: faq-02 era in testa a {QUERY_FACILE!r} — sparisce")
    collection.delete(ids=["faq-02"])
    stampa(search(QUERY_FACILE, K))

    print("\n=== update: faq-02 torna ma parla d'altro → ri-embed + upsert, stesso id")
    nuovo_testo = ("Posso ritirare l'ordine in negozio? Sì: il ritiro in showroom "
                   "a Milano è gratuito, su appuntamento, entro 7 giorni dall'ordine.")
    # il DB non si accorge dei testi cambiati: l'embedding lo ricalcoliamo NOI
    collection.upsert(
        ids=["faq-02"],
        documents=[nuovo_testo],
        embeddings=embed([nuovo_testo], backend=backend),
        metadatas=[{"tipo": "faq"}],
    )
    print(f"per {QUERY_FACILE!r} non esce più:")
    stampa(search(QUERY_FACILE, K))
    print("per 'posso ritirare in negozio?' invece:")
    stampa(search("posso ritirare in negozio?", K))

    # — Esercizio extra (SOLO se il docente lo lancia) · il 49° documento
    print("\n=== extra: il 49° documento — una FAQ che mancava")
    nuova_faq = ("Posso pagare a rate? Sì: al checkout trovi il pagamento in 3 rate "
                 "senza interessi con carta; sopra i 500 euro anche in 12 rate.")
    collection.upsert(
        ids=["faq-13"],                                # id NUOVO: è un insert
        documents=[nuova_faq],
        embeddings=embed([nuova_faq], backend=backend),
        metadatas=[{"tipo": "faq"}],
    )
    print(f"ora i documenti sono {collection.count()}")
    print("la trova anche con parole diverse dal testo:")
    stampa(search("si può pagare un po' alla volta?", K))
    print("col filtro sbagliato invece non esce:")
    stampa(search_filtrata("si può pagare un po' alla volta?", K, "ticket"))
    collection.delete(ids=["faq-13"])

    # ripristino: il DB torna identico al corpus, per rilanci puliti
    carica_corpus_nel_db(collection)
