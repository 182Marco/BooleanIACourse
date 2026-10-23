"""I test del test: il controllo delle risposte, e le risposte giuste di domande.json
verificate sui dati della cartella. Senza modello."""
import csv
import json

import pytest

from valuta import DOMANDE, giusta

DATI = DOMANDE.parent / "ufficio-completo"
DOMANDE_JSON = (json.loads(DOMANDE.read_text(encoding="utf-8"))
                + json.loads((DOMANDE.parent / "domande-extra.json").read_text(encoding="utf-8")))


@pytest.mark.parametrize("d", DOMANDE_JSON, ids=lambda d: str(d["id"]))
def test_la_risposta_giusta_passa_il_suo_controllo(d):
    assert giusta(d["risposta"], d["controllo"])


@pytest.mark.parametrize("d", DOMANDE_JSON, ids=lambda d: str(d["id"]))
def test_non_trovata_non_passa(d):
    assert not giusta("Non ho trovato la risposta nei file della cartella.", d["controllo"])


def leggi(nome):
    with open(DATI / nome, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_i_numeri_delle_domande_sui_csv():
    note = leggi("note_spese.csv")
    sede = {d["id"]: d["sede"] for d in leggi("dipendenti.csv")}
    in_attesa = [n for n in note if n["stato"] == "in attesa"]
    assert len(in_attesa) == 115                                          # domanda 5
    padova = [n for n in note if n["stato"] == "approvata" and sede[n["dipendente_id"]] == "Padova"]
    assert (len(padova), round(sum(float(n["importo"]) for n in padova), 2)) == (502, 29940.27)   # domanda 6
    per_sede = [sede[n["dipendente_id"]] for n in in_attesa]
    assert (per_sede.count("Brescia"), per_sede.count("Padova")) == (78, 37)                     # domanda 8


@pytest.mark.parametrize("file,frammenti", [
    ("procedura-ingresso-dotazioni.pdf", ["IBAN", "TFR", "Patente"]),                     # domanda 1
    ("regolamento-ferie-permessi.pdf", ["2 giorni lavorativi", "72 ore annue", "19,5 giorni"]),   # domande 2, 7, 14
    ("policy-trasferte-note-spese.docx", ["anticipo fino a 300,00 €"]),                    # domanda 3
    ("regolamento-welfare-buoni-pasto.docx", ["8,00 €"]),                                  # domanda 4
])
def test_le_risposte_sono_nei_documenti(file, frammenti):
    from aikit.loaders import load
    testo = " ".join(doc.text for doc in load(str(DATI / file)))
    for frammento in frammenti:
        assert frammento in testo, frammento

