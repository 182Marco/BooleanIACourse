"""assistente.py — l'assistente dell'ufficio del personale di Valtesa, versione 1.0.

Un agente dell'OpenAI Agents SDK con:
- i tool di cartella di strumenti_cartella.py (elenca_file, cerca, leggi_file) sulla cartella
  completa dell'ufficio, ufficio-completo/;
- le skill di skill-assistente/: l'indice nelle istruzioni, il corpo con apri_skill (skill.py);
- due function tool, codice nostro: note_fuori_massimale (con rimborsi.py) e scadenze_ingresso
  (con scadenze.py);
- con --app, i tool del server MCP di un'app dell'ufficio (Trello, Notion o Airtable, in app.py),
  con il login di login_mcp.py.
Con ESEGUI_PYTHON = True ha anche esegui_python di esecuzione.py, che esegue codice scritto dal
modello: sempre sotto approvazione, a ogni chiamata il codice a schermo e sì o no. Ricorda la
conversazione in una sessione salvata in sessioni.db. Sotto ogni risposta la traccia: i tool
chiamati, il loro output, chiamate e token.

rispondi() è un giro dell'assistente su una domanda: la usano main() e valuta.py, quindi quello
che cambiate lì vale per tutti e due. valuta.py usa l'assistente senza app.

Uso:  python assistente.py                            la chat, senza app
      python assistente.py --app trello               la chat, con l'app (il login la prima volta)
      python assistente.py --app trello "domanda"     una domanda sola, senza sessione salvata
      python assistente.py --app trello --login       solo il login; lo rifà anche se c'è già
      python assistente.py --app trello --tool        i tool del server; con * quelli che riceve il modello
      python assistente.py --istruzioni               il testo delle istruzioni che riceve il modello
"""
import argparse
import asyncio
import csv
from pathlib import Path

CARTELLA = Path(__file__).parent

from dotenv import load_dotenv
load_dotenv(CARTELLA / ".env")                      # la chiave, prima di importare agents

from agents import Agent, Runner, SQLiteSession, MaxTurnsExceeded, ToolCallItem, ToolCallOutputItem, function_tool
from aikit.llm_client import cost_usd
from strumenti_cartella import elenca_file, cerca, leggi_file
from esecuzione import esegui_python, ISTRUZIONI_CODICE, esegui_con_approvazione, riprendi_in_sospeso, file_stato
from skill import ISTRUZIONI_SKILL, apri_skill
from app import APP, ISTRUZIONI_APP, server_app
from login_mcp import fai_login
import rimborsi
import scadenze

SESSIONI = CARTELLA / "sessioni.db"
MODELLO = "gpt-6-luna"
ESEGUI_PYTHON = False                               # True: anche esegui_python, sempre sotto approvazione
MAX_TURNI = 40                                      # era 10 prima della 0.9: con l'app servono più chiamate

ISTRUZIONI = """Sei l'assistente dell'ufficio del personale di Valtesa S.r.l., per i dipendenti. Rispondi in italiano, in poche frasi.
Lavori sulla cartella dell'ufficio: i documenti (regolamenti, policy, circolari, procedure, FAQ) e gli export del gestionale in CSV (note spese, massimali, dipendenti, assenze).
Per i file hai tre tool: elenca_file per vedere i file, cerca per trovare le righe che contengono un testo, leggi_file per leggere un file. Cita i file che usi tra parentesi quadre, per esempio [faq-portale-dipendenti.md].
Rispondi SOLO con quello che i tool ti restituiscono. Se non trovi la risposta, di' che non l'hai trovata e dove hai cercato. Se una domanda non riguarda Valtesa, di' che non puoi rispondere, senza usare i tool. Se un tool ritorna un errore due volte di fila, fermati. Non inventare mai."""


def testo_fuori_massimale(mese):
    """Le note spese fuori massimale di un mese AAAA-MM, una riga per nota, dal programma dei rimborsi."""
    with open(rimborsi.NOTE_SPESE, newline="", encoding="utf-8") as f:
        note = [nota for nota in csv.DictReader(f) if nota["giorno"].startswith(mese + "-")]
    fuori = [nota for nota in note if not rimborsi.controlla(nota)]
    righe = [f"{len(fuori)} note fuori massimale in {mese}, su {len(note)}."]
    for nota in fuori:
        righe.append(f"nota {nota['id']}: {nota['dipendente']}, {nota['voce']} a {nota['citta']} il {nota['giorno']}, "
                     f"{float(nota['importo']):.2f} €, massimale {rimborsi.limite_nota(nota):.2f} €")
    return "\n".join(righe)


@function_tool
def note_fuori_massimale(mese: str) -> str:
    """Le note spese fuori massimale di un mese AAAA-MM, calcolate dal programma dei rimborsi: una riga per nota, con id, dipendente, voce, città, giorno, importo e massimale."""
    return testo_fuori_massimale(mese)


@function_tool
def scadenze_ingresso(id_ingresso: str) -> str:
    """Chi è un nuovo assunto di assunzioni.csv, il suo indirizzo di posta e le date della procedura di ingresso, calcolati da scadenze.py. id_ingresso è l'id (per esempio 201), o «tutti» per tutti gli ingressi."""
    assunti = scadenze.carica()
    scelti = assunti if id_ingresso == "tutti" else [a for a in assunti if a["id"] == id_ingresso]
    if not scelti:
        return f"Nessun ingresso con id «{id_ingresso}». Gli id sono: {', '.join(a['id'] for a in assunti)}."
    return "\n\n".join(scadenze.testo(a) for a in scelti)


def crea_agente(app=None, server=None):
    """L'assistente; con app e server, anche i tool dell'app e la riga di istruzioni che li riguarda."""
    istruzioni = ISTRUZIONI + ("\n" + ISTRUZIONI_CODICE if ESEGUI_PYTHON else "")
    if app:
        istruzioni += "\n" + ISTRUZIONI_APP.format(app=app.capitalize())
    istruzioni += "\n\n" + ISTRUZIONI_SKILL
    tools = [elenca_file, cerca, leggi_file] + ([esegui_python] if ESEGUI_PYTHON else [])
    tools += [apri_skill, note_fuori_massimale, scadenze_ingresso]
    return Agent(name="Assistente Valtesa", instructions=istruzioni, tools=tools, model=MODELLO,
                 mcp_servers=[server] if server else [])


agente = crea_agente()                              # senza app: lo usano valuta.py e i test


ULTIMO_PASSO = ("Hai usato tutti i passi a disposizione. Rispondi adesso, senza altri tool, con "
                "quello che hai trovato finora, e di' chiaramente cosa non sei riuscito a verificare.")


async def rispondi(domanda, sessione, con=None):
    """Un giro dell'assistente su una domanda, nella sessione data, con l'agente con (quello senza app
    se non lo si dà). Ritorna il result del run, o None se l'utente esce a metà di un'approvazione
    (lo stato è su file). Se il modello non arriva a una risposta in MAX_TURNI chiamate, invece
    dell'errore una chiamata in più, senza tool, chiede la risposta con quello che ha: come la
    risposta forzata di smolagents. La sessione ha già tutto quello che il modello ha letto."""
    con = con or agente
    try:
        if ESEGUI_PYTHON:
            return await esegui_con_approvazione(con, domanda, sessione, MAX_TURNI)
        return await Runner.run(con, domanda, session=sessione, max_turns=MAX_TURNI)
    except MaxTurnsExceeded as errore:
        senza_tool = con.clone(tools=[], mcp_servers=[])
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


async def chat(con):
    """La chat da terminale, in una sessione con un nome: invio a vuoto per uscire."""
    nome = input("Nome della sessione: ").strip()
    sessione = SQLiteSession(nome, SESSIONI)
    print(f"Sessione «{nome}». Invio a vuoto per uscire.")
    if ESEGUI_PYTHON and file_stato(sessione).exists():   # un run lasciato a metà, al lancio prima
        try:
            result = await riprendi_in_sospeso(con, sessione, MAX_TURNI)
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
            result = await rispondi(domanda, sessione, con)
        except MaxTurnsExceeded:
            print(f"   nessuna risposta dopo {MAX_TURNI} chiamate")
            continue
        if result is None:                          # l'utente è uscito: lo stato è su file
            return
        stampa_traccia(result)
        print(f"→ {result.final_output}")


async def una_domanda(con, domanda):
    """Una domanda sola, in una sessione in memoria che non si salva."""
    result = await rispondi(domanda, SQLiteSession("una-domanda"), con)
    if result is not None:
        stampa_traccia(result)
        print(f"→ {result.final_output}")


async def main():
    parser = argparse.ArgumentParser(description="L'assistente dell'ufficio del personale di Valtesa.")
    parser.add_argument("domanda", nargs="*", help="una domanda sola; senza, la chat")
    parser.add_argument("--app", choices=sorted(APP), help="l'app dell'ufficio da collegare")
    parser.add_argument("--login", action="store_true", help="solo il login all'app; lo rifà anche se c'è già")
    parser.add_argument("--tool", action="store_true", help="i tool del server dell'app")
    parser.add_argument("--istruzioni", action="store_true", help="il testo delle istruzioni che riceve il modello")
    args = parser.parse_args()
    if args.istruzioni:
        print(crea_agente(args.app).instructions)
        return
    if not args.app:
        if args.login or args.tool:
            parser.error("--login e --tool vogliono --app")
        if args.domanda:
            await una_domanda(agente, " ".join(args.domanda))
        else:
            await chat(agente)
        return
    await fai_login(args.app, APP[args.app]["url"], di_nuovo=args.login)
    if args.login:
        print(f"Login a {args.app} fatto: il token è in .mcp-token/{args.app}.json")
        return
    if args.tool:                                   # tutti i tool del server, senza filtro
        async with server_app(args.app, filtro=False) as server:
            for tool in await server.list_tools():
                tenuto = "*" if tool.name in APP[args.app]["tool"] else " "
                print(f"{tenuto} {tool.name}: {(tool.description or '-').splitlines()[0][:110]}")
        return
    server = server_app(args.app)
    async with server:                              # si collega al server dell'app; alla fine chiude
        con = crea_agente(args.app, server)
        if args.domanda:
            await una_domanda(con, " ".join(args.domanda))
        else:
            await chat(con)


if __name__ == "__main__":
    asyncio.run(main())
