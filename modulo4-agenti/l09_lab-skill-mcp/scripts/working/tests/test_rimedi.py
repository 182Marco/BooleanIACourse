"""I test dei rimedi del docente: senza modello, chiamando i tool come fa l'SDK; la risposta
forzata con un modello finto."""
import asyncio

from agents import Agent, SQLiteSession, set_tracing_disabled
from agents.testing import ScriptedModel, assistant_message, function_call

import assistente
from strumenti_cartella import cerca, elenca_file, leggi_file
from tests.test_assistente import chiama

set_tracing_disabled(True)


def test_un_pdf_si_legge_come_testo():
    assert "IBAN" in chiama(leggi_file, percorso="procedura-ingresso-dotazioni.pdf")


def test_un_docx_si_legge_come_testo():
    assert "8,00 €" in chiama(leggi_file, percorso="regolamento-welfare-buoni-pasto.docx")


def test_cerca_trova_anche_nei_pdf():
    assert "regolamento-ferie-permessi.pdf:" in chiama(cerca, testo="preavviso minimo")


def test_leggi_file_dice_da_che_riga_ripartire():
    prima = chiama(leggi_file, percorso="note_spese.csv")
    assert prima.splitlines()[-1].startswith("[Righe 1-") and "da_riga=" in prima


def test_le_pagine_coprono_tutto_il_file_con_l_intestazione():
    righe, da_riga = [], 1
    while True:
        pagina = chiama(leggi_file, percorso="note_spese.csv", da_riga=da_riga).splitlines()
        if pagina[-1].startswith("[Righe"):
            nota = pagina.pop()
            da_riga = int(nota.split("da_riga=")[1].split(")")[0])
        else:
            da_riga = None
        if righe:
            assert pagina[0].startswith("id,dipendente")       # l'intestazione su ogni pagina
            pagina = pagina[1:]
        righe += pagina
        if da_riga is None:
            break
    assert len(righe) == 1501


def test_cerca_dice_che_ci_sono_altre_righe_senza_contarle():
    nota = chiama(cerca, testo="in attesa").splitlines()[-1]
    assert nota.startswith("[Mostrate le prime 30 righe: ce ne sono altre.")
    assert "117" not in nota                    # la nota dice cosa manca, non fa conti


def test_un_nome_sbagliato_torna_con_i_nomi_simili():
    assert "regolamento-ferie-permessi.pdf" in chiama(leggi_file, percorso="regolamento-ferie.md")


def test_al_limite_dei_turni_arriva_comunque_una_risposta(monkeypatch):
    passi = [[function_call("elenca_file", {}, call_id=f"c{i}")] for i in range(assistente.MAX_TURNI)]
    modello = ScriptedModel(passi + [[assistant_message("Con quello che ho trovato: …")]])
    finto = Agent(name="Prova", instructions="", tools=[elenca_file], model=modello)
    monkeypatch.setattr(assistente, "agente", finto)
    result = asyncio.run(assistente.rispondi("una domanda", SQLiteSession("prova")))
    assert result.final_output == "Con quello che ho trovato: …"
    assert len(modello.last_call.input) > 2 * assistente.MAX_TURNI   # ha ricevuto tutto quello che aveva letto
