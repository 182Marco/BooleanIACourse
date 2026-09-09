"""embeddings.py — da testo a vettore, con backend selezionabile.

Il modulo che regge tutto il blocco retrieval (Modulo 2 · Lezione 7-10):

    from embeddings import embed, cosine_similarity

    vecs = embed(["testo uno", "testo due"], backend="openai")
    print(cosine_similarity(vecs[0], vecs[1]))

Due backend dietro la stessa firma:
  - "openai"  → API text-embedding-3-small (a pagamento, i testi escono)
  - "local"   → sentence-transformers sulla tua macchina (gratis, offline)

Si scrive DAL VIVO col docente (TODO 1-3). A fine serata entra nel toolkit,
e da lì si importa senza riscriverlo:

    cp working/embeddings.py scaffolding/aikit/embeddings.py
"""
import time

import numpy as np
from dotenv import load_dotenv

load_dotenv()

# Modelli di default dei due backend (verificati live, luglio 2026).
MODELLO_OPENAI = "text-embedding-3-small"   # 1536 dim — $0.02 / 1M token
MODELLO_LOCAL = "all-MiniLM-L6-v2"          # 384 dim — ~88 MB, gira in CPU


# ------------------------------------------------------------ TODO 1: cosine
def cosine_similarity(a, b):
    """Similarità coseno tra due vettori: cos(θ) = a·b / (|a| |b|).

    Vale 1.0 per vettori paralleli (stesso significato), ~0 per vettori
    ortogonali (nessuna relazione), -1.0 per vettori opposti. Conta l'ANGOLO,
    non la lunghezza: per questo non serve normalizzare prima.

    TODO 1: la formula qui sopra, in numpy. Restituisce un float.
    """
    raise NotImplementedError("TODO 1: cosine_similarity")


# ---------------------------------------------------- TODO 2: i due backend
def embed_openai(texts):
    """Embedding via API OpenAI. I testi VIAGGIANO verso il servizio.

    TODO 2a: chiama l'endpoint embeddings — OpenAI().embeddings.create(...) —
    con MODELLO_OPENAI, stampa token usati e costo (il campo usage della
    risposta; $0.02 / 1M token) e restituisci i vettori come array numpy
    float32.
    """
    raise NotImplementedError("TODO 2a: embed_openai")


_modello_locale = None   # caricato una volta sola: l'import e il load costano


def embed_local(texts):
    """Embedding con sentence-transformers, sulla TUA macchina.

    Il primo uso scarica il modello (~88 MB) nella cache di Hugging Face;
    da lì in poi è tutto offline e gratis.

    TODO 2b: carica SentenceTransformer(MODELLO_LOCAL) una volta sola
    (la variabile _modello_locale è lì per questo) e restituisci
    encode(texts) come array float32.
    """
    raise NotImplementedError("TODO 2b: embed_local")


# --------------------------------------------------- TODO 3: embed() dispatch
def embed(texts, backend="openai"):
    """Embedda una lista di testi con il backend scelto.

    TODO 3: "openai" → embed_openai, "local" → embed_local, qualunque
    altro valore → ValueError. Basta un if.
    """
    raise NotImplementedError("TODO 3: embed")


# ------------------------------------------------------------- demo a occhio
if __name__ == "__main__":
    # TODO 1 su vettori noti: paralleli → 1, perpendicolari → 0, opposti → -1.
    try:
        print("cosine su vettori noti: "
              f"{cosine_similarity([1, 0], [1, 0]):.0f} / "
              f"{cosine_similarity([1, 0], [0, 1]):.0f} / "
              f"{cosine_similarity([1, 0], [-1, 0]):.0f}")
    except NotImplementedError as err:
        print(f"[--] ancora da scrivere — {err}")

    frasi = [
        "La scrivania si alza e si abbassa con il doppio motore.",   # A
        "Il piano motorizzato sale e scende in silenzio.",           # B: come A, parole diverse
        "Il reso va richiesto entro trenta giorni dalla consegna.",  # C: altro tema
    ]
    for backend in ("openai", "local"):
        print(f"\nbackend = {backend}")
        inizio = time.perf_counter()
        try:
            vecs = embed(frasi, backend=backend)
            print(f"  shape {vecs.shape} in {time.perf_counter() - inizio:.2f}s")
            print(f"  A~B (stesso senso, parole diverse): {cosine_similarity(vecs[0], vecs[1]):.3f}")
            print(f"  A~C (temi diversi):                 {cosine_similarity(vecs[0], vecs[2]):.3f}")
        except NotImplementedError as err:
            print(f"  [--] ancora da scrivere — {err}")
            break
