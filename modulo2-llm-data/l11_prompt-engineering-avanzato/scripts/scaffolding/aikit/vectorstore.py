"""vectorstore.py — la collection ChromaDB, da oggi nel toolkit aikit/.

È il modulo che avete scritto sabato a L21 (la collection persistente su
disco, l'upsert con embedding ESPLICITI, la ricerca che parla in score),
promosso in aikit/ — lo stesso percorso di embeddings.py (L19) e search.py
(L20). NON si tocca, si importa:

    from aikit import vectorstore

    collection = vectorstore.apri_collection("lumen_chunks")
    risultati = vectorstore.search(collection, "una domanda", 3)

È questo il `search` di stasera (sul vector DB) — non va confuso con
`aikit.search.search()`, il brute-force in-memory di L20 tenuto per
confronto, che `cerca_chunk` non usa.

**Stasera (L23) si usa SOLO apri_collection()**: la collection `lumen_chunks`
è già pronta (di sabato scorso o dalla riserva) e il retrieval la riapre
così com'è — `cerca_chunk` (TODO 1) non deve mai ricrearla.
`crea_collection()` resta nel modulo per chi rigenera la riserva
(`prepara_collection.py`, che riparte sempre da zero) ma non è la funzione
del retrieval: usarla in `cerca_chunk` cancellerebbe la collection a ogni
chiamata.
"""
from pathlib import Path

import chromadb

from aikit.embeddings import embed

CHROMA_DIR = Path(__file__).parent.parent.parent / "chroma"


def apri_collection(nome):
    """La collection su disco: la crea la prima volta, poi la riapre (L21)."""
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(
        nome, metadata={"hnsw:space": "cosine"}   # la metrica di L19-L21
    )


def crea_collection(nome):
    """Come apri_collection(), ma da ZERO: se la collection esiste la cancella.

    Usata da `prepara_collection.py` per ricostruire la riserva (era la
    funzione di L22, dove si ri-chunk e ri-indicizzava a ogni esperimento).
    Stasera il retrieval (`cerca_chunk`, TODO 1) NON la chiama: la collection
    va riaperta con `apri_collection`, non ricreata a ogni domanda.
    """
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    if nome in [c.name for c in client.list_collections()]:
        client.delete_collection(nome)
    return client.create_collection(nome, metadata={"hnsw:space": "cosine"})


def indicizza(collection, ids, testi, embeddings, metadatas=None):
    """Upsert con embedding ESPLICITI (mai l'embedder di default del DB)."""
    collection.upsert(ids=ids, documents=testi, embeddings=embeddings,
                      metadatas=metadatas)


def search(collection, query, k, backend="openai"):
    """I k documenti più simili alla query, dal più simile in giù.

    Ogni risultato è un dict {"id", "testo", "score", ...metadata}: la query
    viene embeddata nello stesso spazio del corpus (regola di L20) e il DB
    risponde in DISTANZE — lo score è 1 - distanza, come a L21. L'"id"
    (es. "manuale-lumadesk-007") è la fonte da citare nel prompt RAG.
    """
    q = embed([query], backend=backend)[0]
    ris = collection.query(query_embeddings=[q], n_results=k)
    risultati = []
    for i in range(len(ris["ids"][0])):
        r = {
            "id": ris["ids"][0][i],
            "testo": ris["documents"][0][i],
            "score": 1 - ris["distances"][0][i],
        }
        if ris["metadatas"][0][i]:
            r.update(ris["metadatas"][0][i])
        risultati.append(r)
    return risultati
