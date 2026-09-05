"""demo_brief.py — il problema del follow-up, dal vivo (strumento del DOCENTE).

Esegue sul rag.py della lezione scorsa (ora in aikit/) la coppia di domande
del reveal di Modulo 3 · Lezione 2, con pausa [invio] tra l'una e l'altra:

  1. la domanda vera sui ticket — risponde citando le fonti;
  2. il follow-up così com'è ("E per il secondo caso?") — il retrieval
     cerca letteralmente "secondo caso", i chunk non c'entrano niente e
     la risposta è il rifiuto pulito. È il problema della giornata.

Indicizza la collection `lumen_m3` se è vuota. Non fa parte del percorso
studente.

Uso (dalla cartella scripts/):
    python scaffolding/demo_brief.py
"""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from aikit import rag  # noqa: E402

DOMANDA_TICKET = "Perché il piano si ferma sempre a metà corsa?"
FOLLOW_UP = "E per il secondo caso?"

if __name__ == "__main__":
    if rag.vectorstore.apri_collection(rag.CONFIG["collection"]).count() == 0:
        rag.indicizza()
    for domanda in (DOMANDA_TICKET, FOLLOW_UP):
        input("\n[invio per continuare]")
        print("=" * 72)
        print(f"D: {domanda}")
        risposta, chunks = rag.rispondi(domanda)
        rag.stampa_chunks(chunks)
        print(f"→ {risposta}")
