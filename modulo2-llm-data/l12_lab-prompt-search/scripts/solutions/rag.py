"""rag.py — Lab Prompt & Search: A/B di prompt e tuning del retrieval.

Versione COMPLETA (riferimento docente) di working/rag.py: stessi nomi,
stessi import. I testi delle varianti (TODO 1-3) e reindicizza_chunks
(TODO 4) sono UNA soluzione possibile: il come è degli studenti.

    python solutions/rag.py
"""
import sys

from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from aikit import vectorstore              # noqa: E402 — L21-L22
from aikit import chunk as chunklib        # noqa: E402 — L22, da oggi in aikit
from aikit.llm_client import LLMClient     # noqa: E402 — L15

llm = LLMClient()

# ============================================================ Lab 1 · prompt
GROUNDING = "morbido"        # "morbido" | "severo"
CON_COT = False               # True = chiede al modello di ragionare prima di rispondere
CITAZIONE = "breve"          # "breve" (solo id) | "estesa" (id + frase esatta)

SYSTEM_PROMPTS = {
    "morbido": (
        "Sei l'assistente clienti di Lumen S.r.l., produttore delle scrivanie "
        "regolabili LumaDesk. Rispondi in italiano, in tono cordiale e concreto, "
        "al massimo in quattro frasi."
    ),
    "severo": (
        "Sei l'assistente clienti di Lumen S.r.l. Rispondi SOLO sulla base dei "
        "documenti forniti nel messaggio: se un dettaglio non è scritto "
        "testualmente, non aggiungerlo, anche se ti sembra plausibile o vale "
        "per altri prodotti che conosci. In caso di dubbio, di' che non lo sai "
        "invece di indovinare. Tono cordiale, massimo quattro frasi."
    ),
}


def costruisci_prompt(query, chunks):
    """Il prompt RAG: sezioni marcate, grounding, citazioni, rifiuto.

    Le tre manopole GROUNDING / CON_COT / CITAZIONE cambiano SOLO le
    istruzioni: i documenti e la domanda restano uguali in ogni variante,
    così il confronto tra un giro e l'altro è pulito.
    """
    documenti = ""
    for c in chunks:
        documenti += f"<documento fonte=\"{c['id']}\">\n{c['testo']}\n</documento>\n"

    if CITAZIONE == "breve":
        istruzione_citazione = (
            "Cita la fonte tra parentesi quadre, per esempio: "
            "[policy-resi-garanzia-002]."
        )
    else:
        istruzione_citazione = (
            "Dopo ogni affermazione cita la fonte tra parentesi quadre E "
            "riporta tra virgolette la frase esatta del documento su cui ti "
            "basi, per esempio: [policy-resi-garanzia-002] \"la finestra di "
            "reso scende a 14 giorni dalla consegna\"."
        )

    istruzione_cot = ""
    if CON_COT:
        istruzione_cot = (
            "\nPrima di scrivere la risposta, ragiona passo passo: elenca "
            "quali documenti sono rilevanti per la domanda e perché. Poi, "
            "separatamente, scrivi la risposta finale."
        )

    return f"""Rispondi alla domanda del cliente usando SOLO le informazioni
nei documenti qui sotto. {istruzione_citazione} Se la risposta non è nei
documenti, rispondi esattamente: "Non lo trovo nei documenti: ti metto in
contatto con un operatore." — senza inventare nulla.{istruzione_cot}

<documenti>
{documenti}</documenti>

<domanda>
{query}
</domanda>"""


def cerca_chunk(query, k=4, soglia=0.0):
    """I chunk più pertinenti dalla collection `lumen_chunks`, sopra `soglia`."""
    collection = vectorstore.apri_collection("lumen_chunks")
    risultati = vectorstore.search(collection, query, k)
    return [r for r in risultati if r["score"] >= soglia]


def rispondi(query, k=4, soglia=0.0):
    """Il giro completo: cerca_chunk → costruisci_prompt → modello."""
    chunks = cerca_chunk(query, k, soglia)
    if not chunks:
        return "Non lo trovo nei documenti: ti metto in contatto con un operatore."
    prompt = costruisci_prompt(query, chunks)
    return llm.chat([{"role": "user", "content": prompt}],
                    instructions=SYSTEM_PROMPTS[GROUNDING])


# ==================================================== Lab 2 · retrieval TODO
def reindicizza_chunks(strategia, size, overlap=0):
    """Rispezza i 3 documenti lunghi con `strategia`/`size` e ricrea da zero
    la collection `lumen_chunks` (aikit.chunk + aikit.vectorstore, come a
    L22 — richiamato qui come funzione unica, riusabile a ogni giro)."""
    documenti = chunklib.carica_documenti()
    ids, testi, metadati = [], [], []
    for nome, testo in documenti.items():
        if strategia == "fixed":
            pezzi = chunklib.chunk_fixed(testo, size, overlap)
        elif strategia == "recursive":
            pezzi = chunklib.chunk_recursive(testo, size)
        else:
            raise ValueError(f"strategia {strategia!r} sconosciuta")
        for numero, pezzo in enumerate(pezzi):
            ids.append(f"{nome}-{numero:03d}")
            testi.append(pezzo)
            metadati.append({"doc": nome})

    from aikit.embeddings import embed
    vettori = embed(testi)
    collection = vectorstore.crea_collection("lumen_chunks")
    vectorstore.indicizza(collection, ids, testi, vettori, metadati)
    print(f"  re-indicizzati {len(testi)} chunk ({strategia}, size={size})")


if __name__ == "__main__":
    K = 4
    SOGLIA = 0.0

    # None = non tocca la collection (resta recursive/500 di L22-L23).
    # Per ri-chunkare: REINDICIZZA = ("recursive", 800) oppure ("fixed", 500, 50).
    REINDICIZZA = None
    if REINDICIZZA:
        reindicizza_chunks(*REINDICIZZA)

    QUERY_SET = [
        ("facile",       "La centralina mostra il codice E07: cosa devo fare?"),
        ("trappola",     "Quanti giorni ho per restituire un prodotto comprato "
                          "durante i saldi?"),
        ("fuori-corpus", "Posso pagare alla consegna, in contrassegno?"),
        ("facile-2",     "Quanto vale il contributo per la postazione e entro "
                          "quanti giorni va presentata la richiesta?"),
    ]

    print(f"config: grounding={GROUNDING} · cot={CON_COT} · citazione={CITAZIONE} "
          f"· k={K} · soglia={SOGLIA}\n")

    for etichetta, domanda in QUERY_SET:
        risposta = rispondi(domanda, K, SOGLIA)
        in_tok, out_tok, costo = llm.ultimo_uso
        print(f"=== [{etichetta}] {domanda}")
        print("  " + risposta.replace("\n", "\n  "))
        print(f"  ({in_tok} in / {out_tok} out · ${costo:.5f})\n")

    print(f"conto del giro: {llm.n_chiamate} chiamate, ${llm.costo_totale:.4f}")
