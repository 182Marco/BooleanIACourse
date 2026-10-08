"""I test dell'assistente che non chiamano il modello né le API degli embedding."""
import asyncio
import csv
import json
import sqlite3

from agents.tool_context import ToolContext

from aikit import vectorstore
from assistente import CARTELLA, COLLECTION, DB, query_db


def chiama(tool, **argomenti):
    """Chiama un function tool come fa l'SDK quando il modello lo chiede, ma senza modello."""
    testo = json.dumps(argomenti)
    ctx = ToolContext(context=None, tool_name=tool.name, tool_call_id="test", tool_arguments=testo)
    return asyncio.run(tool.on_invoke_tool(ctx, testo))


def test_database_uguale_ai_csv():
    con = sqlite3.connect(DB)
    for tabella in ("note_spese", "massimali", "dipendenti", "assenze"):
        with open(CARTELLA / "dati" / f"{tabella}.csv", newline="", encoding="utf-8") as f:
            righe_csv = len(list(csv.DictReader(f)))
        (righe_db,) = con.execute(f"SELECT COUNT(*) FROM {tabella}").fetchone()
        assert righe_db == righe_csv, tabella
    con.close()


def test_query_db_trova_la_nota_1043():
    risposta = chiama(query_db, sql="SELECT dipendente, voce, citta, importo FROM note_spese WHERE id = 1043")
    assert risposta.splitlines() == ["dipendente | voce | citta | importo", "Luca Ferri | cena | Milano | 52.0"]


def test_query_db_rifiuta_chi_non_e_select():
    assert chiama(query_db, sql="DELETE FROM note_spese") == "Errore: sono ammesse solo query SELECT."


def test_query_db_rimanda_gli_errori_al_modello():
    assert chiama(query_db, sql="SELECT data FROM note_spese").startswith("Errore: no such column")


def test_indice_dei_documenti_costruito():
    assert vectorstore.apri_collection(COLLECTION).count() > 0
