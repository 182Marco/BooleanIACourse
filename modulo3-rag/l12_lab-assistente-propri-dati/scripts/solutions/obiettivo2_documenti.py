"""obiettivo2_documenti.py — un vector DB con i documenti del tema (versione del docente).

Legge tutti i documenti della cartella (PDF, DOCX, HTML, MD), li pulisce, li
taglia in chunk, calcola gli embedding e li salva in una collection. Alla
fine prova una ricerca.

Uso (dalla cartella scripts/):  python solutions/obiettivo2_documenti.py
"""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))    # per importare aikit

from dotenv import load_dotenv
load_dotenv(SCRIPTS / ".env")

from aikit.loaders import load                      # Modulo 2 · Lezione 4
from aikit.clean import clean, pipeline_for         # Modulo 2 · Lezione 5
from aikit.chunk import chunk_recursive             # Modulo 2 · Lezione 10
from aikit.embeddings import embed                  # Modulo 2 · Lezione 7
from aikit import vectorstore                       # Modulo 2 · Lezione 9

TEMA = "valtesa"                                    # oppure "valdoria"
DOCUMENTI = SCRIPTS / "temi" / TEMA / "documenti"
CHUNK = 500                                         # caratteri, come nel resto del modulo
FORMATI = (".txt", ".md", ".pdf", ".docx", ".html")  # quelli che i loader di aikit leggono
PROVA = {"valtesa": "massimale della cena in trasferta",
         "valdoria": "quante volte si rinnova un DVD"}[TEMA]

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

collection = vectorstore.crea_collection(TEMA)      # da zero: rilanciare non raddoppia i chunk
vectorstore.indicizza(collection, ids, testi, embed(testi), fonti)
print(f"{len(testi)} chunk nella collection '{TEMA}'")

print(f"\nProva: {PROVA}")
for r in vectorstore.search(collection, PROVA, 3):
    print(f"  {r['score']:.2f}  {r['source']}  {r['testo'][:70]!r}")
