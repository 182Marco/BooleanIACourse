"""Test di scadenze.py: giorni lavorativi, festività, indirizzi con gli omonimi."""
from datetime import date

from scadenze import carica, indirizzo, lavorativi_dopo, lavorativi_prima, scadenze, testo


def test_dieci_giorni_lavorativi_prima_senza_festivita():
    assert lavorativi_prima(date(2026, 11, 16), 10) == date(2026, 11, 2)


def test_l_8_dicembre_non_e_lavorativo():
    # Sara Conti entra il 14/12/2026: contando l'8 dicembre la lettera sarebbe il 30/11
    assert lavorativi_prima(date(2026, 12, 14), 10) == date(2026, 11, 27)


def test_cinque_giorni_lavorativi_dopo():
    assert lavorativi_dopo(date(2026, 11, 9), 5) == date(2026, 11, 16)
    assert lavorativi_dopo(date(2026, 12, 4), 5) == date(2026, 12, 14)     # salta sabato, domenica e l'8


def test_l_indirizzo_di_chi_non_ha_omonimi():
    assert indirizzo("Elena", "Fabbri") == "elena.fabbri@valtesa.it"


def test_due_omonimi_danno_il_numero_3():
    # in dati/dipendenti.csv ci sono già due Sara Conti
    assert indirizzo("Sara", "Conti") == "sara.conti3@valtesa.it"


def test_accenti_e_apostrofi():
    assert indirizzo("Niccolò", "D'Angelo") == "niccolo.dangelo@valtesa.it"


def test_le_date_di_un_ingresso():
    date_ = scadenze(date(2026, 11, 16))
    assert date_["ultimo giorno lavorativo prima (visita medica, per Produzione e Logistica)"] == date(2026, 11, 13)
    assert date_["fine della quarta settimana (colloquio di verifica)"] == date(2026, 12, 11)
    assert date_["30 giorni dall'ingresso"] == date(2026, 12, 16)


def test_la_scheda_di_un_ingresso():
    sara = next(a for a in carica() if a["id"] == "205")
    scheda = testo(sara)
    assert "sara.conti3@valtesa.it" in scheda
    assert "venerdì 27/11/2026" in scheda


def test_ci_sono_sei_ingressi():
    assert [a["id"] for a in carica()] == ["201", "202", "203", "204", "205", "206"]


def test_le_feste_di_fine_anno():
    # Davide Russo entra l'11/01/2027: in mezzo Epifania, Capodanno e Natale
    assert lavorativi_prima(date(2027, 1, 11), 10) == date(2026, 12, 23)
