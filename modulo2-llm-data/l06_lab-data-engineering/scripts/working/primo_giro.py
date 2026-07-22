"""Il "primo giro" — la demo guida del docente (CANOVACCIO: si scrive dal vivo).

⚠️ Questo file è volutamente quasi vuoto: si riempie DURANTE la demo, non prima.

Un solo file, tutto il metodo del giorno. Il docente lo costruisce a schermo su
`faq_prodotto.html`; tu replica pure qui mentre guardi. Nel Lab 1 applicherai
lo stesso ciclo a tutto il dataset (`triage.py`).

    python primo_giro.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scaffolding"))   # aikit vive lì

from aikit import load

PATH = Path(__file__).parent.parent / "dataset" / "faq_prodotto.html"

# 1 · CARICA


# 2 · GUARDA — mai fidarsi del "nessun errore": quanti caratteri? che aspetto ha?


# 3 · DIAGNOSTICA — che cosa c'è nell'output che NON vorresti dare al chatbot?


# 4 · CORREGGI — un primo fix mirato (quello sistematico è il Lab 2)
