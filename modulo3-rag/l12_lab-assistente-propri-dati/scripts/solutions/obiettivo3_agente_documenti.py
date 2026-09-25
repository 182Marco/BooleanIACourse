"""obiettivo3_agente_documenti.py — l'agente con i documenti (versione del docente).

L'agente dell'obiettivo 1 con un tool: cerca_documenti sulla collection
dell'obiettivo 2. Sotto ogni risposta la traccia: quale tool ha chiamato,
con quale argomento, e la strada presa. Prima si lancia obiettivo2_documenti.py.

Uso (dalla cartella scripts/):  python solutions/obiettivo3_agente_documenti.py
"""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))    # per importare aikit

from dotenv import load_dotenv
load_dotenv(SCRIPTS / ".env")                       # la chiave, prima di importare agents

from agents import Agent, Runner, function_tool, SQLiteSession, MaxTurnsExceeded, ToolCallItem
from aikit import vectorstore

TEMA = "valtesa"
SESSIONI = SCRIPTS / "sessioni.db"
MODELLO = "gpt-5.6-luna"
K = 4                                               # quanti chunk rimanda cerca_documenti
MAX_TURNI = 10


@function_tool
def cerca_documenti(domanda: str) -> str:
    """Cerca nei documenti dell'ufficio del personale di Valtesa (regolamento
    ferie e permessi, policy trasferte e note spese, circolari del personale
    del 2026, regolamento welfare e buoni pasto, procedura di ingresso e
    dotazioni, FAQ del portale dipendenti) e ritorna i passaggi più pertinenti,
    ognuno preceduto dal suo id da citare. I passaggi possono non contenere la
    risposta.

    Args:
        domanda: la domanda da cercare nei documenti.
    """
    collection = vectorstore.apri_collection(TEMA)
    testo = ""
    for c in vectorstore.search(collection, domanda, K):
        testo += f"[{c['id']}]\n{c['testo']}\n\n"
    return testo.strip()


ISTRUZIONI = """Sei l'assistente dell'ufficio del personale di Valtesa S.r.l., per i dipendenti. Rispondi in italiano, in poche frasi.
Per le domande su regole e procedure (ferie e permessi, trasferte e note spese, welfare e buoni pasto, ingresso e dotazioni, circolari, portale) usa cerca_documenti e cita i passaggi che usi con il loro id tra parentesi quadre, per esempio [regolamento-ferie-permessi-003].
Rispondi SOLO con quello che il tool ti restituisce. Se non trovi la risposta, di' che non l'hai trovata e dove hai cercato. Se una domanda non riguarda Valtesa, di' che non puoi rispondere, senza usare il tool. Se il tool ritorna un errore due volte di fila, fermati. Non inventare mai."""

agente = Agent(
    name="Assistente Valtesa",
    instructions=ISTRUZIONI,
    tools=[cerca_documenti],
    model=MODELLO,
)


def tool_chiamati(result):
    """I tool chiamati per questa domanda: (nome, argomento)."""
    return [(item.raw_item.name, item.raw_item.arguments)
            for item in result.new_items if isinstance(item, ToolCallItem)]


def strada(result):
    """Dove ha cercato: "documenti", "dati", "documenti+dati" o "nessuna"."""
    nomi = [nome for nome, argomento in tool_chiamati(result)]
    if "cerca_documenti" in nomi and "query_db" in nomi:
        return "documenti+dati"
    if "cerca_documenti" in nomi:
        return "documenti"
    if "query_db" in nomi:
        return "dati"
    return "nessuna"


if __name__ == "__main__":
    nome = input("Nome della sessione: ").strip()
    sessione = SQLiteSession(nome, SESSIONI)
    print(f"Sessione «{nome}». Invio a vuoto per uscire.")
    while True:
        domanda = input("\nTu> ").strip()
        if not domanda:
            break
        try:
            result = Runner.run_sync(agente, domanda, session=sessione, max_turns=MAX_TURNI)
        except MaxTurnsExceeded:
            print(f"   nessuna risposta dopo {MAX_TURNI} chiamate")
            continue
        for nome_tool, argomento in tool_chiamati(result):
            print(f"   tool: {nome_tool}({argomento})")
        print(f"→ {result.final_output}")
        print(f"   strada: {strada(result)}")
