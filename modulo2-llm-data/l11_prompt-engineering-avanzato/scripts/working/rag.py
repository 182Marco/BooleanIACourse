"""rag.py — il primo RAG completo del corso: domanda → documenti → risposta.

Prima si scrive il retrieval (col docente), poi scrivete voi il prompt RAG
e il giro completo, e li provate sulle domande del main:

    python working/rag.py
"""
import sys

from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from aikit import vectorstore              # noqa: E402 — L21-L22
from aikit.llm_client import LLMClient     # noqa: E402 — L15

llm = LLMClient()

# TODO 4 (esercizio 2): miglioratelo — tono, formato delle citazioni,
# come deve suonare il "non c'è nei documenti".
SYSTEM_PROMPT = "Sei l'assistente clienti di Lumen S.r.l."


# --------------------------------------------------- TODO 1 · col docente 🎤
def cerca_chunk(query, k=4):
    """I k chunk più pertinenti dalla collection `lumen_chunks` di L22.

    Ogni risultato è un dict {"id", "testo", "score", "doc"} (è il
    vectorstore di aikit a restituirlo così). L'"id" (es.
    "manuale-lumadesk-007") è la fonte da citare nel prompt — "doc" è solo
    il nome del documento, senza il numero di chunk.

    Fatto quando: sulla E07 tornano 4 chunk con score, come a schermo.
    """
    raise NotImplementedError


# ----------------------------------------------------------- TODO 2 · voi ⌨️
def costruisci_prompt(query, chunks):
    """Il prompt RAG (prompt-as-function, come a L15): restituisce la stringa.

    Deve tenere separati, in sezioni marcate, le istruzioni, i documenti e
    la domanda — e chiedere: risposta fondata SOLO sui documenti, fonte
    citata, e il rifiuto esplicito quando la risposta non c'è.

    Fatto quando: usato dentro rispondi() (TODO 3), su DOMANDA_NEI_DOCUMENTI
    la risposta cita la fonte vera invece di inventare.
    """
    raise NotImplementedError


# ----------------------------------------------------------- TODO 3 · voi ⌨️
def rispondi(query, k=4):
    """Il giro completo: cerca_chunk → costruisci_prompt → modello.

    Restituisce il testo della risposta.
    (La chiamata è: llm.chat(messaggi, instructions=SYSTEM_PROMPT).)

    Fatto quando: su DOMANDA_NEI_DOCUMENTI (E07) risponde con la procedura
    vera del manuale, con la fonte; su DOMANDA_FUORI (contrassegno) esce il
    rifiuto pulito, non metodi di pagamento inventati.
    """
    raise NotImplementedError


# --------------------------------------------- fornita: il confronto "senza"
def rispondi_senza_documenti(query):
    """La stessa domanda, senza RAG: il modello da solo. Per il confronto."""
    return llm.chat([{"role": "user", "content": query}],
                    instructions=SYSTEM_PROMPT)


if __name__ == "__main__":
    DOMANDA_NEI_DOCUMENTI = "La centralina mostra il codice E07: cosa devo fare?"
    DOMANDA_FUORI = "Posso pagare alla consegna, in contrassegno?"
    K = 4

    # Provate ogni domanda con rispondi() e con rispondi_senza_documenti():
    # cosa cambia? Da dove arriva la risposta? E sulla domanda che nei
    # documenti NON c'è? In fondo, stampate il conto della serata
    # (llm.costo_totale). Da qui in giù scrivete voi.
