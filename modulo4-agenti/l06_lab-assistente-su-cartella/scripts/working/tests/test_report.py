"""I test del report mensile: note costruite qui, e i numeri di luglio del ticket. Non scrivono in dati/."""
import csv
import subprocess
import sys
from pathlib import Path

from report import pagina, riepilogo

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
    testo = pagina("2026-07", riepilogo([nota("1", "taxi", "Roma", "2026-07-02", "30.00", "23")], SEDI))
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
