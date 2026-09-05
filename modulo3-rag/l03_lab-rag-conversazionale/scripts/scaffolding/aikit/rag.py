"""rag.py — la pipeline RAG del modulo, da oggi nel toolkit aikit/.

È il file scritto a Modulo 3 · Lezione 2 (tre funzioni piatte e un CONFIG
in cima), promosso in aikit/ con lo stesso rito di embeddings.py,
vectorstore.py e chunk.py nel Modulo 2. Si importa:

    from aikit import rag

    chunks = rag.recupera("una domanda", 4)     # i k chunk più pertinenti
    risposta, usati = rag.rispondi("una domanda")   # single-turn, con citazioni

L'unica differenza rispetto alla versione di Modulo 3 · Lezione 2 è la
riga SCRIPTS qui sotto: il file sta un livello più in basso (scaffolding/
aikit/ invece di solutions/), quindi risale di tre cartelle invece di due
per trovare dataset/ e chroma/. Tutto il resto è identico: sopra le
funzioni non ci sono più i «TODO 1-3» della lezione scorsa, qui è tutto
scritto.

Le tre funzioni sono le tre interfacce dell'architettura RAG
(Modulo 3 · Lezione 1):

    indicizza()            l'INGEST: corpus → chunk → embedding → collection
    recupera(query, k)     il RETRIEVE: domanda → i k chunk più pertinenti
    rispondi(query)        il GENERATE: domanda → (risposta, chunk usati)

OGGI (Modulo 3 · Lezione 3) QUESTO FILE SI MODIFICA UNA VOLTA, IN AULA.
rispondi() fa tre cose in una — recupera, costruisce il prompt, chiama il
modello — e non c'è modo di darle chunk diversi o una storia. Nel live
coding di apertura si spacca in due: genera(chunks, domanda, storia=None),
che costruisce il prompt e chiama il modello, e rispondi(query, storia=None),
che diventa genera(recupera(query), query, storia). Le regole del prompt
passano in ISTRUZIONI, in cima. La versione finita è in solutions/aikit/rag.py.
Un modulo di aikit/ si modifica così: in aula, dichiarato, mai in silenzio.
"""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent.parent   # scripts/, tre livelli sopra
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from dotenv import load_dotenv               # noqa: E402
from openai import OpenAI                    # noqa: E402

from aikit.loaders import load               # noqa: E402 — Modulo 2 · Lezione 4
from aikit.clean import clean, pipeline_for  # noqa: E402 — Modulo 2 · Lezione 5
from aikit.chunk import chunk_recursive      # noqa: E402 — Modulo 2 · Lezione 10
from aikit.embeddings import embed           # noqa: E402 — Modulo 2 · Lezione 7
from aikit import vectorstore                # noqa: E402 — Modulo 2 · Lezione 9

load_dotenv()

client = OpenAI()

# ---------------------------------------- il punto unico di configurazione
# Tutto ciò che nel Progetto Modulo 2 stava sparso nel codice ora sta qui:
# per cambiare un parametro si tocca UNA riga, e si vede subito cosa c'è da
# tarare. Da Modulo 3 · Lezione 4 in poi le manopole si girano da qui.
CONFIG = {
    "corpus_dir": SCRIPTS / "dataset" / "lumen_m3",  # i sei documenti Lumen
    "collection": "lumen_m3",       # la collection del modulo, si indicizza una volta
    "chunk_size": 500,              # recursive, come nel Modulo 2
    "k": 4,                         # chunk recuperati per domanda
    "modello": "gpt-4o-mini",       # il generator
}

# Le domande di prova del main: una sui documenti storici, una sui documenti
# nuovi del corpus esteso, una FUORI corpus (deve uscire il rifiuto pulito).
DOMANDA_STORICA = "Quanto tempo ho per richiedere il contributo per la postazione di casa?"
DOMANDA_NUOVA = "Quanto costa il vassoio portacavi e come si fissa?"
DOMANDA_FUORI = "Posso pagare alla consegna, in contrassegno?"


# ------------------------- indicizza · scritta a Modulo 3 · Lezione 2
def indicizza():
    """L'ingest: load → clean → chunk → embed → upsert, su tutto il corpus.

    Ricrea la collection da ZERO (vectorstore.crea_collection): rilanciare
    non raddoppia i chunk. Stampa il conteggio per documento e ritorna il
    numero totale di chunk indicizzati.
    """
    collection = vectorstore.crea_collection(CONFIG["collection"])
    ids, testi, meta = [], [], []
    for percorso in sorted(CONFIG["corpus_dir"].glob("*.txt")):
        documenti = load(str(percorso))                                  # Modulo 2 · Lezione 4
        testo_grezzo = "\n".join(d.text for d in documenti)
        testo_pulito = clean(testo_grezzo, pipeline_for(str(percorso)))  # Modulo 2 · Lezione 5
        pezzi = chunk_recursive(testo_pulito, CONFIG["chunk_size"])      # Modulo 2 · Lezione 10
        for i, pezzo in enumerate(pezzi):
            ids.append(f"{percorso.stem}-{i:03d}")
            testi.append(pezzo)
            meta.append({"source": percorso.name})
        print(f"  {percorso.stem}: {len(pezzi)} chunk")
    vettori = embed(testi)                                               # Modulo 2 · Lezione 7
    vectorstore.indicizza(collection, ids, testi, vettori, meta)
    print(f"indicizzati {len(testi)} chunk da {len(list(CONFIG['corpus_dir'].glob('*.txt')))} "
          f"documenti in '{CONFIG['collection']}'")
    return len(testi)


# -------------------------- recupera · scritta a Modulo 3 · Lezione 2
def recupera(query, k=None):
    """Il retrieve: i k chunk più pertinenti per la query, dal più simile.

    Ogni chunk è un dict {"id", "testo", "score", "source"}. Se k non è
    indicato vale quello di CONFIG. La collection si riapre qui dentro con
    vectorstore.apri_collection(CONFIG["collection"]).
    """
    if k is None:
        k = CONFIG["k"]
    collection = vectorstore.apri_collection(CONFIG["collection"])
    return vectorstore.search(collection, query, k)


# -------------------------- rispondi · scritta a Modulo 3 · Lezione 2
def rispondi(query):
    """Il generate: risposta con citazioni, insieme ai chunk usati.

    Il prompt è quello di Modulo 2 · Lezione 11 — sezioni marcate, risposta
    SOLO dai documenti, citazione della fonte tra parentesi quadre, rifiuto
    pulito quando la risposta non c'è. Ritorna (risposta, chunks): i chunk
    che hanno fatto da contesto sono lo strumento di debug del modulo.
    """
    chunks = recupera(query)
    documenti = ""
    for c in chunks:
        documenti += f'<documento fonte="{c["id"]}">\n{c["testo"]}\n</documento>\n'

    prompt = f"""Rispondi alla domanda usando SOLO le informazioni nei documenti
qui sotto. Cita la fonte tra parentesi quadre, per esempio:
[policy-resi-garanzia-002]. Se la risposta non è nei documenti, rispondi
esattamente: "Non lo trovo nei documenti." — senza inventare nulla.

<documenti>
{documenti}</documenti>

<domanda>
{query}
</domanda>"""

    r = client.responses.create(
        model=CONFIG["modello"],
        input=[{"role": "user", "content": prompt}],
    )
    return r.output_text, chunks


# ------------------------------------------------- helper di stampa (dati)
def stampa_chunks(chunks):
    """I chunk recuperati, uno per riga: posizione, id, score, anteprima."""
    for posizione, c in enumerate(chunks, start=1):
        anteprima = " ".join(c["testo"].split())[:58]
        print(f"   {posizione}. {c['id']}  score={c['score']:.3f}  {anteprima}…")


if __name__ == "__main__":
    # L'ingest si fa una volta: se la collection è già piena non si ripaga.
    # Per ricostruirla da zero (corpus cambiato): chiamare indicizza() a mano.
    try:
        collection = vectorstore.apri_collection(CONFIG["collection"])
        if collection.count() == 0:
            indicizza()
            # crea_collection ricrea da zero: il riferimento va riaperto
            collection = vectorstore.apri_collection(CONFIG["collection"])
        print(f"collection '{CONFIG['collection']}': {collection.count()} chunk")
    except NotImplementedError:
        raise SystemExit("indicizza() è ancora da scrivere: si parte da lì.")

    for domanda in (DOMANDA_STORICA, DOMANDA_NUOVA, DOMANDA_FUORI):
        print("\n" + "=" * 72)
        print(f"D: {domanda}")
        try:
            chunks = recupera(domanda)
        except NotImplementedError:
            print("   recupera(): ancora da scrivere")
            continue
        stampa_chunks(chunks)
        try:
            risposta, usati = rispondi(domanda)
        except NotImplementedError:
            print("   rispondi(): ancora da scrivere")
            continue
        print(f"→ {risposta}")
