"""I test del report mensile: note costruite qui, i numeri di luglio del ticket 214 e il confronto con
giugno del ticket 215. Non scrivono in dati/."""
import csv
import subprocess
import sys
from pathlib import Path

from report import mese_prima, pagina, riepilogo

CARTELLA = Path(__file__).parent.parent
SEDI = {"23": "Brescia", "79": "Padova"}


def nota(id, voce, citta, giorno, importo, dipendente_id, notti=""):
    return {"id": id, "dipendente": "X", "voce": voce, "citta": citta, "giorno": giorno,
            "importo": importo, "stato": "approvata", "dipendente_id": dipendente_id, "notti": notti}


def test_totali_per_sede_e_per_voce():
    note = [nota("1", "taxi", "Roma", "2026-07-02", "30.00", "23"),
            nota("2", "hotel", "Roma", "2026-07-11", "390.00", "79", "3"),
            nota("3", "pranzo", "Torino", "2026-07-03", "20.00", "79")]
    r = riepilogo(note, SEDI)
    assert r["note"] == 3 and round(r["totale"], 2) == 440.00
    assert r["per_sede"] == {"Brescia": 30.00, "Padova": 410.00}
    assert r["per_voce"]["hotel"] == 390.00


def test_fuori_massimale_con_le_notti():
    note = [nota("1", "hotel", "Roma", "2026-07-11", "390.00", "79", "3"),     # 130 € a notte: ok
            nota("2", "hotel", "Roma", "2026-07-11", "450.00", "79", "3"),     # 150 € a notte: fuori
            nota("3", "taxi", "Roma", "2026-05-02", "52.00", "23")]
    fuori = riepilogo(note, SEDI)["fuori"]
    assert [n["id"] for n in fuori] == ["2", "3"]
    assert (fuori[0]["limite"], fuori[0]["eccedenza"]) == (420.00, 30.00)
    assert (fuori[1]["limite"], fuori[1]["eccedenza"]) == (40.00, 12.00)


def test_la_pagina_si_apre_senza_connessione():
    r = riepilogo([nota("1", "taxi", "Roma", "2026-07-02", "30.00", "23")], SEDI)
    # pagina() ora vuole anche il mese prima (ticket 215): cambia la chiamata, non cosa controlla il test
    testo = pagina("2026-07", r, "2026-06", riepilogo([], SEDI))
    assert "http://" not in testo and "https://" not in testo
    assert "<svg" in testo


def test_i_numeri_di_luglio(tmp_path):
    # i numeri del ticket, sul vero export (in sola lettura)
    esito = subprocess.run([sys.executable, str(CARTELLA / "report.py"), "2026-07"],
                           capture_output=True, text=True, encoding="utf-8", cwd=tmp_path)
    assert esito.returncode == 0, esito.stderr
    testo = (CARTELLA / "output" / "report-2026-07.html").read_text(encoding="utf-8")
    assert "164 note spese, per un totale di 8.963,53 €. 20 fuori massimale." in testo
    assert "5.141,74 €" in testo and "3.821,79 €" in testo


def test_il_mese_prima():
    assert mese_prima("2026-07") == "2026-06"
    assert mese_prima("2026-01") == "2025-12"


def test_il_confronto_con_giugno(tmp_path):
    # i numeri del ticket 215, sul vero export (in sola lettura)
    esito = subprocess.run([sys.executable, str(CARTELLA / "report.py"), "2026-07"],
                           capture_output=True, text=True, encoding="utf-8", cwd=tmp_path)
    assert esito.returncode == 0, esito.stderr
    testo = (CARTELLA / "output" / "report-2026-07.html").read_text(encoding="utf-8")
    assert "<td>Note</td><td>164</td><td>193</td><td>−29</td>" in testo
    assert "<td>8.963,53 €</td><td>10.836,01 €</td><td>−1.872,48 €</td>" in testo
    assert "6.395,67 €" in testo and "4.440,34 €" in testo
    assert "<td>Fuori massimale</td><td>20</td><td>42</td><td>−22</td>" in testo


def test_gennaio_con_il_mese_prima_vuoto(tmp_path):
    esito = subprocess.run([sys.executable, str(CARTELLA / "report.py"), "2026-01"],
                           capture_output=True, text=True, encoding="utf-8", cwd=tmp_path)
    assert esito.returncode == 0, esito.stderr
    testo = (CARTELLA / "output" / "report-2026-01.html").read_text(encoding="utf-8")
    assert "<th>2025-12</th>" in testo
