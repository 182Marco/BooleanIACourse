"""I test del ciclo di approvazione, senza API: il modello è modello_finto() e le risposte
dell'utente le dà un input() finto. Sessione e file di stato stanno in una cartella temporanea."""
import asyncio
import builtins

import pytest
from agents import Agent, SQLiteSession
from agents.testing import ScriptedModel, assistant_message

import esecuzione
from esecuzione import esegui_con_approvazione, esegui_python, file_stato, riprendi_in_sospeso
from tests.test_esecuzione import modello_finto

CODICE = "print(6 * 7)"


@pytest.fixture
def sessione(tmp_path, monkeypatch):
    monkeypatch.setattr(esecuzione, "CARTELLA", tmp_path)          # il file di stato va in tmp_path
    return SQLiteSession("prova", tmp_path / "sessioni.db")


def risposte(monkeypatch, *testi):
    """Sostituisce input() con uno che dà queste risposte, in ordine."""
    coda = list(testi)
    monkeypatch.setattr(builtins, "input", lambda prompt="": coda.pop(0))


def agente_con(modello):
    return Agent(name="Prova", instructions="", tools=[esegui_python], model=modello)


def output_del_tool(modello):
    """Il testo che il modello ha ricevuto come output di esegui_python, all'ultima chiamata."""
    for item in modello.last_call.input:
        if isinstance(item, dict) and item.get("type") == "function_call_output":
            return item["output"]


def test_il_si_esegue_il_codice(monkeypatch, sessione):
    risposte(monkeypatch, "s")
    modello = modello_finto(CODICE, "Fa 42.")
    result = asyncio.run(esegui_con_approvazione(agente_con(modello), "domanda", sessione, 5))
    assert result.final_output == "Fa 42."
    assert output_del_tool(modello) == "codice di uscita 0\n42\n"


def test_il_no_senza_motivo_manda_il_testo_dell_sdk(monkeypatch, sessione):
    risposte(monkeypatch, "n", "")
    modello = modello_finto(CODICE)
    asyncio.run(esegui_con_approvazione(agente_con(modello), "domanda", sessione, 5))
    assert output_del_tool(modello) == "Tool execution was not approved."


def test_il_no_con_motivo_manda_il_motivo(monkeypatch, sessione):
    risposte(monkeypatch, "n", "I file dell'ufficio non si modificano.")
    modello = modello_finto(CODICE)
    asyncio.run(esegui_con_approvazione(agente_con(modello), "domanda", sessione, 5))
    assert output_del_tool(modello) == "I file dell'ufficio non si modificano."


def test_una_risposta_che_non_e_si_vale_come_no(monkeypatch, sessione):
    risposte(monkeypatch, "forse", "")
    modello = modello_finto(CODICE)
    asyncio.run(esegui_con_approvazione(agente_con(modello), "domanda", sessione, 5))
    assert output_del_tool(modello) == "Tool execution was not approved."


def test_uscire_salva_lo_stato_e_il_lancio_dopo_riprende(monkeypatch, sessione):
    risposte(monkeypatch, "e")
    primo = modello_finto(CODICE)
    assert asyncio.run(esegui_con_approvazione(agente_con(primo), "domanda", sessione, 5)) is None
    assert file_stato(sessione).exists() and len(primo.calls) == 1

    # il lancio dopo: un agente nuovo, con un modello che sa solo rispondere
    risposte(monkeypatch, "s")
    secondo = ScriptedModel([[assistant_message("Fa 42.")]])
    result = asyncio.run(riprendi_in_sospeso(agente_con(secondo), sessione, 5))
    assert result.final_output == "Fa 42."
    assert output_del_tool(secondo) == "codice di uscita 0\n42\n"
    assert not file_stato(sessione).exists()


def test_se_la_ripresa_si_rompe_lo_stato_resta(monkeypatch, sessione):
    risposte(monkeypatch, "e")
    asyncio.run(esegui_con_approvazione(agente_con(modello_finto(CODICE)), "domanda", sessione, 5))

    # il lancio dopo: il modello non risponde (un errore di rete, per esempio)
    risposte(monkeypatch, "s")
    rotto = ScriptedModel([RuntimeError("rete giù")])
    with pytest.raises(RuntimeError):
        asyncio.run(riprendi_in_sospeso(agente_con(rotto), sessione, 5))
    assert file_stato(sessione).exists()                           # al lancio dopo si riprova
