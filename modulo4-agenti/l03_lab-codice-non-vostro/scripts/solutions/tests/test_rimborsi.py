from rimborsi import controlla


def test_pranzo_torino_nel_massimale():
    assert controlla({"voce": "pranzo", "citta": "Torino", "giorno": "2026-03-10", "importo": "18.50"})


def test_taxi_roma_fuori_massimale():
    assert not controlla({"voce": "taxi", "citta": "Roma", "giorno": "2026-05-02", "importo": "52.00"})


def test_cena_milano_prima_di_luglio():
    assert not controlla({"voce": "cena", "citta": "Milano", "giorno": "2026-06-12", "importo": "50.00"})


def test_cena_milano_dopo_luglio():
    # Nota 1043: dal 01/07/2026 il massimale cena a Milano è 55 € (circolare 7/2026)
    assert controlla({"voce": "cena", "citta": "Milano", "giorno": "2026-07-14", "importo": "52.00"})


def test_cena_milano_primo_luglio():
    assert controlla({"voce": "cena", "citta": "Milano", "giorno": "2026-07-01", "importo": "55.00"})
    assert not controlla({"voce": "cena", "citta": "Milano", "giorno": "2026-06-30", "importo": "55.00"})


def test_hotel_milano_dopo_luglio():
    assert controlla({"voce": "hotel", "citta": "Milano", "giorno": "2026-08-03", "importo": "145.00"})
    assert not controlla({"voce": "hotel", "citta": "Milano", "giorno": "2026-06-03", "importo": "145.00"})


def test_hotel_roma_tre_notti():
    # Nota 1441, la segnalazione dell'ufficio: tre notti a Roma per 390 € (130 € a notte, massimale 140 €)
    assert controlla({"voce": "hotel", "citta": "Roma", "giorno": "2026-07-11", "importo": "390.00", "notti": "3"})
    assert not controlla({"voce": "hotel", "citta": "Roma", "giorno": "2026-07-11", "importo": "450.00", "notti": "3"})


def test_notti_vuote_per_le_voci_che_non_sono_hotel():
    assert not controlla({"voce": "taxi", "citta": "Roma", "giorno": "2026-05-02", "importo": "52.00", "notti": ""})


# --- Modulo 4 · Lezione 2: il file come argomento, il riepilogo, le città senza massimale

import subprocess
import sys
from pathlib import Path

PROGRAMMA = Path(__file__).parent.parent / "rimborsi.py"
INTESTAZIONE = "id,dipendente,voce,citta,giorno,importo,stato,dipendente_id\n"


def lancia(*argomenti):
    """Lancia rimborsi.py come da terminale e restituisce l'output."""
    esito = subprocess.run([sys.executable, str(PROGRAMMA), *argomenti],
                           capture_output=True, text=True, encoding="utf-8")
    assert esito.returncode == 0, esito.stderr
    return esito.stdout


def test_citta_senza_massimale_non_ferma_il_programma(tmp_path):
    export = tmp_path / "export.csv"
    export.write_text(INTESTAZIONE
                      + "1,Luca Ferri,cena,Bologna,2026-09-10,30.00,in attesa,23\n"
                      + "2,Luca Ferri,cena,Milano,2026-09-11,60.00,in attesa,23\n", encoding="utf-8")
    output = lancia(str(export))
    assert "MASSIMALE MANCANTE" in output
    assert output.strip().splitlines()[-1] == "2 note spese, 1 fuori massimale, 1 con massimale mancante"


def test_solo_le_note_di_una_persona(tmp_path):
    export = tmp_path / "export.csv"
    export.write_text(INTESTAZIONE
                      + "1,Luca Ferri,taxi,Roma,2026-05-02,52.00,approvata,23\n"
                      + "2,Sara Conti,taxi,Roma,2026-05-02,52.00,approvata,17\n"
                      + "3,Luca Ferri,pranzo,Torino,2026-03-10,18.50,approvata,23\n", encoding="utf-8")
    output = lancia(str(export), "--dipendente", "Luca Ferri")
    assert "Sara Conti" not in output
    assert output.strip().splitlines()[-1] == "2 note spese, 1 fuori massimale"


def test_riepilogo_per_citta(tmp_path):
    export = tmp_path / "export.csv"
    export.write_text(INTESTAZIONE
                      + "1,Luca Ferri,taxi,Roma,2026-05-02,52.00,approvata,23\n"
                      + "2,Sara Conti,taxi,Roma,2026-05-02,12.00,approvata,17\n", encoding="utf-8")
    output = lancia(str(export))
    assert "  Roma         2 note,    1 fuori massimale" in output.splitlines()
