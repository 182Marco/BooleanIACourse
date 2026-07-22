"""embeddings.py — da testo a vettore, con backend selezionabile e cache.

Il modulo che regge tutto il blocco retrieval (L19-L22):

    from embeddings import embed, cosine_similarity

    vecs = embed(["testo uno", "testo due"], backend="openai")
    print(cosine_similarity(vecs[0], vecs[1]))

Due backend dietro la stessa firma:
  - "openai"  → API text-embedding-3-small (a pagamento, i testi escono)
  - "local"   → sentence-transformers sulla tua macchina (gratis, offline)

La cache su disco (.cache_embeddings/) evita di ri-pagare due volte lo stesso
testo: la chiave è (backend, modello, testo) — se uno dei tre cambia, il
vettore va ricalcolato.
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
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    return float((a @ b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# ---------------------------------------------------- TODO 2: i due backend
def embed_openai(texts: list[str]) -> np.ndarray:
    """Embedding via API OpenAI. I testi VIAGGIANO verso il servizio."""
    from openai import OpenAI

    risposta = OpenAI().embeddings.create(model=MODELLO_OPENAI, input=texts)
    token = risposta.usage.total_tokens
    costo = token / 1_000_000 * PREZZO_PER_MTOK[MODELLO_OPENAI]
    print(f"  [openai] {len(texts)} testi, {token} token → ${costo:.6f}")
    return np.array([d.embedding for d in risposta.data], dtype=np.float32)


_modello_locale = None   # caricato una volta sola: l'import e il load costano


def embed_local(texts: list[str]) -> np.ndarray:
    """Embedding con sentence-transformers, sulla TUA macchina.

    Il primo uso scarica il modello (~88 MB) nella cache di Hugging Face;
    da lì in poi è tutto offline e gratis.
    """
    global _modello_locale
    if _modello_locale is None:
        from sentence_transformers import SentenceTransformer

        _modello_locale = SentenceTransformer(MODELLO_LOCAL)
    return np.asarray(_modello_locale.encode(texts), dtype=np.float32)


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
    """Embedda una lista di testi. Ricalcola SOLO ciò che non è in cache."""
    if backend not in EMBEDDERS:
        raise ValueError(
            f"backend {backend!r} sconosciuto: scegli tra {sorted(EMBEDDERS)}"
        )
    CACHE_DIR.mkdir(exist_ok=True)

    vettori: list[np.ndarray | None] = []
    mancanti: list[tuple[int, str]] = []
    for i, testo in enumerate(texts):
        percorso = _chiave_cache(backend, testo)
        if percorso.exists():
            vettori.append(np.load(percorso))
        else:
            vettori.append(None)
            mancanti.append((i, testo))

    if mancanti:
        nuovi = EMBEDDERS[backend]([t for _, t in mancanti])
        for (i, testo), vettore in zip(mancanti, nuovi):
            np.save(_chiave_cache(backend, testo), vettore)
            vettori[i] = vettore

    print(f"  [cache] {len(texts) - len(mancanti)}/{len(texts)} testi già in cache")
    return np.stack(vettori)


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
