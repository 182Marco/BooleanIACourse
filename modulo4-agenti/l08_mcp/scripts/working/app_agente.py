"""app_agente.py — l'assistente con il server MCP di un'app: Trello, Notion o Airtable.

Due tipi di tool, uno accanto all'altro:
- note_fuori_massimale è un function tool: il codice è nostro (chiama rimborsi.py) e gira
  dentro l'assistente;
- i tool dell'app sono di un altro: il loro server MCP sta in cloud, dal fornitore, e
  l'assistente gli inoltra le chiamate del modello. Il login lo fa login_mcp.py.

Di ogni app si tengono solo i tool che servono (tool_filter): un server ne ha decine, e
l'SDK manda le loro definizioni al modello a ogni chiamata.

Uso:  python app_agente.py trello --login        il login (si apre il browser); lo rifà anche se c'è già
      python app_agente.py trello --tool         tutti i tool del server; con * quelli che riceve il modello
      python app_agente.py trello "Metti in Trello le note fuori massimale di luglio 2026"
"""
import asyncio
import csv
import sys

import rimborsi
from assistente import stampa_traccia                    # assistente.py carica .env prima di importare agents
from assistente import agente as assistente_base        # l'assistente di assistente.py, così com'è
from login_mcp import autenticazione, fai_login

from agents import MaxTurnsExceeded, Runner, function_tool
from agents.mcp import MCPServerStreamableHttp, create_static_tool_filter

MAX_TURNI = 15

# Le istruzioni dell'assistente dicono che lavora sulla cartella e che rifiuta il resto: senza
# questa riga, alle domande sull'app risponde «non riguarda Valtesa», anche se il tool ce l'ha.
ISTRUZIONI_APP = """L'ufficio usa anche {app}: con i suoi tool leggi quello che c'è e crei quello che ti chiedono, senza modificare né cancellare niente che esiste già.
I conti delle note spese li fa il tool note_fuori_massimale: non rifarli leggendo i CSV."""

APP = {
    "trello": {
        "url": "https://mcp.trello.com/v1",
        "tool": ["trelloReadWorkspace", "trelloReadBoard", "trelloWriteBoard",
                 "trelloReadList", "trelloWriteList", "trelloWriteCard"],
        "strutturato": False,
    },
    "notion": {
        "url": "https://mcp.notion.com/mcp",
        "tool": ["notion-search", "notion-fetch", "notion-create-pages", "notion-create-database"],
        "strutturato": False,
    },
    "airtable": {
        "url": "https://mcp.airtable.com/mcp",
        "tool": ["list_workspaces", "list_bases", "create_base", "list_tables_for_base",
                 "list_records_for_table", "create_records_for_table"],
        "strutturato": True,                            # risponde solo con dati strutturati, senza testo
    },
}


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


def server_app(nome, filtro=True):
    app = APP[nome]
    return MCPServerStreamableHttp(
        name=nome,
        params={"url": app["url"], "auth": autenticazione(nome, app["url"]), "timeout": 60},
        tool_filter=create_static_tool_filter(allowed_tool_names=app["tool"]) if filtro else None,
        cache_tools_list=True,                          # tools/list una volta sola
        use_structured_content=app["strutturato"],
        client_session_timeout_seconds=120,
    )


async def main():
    if len(sys.argv) < 2 or sys.argv[1] not in APP:
        sys.exit(f"Uso: python app_agente.py {'|'.join(APP)} [--login | --tool | domanda]")
    nome, resto = sys.argv[1], sys.argv[2:]
    await fai_login(nome, APP[nome]["url"], di_nuovo=(resto == ["--login"]))
    if resto == ["--login"]:
        print(f"Login a {nome} fatto: il token è in .mcp-token/{nome}.json")
        return
    if resto == ["--tool"]:                             # tutti i tool del server, senza filtro
        server = server_app(nome, filtro=False)
        async with server:
            for tool in await server.list_tools():
                tenuto = "*" if tool.name in APP[nome]["tool"] else " "
                print(f"{tenuto} {tool.name}: {(tool.description or '-').splitlines()[0][:110]}")
        return
    server = server_app(nome)
    agente = assistente_base.clone(instructions=assistente_base.instructions + "\n" + ISTRUZIONI_APP.format(app=nome.capitalize()),
                                   tools=assistente_base.tools + [note_fuori_massimale], mcp_servers=[server])
    domanda = " ".join(resto) or input("Tu> ")
    async with server:                                  # si collega al server dell'app; alla fine chiude
        try:
            result = await Runner.run(agente, domanda, max_turns=MAX_TURNI)
        except MaxTurnsExceeded:
            sys.exit(f"Il giro si è fermato dopo {MAX_TURNI} chiamate al modello. Guardate nell'app cosa ha già "
                     "creato, e chiedete di finire in quello spazio, senza crearne un altro.")
    stampa_traccia(result)
    print(f"→ {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
