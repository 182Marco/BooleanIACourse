"""assistente.py — l'assistente dell'ufficio del personale di Valtesa.

Un agente dell'OpenAI Agents SDK con i tool di cartella di strumenti_cartella.py
(elenca_file, cerca, leggi_file) sulla cartella completa dell'ufficio,
ufficio-completo/. Con ESEGUI_PYTHON = True ha anche esegui_python di
esecuzione.py, che esegue codice scritto dal modello: sempre sotto approvazione,
a ogni chiamata il codice a schermo e sì o no. Ricorda la conversazione in una
sessione salvata in sessioni.db. Sotto ogni risposta la traccia: i tool chiamati,
il loro output, chiamate e token.

È l'assistente del docente di Modulo 4 · Lezione 6: rispondi() dà la risposta forzata
quando il modello arriva al limite dei turni. Da questa lezione i tool di Modulo 3
(cerca_documenti e query_db) non ci sono più: l'assistente lavora solo sulla cartella. rispondi() è un giro dell'assistente su una domanda: la usano
main() e valuta.py, quindi quello che cambiate lì vale per tutti e due.

Uso:  python assistente.py
"""
import asyncio
from pathlib import Path

CARTELLA = Path(__file__).parent

from dotenv import load_dotenv
load_dotenv(CARTELLA / ".env")                      # la chiave, prima di importare agents

from agents import Agent, Runner, SQLiteSession, MaxTurnsExceeded, ToolCallItem, ToolCallOutputItem
from aikit.llm_client import cost_usd
from strumenti_cartella import elenca_file, cerca, leggi_file
from esecuzione import esegui_python, ISTRUZIONI_CODICE, esegui_con_approvazione, riprendi_in_sospeso, file_stato

SESSIONI = CARTELLA / "sessioni.db"
MODELLO = "gpt-6-luna"
ESEGUI_PYTHON = False                               # True: anche esegui_python, sempre sotto approvazione
MAX_TURNI = 10

ISTRUZIONI = """Sei l'assistente dell'ufficio del personale di Valtesa S.r.l., per i dipendenti. Rispondi in italiano, in poche frasi.
Lavori sulla cartella dell'ufficio: i documenti (regolamenti, policy, circolari, procedure, FAQ) e gli export del gestionale in CSV (note spese, massimali, dipendenti, assenze).
Hai tre tool: elenca_file per vedere i file, cerca per trovare le righe che contengono un testo, leggi_file per leggere un file. Cita i file che usi tra parentesi quadre, per esempio [faq-portale-dipendenti.md].
Rispondi SOLO con quello che i tool ti restituiscono. Se non trovi la risposta, di' che non l'hai trovata e dove hai cercato. Se una domanda non riguarda Valtesa, di' che non puoi rispondere, senza usare i tool. Se un tool ritorna un errore due volte di fila, fermati. Non inventare mai."""

if ESEGUI_PYTHON:
    agente = Agent(name="Assistente Valtesa", instructions=ISTRUZIONI + "\n" + ISTRUZIONI_CODICE,
                   tools=[elenca_file, cerca, leggi_file, esegui_python], model=MODELLO)
else:
    agente = Agent(name="Assistente Valtesa", instructions=ISTRUZIONI,
                   tools=[elenca_file, cerca, leggi_file], model=MODELLO)


ULTIMO_PASSO = ("Hai usato tutti i passi a disposizione. Rispondi adesso, senza altri tool, con "
                "quello che hai trovato finora, e di' chiaramente cosa non sei riuscito a verificare.")


async def rispondi(domanda, sessione):
    """Un giro dell'assistente su una domanda, nella sessione data. Ritorna il result del run,
    o None se l'utente esce a metà di un'approvazione (lo stato è su file). Se il modello non
    arriva a una risposta in MAX_TURNI chiamate, invece dell'errore una chiamata in più, senza
    tool, chiede la risposta con quello che ha: come la risposta forzata di smolagents. La
    sessione ha già tutto quello che il modello ha letto."""
    try:
        if ESEGUI_PYTHON:
            return await esegui_con_approvazione(agente, domanda, sessione, MAX_TURNI)
        return await Runner.run(agente, domanda, session=sessione, max_turns=MAX_TURNI)
    except MaxTurnsExceeded as errore:
        senza_tool = agente.clone(tools=[])
        result = await Runner.run(senza_tool, ULTIMO_PASSO, session=sessione, max_turns=1)
        if errore.run_data is not None:             # chiamate, token e traccia di tutto il giro
            result.context_wrapper.usage.add(errore.run_data.context_wrapper.usage)
            result.new_items[:0] = errore.run_data.new_items
        return result


def stampa_traccia(result):
    """La traccia del run, come in Modulo 3 · Lezione 10: ogni tool chiesto con i suoi
    argomenti e, sotto, l'inizio del suo output (il modello riceve tutto). In fondo
    chiamate al modello, token e costo."""
    for item in result.new_items:
        if isinstance(item, ToolCallItem):
            print(f"   tool     {item.raw_item.name}({item.raw_item.arguments})")
        elif isinstance(item, ToolCallOutputItem):
            output = item.output["text"] if isinstance(item.output, dict) else item.output   # i tool MCP: {"type": "text", ...}
            righe = str(output).split("\n")
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
            result = await rispondi(domanda, sessione)
        except MaxTurnsExceeded:
            print(f"   nessuna risposta dopo {MAX_TURNI} chiamate")
            continue
        if result is None:                          # l'utente è uscito: lo stato è su file
            return
        stampa_traccia(result)
        print(f"→ {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
