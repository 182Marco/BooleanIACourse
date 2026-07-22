"""esplora_corpus.py — embedda il corpus Lumen e misura le coppie assegnate.

L'esercizio della serata (TODO 4-6):

    python working/esplora_corpus.py            # backend openai (default)
    python working/esplora_corpus.py local      # backend locale, per confronto

1. carica i 48 testi brevi di dataset/corpus_lumen.jsonl;
2. li embedda con embeddings.embed() (la cache evita di ri-pagare i rilanci);
3. stampa la similarità delle COPPIE assegnate — facili e trappole;
4. salva corpus_embeddings.npz + corpus_meta.json: il corpus vettorizzato
   che L20 riaprirà per farci sopra la ricerca semantica.
"""
import json
import sys

from pathlib import Path

import numpy as np

from embeddings import MODELLI, cosine_similarity, embed

SCRIPTS = Path(__file__).parent.parent
CORPUS = SCRIPTS / "dataset" / "corpus_lumen.jsonl"

# Le coppie assegnate: (id_a, id_b, cosa ci aspettiamo di vedere).
COPPIE = [
    ("faq-01", "tic-04", "garanzia ↔ ticket garanzia: parole in comune"),
    ("faq-03", "tic-05", "stessa cosa, parole TUTTE diverse"),
    ("faq-02", "rec-06", "spedizione ↔ estetica del bambù (controllo)"),
    ("rec-03", "rec-04", "TRAPPOLA: stesse parole, verdetto opposto"),
    ("faq-03", "faq-09", "TRAPPOLA: italiano ↔ inglese"),
    ("prod-04", "rec-01", "descrizione LD-200 ↔ recensione LD-200"),
]


def carica_corpus() -> list[dict]:
    """Legge il corpus JSONL: una riga = {"id", "tipo", "testo"}."""
    righe = CORPUS.read_text(encoding="utf-8").splitlines()
    return [json.loads(r) for r in righe if r.strip()]


# --------------------------------------------- TODO 4: il ponte id → riga
def indice_per_id(corpus: list[dict]) -> dict[str, int]:
    """Costruisce il dizionario id → indice di riga."""
    return {doc["id"]: i for i, doc in enumerate(corpus)}


# ------------------------------------------------ TODO 5: misura le coppie
def misura_coppie(corpus: list[dict], vettori: np.ndarray) -> None:
    """Stampa la similarità coseno di ogni coppia assegnata."""
    indice = indice_per_id(corpus)
    print(f"\n{'coppia':<18} {'cosine':>7}   attesa")
    for id_a, id_b, attesa in COPPIE:
        sim = cosine_similarity(vettori[indice[id_a]], vettori[indice[id_b]])
        print(f"{id_a} ↔ {id_b:<8} {sim:>7.3f}   {attesa}")


# --------------------------------------------- TODO 6: salva il corpus vettorizzato
def salva(corpus: list[dict], vettori: np.ndarray, backend: str,
          outdir: Path) -> None:
    """Scrive corpus_embeddings.npz + corpus_meta.json (l'input di L20)."""
    np.savez(outdir / "corpus_embeddings.npz",
             vectors=vettori.astype(np.float32))
    meta = {
        "ids": [doc["id"] for doc in corpus],
        "tipi": [doc["tipo"] for doc in corpus],
        "backend": backend,
        "modello": MODELLI.get(backend, "?"),
        "dimensioni": int(vettori.shape[1]),
    }
    (outdir / "corpus_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nsalvati corpus_embeddings.npz {vettori.shape} + corpus_meta.json"
          f" (backend={backend})")


def main(backend: str = "openai", outdir: Path | None = None) -> None:
    outdir = Path(outdir) if outdir else Path(__file__).parent
    corpus = carica_corpus()
    print(f"corpus: {len(corpus)} testi da {CORPUS.name}, backend={backend}")
    vettori = embed([doc["testo"] for doc in corpus], backend=backend)
    misura_coppie(corpus, vettori)
    salva(corpus, vettori, backend, outdir)


if __name__ == "__main__":
    main(backend=sys.argv[1] if len(sys.argv) > 1 else "openai")
