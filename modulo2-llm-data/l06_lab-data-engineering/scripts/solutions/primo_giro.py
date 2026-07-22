"""Il "primo giro" — la demo guida del docente (VERSIONE FINITA di riferimento).

Un solo file, tutto il metodo del giorno: carica → guarda → diagnostica →
correggi. Il docente lo scrive dal vivo su `faq_prodotto.html`; gli studenti
replicano lo stesso ciclo su tutto il dataset nel Lab 1 (`triage.py`).

    python primo_giro.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scaffolding"))   # aikit vive lì

from aikit import load

PATH = Path(__file__).parent.parent / "dataset" / "faq_prodotto.html"

# 1 · CARICA
docs = load(str(PATH))

# 2 · GUARDA — mai fidarsi del "nessun errore": quanti caratteri? che aspetto ha?
testo = "\n".join(d.text for d in docs)
print(f"{PATH.name}: {len(docs)} document(i), {len(testo)} caratteri\n")
print("--- inizio dell'output ---")
print(testo[:400])
print("…\n")

# 3 · DIAGNOSTICA — il contenuto c'è, ma è annegato nel boilerplate web:
#     cookie banner, menu, newsletter, footer. Al chatbot arriverebbe TUTTO.

# 4 · CORREGGI — il primo fix, mirato: via le righe del cookie banner.
#     (Il fix sistematico, con una pipeline per ogni file, è il Lab 2.)
senza_cookie = "\n".join(l for l in testo.split("\n") if "cookie" not in l.lower())
print(f"dopo il primo fix: {len(senza_cookie)} caratteri "
      f"({len(testo) - len(senza_cookie)} di cookie banner in meno)")
