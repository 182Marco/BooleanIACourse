"""I test dei tool di cartella: senza modello, chiamandoli come fa l'SDK."""
import os

import pytest

import strumenti_cartella
from strumenti_cartella import RADICE, cerca, elenca_file, leggi_file
from tests.test_assistente import chiama


def test_elenca_file_vede_documenti_ed_export():
    righe = chiama(elenca_file).splitlines()
    assert "policy-trasferte-note-spese.docx" in righe
    assert "note_spese.csv" in righe


def test_leggi_file_legge_un_documento():
    assert chiama(leggi_file, percorso="faq-portale-dipendenti.md").startswith("# FAQ")


def test_leggi_file_si_ferma_a_max_caratteri():
    assert len(chiama(leggi_file, percorso="note_spese.csv")) == strumenti_cartella.MAX_CARATTERI


def test_cerca_rimanda_file_e_riga():
    prima = chiama(cerca, testo="buoni pasto").splitlines()[0]
    file, riga, testo = prima.split(":", 2)
    assert (RADICE / file).exists() and riga.isdigit() and "buoni pasto" in testo.lower()


def test_cerca_dice_quando_non_trova():
    assert chiama(cerca, testo="parola che non c'è da nessuna parte").startswith("Nessuna riga")


@pytest.mark.parametrize("percorso", ["../.env", "../assistente.py", "/etc/hostname"])
def test_leggi_file_non_esce_dalla_cartella(percorso):
    assert "fuori dalla cartella" in chiama(leggi_file, percorso=percorso)


def test_un_link_che_porta_fuori_non_si_legge(tmp_path, monkeypatch):
    segreto = tmp_path / "segreto.txt"
    segreto.write_text("password", encoding="utf-8")
    cartella = tmp_path / "ufficio"
    cartella.mkdir()
    try:
        os.symlink(segreto, cartella / "link.txt")
    except OSError:
        pytest.skip("i link simbolici qui non si possono creare (Windows senza permessi)")
    monkeypatch.setattr(strumenti_cartella, "RADICE", cartella.resolve())
    assert "link.txt" not in chiama(elenca_file)
    assert "fuori dalla cartella" in chiama(leggi_file, percorso="link.txt")
    assert chiama(cerca, testo="password").startswith("Nessuna riga")
