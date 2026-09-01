"""demo_failure.py — Modulo 3 · Lezione 1: dove fallisce il nostro RAG.

La pipeline è quella del Progetto Modulo 2 (load → clean → chunk → embed →
index, poi search → prompt → risposta strutturata), sul corpus Lumen già noto.
Quattro sezioni, una per failure mode: retrieval miss, context overflow,
hallucination nonostante il contesto, lost-in-the-middle.

Il docente la ESEGUE e la commenta — stasera nessuno scrive codice:

    python scaffolding/demo_failure.py

Ogni sezione si ferma con [invio], così si commenta con calma quello che è
appena successo. Le query sono state scelte perché falliscono DAVVERO su
questo corpus (verificate con chiamate reali, 5 run su 5): se ne cambiate una,
il failure può non scattare più.
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

CORPUS_DIR = SCRIPTS / "dataset" / "lumen"
COLLECTION_NAME = "lumen_l01"
CHUNK_SIZE = 500
K = 4                                      # il k del Progetto Modulo 2

# prezzo USD per 1M token (listino OpenAI, verificato agosto 2026)
PREZZO_INPUT = 0.15
PREZZO_OUTPUT = 0.60

# Le query della demo. Scelte (e verificate live) perché fanno scattare
# ciascuna il proprio failure mode su QUESTO corpus.
QUERY_MISS = "La scrivania non sta ferma, si muove tutta quando scrivo: che controllo faccio?"
QUERY_MISS_RIFORMULATA = "Il piano oscilla alla massima altezza: cosa devo controllare?"
QUERY_FACILE = "Quanto tempo ho per segnalare un danno da trasporto?"
QUERY_HALLUC = "Come si toglie il blocco tastiera una volta attivato?"
QUERY_MIDDLE = "Con l'errore E07, per quanti secondi devo scollegare l'alimentazione?"

CHUNK_GIUSTO_MISS = "manuale-lumadesk-013"     # "Se il piano oscilla alla massima altezza..."
CHUNK_GIUSTO_MIDDLE = "manuale-lumadesk-009"   # la procedura completa dell'errore E07


class RispostaRAG(BaseModel):
    """La risposta strutturata del Progetto Modulo 2: testo, fonti, trovato."""
    risposta: str
    fonti: list[str]
    trovato: bool


def indicizza_corpus():
    """La pipeline di ingest del Progetto Modulo 2, tale e quale, su dataset/lumen/."""
    collection = vectorstore.crea_collection(COLLECTION_NAME)
    ids, testi, meta = [], [], []
    for percorso in sorted(CORPUS_DIR.glob("*.txt")):
        documenti = load(str(percorso))                                  # Modulo 2 · Lezione 4
        testo_grezzo = "\n".join(d.text for d in documenti)
        testo_pulito = clean(testo_grezzo, pipeline_for(str(percorso)))  # Modulo 2 · Lezione 5
        for i, pezzo in enumerate(chunk_recursive(testo_pulito, CHUNK_SIZE)):
            ids.append(f"{percorso.stem}-{i:03d}")
            testi.append(pezzo)
            meta.append({"source": percorso.name})
    vettori = embed(testi)                                               # Modulo 2 · Lezione 7
    vectorstore.indicizza(collection, ids, testi, vettori, meta)
    print(f"indicizzati {len(testi)} chunk da {len(list(CORPUS_DIR.glob('*.txt')))} file "
          f"in '{COLLECTION_NAME}'")
    return len(testi)


def cerca_chunk(query, k=K):
    collection = vectorstore.apri_collection(COLLECTION_NAME)
    return vectorstore.search(collection, query, k)


def contesto_da(chunks):
    documenti = ""
    for c in chunks:
        documenti += f'<documento fonte="{c["id"]}">\n{c["testo"]}\n</documento>\n'
    return documenti


def genera_risposta(query, chunks):
    """Il prompt RAG con rifiuto pulito (Modulo 2 · Lezione 11) + structured
    outputs (Modulo 2 · Lezione 13): è la generazione del Progetto Modulo 2.
    Restituisce (risposta, usage) — l'usage serve a contare i token."""
    prompt = f"""Rispondi alla domanda usando SOLO le informazioni nei documenti
qui sotto. Elenca in "fonti" gli id dei documenti citati. Se la risposta non
è nei documenti, imposta trovato=false e scrivi in "risposta" che non c'è nei
documenti — senza inventare nulla.

<documenti>
{contesto_da(chunks)}</documenti>

<domanda>
{query}
</domanda>"""
    r = client.responses.parse(
        model=MODELLO,
        input=[{"role": "user", "content": prompt}],
        text_format=RispostaRAG,
    )
    return r.output_parsed, r.usage


def genera_senza_vincolo(query, chunks):
    """Lo stesso giro SENZA il vincolo di grounding: il prompt "ingenuo" che
    un RAG scritto di fretta userebbe. Serve alla sezione hallucination."""
    prompt = (f"Rispondi alla domanda dell'utente. Puoi usare i documenti qui sotto.\n\n"
              f"<documenti>\n{contesto_da(chunks)}</documenti>\n\n"
              f"<domanda>\n{query}\n</domanda>")
    r = client.responses.create(model=MODELLO, input=[{"role": "user", "content": prompt}])
    return r.output_text, r.usage


# ------------------------------------------------------------------ helper video
def stampa_chunks(chunks, evidenzia=None):
    for posizione, c in enumerate(chunks, start=1):
        anteprima = " ".join(c["testo"].split())[:58]
        freccia = "  ◄── il chunk giusto" if c["id"] == evidenzia else ""
        print(f"   {posizione}. {c['id']}  score={c['score']:.3f}  {anteprima}…{freccia}")


def stampa_risposta(r):
    print(f"   trovato={r.trovato}  fonti={r.fonti}")
    print(f"   → {r.risposta}")


def costo(usage):
    dollari = (usage.input_tokens / 1e6 * PREZZO_INPUT
               + usage.output_tokens / 1e6 * PREZZO_OUTPUT)
    return f"{usage.input_tokens} token input · ${dollari:.5f}"


def sezione(titolo):
    input("\n[invio per continuare]")
    print("\n" + "=" * 72)
    print(titolo)
    print("=" * 72)


if __name__ == "__main__":
    print("Demo: dove fallisce il nostro RAG — corpus Lumen, pipeline del Progetto Modulo 2")
    print("-" * 72)
    indicizza_corpus()

    # ---------------------------------------------------------- 1. RETRIEVAL MISS
    sezione("1 · RETRIEVAL MISS — il chunk giusto non esce")
    print(f'\nDomanda: "{QUERY_MISS}"')
    print(f"(la risposta ESISTE nel corpus: {CHUNK_GIUSTO_MISS} — serraggio delle viti)\n")
    chunks = cerca_chunk(QUERY_MISS)
    stampa_chunks(chunks, evidenzia=CHUNK_GIUSTO_MISS)
    risposta, uso_base = genera_risposta(QUERY_MISS, chunks)
    stampa_risposta(risposta)

    tutti = cerca_chunk(QUERY_MISS, 45)
    posizione = [c["id"] for c in tutti].index(CHUNK_GIUSTO_MISS) + 1
    print(f"\n   Il chunk giusto è al posto {posizione} su {len(tutti)}: con k={K} non entra.")
    print('   L\'utente dice "non sta ferma", il documento dice "oscilla": parole')
    print("   diverse, vettori lontani. Controprova con le parole del documento:")
    print(f'\nDomanda riformulata: "{QUERY_MISS_RIFORMULATA}"')
    chunks_ok = cerca_chunk(QUERY_MISS_RIFORMULATA)
    stampa_chunks(chunks_ok, evidenzia=CHUNK_GIUSTO_MISS)
    risposta_ok, _ = genera_risposta(QUERY_MISS_RIFORMULATA, chunks_ok)
    stampa_risposta(risposta_ok)

    # ------------------------------------------------------- 2. CONTEXT OVERFLOW
    sezione("2 · CONTEXT OVERFLOW — la cura ingenua: alzo k e prendo tutto")
    print(f'\nStessa domanda: "{QUERY_MISS}"')
    print(f"Con k=45 il corpus intero finisce nel prompt: il chunk giusto ORA c'è")
    print(f"(posto {posizione} su 45). Vediamo se il modello lo usa.\n")
    risposta45, uso45 = genera_risposta(QUERY_MISS, tutti)
    stampa_risposta(risposta45)
    print(f"\n   k={K}:  {costo(uso_base)}")
    print(f"   k=45: {costo(uso45)}  (×{uso45.input_tokens / uso_base.input_tokens:.0f} sui token input)")
    print("   Il chunk c'è ma il modello annega nei distrattori — e ogni domanda")
    print("   costa 7 volte tanto. Le domande facili invece reggono anche così:")
    print(f'\nDomanda facile, sempre k=45: "{QUERY_FACILE}"')
    risposta_facile, _ = genera_risposta(QUERY_FACILE, cerca_chunk(QUERY_FACILE, 45))
    stampa_risposta(risposta_facile)
    print("\n   È il failure più subdolo: non rompe tutto, rompe le domande fragili.")

    # ---------------------------------- 3. HALLUCINATION NONOSTANTE IL CONTESTO
    sezione("3 · HALLUCINATION — il contesto c'è, la risposta inventa")
    print(f'\nDomanda: "{QUERY_HALLUC}"')
    print("Il manuale dice solo come si ATTIVA il blocco (M + «-» per tre secondi):")
    print("come si toglie non è scritto da nessuna parte.\n")
    chunks = cerca_chunk(QUERY_HALLUC)
    stampa_chunks(chunks)
    print("\n   Con il prompt del Progetto Modulo 2 (vincolo di grounding, Modulo 2 · Lezione 11):")
    risposta, _ = genera_risposta(QUERY_HALLUC, chunks)
    stampa_risposta(risposta)
    print("\n   Con un prompt SENZA vincolo di grounding (com'è scritto un RAG di fretta):")
    testo, _ = genera_senza_vincolo(QUERY_HALLUC, chunks)
    print(f"   → {' '.join(testo.split())}")
    print("\n   La procedura di sblocco è INVENTATA: plausibile, sicura di sé, e non")
    print("   scritta in nessun documento. Il vincolo di grounding la para spesso —")
    print("   non sempre: rilanciate la domanda qualche volta e capita che inventi")
    print("   anche col vincolo.")

    # ------------------------------------------------------ 4. LOST IN THE MIDDLE
    sezione("4 · LOST-IN-THE-MIDDLE — l'informazione c'è, ma sta in mezzo")
    print(f'\nDomanda: "{QUERY_MIDDLE}"  (risposta nel corpus: 30 secondi)')
    print("Esperimento controllato: contesto IDENTICO (tutti i 45 chunk), cambiamo")
    print("solo la POSIZIONE del chunk giusto nel prompt.\n")
    tutti = cerca_chunk(QUERY_MIDDLE, 45)
    giusto = [c for c in tutti if c["id"] == CHUNK_GIUSTO_MIDDLE]
    altri = [c for c in tutti if c["id"] != CHUNK_GIUSTO_MIDDLE]
    meta = len(altri) // 2

    print(f"   {CHUNK_GIUSTO_MIDDLE} in CIMA al contesto (posizione 1 di 45):")
    risposta, _ = genera_risposta(QUERY_MIDDLE, giusto + altri)
    stampa_risposta(risposta)
    print(f"\n   {CHUNK_GIUSTO_MIDDLE} in MEZZO al contesto (posizione {meta + 1} di 45):")
    risposta, _ = genera_risposta(QUERY_MIDDLE, altri[:meta] + giusto + altri[meta:])
    stampa_risposta(risposta)
    print("\n   Stessi 45 chunk, stessa domanda: cambia solo dove sta l'informazione.")
    print("   In cima risponde, in mezzo la perde. Ed è anche il perché del punto 2:")
    print("   più contesto = più roba in mezzo.")

    print("\n" + "=" * 72)
    print("Quattro failure, quattro righe nel catalogo — si compila insieme.")
    print("=" * 72)
