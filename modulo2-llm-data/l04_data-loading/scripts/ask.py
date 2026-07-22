"""Il banco di prova: chiedere al modello qualcosa sul documento.

Come sappiamo se un loader funziona *davvero*? Non basta vedere del testo: deve
essere testo che il modello capisce. Allora, dopo ogni loader, gli facciamo una
domanda sul documento.

⚠️ `ask()` è volutamente NAIVE: infila TUTTO il testo nel prompt, niente
retrieval. È la BASELINE — funziona ora, ma con un PDF da 300 pagine o 500
documenti non ci sta nel contesto e costa troppo. Quel muro è il motivo per cui
esistono embeddings, search e chunking (il resto del modulo).

È anche lo strumento per fare le prove dal vivo:

    python ask.py sample_docs/bilancio.pdf
        → carica e mostra il testo (nessuna chiave necessaria)

    python ask.py sample_docs/bilancio.pdf "di quanto è cresciuto il fatturato?"
        → + la risposta del modello (serve OPENAI_API_KEY nel .env)

Riusa il `LLMClient` della L15.
"""
from loaders import Document, load

ISTRUZIONI = (
    "Rispondi alla domanda usando SOLO il documento fornito. "
    "Se l'informazione non è nel documento, dillo invece di inventare."
)

_client = None


def _get_client():
    # creato solo quando serve davvero: così il loading gira anche senza chiave
    global _client
    if _client is None:
        from llm_client import LLMClient
        _client = LLMClient()
    return _client


def ask(docs, domanda: str) -> str:
    if isinstance(docs, Document):
        docs = [docs]
    testo = "\n\n".join(d.text for d in docs)
    messaggi = [{
        "role": "user",
        "content": f'Documento:\n"""\n{testo}\n"""\n\nDomanda: {domanda}',
    }]
    return _get_client().chat(messaggi, instructions=ISTRUZIONI)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("uso: python ask.py <file> [domanda]")
        raise SystemExit(1)

    path = sys.argv[1]
    docs = load(path)
    print(f"{path} → {len(docs)} Document")
    print(f"  metadata: {docs[0].metadata}")
    anteprima = " ".join(docs[0].text.split())[:200]
    print(f"  testo:    {anteprima}…")

    if len(sys.argv) >= 3:
        domanda = sys.argv[2]
        print(f"  🤖 {domanda}")
        print(f"     → {ask(docs, domanda)}")
