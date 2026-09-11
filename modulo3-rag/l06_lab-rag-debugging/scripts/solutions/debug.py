"""debug.py — il banco di prova del retrieval: dove si rompe, e quale leva lo cura.

Le leve ci sono tutte: k, soglia, chunk size e prompt (Modulo 2 · Lezione
12), hybrid (Modulo 3 · Lezione 4), rerank (Modulo 3 · Lezione 5). Oggi
non se ne impara una nuova: si impara a capire QUALE serve, partendo da
dove la pipeline si è rotta. Tre domande, in ordine, e al primo «no» il
colpevole è il passaggio che doveva dire «sì»:

  1. il chunk giusto esiste nel corpus?   no → non è un bug: la domanda non
                                          ha risposta, e il sistema deve dirlo
  2. è nel top-k del retrieval?           no → è il retrieval (guarda dov'è:
                                          vicino al taglio o lontano)
  3. la risposta lo usa?                  no → è la generazione

Le tre domande sono i tre TODO: trova_nel_corpus() risponde alla prima,
diagnostica() le mette in fila su una query, giro() le ripete su tutto
il set.

  TODO 1 (Lab 1)   trova_nel_corpus(frase): la domanda 1
  TODO 2 (Lab 1)   diagnostica(query, frase_attesa): le tre domande su una query
  TODO 3 (Lab 1)   giro(): tutto il query set con la CONFIG corrente

Nel Lab 2 si cacciano i failure con domande proprie; nel Lab 3 non si
scrive codice: si gira UNA leva in CONFIG, si rilancia il giro e si
confronta la tabella con quella di prima. I failure si annotano in
working/griglia.md, una riga ciascuno. La consegna completa è in
CONSEGNA.md.

Uso (dalla cartella scripts/):
    python working/debug.py
"""
import sys
import time
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from aikit import rag                            # noqa: E402 — Modulo 3 · Lezione 2
from aikit import hybrid                         # noqa: E402 — Modulo 3 · Lezione 4
from aikit import rerank                         # noqa: E402 — Modulo 3 · Lezione 5
from aikit import vectorstore                    # noqa: E402 — Modulo 2 · Lezione 9

# ---------------------------------------- le leve, tutte in un posto
CONFIG = {
    # --- il retrieval: quali chunk, in che ordine
    "retrieval": "semantico",   # "semantico" (rag.recupera) · "hybrid" (BM25 + RRF) · "rerank" (hybrid + secondo stadio)
    "backend": "llm",           # il reranker, solo se retrieval = "rerank": "cohere" oppure "llm"
    "chunk_size": 500,          # la dimensione dei chunk: cambiarla ri-indicizza il corpus (2 minuti, meno di un centesimo)
    "soglia": None,             # sotto questo score il chunk non entra nel prompt; None = nessuna soglia. Solo col
                                # semantico o con rerank cohere: lì lo score è una pertinenza (coseno, relevance 0-1);
                                # con hybrid e llm è una posizione, e la soglia non vuol dire niente.
    # --- quanti chunk
    "k": 4,                     # i primi k entrano nel prompt (la baseline di rag.py)
    "candidati": 10,            # quanti ne guarda la diagnostica per dire DOVE sta il chunk giusto (e quanti ne riordina il rerank)
    # --- le regole che il modello segue con il prompt
    "istruzioni": None,         # None = le ISTRUZIONI di rag.py; una stringa per provarne altre
}

# Per provare UNA domanda sola (Lab 1): (domanda, frase attesa). Con None
# il main fa il giro completo di QUERY_SET + LE_MIE_QUERY.
SOLO = None

# Il query set fisso del modulo (Modulo 3 · Lezione 4-5), oggi con accanto
# a ogni domanda una FRASE ATTESA: un pezzo di testo che sta solo nel chunk
# giusto. None = la risposta non è nel corpus.
QUERY_SET = [
    ("Cosa è successo nel ticket TCK-1152?", "TCK-1152"),
    ("Cosa copre SRV-02?", "SRV-02 — ritiro"),
    ("Com'è stato risolto il TCK-1201?", "TCK-1201"),
    ("Con l'errore E07, per quanti secondi devo scollegare l'alimentazione?", "scollega l'alimentazione per 30 secondi"),
    ("Quale RMA devo aprire per un danno da trasporto?", "RMA-2 — reso per danno da trasporto"),
    ("Cosa ha introdotto il firmware 2.3.0?", "La 2.3.0 ha corretto"),
    ("La scrivania non sta ferma, si muove tutta quando scrivo: che controllo faccio?", "oscilla alla massima altezza"),
    ("Quanto tempo ho per richiedere il contributo per la postazione di casa?", "entro 60 giorni"),
    ("Posso lavorare dall'estero?", "massimo di 2 settimane"),
    ("Il monitor scende piano piano da solo: cosa faccio?", "TCK-1118"),
    ("Ho comprato con un codice sconto: posso restituire?", "ESTATE15"),
    ("Perché il piano si ferma sempre a metà corsa?", "TCK-1156"),
    ("Posso pagare alla consegna, in contrassegno?", None),
]

# Le query avversarie VOSTRE (Lab 1): stessa forma, (domanda, frase attesa).
# La frase la trovate con trova_nel_corpus(); None se la risposta non c'è.
LE_MIE_QUERY = [
]


# ------------------------------------------------ dato: le leve, applicate
def prepara():
    """Applica le leve che agiscono PRIMA della ricerca: il chunk size
    (la collection giusta, indicizzata se manca), l'indice BM25 su quella
    collection, quanti candidati chiede l'hybrid, le istruzioni del prompt."""
    if CONFIG["chunk_size"] != 500:                      # 500 è la collection lumen_m3 del modulo
        rag.CONFIG["collection"] = f"lumen_m3_{CONFIG['chunk_size']}"
        rag.CONFIG["chunk_size"] = CONFIG["chunk_size"]
    if vectorstore.apri_collection(rag.CONFIG["collection"]).count() == 0:
        rag.indicizza()
    n = hybrid.costruisci_indice_bm25()                   # legge la collection di rag.CONFIG
    hybrid.CONFIG["candidati"] = CONFIG["candidati"]      # quanti ne chiede a ogni lista prima di fondere
    if CONFIG["istruzioni"] is not None:
        rag.ISTRUZIONI = CONFIG["istruzioni"]
    print(f"collection {rag.CONFIG['collection']}: {n} chunk · retrieval {CONFIG['retrieval']}"
          f"{' (' + CONFIG['backend'] + ')' if CONFIG['retrieval'] == 'rerank' else ''}"
          f" · candidati {CONFIG['candidati']} · soglia {CONFIG['soglia']} · k {CONFIG['k']}")


def cerca(query):
    """Il retrieval secondo CONFIG: CONFIG["candidati"] chunk dal più
    pertinente in giù, nella forma di rag.recupera() (dict con id, testo,
    score, source): nel prompt ne entrano i primi k, gli altri servono alla
    diagnosi. Poi la soglia, se c'è."""
    if CONFIG["retrieval"] == "semantico":
        candidati = rag.recupera(query, CONFIG["candidati"])
    elif CONFIG["retrieval"] == "hybrid":
        candidati = hybrid.cerca_hybrid(query, CONFIG["candidati"])
    else:
        candidati = rerank.cerca_due_stadi(query, CONFIG["candidati"], CONFIG["candidati"], CONFIG["backend"])
        if CONFIG["backend"] == "cohere":
            time.sleep(rerank.CONFIG["pausa"])            # il free tier Cohere fa 10 chiamate al minuto
    if CONFIG["soglia"] is not None:
        candidati = [c for c in candidati if c["score"] >= CONFIG["soglia"]]
    return candidati


# ------------------------------------------------------------- TODO 1 · ⌨️
def trova_nel_corpus(frase):
    """La domanda 1: gli id dei chunk che contengono la frase (maiuscole e
    minuscole non contano). I chunk sono tutti in hybrid.INDICE["chunks"]
    (una lista di dict con id, testo, source), riempita da prepara(): il
    main la chiama per primo, quindi questa funzione si prova dal main
    (con SOLO), non da sola. Ritorna una lista di id, vuota se la frase
    non c'è."""
    trovati = []
    for c in hybrid.INDICE["chunks"]:
        if frase.lower() in c["testo"].lower():
            trovati.append(c["id"])
    return trovati


# ------------------------------------------------------------- TODO 2 · ⌨️
def diagnostica(query, frase_attesa):
    """Le tre domande su una query, con la CONFIG corrente. frase_attesa
    è un pezzo di testo che sta nel chunk giusto (None se la risposta non
    è nel corpus). Stampa: (1) se la frase esiste nel corpus e in quali
    chunk; (2) se il primo di quei chunk è nel top-k, cioè tra i primi
    CONFIG["k"] dei candidati di cerca(), e a che posizione sta (cerca() ne
    ritorna CONFIG["candidati"], di più, per dire quanto è lontano); (3) la
    risposta di rag.genera() sui primi k, e se la usa, cioè se cita uno di
    quei chunk (le citazioni sono tra parentesi quadre: [id]).
    Ritorna (posizione, nel_topk, giusta): posizione None se il chunk non
    è tra i candidati; giusta = la risposta cita il chunk atteso, oppure —
    se la risposta non è nel corpus — dice «Non lo trovo nei documenti.»"""
    stampa_domanda(query)
    attesi = []
    if frase_attesa is not None:
        attesi = trova_nel_corpus(frase_attesa)
    if frase_attesa is None:
        print("   1. esiste?         no: domanda senza risposta, il sistema deve dirlo")
    elif attesi == []:
        print(f"   1. esiste?         la frase «{frase_attesa}» non c'è: la frase è sbagliata, o la risposta non è nel corpus")
    else:
        print(f"   1. esiste?         sì: {', '.join(attesi)}")

    candidati = cerca(query)
    posizione = None
    for i, c in enumerate(candidati, start=1):
        if c["id"] in attesi:
            posizione = i
            break
    if attesi:
        if posizione is None:
            print(f"   2. nel top-k?      no: non è nemmeno tra i primi {len(candidati)} ({CONFIG['retrieval']})")
        else:
            print(f"   2. nel top-k?      {'sì' if posizione <= CONFIG['k'] else 'no'}: posizione {posizione} (k = {CONFIG['k']}, guardati i primi {len(candidati)}, {CONFIG['retrieval']})")

    nel_topk = posizione is not None and posizione <= CONFIG["k"]
    if attesi:
        stampa_chunks(candidati[:CONFIG["k"]], attesi)

    risposta = rag.genera(candidati[:CONFIG["k"]], query)
    print(f"   risposta: {' '.join(risposta.split())}")
    if frase_attesa is None:
        giusta = "Non lo trovo" in risposta
        print(f"   3. dice che non c'è? {'sì' if giusta else 'NO: ha risposto lo stesso'}")
    else:
        giusta = False
        for cid in attesi:
            if f"[{cid}]" in risposta:
                giusta = True
        print(f"   3. la usa?         {'sì' if giusta else 'no'}")
    return posizione, nel_topk, giusta


# ------------------------------------------------------------- TODO 3 · ⌨️
def giro():
    """Tutto QUERY_SET + LE_MIE_QUERY con la CONFIG corrente: per ogni
    query diagnostica(), poi una tabella riassuntiva (una riga per query:
    posizione, nel top-k, giusta) e quante risposte sono giuste in tutto.
    È la tabella che si confronta prima e dopo una leva."""
    esiti = []
    for query, frase in QUERY_SET + LE_MIE_QUERY:
        esiti.append((query, diagnostica(query, frase)))
    stampa_tabella(esiti)


# ------------------------------------------------- helper di stampa (dati)
def stampa_domanda(query):
    print("\n" + "=" * 78)
    print(f"D: {query}")


def stampa_chunks(chunks, evidenzia):
    """I chunk che entrano nel prompt, uno per riga; il chunk atteso è
    segnato."""
    for posizione, c in enumerate(chunks, start=1):
        anteprima = " ".join(c["testo"].split())[:44]
        segno = "  ◄ atteso" if c["id"] in evidenzia else ""
        print(f"      {posizione}. {c['id']:<24} score={c['score']:8.3f}  {anteprima}…{segno}")


def stampa_tabella(esiti):
    """La tabella riassuntiva del giro: esiti è una lista di
    (query, (posizione, nel_topk, giusta))."""
    print("\n\n" + "#" * 78)
    print(f"# RIASSUNTO · retrieval {CONFIG['retrieval']}"
          f"{' (' + CONFIG['backend'] + ')' if CONFIG['retrieval'] == 'rerank' else ''}"
          f" · candidati {CONFIG['candidati']} · soglia {CONFIG['soglia']} · k {CONFIG['k']} · chunk {CONFIG['chunk_size']}")
    print("#" * 78)
    print(f"  {'#':>2}  {'domanda':<44} {'pos':>4}  {'top-k':<6}  giusta")
    giuste = 0
    for n, (query, (posizione, nel_topk, giusta)) in enumerate(esiti, start=1):
        giuste += giusta
        print(f"  {n:>2}  {query[:44]:<44} {posizione if posizione else '—':>4}  "
              f"{'sì' if nel_topk else 'no':<6}  {'sì' if giusta else 'no'}")
    print(f"\n  risposte giuste: {giuste}/{len(esiti)}")


if __name__ == "__main__":
    prepara()
    if SOLO is not None:
        try:
            diagnostica(SOLO[0], SOLO[1])
        except NotImplementedError as e:
            raise SystemExit(f"ancora da scrivere: {e}")
    else:
        try:
            giro()
        except NotImplementedError as e:
            raise SystemExit(f"ancora da scrivere: {e} — per provare una domanda sola, metti la coppia in SOLO")
