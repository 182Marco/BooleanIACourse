"""esplora_corpus.py — embedda il corpus Lumen e misura le coppie assegnate.

L'esercizio della serata (TODO 4-5):

1. carica i 48 testi brevi di dataset/corpus_lumen.jsonl (già scritto);
2. li embedda con embeddings.embed();
3. stampa la similarità delle COPPIE assegnate — facili e trappole;
4. salva corpus_embeddings.npz + corpus_meta.json (già scritto): il corpus
   vettorizzato che la prossima lezione (Modulo 2 · Lezione 8) riapre per
   farci sopra la ricerca semantica.

Il backend si sceglie con la variabile BACKEND in cima al main.
"""
import json

from pathlib import Path

import numpy as np

from embeddings import MODELLO_LOCAL, MODELLO_OPENAI, cosine_similarity, embed

SCRIPTS = Path(__file__).parent.parent
CORPUS = SCRIPTS / "dataset" / "corpus_lumen.jsonl"
OUT = SCRIPTS / "working"    # il corpus vettorizzato atterra qui: la prossima lezione lo riapre da qui

# Le coppie assegnate: (id_a, id_b, cosa ci aspettiamo di vedere).
COPPIE = [
    ("faq-01", "tic-04", "garanzia ↔ ticket garanzia: parole in comune"),
    ("faq-03", "tic-05", "stessa richiesta, detta con altre parole"),
    ("faq-02", "rec-06", "spedizione ↔ estetica del bambù (controllo)"),
    ("rec-03", "rec-04", "TRAPPOLA: stesse parole, verdetto opposto"),
    ("faq-03", "faq-09", "TRAPPOLA: italiano ↔ inglese"),
    ("prod-04", "rec-01", "descrizione LD-200 ↔ recensione LD-200"),
]


def carica_corpus():
    """Legge il corpus JSONL: una riga = {"id", "tipo", "testo"}."""
    righe = CORPUS.read_text(encoding="utf-8").splitlines()
    return [json.loads(r) for r in righe if r.strip()]


# --------------------------------------------- TODO 4: il ponte id → riga
def indice_per_id(corpus):
    """Il ponte tra le COPPIE (che parlano per id) e i vettori (che parlano
    per posizione): restituisce il dizionario id → indice di riga nel corpus.
    """
    return {doc["id"]: i for i, doc in enumerate(corpus)}


# ------------------------------------------------ TODO 5: misura le coppie
def misura_coppie(corpus, vettori):
    """Stampa una riga per ogni coppia di COPPIE: i due id, la similarità
    coseno tra i loro vettori, l'attesa. Dagli id alle righe si passa con
    indice_per_id (TODO 4).
    """
    indice = indice_per_id(corpus)
    print(f"\n{'coppia':<18} {'cosine':>7}   attesa")
    for id_a, id_b, attesa in COPPIE:
        sim = cosine_similarity(vettori[indice[id_a]], vettori[indice[id_b]])
        print(f"{id_a} ↔ {id_b:<8} {sim:>7.3f}   {attesa}")


# ------------------------------------------- già scritta: salva il deliverable
def salva(corpus, vettori, backend):
    """Scrive il corpus vettorizzato in working/: corpus_embeddings.npz
    (chiave "vectors", float32) + corpus_meta.json. Non si cancella: è
    l'input della prossima lezione.
    """
    np.savez(OUT / "corpus_embeddings.npz", vectors=vettori.astype(np.float32))
    meta = {
        "ids": [doc["id"] for doc in corpus],
        "tipi": [doc["tipo"] for doc in corpus],
        "backend": backend,
        "modello": MODELLO_OPENAI if backend == "openai" else MODELLO_LOCAL,
        "dimensioni": int(vettori.shape[1]),
    }
    (OUT / "corpus_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nsalvati corpus_embeddings.npz {vettori.shape} + corpus_meta.json"
          f" (backend={backend})")


if __name__ == "__main__":
    BACKEND = "openai"    # "local" per il giro gratis sulla vostra macchina

    corpus = carica_corpus()
    print(f"corpus: {len(corpus)} testi da {CORPUS.name}, backend={BACKEND}")

    try:
        vettori = embed([doc["testo"] for doc in corpus], backend=BACKEND)
    except NotImplementedError as err:
        print(f"[--] prima il live coding ({err} in working/embeddings.py)")
        raise SystemExit(1)

    try:
        misura_coppie(corpus, vettori)
    except NotImplementedError as err:
        print(f"[--] ancora da scrivere — {err}: completa il TODO e rilancia "
              "(senza tabella non si salva niente)")
        raise SystemExit(1)

    salva(corpus, vettori, BACKEND)
