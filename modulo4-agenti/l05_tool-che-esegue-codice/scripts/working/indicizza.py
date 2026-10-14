"""indicizza.py — costruisce l'indice dei documenti di ufficio/ per l'assistente.

Legge tutti i documenti della cartella (PDF, DOCX, HTML, MD), li pulisce, li
taglia in chunk, calcola gli embedding e li salva nella collection «valtesa»
in indice/. Alla fine prova una ricerca. L'indice non è in git (Chroma
riscrive i suoi file a ogni apertura): si lancia una volta in ogni cartella
di lezione, e di nuovo se cambiano i documenti.

È lo script dell'obiettivo 2 di Modulo 3 · Lezione 12, sui documenti del progetto.

Uso:  python indicizza.py
"""
from pathlib import Path

CARTELLA = Path(__file__).parent

from dotenv import load_dotenv
load_dotenv(CARTELLA / ".env")

from aikit.loaders import load                      # Modulo 2 · Lezione 4
from aikit.clean import clean, pipeline_for         # Modulo 2 · Lezione 5
from aikit.chunk import chunk_recursive             # Modulo 2 · Lezione 10
from aikit.embeddings import embed                  # Modulo 2 · Lezione 7
from aikit import vectorstore                       # Modulo 2 · Lezione 9

COLLECTION = "valtesa"
DOCUMENTI = CARTELLA / "ufficio"
CHUNK = 500                                         # caratteri, come nel resto del corso
FORMATI = (".txt", ".md", ".pdf", ".docx", ".html")  # quelli che i loader di aikit leggono
PROVA = "massimale della cena in trasferta a Milano"

ids, testi, fonti = [], [], []
for percorso in sorted(DOCUMENTI.iterdir()):
    if percorso.suffix.lower() not in FORMATI:
        continue                                    # file nascosti (.DS_Store) e formati che i loader non leggono
    pagine = load(str(percorso))                    # una lista di Document (nei PDF, una per pagina)
    testo = "\n".join(p.text for p in pagine)
    testo = clean(testo, pipeline_for(str(percorso)))
    pezzi = chunk_recursive(testo, CHUNK)
    for i, pezzo in enumerate(pezzi):
        ids.append(f"{percorso.stem}-{i:03d}")      # l'id è quello che il modello cita
        testi.append(pezzo)
        fonti.append({"source": percorso.name})
    print(f"{percorso.name}: {len(pezzi)} chunk")

collection = vectorstore.crea_collection(COLLECTION)   # da zero: rilanciare non raddoppia i chunk
vectorstore.indicizza(collection, ids, testi, embed(testi), fonti)
print(f"{len(testi)} chunk nella collection '{COLLECTION}'")

print(f"\nProva: {PROVA}")
for r in vectorstore.search(collection, PROVA, 3):
    print(f"  {r['score']:.2f}  {r['source']}  {r['testo'][:70]!r}")
