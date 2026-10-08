"""La prova della domanda 3 (obiettivo 1): cosa riceve il modello quando un tool fallisce.

Chiama i tool come fa l'SDK, con chiama() di tests/test_assistente.py, senza il modello.
assistente.py non si cambia: le costanti le cambia questo script. Il caso 3 chiama l'API degli
embedding per la domanda (meno di un centesimo) e lascia in indice/ una collection vuota,
«valtesa-vecchia», che non dà fastidio.

Uso, dalla cartella del progetto:  python prova_tool.py
(il docente, da scripts/ del materiale del corso: cp solutions/prova_tool.py . && python prova_tool.py)
"""
import os

import assistente
from tests.test_assistente import chiama

print("1. query_db, una query sbagliata:")
print("  ", chiama(assistente.query_db, sql="SELECT data FROM note_spese"))

print("2. cerca_documenti, con la chiave OpenAI sbagliata:")
chiave = os.environ["OPENAI_API_KEY"]
os.environ["OPENAI_API_KEY"] = "sk-chiave-sbagliata"
print("  ", chiama(assistente.cerca_documenti, domanda="ferie")[:150], "…")
os.environ["OPENAI_API_KEY"] = chiave

print("3. cerca_documenti, con una collection che non c'è (come senza indice):")
assistente.COLLECTION = "valtesa-vecchia"
print("  ", repr(chiama(assistente.cerca_documenti, domanda="ferie")))
