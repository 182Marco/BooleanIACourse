"""app.py — Progetto Modulo 2: tutta la pipeline, sul vostro corpus.

Versione COMPLETA (riferimento docente) di working/app.py: stessi nomi, stessi
import. Il corpus (dataset/mio_corpus/) e le query di prova sono una scelta
possibile tra tante — negli esercizi il corpus sta a voi.

Non si impara niente di nuovo oggi: ogni funzione qui sotto è il riuso diretto
di una lezione già fatta.

    python solutions/app.py
"""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from dotenv import load_dotenv             # noqa: E402
from openai import OpenAI                  # noqa: E402
from pydantic import BaseModel             # noqa: E402

from aikit.loaders import load             # noqa: E402 — Modulo 2 · Lezione 4
from aikit.clean import clean, pipeline_for  # noqa: E402 — Modulo 2 · Lezione 5
from aikit.chunk import chunk_recursive    # noqa: E402 — Modulo 2 · Lezione 10
from aikit.embeddings import embed         # noqa: E402 — Modulo 2 · Lezione 7
from aikit import vectorstore              # noqa: E402 — Modulo 2 · Lezione 9

load_dotenv()

MODELLO = "gpt-4o-mini"
client = OpenAI()

CORPUS_DIR = SCRIPTS / "dataset" / "mio_corpus"      # <- i vostri file (o la riserva Lumen)
COLLECTION_NAME = "progetto_finale"
CHUNK_SIZE = 500

FATTURE_DIR = SCRIPTS / "dataset" / "fatture_lumen"  # fisse, uguali per tutti


class RispostaRAG(BaseModel):
    """La risposta strutturata: testo, fonti citate, se è stata trovata nei documenti."""
    risposta: str
    fonti: list[str]
    trovato: bool


class RigaFattura(BaseModel):
    prodotto: str
    quantita: int
    prezzo_unitario: float


class Fattura(BaseModel):
    """Stesso schema di Modulo 2 · Lezione 14 — non si riscrive, si riusa."""
    numero: str
    data: str
    cliente: str
    righe: list[RigaFattura]
    imponibile: float
    iva: float
    sconto: float | None = None
    totale: float
    note: str | None = None


# --------------------------------------------------------------- TODO 1
def indicizza_corpus():
    """load + clean + chunk + embed + index su tutti i file di CORPUS_DIR.

    Ogni passo è una lezione già fatta (Modulo 2 · Lezione 4-5, 7, 9-10): qui si
    incatenano. Ricrea la collection da zero (vectorstore.crea_collection), così
    si può rilanciare senza doppioni se si cambia corpus.
    """
    file_corpus = sorted(p for p in CORPUS_DIR.glob("*.*") if p.name != ".gitkeep")
    if not file_corpus:
        raise SystemExit(
            f"Nessun file in {CORPUS_DIR}: mettete i vostri documenti, oppure "
            f"copiate lì il contenuto di dataset/riserva_lumen/."
        )

    collection = vectorstore.crea_collection(COLLECTION_NAME)
    ids, testi, meta = [], [], []
    for percorso in file_corpus:
        documenti = load(str(percorso))                                # Modulo 2 · Lezione 4
        testo_grezzo = "\n".join(d.text for d in documenti)
        testo_pulito = clean(testo_grezzo, pipeline_for(str(percorso)))  # Modulo 2 · Lezione 5
        pezzi = chunk_recursive(testo_pulito, CHUNK_SIZE)                # Modulo 2 · Lezione 10
        for i, pezzo in enumerate(pezzi):
            ids.append(f"{percorso.stem}-{i:03d}")
            testi.append(pezzo)
            meta.append({"source": percorso.name})

    vettori = embed(testi)                                               # Modulo 2 · Lezione 7
    vectorstore.indicizza(collection, ids, testi, vettori, meta)
    print(f"indicizzati {len(testi)} chunk da {len(file_corpus)} file in '{COLLECTION_NAME}'")


# --------------------------------------------------------------- TODO 2
def cerca_chunk(query, k=4):
    """Riuso quasi identico di Modulo 2 · Lezione 11: cambia solo la collection."""
    collection = vectorstore.apri_collection(COLLECTION_NAME)
    return vectorstore.search(collection, query, k)


# --------------------------------------------------------------- TODO 3
def genera_risposta(query, chunks):
    """Il prompt RAG di Modulo 2 · Lezione 11, chiamato con structured outputs
    (Modulo 2 · Lezione 13) invece di restituire testo libero."""
    documenti = ""
    for c in chunks:
        documenti += f'<documento fonte="{c["id"]}">\n{c["testo"]}\n</documento>\n'

    prompt = f"""Rispondi alla domanda usando SOLO le informazioni nei documenti
qui sotto. Elenca in "fonti" gli id dei documenti citati. Se la risposta non
è nei documenti, imposta trovato=false e scrivi in "risposta" che non c'è nei
documenti — senza inventare nulla.

<documenti>
{documenti}</documenti>

<domanda>
{query}
</domanda>"""

    r = client.responses.parse(
        model=MODELLO,
        input=[{"role": "user", "content": prompt}],
        text_format=RispostaRAG,
    )
    return r.output_parsed


# --------------------------------------------------------------- TODO 4
def estrai_fattura(path):
    """Schema Fattura di Modulo 2 · Lezione 14, riusato tale e quale su un
    dataset a sé (le fatture Lumen) — indipendente dal corpus indicizzato."""
    testo = Path(path).read_text(encoding="utf-8")
    r = client.responses.parse(
        model=MODELLO,
        input=[
            {"role": "system", "content": "Estrai i dati della fattura dal testo dell'utente."},
            {"role": "user", "content": testo},
        ],
        text_format=Fattura,
    )
    return r.output_parsed


if __name__ == "__main__":
    indicizza_corpus()

    QUERY_DI_PROVA = [
        "Come si calibra la scrivania alla prima accensione?",
        "Posso pagare alla consegna, in contrassegno?",
    ]
    K = 4
    for query in QUERY_DI_PROVA:
        chunks = cerca_chunk(query, K)
        risposta = genera_risposta(query, chunks)
        print(f"\n=== {query}")
        print(risposta)

    print("\n--- estrazione fatture Lumen ---")
    for percorso in sorted(FATTURE_DIR.glob("*.txt")):
        print(f"\n=== {percorso.name}")
        print(estrai_fattura(percorso))
