"""obiettivo1_chat.py — un agente in chat, con la sessione su file (versione del docente).

Ancora senza tool: l'agente risponde con quello che sa. La sessione tiene la
storia: chiusa e riaperta la chat con lo stesso nome, ricorda lo scambio prima.

Uso (dalla cartella scripts/):  python solutions/obiettivo1_chat.py
"""
from pathlib import Path

from dotenv import load_dotenv

SCRIPTS = Path(__file__).parent.parent
load_dotenv(SCRIPTS / ".env")                       # la chiave, prima di importare agents

from agents import Agent, Runner, SQLiteSession     # Modulo 3 · Lezione 10 e 11

MODELLO = "gpt-5.6-luna"
SESSIONI = SCRIPTS / "sessioni.db"

agente = Agent(
    name="Assistente Valtesa",
    instructions="Sei l'assistente dell'ufficio del personale di Valtesa S.r.l. Rispondi in italiano, in poche frasi.",
    model=MODELLO,
)

nome = input("Nome della sessione: ").strip()
sessione = SQLiteSession(nome, SESSIONI)
print(f"Sessione «{nome}». Invio a vuoto per uscire.")

while True:
    domanda = input("\nTu> ").strip()
    if not domanda:
        break
    result = Runner.run_sync(agente, domanda, session=sessione)
    print(f"→ {result.final_output}")
