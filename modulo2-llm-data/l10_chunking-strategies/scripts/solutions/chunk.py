"""chunk.py — spezzare i documenti lunghi, e vedere l'effetto sul retrieval.

Versione COMPLETA (riferimento docente) di working/chunk.py: stessi nomi,
stessi import. L'unico file della serata: le strategie di chunking qui
sopra, gli esperimenti nel main, la tabella da compilare in fondo.

    python solutions/chunk.py
"""
import sys

from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from aikit.embeddings import embed, cosine_similarity   # noqa: E402 — Modulo 2 · Lezione 7
from aikit import vectorstore                           # noqa: E402 — Modulo 2 · Lezione 9

DATASET = SCRIPTS / "dataset"

# Le manopole degli esperimenti: si cambia UNA manopola, si rilancia,
# si annota l'esito nella tabella in fondo al file.
STRATEGIA = "fixed"          # "fixed" | "recursive" | "semantic"
CHUNK_SIZE = 500             # caratteri (fixed e recursive), sempre positivo
OVERLAP = 0                  # caratteri ripetuti tra chunk vicini (solo fixed).
                             # Tenetelo MINORE di CHUNK_SIZE: se il taglio non
                             # avanza (overlap uguale o maggiore del size, o un
                             # size a zero) i chunk non finiscono mai e lo
                             # script si pianta lì.
SOGLIA = 0.4                 # sotto questa similarità si taglia (solo semantic)


# --------------------------------------------------- TODO 1 · col docente 🎤
def chunk_fixed(testo, size, overlap):
    """Blocchi di `size` caratteri; ogni blocco riparte `overlap` caratteri
    prima della fine del precedente. Restituisce la lista dei pezzi."""
    pezzi = []
    inizio = 0
    while inizio < len(testo):
        pezzi.append(testo[inizio:inizio + size])
        inizio = inizio + size - overlap
    return pezzi


# --------------------------------------------------- TODO 2 · col docente 🎤
def chunk_recursive(testo, size):
    """Taglia sull'ULTIMO separatore che ci sta in `size` caratteri, provando
    i separatori dal più forte al più debole (paragrafo, riga, frase); se
    nessuno ci sta, taglio secco a `size`. Poi riparte da dove ha tagliato,
    fino in fondo. Restituisce pezzi lunghi al massimo `size`."""
    pezzi = []
    inizio = 0
    while inizio < len(testo):
        resto = testo[inizio:]
        if len(resto) <= size:          # l'ultimo pezzo ci sta tutto
            pezzi.append(resto)
            break
        finestra = resto[:size]
        posizione, lunghezza = -1, 0    # il primo separatore che ci sta vince
        for separatore in ("\n\n", "\n", ". "):
            posizione = finestra.rfind(separatore)
            if posizione > 0:
                lunghezza = len(separatore)
                break
        if posizione > 0:
            pezzi.append(resto[:posizione])
            inizio = inizio + posizione + lunghezza
        else:
            pezzi.append(finestra)      # nessun separatore: taglio secco
            inizio = inizio + size
    return pezzi


# ------------------------- già scritta: la mostra il DOCENTE in demo 🎤 —
def chunk_semantic(testo, soglia):
    """Taglia dove il DISCORSO cambia: embedda le frasi una per una e chiude
    il chunk quando la similarità tra una frase e la successiva scende sotto
    `soglia` — un calo di similarità è un cambio di argomento. Stasera si
    USA (negli esperimenti), non si scrive."""
    frasi = []
    for riga in testo.split("\n"):
        for frase in riga.split(". "):
            if frase.strip():
                frasi.append(frase.strip())

    vettori = embed(frasi)          # una chiamata sola: il chunking si paga

    pezzi = []
    corrente = [frasi[0]]
    for i in range(1, len(frasi)):
        simile = cosine_similarity(vettori[i - 1], vettori[i])
        if simile < soglia:         # il discorso cambia: si chiude il chunk
            pezzi.append(" ".join(corrente))
            corrente = []
        corrente.append(frasi[i])
    pezzi.append(" ".join(corrente))
    return pezzi


# ------------------------------------------------------- già scritte: date —
def carica_documenti():
    """I 3 documenti lunghi di Lumen, da dataset/: {nome: testo}."""
    documenti = {}
    for percorso in sorted(DATASET.glob("*.txt")):
        documenti[percorso.stem] = percorso.read_text(encoding="utf-8")
    return documenti


def mostra_chunk(pezzi):
    """Com'è venuto lo spezzatino: taglia e confini di ogni chunk."""
    for numero, pezzo in enumerate(pezzi):
        pulito = " ".join(pezzo.split())
        print(f"  {numero:3d} · {len(pezzo):4d} car · "
              f"{pulito[:34]} ⟨…⟩ {pulito[-34:]}")


if __name__ == "__main__":
    # Le tre query note della serata, ognuna con la RISPOSTA che deve uscire:
    # così giudicate il primo risultato senza rileggervi i documenti interi.
    QUERY = [
        # colonna "saldi" della tabella in fondo al file
        ("Quanti giorni ho per restituire un prodotto comprato durante i saldi?",
         "14 giorni, e il rimborso è solo un buono acquisto"),
        # colonna "contributo"
        ("Quanto vale il contributo per la postazione e entro quanti giorni va presentata la richiesta?",
         "250 euro, e la richiesta va presentata entro 60 giorni dall'attivazione"),
        # colonna "E07"
        ("La centralina mostra il codice E07: cosa devo fare?",
         "staccare l'alimentazione per 30 secondi, poi ricalibrare col tasto -"),
    ]
    K = 3

    print(f"config: {STRATEGIA} · size {CHUNK_SIZE} · overlap {OVERLAP} · soglia {SOGLIA}\n")

    # 1 · si spezza: ogni documento con la strategia scelta
    documenti = carica_documenti()
    pezzi_per_doc = {}
    try:
        for nome, testo in documenti.items():
            if STRATEGIA == "fixed":
                pezzi = chunk_fixed(testo, CHUNK_SIZE, OVERLAP)
            elif STRATEGIA == "recursive":
                pezzi = chunk_recursive(testo, CHUNK_SIZE)
            elif STRATEGIA == "semantic":
                pezzi = chunk_semantic(testo, SOGLIA)
            else:
                raise ValueError(f"STRATEGIA {STRATEGIA!r} sconosciuta")
            pezzi_per_doc[nome] = pezzi
            taglie = [len(p) for p in pezzi]
            print(f"{nome}: {len(pezzi)} chunk · da {min(taglie)} a {max(taglie)} caratteri")
    except NotImplementedError as err:
        print(f"[--] ancora da scrivere — {err}")
        raise SystemExit(0)

    # I tagli da vicino sui due documenti che nascondono le risposte più
    # difficili: dove finisce un chunk e dove ricomincia il successivo. Il
    # manuale non si stampa qui — è chunkato e indicizzato come gli altri,
    # ma i suoi tagli si giudicano dal risultato della terza query.
    for nome in ("policy-resi-garanzia", "guida-smart-working"):
        print(f"\ni tagli da vicino ({nome}):")
        mostra_chunk(pezzi_per_doc[nome])

    # 2 · si indicizza: embed dei chunk + collection RICREATA da zero
    ids, testi, metadati = [], [], []
    for nome, pezzi in pezzi_per_doc.items():
        for numero, pezzo in enumerate(pezzi):
            ids.append(f"{nome}-{numero:03d}")
            testi.append(pezzo)
            metadati.append({"doc": nome})

    print(f"\nindicizzo {len(testi)} chunk (la collection si ricrea a ogni giro):")
    vettori = embed(testi)
    collection = vectorstore.crea_collection("lumen_chunks")
    vectorstore.indicizza(collection, ids, testi, vettori, metadati)

    # 3 · le query note: il primo risultato si legge PER INTERO e si confronta
    #     con la risposta attesa — c'è tutta (OK)? si interrompe a metà (META)?
    #     o il chunk parla d'altro (FUORI)?
    for query, attesa in QUERY:
        print(f"\n=== {query}")
        print(f"    risposta attesa: {attesa}")
        risultati = vectorstore.search(collection, query, K)
        primo = risultati[0]
        print(f"  1° · score {primo['score']:.3f} · [{primo['id']}]")
        for riga in primo["testo"].strip().splitlines():
            print(f"  │ {riga}")
        for r in risultati[1:]:
            pulito = " ".join(r["testo"].split())
            print(f"  poi · {r['score']:.3f} · [{r['id']}] {pulito[:56]}…")


# ---------------------------------------------------------------------------
# TABELLA ESPERIMENTI — una riga per giro: annotate PRIMA di cambiare
# manopola, così la storia dei tentativi resta leggibile.
#
# Esito per query, guardando il 1° risultato:
#   OK     contiene la risposta, tutta
#   META   la contiene a metà: si interrompe a metà frase
#   FUORI  non è la risposta: parla d'altro, o me la fa cercare io
#
# | STRATEGIA | SIZE  | OVERLAP/SOGLIA | chunk | saldi | contributo | E07 |
# |-----------|-------|----------------|-------|-------|------------|-----|
# | fixed     | 500   | 0              |       |       |            |     |
# |           |       |                |       |       |            |     |
# |           |       |                |       |       |            |     |
# |           |       |                |       |       |            |     |
# |           |       |                |       |       |            |     |
# |           |       |                |       |       |            |     |
# |           |       |                |       |       |            |     |
# |           |       |                |       |       |            |     |
#
# Quale configurazione porta a casa TUTTE e tre le query? Ce n'è una sola?
#
# Prima di chiudere: rimettete la configurazione che avete scelto e
# rilanciate un'ultima volta — la collection che resta su disco è quella
# dell'ULTIMO lancio, ed è da lì che riparte la prossima lezione.
# ---------------------------------------------------------------------------
