"""assistente.py — l'assistente dell'ufficio del personale di Valtesa.

Un agente dell'OpenAI Agents SDK. Con TOOL_DI_CARTELLA = False ha i due tool di
Modulo 3: cerca_documenti sull'indice dei documenti di ufficio/ (costruito da
indicizza.py, in indice/) e query_db sul database dati/valtesa.db, in sola
lettura. Con TOOL_DI_CARTELLA = True ha i tool di cartella di
strumenti_cartella.py: elenca_file, cerca e leggi_file su ufficio/. Con anche
ESEGUI_PYTHON = True ha esegui_python di esecuzione.py, che esegue codice scritto
dal modello: sempre sotto approvazione, a ogni chiamata il codice a schermo e
sì o no. Ricorda la conversazione in una sessione salvata in sessioni.db. Sotto
ogni risposta la traccia: i tool chiamati, il loro output, chiamate e token.

È l'assistente del docente di Modulo 3 · Lezione 12, sui dati del progetto,
portato ad async e a gpt-6-luna in Modulo 4 · Lezione 4, con i tool di
cartella di Modulo 4 · Lezione 4 ed esegui_python di Modulo 4 · Lezione 5.

Uso:  python assistente.py
"""
import asyncio
import sqlite3
from pathlib import Path

CARTELLA = Path(__file__).parent

from dotenv import load_dotenv
load_dotenv(CARTELLA / ".env")                      # la chiave, prima di importare agents

from agents import Agent, Runner, function_tool, SQLiteSession, MaxTurnsExceeded, ToolCallItem, ToolCallOutputItem
from aikit import vectorstore
from aikit.llm_client import cost_usd
from strumenti_cartella import elenca_file, cerca, leggi_file
from esecuzione import esegui_python, ISTRUZIONI_CODICE, esegui_con_approvazione, riprendi_in_sospeso, file_stato

COLLECTION = "valtesa"                              # la collection in indice/
DB = CARTELLA / "dati" / "valtesa.db"
SESSIONI = CARTELLA / "sessioni.db"
MODELLO = "gpt-6-luna"
TOOL_DI_CARTELLA = True                             # True: i tool di cartella al posto di quelli di Modulo 3
ESEGUI_PYTHON = False                               # True: anche esegui_python, sempre sotto approvazione (con i tool di cartella)
K = 4                                               # quanti chunk rimanda cerca_documenti
LIMITE = 50                                         # quante righe rimanda query_db, al massimo
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
    collection = vectorstore.apri_collection(COLLECTION)
    testo = ""
    for c in vectorstore.search(collection, domanda, K):
        testo += f"[{c['id']}]\n{c['testo']}\n\n"
    return testo.strip()


@function_tool
def query_db(sql: str) -> str:
    """Esegue una query SQL (solo SELECT, dialetto SQLite) sul database del
    personale di Valtesa e ritorna le righe trovate. Tabelle e colonne:
    dipendenti(id INTEGER, nome TEXT, cognome TEXT, sede TEXT, reparto TEXT, ruolo TEXT, data_assunzione TEXT, contratto TEXT)
    assenze(id INTEGER, dipendente_id INTEGER, tipo TEXT, data_inizio TEXT, data_fine TEXT, quantita INTEGER, unita TEXT)
    note_spese(id INTEGER, dipendente TEXT, voce TEXT, citta TEXT, giorno TEXT, importo REAL, stato TEXT, dipendente_id INTEGER, notti INTEGER)
    massimali(voce TEXT, citta TEXT, massimale INTEGER, valido_dal TEXT)

    Args:
        sql: la query SELECT da eseguire.
    """
    if not sql.strip().lower().startswith("select"):
        return "Errore: sono ammesse solo query SELECT."
    try:
        con = sqlite3.connect(DB.as_uri() + "?mode=ro", uri=True)   # sola lettura
        cursore = con.execute(sql)
        colonne = [c[0] for c in cursore.description]
        righe = cursore.fetchmany(LIMITE + 1)
        con.close()
    except Exception as e:
        return f"Errore: {e}"                       # torna al modello, che può correggere la query
    testo = " | ".join(colonne)
    for riga in righe[:LIMITE]:
        testo += "\n" + " | ".join(str(v) for v in riga)
    if len(righe) > LIMITE:
        testo += f"\n(mostrate solo le prime {LIMITE} righe)"
    return testo


ISTRUZIONI = """Sei l'assistente dell'ufficio del personale di Valtesa S.r.l., per i dipendenti. Rispondi in italiano, in poche frasi.
Per rispondere hai due strade:
- domande su regole e procedure (ferie e permessi, trasferte e note spese, welfare e buoni pasto, ingresso e dotazioni, circolari, portale): usa cerca_documenti e cita i passaggi che usi con il loro id tra parentesi quadre, per esempio [regolamento-ferie-permessi-003];
- domande su dipendenti, assenze e note spese: usa query_db.
Se una domanda ha bisogno di tutte e due, usa tutti e due i tool.
Rispondi SOLO con quello che i tool ti restituiscono. Se non trovi la risposta, di' che non l'hai trovata e dove hai cercato. Se una domanda non riguarda Valtesa, di' che non puoi rispondere, senza usare i tool. Se un tool ritorna un errore due volte di fila, fermati. Non inventare mai."""

ISTRUZIONI_CARTELLA = """Sei l'assistente dell'ufficio del personale di Valtesa S.r.l., per i dipendenti. Rispondi in italiano, in poche frasi.
Lavori sulla cartella dell'ufficio: i documenti (regolamenti, policy, circolari, procedure, FAQ) e gli export del gestionale in CSV (note spese, massimali, dipendenti, assenze).
Hai tre tool: elenca_file per vedere i file, cerca per trovare le righe che contengono un testo, leggi_file per leggere un file. Cita i file che usi tra parentesi quadre, per esempio [regolamento-ferie-permessi.md].
Rispondi SOLO con quello che i tool ti restituiscono. Se non trovi la risposta, di' che non l'hai trovata e dove hai cercato. Se una domanda non riguarda Valtesa, di' che non puoi rispondere, senza usare i tool. Se un tool ritorna un errore due volte di fila, fermati. Non inventare mai."""

if TOOL_DI_CARTELLA and ESEGUI_PYTHON:
    agente = Agent(name="Assistente Valtesa", instructions=ISTRUZIONI_CARTELLA + "\n" + ISTRUZIONI_CODICE,
                   tools=[elenca_file, cerca, leggi_file, esegui_python], model=MODELLO)
elif TOOL_DI_CARTELLA:
    agente = Agent(name="Assistente Valtesa", instructions=ISTRUZIONI_CARTELLA,
                   tools=[elenca_file, cerca, leggi_file], model=MODELLO)
else:
    agente = Agent(name="Assistente Valtesa", instructions=ISTRUZIONI,
                   tools=[cerca_documenti, query_db], model=MODELLO)


def stampa_traccia(result):
    """La traccia del run, come in Modulo 3 · Lezione 10: ogni tool chiesto con i suoi
    argomenti e, sotto, l'inizio del suo output (il modello riceve tutto). In fondo
    chiamate al modello, token e costo."""
    for item in result.new_items:
        if isinstance(item, ToolCallItem):
            print(f"   tool     {item.raw_item.name}({item.raw_item.arguments})")
        elif isinstance(item, ToolCallOutputItem):
            righe = str(item.output).split("\n")
            print(f"   output   {righe[0][:200]}")
            for riga in righe[1:4]:
                print(f"            {riga[:200]}")
            if len(righe) > 4:
                print(f"            … altre {len(righe) - 4} righe")
    u = result.context_wrapper.usage
    costo = cost_usd(MODELLO, u.input_tokens, u.output_tokens)
    print(f"   {u.requests} chiamat{'a' if u.requests == 1 else 'e'} · {u.input_tokens} token in, {u.output_tokens} out · ${costo:.5f}")


async def main():
    nome = input("Nome della sessione: ").strip()
    sessione = SQLiteSession(nome, SESSIONI)
    print(f"Sessione «{nome}». Invio a vuoto per uscire.")
    if ESEGUI_PYTHON and file_stato(sessione).exists():   # un run lasciato a metà, al lancio prima
        try:
            result = await riprendi_in_sospeso(agente, sessione, MAX_TURNI)
        except MaxTurnsExceeded:
            print(f"   nessuna risposta dopo {MAX_TURNI} chiamate; lo stato resta in {file_stato(sessione).name}")
            return
        if result is None:                          # uscito di nuovo: lo stato è di nuovo su file
            return
        stampa_traccia(result)
        print(f"→ {result.final_output}")
    while True:
        domanda = input("\nTu> ").strip()
        if not domanda:
            break
        try:
            if ESEGUI_PYTHON:
                result = await esegui_con_approvazione(agente, domanda, sessione, MAX_TURNI)
            else:
                result = await Runner.run(agente, domanda, session=sessione, max_turns=MAX_TURNI)
        except MaxTurnsExceeded:
            print(f"   nessuna risposta dopo {MAX_TURNI} chiamate")
            continue
        if result is None:                          # l'utente è uscito: lo stato è su file
            return
        stampa_traccia(result)
        print(f"→ {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
