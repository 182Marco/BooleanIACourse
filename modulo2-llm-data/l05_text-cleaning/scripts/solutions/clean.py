"""clean.py — ripulire il testo estratto, uno step alla volta. (VERSIONE COMPLETA)

Riferimento del docente: è UNA soluzione possibile, non l'unica. Gli studenti
possono arrivarci con codice diverso e va benissimo.

Ogni step è una funzione normale: prende una stringa, restituisce una stringa.
Le ricette in fondo le mettono in fila. Niente registry, niente funzioni che
restituiscono funzioni: si legge dall'alto in basso.
"""
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from aikit import load                                            # noqa: E402
from ask import mostra_confronto, rispondi                        # noqa: E402

DOCUMENTO = SCRIPTS / "dataset" / "manuale-lumadesk.pdf"
DOMANDA = "Qual è la portata del piano?"


# ------------------------------------------------------- 🎤 col docente
def normalize_whitespace(text):
    """Spazi multipli, tabulazioni e righe vuote di troppo → uno spazio, una riga.

    Prima però `unicodedata.normalize("NFKC", ...)`: l'estrazione da PDF porta
    dentro apostrofi curvi, spazi non-divisibili e legature (ﬁ, ﬂ) che sembrano
    normali ma sono caratteri diversi. NFKC li riporta alla forma semplice.
    """
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    righe = [r.strip() for r in text.split("\n")]
    return "\n".join(righe).strip()


def dehyphenate(text):
    """Riunisce le parole spezzate a fine riga: 'lit-\\nerature' → 'literature'."""
    return re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)


def reflow_paragraphs(text):
    """Ricuce le righe spezzate dall'impaginazione.

    Una riga che non finisce con un segno di punteggiatura forte — punto,
    esclamativo, interrogativo, due punti, punto e virgola — non è finita:
    continua nella riga dopo. Le uniamo con uno spazio.
    """
    righe = text.split("\n")
    fuori = []
    for riga in righe:
        riga = riga.strip()
        if fuori and riga and not fuori[-1].endswith((".", "!", "?", ":", ";")):
            fuori[-1] = fuori[-1] + " " + riga
        else:
            fuori.append(riga)
    return "\n".join(fuori)


# ------------------------------------------------------- ⌨️ tocca a voi
def remove_repeated_lines(text):
    """Toglie le righe corte che si ripetono: intestazioni e piedi di pagina.

    Sono impaginazione, non contenuto — e possono contenere fatti su ALTRE cose.
    """
    conteggio = Counter()
    for riga in text.split("\n"):
        riga = riga.strip()
        if riga:
            conteggio[riga] += 1

    da_togliere = set()
    for riga, quante in conteggio.items():
        if quante >= 3 and len(riga) <= 80:
            da_togliere.add(riga)

    tenute = []
    for riga in text.split("\n"):
        if riga.strip() not in da_togliere:
            tenute.append(riga)
    return "\n".join(tenute)


def remove_page_numbers(text):
    """Toglie le righe che sono solo un numero di pagina ('7', 'pagina 2 di 4')."""
    tenute = []
    for riga in text.split("\n"):
        if re.fullmatch(r"\s*(pagina\s+)?\d+(\s+di\s+\d+)?\s*", riga, re.I):
            continue
        tenute.append(riga)
    return "\n".join(tenute)


# ------------------------------------------------------- le ricette
def pulisci_pdf(text):
    """Un PDF impaginato: mobilia di pagina, righe spezzate, sillabazione."""
    text = remove_repeated_lines(text)
    text = remove_page_numbers(text)
    text = dehyphenate(text)
    text = normalize_whitespace(text)
    text = reflow_paragraphs(text)
    return text


def pulisci_txt(text):
    """Un libro in testo semplice: righe a lunghezza fissa, spaziatura irregolare."""
    text = normalize_whitespace(text)
    text = reflow_paragraphs(text)
    return text


def pulisci(path, text):
    """La ricetta giusta per il formato. Un if, non un registry."""
    if str(path).endswith(".pdf"):
        return pulisci_pdf(text)
    elif str(path).endswith(".txt"):
        return pulisci_txt(text)
    else:
        return normalize_whitespace(text)


if __name__ == "__main__":
    sporco = "\n".join(d.text for d in load(str(DOCUMENTO)))
    pulito = pulisci(DOCUMENTO, sporco)

    print("### Il documento, prima e dopo")
    mostra_confronto(sporco, pulito, spia="80 kg")

    print("\n### La stessa domanda, sui due testi")
    print(f"  domanda: {DOMANDA}")
    print(f"  sul testo SPORCO : {rispondi(sporco, DOMANDA)}")
    print(f"  sul testo PULITO : {rispondi(pulito, DOMANDA)}")
