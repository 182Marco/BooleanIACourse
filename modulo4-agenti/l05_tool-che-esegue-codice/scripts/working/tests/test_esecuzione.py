"""I test di esegui_python, senza modello: il tool si chiama come fa l'SDK, con chiama(), e il
programma gira davvero, nella cartella dell'ufficio. In fondo modello_finto(), per provare il
ciclo di approvazione senza API."""
import asyncio

from agents import Agent, Runner, set_tracing_disabled
from agents.testing import ScriptedModel, assistant_message, function_call

import esecuzione
from esecuzione import esegui_python
from tests.test_assistente import chiama

set_tracing_disabled(True)                          # i run con il modello finto non mandano la traccia


def test_esegui_python_chiede_sempre_l_approvazione():
    assert esegui_python.needs_approval is True


def test_esegui_python_lavora_nella_cartella_dell_ufficio():
    codice = "import csv\nprint(len(list(csv.DictReader(open('note_spese.csv')))))"
    assert chiama(esegui_python, codice=codice) == "codice di uscita 0\n1500\n"


def test_esegui_python_rimanda_gli_errori_al_modello():
    risposta = chiama(esegui_python, codice="print(1 / 0)")
    assert risposta.startswith("codice di uscita 1") and "ZeroDivisionError" in risposta


def test_esegui_python_si_ferma_al_timeout(monkeypatch):
    monkeypatch.setattr(esecuzione, "TIMEOUT", 1)
    assert chiama(esegui_python, codice="while True:\n    pass").startswith("Il programma è stato fermato dopo 1 s")


def test_esegui_python_non_vede_la_chiave(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-prova")
    codice = "import os\nprint(os.environ.get('OPENAI_API_KEY'))"
    assert chiama(esegui_python, codice=codice) == "codice di uscita 0\nNone\n"


def test_esegui_python_stampa_in_utf8():
    assert "€ è" in chiama(esegui_python, codice="print('€ è')")


def test_testa_e_coda_taglia_in_mezzo():
    tagliato = esecuzione.testa_e_coda("a" * 6_000 + "b" * 6_000)
    assert tagliato.startswith("Output troppo lungo: 2000 caratteri tolti")
    assert "a" * 5_000 in tagliato and tagliato.endswith("b" * 5_000)


def modello_finto(codice, risposta="Fatto."):
    """Un modello finto (ScriptedModel di agents.testing), per provare l'approvazione senza API:
    alla prima chiamata chiede esegui_python con questo codice, alla seconda risponde con questo
    testo. Si passa ad Agent(model=...) al posto del nome del modello. Dopo il run,
    modello.last_call.input è quello che il modello ha ricevuto all'ultima chiamata."""
    return ScriptedModel([
        [function_call("esegui_python", {"codice": codice}, call_id="chiamata-1")],
        [assistant_message(risposta)],
    ])


def test_il_run_si_ferma_prima_di_esegui_python():
    agente = Agent(name="Prova", instructions="", tools=[esegui_python], model=modello_finto("print(42)"))
    result = asyncio.run(Runner.run(agente, "una domanda"))
    assert result.final_output is None
    assert [i.name for i in result.interruptions] == ["esegui_python"]
