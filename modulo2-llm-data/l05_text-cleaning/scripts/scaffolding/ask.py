"""Il banco di prova: le stesse domande, sul testo sporco e su quello pulito.

Già scritto, non si tocca: è l'attrezzo con cui si guarda l'effetto del
cleaning. `rispondi()` fa la domanda al modello, `mostra_confronto()` stampa i
numeri del prima/dopo.

`temperature=0`: due risposte diverse devono venire dal testo, non dal caso.
"""
import os
from pathlib import Path

MODELLO = "gpt-4.1-mini"
ISTRUZIONI = (
    "Rispondi alla domanda usando SOLO il documento fornito. "
    "Se l'informazione non c'è, dillo invece di inventare."
)

_client = None


def _cliente():
    """Il client, creato solo quando serve davvero (così il resto gira offline)."""
    global _client
    if _client is None:
        from dotenv import load_dotenv
        from openai import OpenAI
        load_dotenv(Path(__file__).resolve().parent.parent / ".env")
        if not os.getenv("OPENAI_API_KEY"):
            return None
        _client = OpenAI()
    return _client


def rispondi(testo, domanda):
    """La risposta del modello a `domanda`, avendo davanti solo `testo`."""
    cli = _cliente()
    if cli is None:
        return "(nessuna chiave: alza la mano, il docente ne ha una di riserva)"
    risposta = cli.chat.completions.create(
        model=MODELLO,
        temperature=0,
        messages=[
            {"role": "system", "content": ISTRUZIONI},
            {"role": "user", "content": f"{testo}\n\nDomanda: {domanda}"},
        ],
    )
    return risposta.choices[0].message.content.strip()


def mostra_confronto(sporco, pulito, spia=None):
    """Prima/dopo in numeri: caratteri, righe, e quanto è stato tolto.

    `spia` è una stringa da cercare nei due testi (es. un dato del contorno):
    serve a vedere che cosa è sparito, non solo quanto.
    """
    tolti = len(sporco) - len(pulito)
    quota = tolti / len(sporco) * 100 if sporco else 0
    print(f"  sporco : {len(sporco):6d} caratteri · {len(sporco.splitlines()):5d} righe")
    print(f"  pulito : {len(pulito):6d} caratteri · {len(pulito.splitlines()):5d} righe")
    print(f"  tolti  : {tolti:6d} caratteri ({quota:.1f}%)")
    if spia:
        print(f"  «{spia}» nel testo: sporco {sporco.count(spia)}x · "
              f"pulito {pulito.count(spia)}x")
