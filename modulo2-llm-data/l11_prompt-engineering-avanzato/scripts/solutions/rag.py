"""rag.py — il primo RAG completo del corso: domanda → documenti → risposta.

Versione COMPLETA (riferimento docente) di working/rag.py: stessi nomi,
stessi import. Il main e il prompt sono UNA soluzione possibile: negli
esercizi il come sta agli studenti.

    python solutions/rag.py
"""
import sys

from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from aikit import vectorstore              # noqa: E402 — L21-L22
from aikit.llm_client import LLMClient     # noqa: E402 — L15

llm = LLMClient()

# TODO 4 (esercizio 2): la versione "migliorata" — ruolo, vincoli, formato.
SYSTEM_PROMPT = (
    "Sei l'assistente clienti di Lumen S.r.l., produttore delle scrivanie "
    "regolabili LumaDesk. Rispondi in italiano, in tono cordiale e concreto, "
    "al massimo in quattro frasi."
)


# --------------------------------------------------- TODO 1 · col docente 🎤
def cerca_chunk(query, k=4):
    """I k chunk più pertinenti dalla collection `lumen_chunks` di L22."""
    collection = vectorstore.apri_collection("lumen_chunks")
    return vectorstore.search(collection, query, k)


# ----------------------------------------------------------- TODO 2 · voi ⌨️
def costruisci_prompt(query, chunks):
    """Il prompt RAG (prompt-as-function, come a L15): restituisce la stringa."""
    documenti = ""
    for c in chunks:
        documenti += f"<documento fonte=\"{c['id']}\">\n{c['testo']}\n</documento>\n"

    return f"""Rispondi alla domanda del cliente usando SOLO le informazioni
nei documenti qui sotto. Cita la fonte tra parentesi quadre, per esempio:
[policy-resi-garanzia-002]. Se la risposta non è nei documenti, rispondi
esattamente: "Non lo trovo nei documenti: ti metto in contatto con un
operatore." — senza inventare nulla.

<documenti>
{documenti}</documenti>

<domanda>
{query}
</domanda>"""


# ----------------------------------------------------------- TODO 3 · voi ⌨️
def rispondi(query, k=4):
    """Il giro completo: cerca_chunk → costruisci_prompt → modello."""
    chunks = cerca_chunk(query, k)
    prompt = costruisci_prompt(query, chunks)
    return llm.chat([{"role": "user", "content": prompt}],
                    instructions=SYSTEM_PROMPT)


# --------------------------------------------- fornita: il confronto "senza"
def rispondi_senza_documenti(query):
    """La stessa domanda, senza RAG: il modello da solo. Per il confronto."""
    return llm.chat([{"role": "user", "content": query}],
                    instructions=SYSTEM_PROMPT)


if __name__ == "__main__":
    DOMANDA_NEI_DOCUMENTI = "La centralina mostra il codice E07: cosa devo fare?"
    DOMANDA_FUORI = "Posso pagare alla consegna, in contrassegno?"
    K = 4

    for domanda in (DOMANDA_NEI_DOCUMENTI, DOMANDA_FUORI):
        print(f"\n=== {domanda}")
        print("— senza documenti (il modello da solo):")
        print("  " + rispondi_senza_documenti(domanda).replace("\n", "\n  "))
        print("— col RAG (fondata sui documenti):")
        print("  " + rispondi(domanda, K).replace("\n", "\n  "))

    print(f"\nconto della serata: {llm.n_chiamate} chiamate, "
          f"${llm.costo_totale:.4f}")
