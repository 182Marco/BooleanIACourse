"""esplora_corpus.py — embedda il corpus Lumen e misura le coppie assegnate.

L'esercizio della serata (TODO 4-6):

    python working/esplora_corpus.py            # backend openai (default)
    python working/esplora_corpus.py local      # backend locale, per confronto

1. carica i 48 testi brevi di dataset/corpus_lumen.jsonl;
2. li embedda con embeddings.embed() (la cache evita di ri-pagare i rilanci);
3. stampa la similarità delle COPPIE assegnate — facili e trappole;
4. salva corpus_embeddings.npz + corpus_meta.json: il corpus vettorizzato
   che L20 riaprirà per farci sopra la ricerca semantica.

Fatto quando: la tabella delle coppie è stampata, i due file sono su disco
e check_lab19.py è tutto [OK].
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
    """Costruisce il dizionario id → indice di riga.

    Cosa hai in mano: corpus è una lista di dict, uno per testo. Esempio
    di elemento:
        {"id": "faq-01", "tipo": "faq", "testo": "Quanto dura la garanzia? ..."}
    L'elemento in posizione i del corpus corrisponde alla riga i di
    vettori (guarda main(): embed() riceve i testi nell'ordine del corpus).

    Il problema: le COPPIE in cima al file parlano per id ("faq-01"), i
    vettori per posizione (riga 0, 1, 2...). Questo dizionario è il ponte.

    TODO 4: restituisci {id del documento: sua posizione nel corpus},
    es. {"faq-01": 0, "faq-02": 1, ...} — enumerate è tuo amico.
    """
    raise NotImplementedError("TODO 4: {id: indice di riga}")


# ------------------------------------------------ TODO 5: misura le coppie
def misura_coppie(corpus: list[dict], vettori: np.ndarray) -> None:
    """Stampa la similarità coseno di ogni coppia assegnata.

    Cosa hai in mano:
      - vettori: array (48, dim) allineato per posizione al corpus —
        vettori[i] è l'embedding di corpus[i]["testo"];
      - indice_per_id(corpus), il tuo TODO 4: da un id alla sua riga;
      - COPPIE (in cima al file): tuple (id_a, id_b, attesa). L'attesa è
        già scritta: va solo stampata accanto al numero.

    TODO 5: per ogni (id_a, id_b, attesa) in COPPIE calcola la
    cosine_similarity tra i due vettori corrispondenti (dagli id alle
    righe si passa col dizionario del TODO 4) e stampa una riga:
    id_a, id_b, similarità con 3 decimali, attesa.

    Una riga di output, per capirsi (backend openai):
        faq-01 ↔ tic-04     0.516   garanzia ↔ ticket garanzia: parole in comune
    """
    raise NotImplementedError("TODO 5: una riga per coppia, via indice_per_id")


# --------------------------------------------- TODO 6: salva il corpus vettorizzato
def salva(corpus: list[dict], vettori: np.ndarray, backend: str,
          outdir: Path) -> None:
    """Scrive corpus_embeddings.npz + corpus_meta.json (l'input di L20).

    TODO 6: np.savez(outdir / "corpus_embeddings.npz",
    vectors=vettori.astype(np.float32)); poi scrivi corpus_meta.json con
    ESATTAMENTE queste chiavi (il check le verifica per nome):
      "ids"         → gli id, nell'ordine del corpus
      "tipi"        → i tipi, nello stesso ordine
      "backend"     → il backend usato
      "modello"     → MODELLI.get(backend, "?")
      "dimensioni"  → vettori.shape[1] (come int)
    """
    raise NotImplementedError("TODO 6: npz + json dei metadata")


def main(backend: str = "openai", outdir: Path | None = None) -> None:
    outdir = Path(outdir) if outdir else Path(__file__).parent
    corpus = carica_corpus()
    print(f"corpus: {len(corpus)} testi da {CORPUS.name}, backend={backend}")
    vettori = embed([doc["testo"] for doc in corpus], backend=backend)
    misura_coppie(corpus, vettori)
    salva(corpus, vettori, backend, outdir)


if __name__ == "__main__":
    main(backend=sys.argv[1] if len(sys.argv) > 1 else "openai")
