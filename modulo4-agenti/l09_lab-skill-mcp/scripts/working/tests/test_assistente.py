"""I test dell'assistente che non chiamano il modello, e chiama(), con cui gli altri test
chiamano un tool come fa l'SDK."""
import asyncio
import csv
import json

from agents.tool_context import ToolContext

from app import server_app
from assistente import CARTELLA, ESEGUI_PYTHON, agente, crea_agente


def chiama(tool, **argomenti):
    """Chiama un function tool come fa l'SDK quando il modello lo chiede, ma senza modello."""
    testo = json.dumps(argomenti)
    ctx = ToolContext(context=None, tool_name=tool.name, tool_call_id="test", tool_arguments=testo)
    return asyncio.run(tool.on_invoke_tool(ctx, testo))


def test_l_assistente_ha_i_tool_di_cartella_le_skill_e_i_function_tool():
    attesi = ["elenca_file", "cerca", "leggi_file"] + (["esegui_python"] if ESEGUI_PYTHON else [])
    attesi += ["apri_skill", "note_fuori_massimale"]
    assert [t.name for t in agente.tools if t.name != "registra_richiesta"] == attesi   # l'estensione


def test_senza_app_niente_server_e_niente_istruzioni_dell_app():
    assert agente.mcp_servers == []
    assert "L'ufficio usa anche" not in agente.instructions
    assert "- rimborso-trasferta:" in agente.instructions                 # l'indice delle skill


def test_con_l_app_il_server_e_la_riga_delle_istruzioni():
    server = server_app("trello")                                         # non si collega: si crea soltanto
    con = crea_agente("trello", server)
    assert con.mcp_servers == [server]
    assert "L'ufficio usa anche Trello" in con.instructions


def test_gli_export_della_cartella_sono_quelli_di_dati():
    for nome in ("note_spese.csv", "massimali.csv", "dipendenti.csv", "assenze.csv", "assunzioni.csv"):
        assert (CARTELLA / "ufficio-completo" / nome).read_bytes() == (CARTELLA / "dati" / nome).read_bytes(), nome
