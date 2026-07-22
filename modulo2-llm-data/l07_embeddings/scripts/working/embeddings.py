"""embeddings.py — da testo a vettore, con backend selezionabile e cache.

Il modulo che regge tutto il blocco retrieval (L19-L22):

    from embeddings import embed, cosine_similarity

    vecs = embed(["testo uno", "testo due"], backend="openai")
    print(cosine_similarity(vecs[0], vecs[1]))

Due backend dietro la stessa firma:
  - "openai"  → API text-embedding-3-small (a pagamento, i testi escono)
  - "local"   → sentence-transformers sulla tua macchina (gratis, offline)

Si scrive DAL VIVO col docente (TODO 1-3). Verifica a ogni salvataggio:

    python scaffolding/check_lab19.py
"""
import hashlib
import time

from pathlib import Path

import numpy as np
from dotenv import load_dotenv

load_dotenv()

CACHE_DIR = Path(__file__).parent / ".cache_embeddings"

# Modelli di default dei due backend (verificati live, luglio 2026).
MODELLO_OPENAI = "text-embedding-3-small"   # 1536 dim — $0.02 / 1M token
MODELLO_LOCAL = "all-MiniLM-L6-v2"          # 384 dim — ~88 MB, gira in CPU

PREZZO_PER_MTOK = {"text-embedding-3-small": 0.02, "text-embedding-3-large": 0.13}


# ------------------------------------------------------------ TODO 1: cosine
def cosine_similarity(a, b) -> float:
    """Similarità coseno tra due vettori: cos(θ) = a·b / (|a| |b|).

    Vale 1.0 per vettori paralleli (stesso significato), ~0 per vettori
    ortogonali (nessuna relazione), -1.0 per vettori opposti. Conta l'ANGOLO,
    non la lunghezza: per questo non serve normalizzare prima.

    TODO 1: implementala con numpy — prodotto scalare diviso il prodotto
    delle norme (np.linalg.norm). Converti gli input con np.asarray e
    restituisci un float Python, non un np.float64.
    """
    raise NotImplementedError("TODO 1: cosine = a·b / (|a| |b|)")


# ---------------------------------------------------- TODO 2: i due backend
def embed_openai(texts: list[str]) -> np.ndarray:
    """Embedding via API OpenAI. I testi VIAGGIANO verso il servizio.

    TODO 2a: importa il client DENTRO la funzione (from openai import OpenAI)
    e chiama OpenAI().embeddings.create(model=MODELLO_OPENAI, input=texts).
    Stampa token e costo in questo formato (è la riga citata in slide):
        print(f"  [openai] {len(texts)} testi, {token} token → ${costo:.6f}")
    con token = risposta.usage.total_tokens e costo = token / 1_000_000 *
    PREZZO_PER_MTOK[MODELLO_OPENAI]. Restituisci np.array dei vettori,
    dtype float32.
    """
    raise NotImplementedError("TODO 2a: chiamata → costo → vettori")


_modello_locale = None   # caricato una volta sola: l'import e il load costano


def embed_local(texts: list[str]) -> np.ndarray:
    """Embedding con sentence-transformers, sulla TUA macchina.

    Il primo uso scarica il modello (~88 MB) nella cache di Hugging Face;
    da lì in poi è tutto offline e gratis.

    TODO 2b: importa DENTRO la funzione (from sentence_transformers import
    SentenceTransformer), carica SentenceTransformer(MODELLO_LOCAL) una
    volta sola (usa la variabile globale _modello_locale) e restituisci
    _modello_locale.encode(texts) come array float32.
    """
    raise NotImplementedError("TODO 2b: SentenceTransformer + encode")


# Il registro dei backend: aggiungerne uno = una riga (es. "cohere").
EMBEDDERS = {"openai": embed_openai, "local": embed_local}
MODELLI = {"openai": MODELLO_OPENAI, "local": MODELLO_LOCAL}


# ------------------------------------------- TODO 3: embed() con cache disco
def _chiave_cache(backend: str, testo: str) -> Path:
    """Un file per (backend, modello, testo): se uno cambia, cache diversa."""
    impronta = hashlib.sha1(
        f"{backend}|{MODELLI.get(backend, '?')}|{testo}".encode("utf-8")
    ).hexdigest()
    return CACHE_DIR / f"{impronta}.npy"


def embed(texts: list[str], backend: str = "openai") -> np.ndarray:
    """Embedda una lista di testi. Ricalcola SOLO ciò che non è in cache.

    TODO 3:
    1. backend sconosciuto → raise ValueError (PRIMA di qualunque chiamata);
    2. per ogni testo: se _chiave_cache(backend, testo) esiste, np.load;
       altrimenti segnati (indice, testo) tra i mancanti;
    3. embedda i soli mancanti con EMBEDDERS[backend], salva ogni vettore
       con np.save nella sua chiave di cache;
    4. restituisci np.stack di tutti i vettori nell'ordine di partenza.
    """
    raise NotImplementedError("TODO 3: registro + cache + stack")


# ------------------------------------------------------------- demo a occhio
if __name__ == "__main__":
    frasi = [
        "La scrivania si alza e si abbassa con il doppio motore.",   # A
        "Il piano motorizzato sale e scende in silenzio.",           # B: come A, parole diverse
        "Il reso va richiesto entro trenta giorni dalla consegna.",  # C: altro tema
    ]
    for backend in ("openai", "local"):
        print(f"\nbackend = {backend}")
        inizio = time.perf_counter()
        vecs = embed(frasi, backend=backend)
        print(f"  shape {vecs.shape} in {time.perf_counter() - inizio:.2f}s")
        print(f"  A~B (stesso senso, parole diverse): {cosine_similarity(vecs[0], vecs[1]):.3f}")
        print(f"  A~C (temi diversi):                 {cosine_similarity(vecs[0], vecs[2]):.3f}")
