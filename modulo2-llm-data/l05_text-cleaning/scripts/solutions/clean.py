"""clean.py — punto di partenza DOPO il live coding: TODO 1-3 già scritti (🎤), TODO 4-6 da fare (⌨️).

Copia di working/clean.py con la parte del docente completata: se siete rimasti
indietro col live coding, partite da qui per l'esercizio.

Il file della serata: si lavora qui, dall'alto in basso.

Ogni step è una funzione normale: prende una stringa, restituisce una stringa.
Le ricette in fondo le mettono in fila.

    python working/clean.py     ← lancialo dopo OGNI todo: stampa quello che c'è

TODO 1-3  🎤  col docente
TODO 4-5  ⌨️  da soli — il 4 è quello che cambia la risposta
TODO 6    ⌨️  metteteli nella ricetta del PDF
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

# Il documento della serata. Se lo cambiate per provare gli altri due del
# dataset/, RIMETTETELO su manuale-lumadesk.pdf prima dei TODO 4-6: il
# "fatto quando" della serata (120 kg) vale solo su questo documento.
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
    raise NotImplementedError("TODO 4: remove_repeated_lines")


def remove_page_numbers(text):
    """Toglie le righe che sono solo un numero di pagina ('7', 'pagina 2 di 4')."""
    raise NotImplementedError("TODO 5: remove_page_numbers")


# ------------------------------------------------------- le ricette
def pulisci_pdf(text):
    """Un PDF impaginato: mobilia di pagina, righe spezzate, sillabazione."""
    raise NotImplementedError("TODO 6: pulisci_pdf")


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
    print(f"documento: {DOCUMENTO.name} — {len(sporco)} caratteri estratti\n")

    # Ogni step si prova DA SOLO, appena scritto, sul testo grezzo: qui non
    # stiamo costruendo la pipeline, stiamo guardando un pezzo alla volta.
    # Nella ricetta (TODO 6) l'ordine sarà un altro, e conta.
    # Gli step non ancora fatti lo dicono e si va avanti: non serve finire
    # tutto per vedere qualcosa.
    for numero, step in enumerate(
        [normalize_whitespace, dehyphenate, reflow_paragraphs,
         remove_repeated_lines, remove_page_numbers], start=1
    ):
        try:
            dopo = step(sporco)          # sempre dal testo GREZZO, non in cascata
            print(f"TODO {numero} · {step.__name__:22s} "
                  f"{len(sporco):6d} → {len(dopo):6d} caratteri · "
                  f"{len(sporco.splitlines()):4d} → {len(dopo.splitlines()):4d} righe")
            print(f"           «LumaDesk Mini» nel testo: {dopo.count('LumaDesk Mini')}x"
                  f" · «120 kg»: {dopo.count('120 kg')}x")
            print(f"           {dopo.strip()[:88]!r}…")
        except NotImplementedError:
            print(f"TODO {numero} · {step.__name__:22s} ancora da fare")

    print()
    try:
        pulito = pulisci(DOCUMENTO, sporco)
    except NotImplementedError:
        print("TODO 6 · la ricetta del PDF è ancora da scrivere")
        raise SystemExit(0)

    print("### Il documento, prima e dopo")
    mostra_confronto(sporco, pulito, spia="80 kg")

    print("\n### La stessa domanda, sui due testi")
    print(f"  domanda: {DOMANDA}")
    print(f"  sul testo SPORCO : {rispondi(sporco, DOMANDA)}")
    print(f"  sul testo PULITO : {rispondi(pulito, DOMANDA)}")
