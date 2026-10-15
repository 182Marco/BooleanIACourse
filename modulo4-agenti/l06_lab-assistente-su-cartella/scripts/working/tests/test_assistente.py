"""I test dell'assistente che non chiamano il modello, e chiama(), con cui gli altri test
chiamano un tool come fa l'SDK."""
import asyncio
import csv
import json

from agents.tool_context import ToolContext

from assistente import CARTELLA, ESEGUI_PYTHON, agente


def chiama(tool, **argomenti):
    """Chiama un function tool come fa l'SDK quando il modello lo chiede, ma senza modello."""
    testo = json.dumps(argomenti)
    ctx = ToolContext(context=None, tool_name=tool.name, tool_call_id="test", tool_arguments=testo)
    return asyncio.run(tool.on_invoke_tool(ctx, testo))


def test_l_assistente_ha_i_tool_di_cartella():
    attesi = ["elenca_file", "cerca", "leggi_file"] + (["esegui_python"] if ESEGUI_PYTHON else [])
    assert [t.name for t in agente.tools if t.name != "registra_richiesta"] == attesi   # l'estensione


def test_gli_export_della_cartella_sono_quelli_di_dati():
    for nome in ("note_spese.csv", "massimali.csv", "dipendenti.csv", "assenze.csv"):
        assert (CARTELLA / "ufficio-completo" / nome).read_bytes() == (CARTELLA / "dati" / nome).read_bytes(), nome
