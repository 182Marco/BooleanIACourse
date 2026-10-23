"""app.py — il server MCP di un'app dell'ufficio: Trello, Notion o Airtable.

I tool dell'app sono di un altro: il loro server MCP sta in cloud, dal fornitore, e l'assistente
gli inoltra le chiamate del modello. Il login lo fa login_mcp.py. Di ogni app si tengono solo i
tool che servono (tool_filter): un server ne ha decine, e l'SDK manda le loro definizioni al
modello a ogni chiamata.

Era app_agente.py (Modulo 4 · Lezione 8), senza l'agente, il main e note_fuori_massimale, che
è codice nostro e sta con gli altri function tool in assistente.py. Dalla versione 0.9 l'app si
sceglie al lancio di assistente.py, con --app.
"""
from agents.mcp import MCPServerStreamableHttp, create_static_tool_filter

from login_mcp import autenticazione

# Le istruzioni dell'assistente dicono che lavora sulla cartella e che rifiuta il resto: senza
# questa riga, alle domande sull'app risponde «non riguarda Valtesa», anche se il tool ce l'ha.
ISTRUZIONI_APP = """L'ufficio usa anche {app}: con i suoi tool leggi quello che c'è e crei quello che ti chiedono, senza modificare né cancellare niente che esiste già.
I conti e le date li fanno i tuoi function tool: non rifarli leggendo i CSV."""

APP = {
    "trello": {
        "url": "https://mcp.trello.com/v1",
        "tool": ["trelloReadWorkspace", "trelloReadBoard", "trelloWriteBoard",
                 "trelloReadList", "trelloWriteList", "trelloWriteCard",
                 "trelloReadCard", "trelloReadChecklist", "trelloWriteChecklist"],   # le checklist, dalla 0.9
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

