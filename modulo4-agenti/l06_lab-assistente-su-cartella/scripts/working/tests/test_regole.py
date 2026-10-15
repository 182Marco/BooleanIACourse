"""Le regole del lab, controllate: i rimedi cambiano cosa sa il modello, non quanto riceve.
Senza modello: i tool si chiamano con chiama(), il giro con un modello finto."""
import asyncio

import pytest
from agents import Agent, SQLiteSession, Usage, set_tracing_disabled
from agents.exceptions import AgentsException
from agents.testing import ScriptedModel, assistant_message, function_call

import assistente
import strumenti_cartella
from strumenti_cartella import RADICE, cerca, elenca_file, leggi_file
from tests.test_assistente import chiama

set_tracing_disabled(True)
NOTA = 300                                          # i caratteri in più per una nota al modello


def test_i_limiti_restano_quelli_del_lab():
    assert (strumenti_cartella.MAX_CARATTERI, strumenti_cartella.MAX_RISULTATI) == (20_000, 30)
    assert (assistente.MAX_TURNI, assistente.MODELLO) == (10, "gpt-6-luna")
    assert assistente.agente.model == "gpt-6-luna"


def test_i_tool_restano_tre_e_generici():
    nomi = [t.name for t in assistente.agente.tools if t.name not in ("esegui_python", "registra_richiesta")]
    assert nomi == ["elenca_file", "cerca", "leggi_file"]
    assert set(cerca.params_json_schema["properties"]) == {"testo"}
    assert set(leggi_file.params_json_schema["properties"]) <= {"percorso", "da_riga"}


@pytest.mark.parametrize("file", sorted(f.name for f in RADICE.iterdir()))
def test_leggi_file_non_rimanda_piu_di_max_caratteri(file):
    assert len(chiama(leggi_file, percorso=file)) <= strumenti_cartella.MAX_CARATTERI + NOTA
    if "da_riga" in leggi_file.params_json_schema["properties"]:   # anche le pagine dopo la prima
        assert len(chiama(leggi_file, percorso=file, da_riga=2)) <= strumenti_cartella.MAX_CARATTERI + NOTA


@pytest.mark.parametrize("testo", ["in attesa", "Milano", "a"])
def test_cerca_non_rimanda_piu_di_max_risultati(testo):
    risultato = chiama(cerca, testo=testo)
    assert len(risultato.splitlines()) <= strumenti_cartella.MAX_RISULTATI + 1   # più una nota
    assert len(risultato) <= strumenti_cartella.MAX_CARATTERI + NOTA


def test_rispondi_non_supera_i_turni(monkeypatch):
    """Un modello che chiede sempre un tool: al massimo MAX_TURNI chiamate con i tool, più una
    senza tool per la risposta finale."""
    modello = ScriptedModel([[function_call("elenca_file", {}, call_id=f"c{i}")] for i in range(3 * assistente.MAX_TURNI)])
    monkeypatch.setattr(assistente, "agente", Agent(name="Prova", instructions="", tools=[elenca_file], model=modello))
    try:
        asyncio.run(assistente.rispondi("una domanda", SQLiteSession("prova")))
    except AgentsException:
        pass                                        # al limite, o il modello finto che non sa rispondere
    assert len(modello.calls) <= assistente.MAX_TURNI + 1


def test_rispondi_conta_tutte_le_chiamate(monkeypatch):
    """Le chiamate e i token che valuta.py legge dal result sono quelli di tutto il giro, anche
    con una risposta finale dopo il limite: il punteggio in token non si abbassa togliendone."""
    passi = [[function_call("elenca_file", {}, call_id=f"c{i}")] for i in range(assistente.MAX_TURNI)]
    modello = ScriptedModel(passi + [[assistant_message("Con quello che ho trovato: …")]],
                            default_usage=Usage(requests=1, input_tokens=1000, output_tokens=10))
    monkeypatch.setattr(assistente, "agente", Agent(name="Prova", instructions="", tools=[elenca_file], model=modello))
    try:
        result = asyncio.run(assistente.rispondi("una domanda", SQLiteSession("prova")))
    except AgentsException:
        return                                      # nessuna risposta: valuta.py legge l'errore
    if result is not None:
        usage = result.context_wrapper.usage
        chiamate = len(modello.calls)
        assert (usage.requests, usage.input_tokens, usage.output_tokens) == (chiamate, 1000 * chiamate, 10 * chiamate)
