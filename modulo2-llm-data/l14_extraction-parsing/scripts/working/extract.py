"""extract.py — dal documento vero al record: Pydantic + Structured Outputs.

L'unico file della serata (L26). Il pattern (schema Pydantic + chiamata con
structured outputs) è quello di L25 e non si ri-spiega. La novità: il testo
viene da un documento vero (una fattura Lumen), letto da file — non scritto
per l'occasione — e due campi possono mancare (`sconto`, `note`): nullable
sul serio, non solo un bonus come a L25.

    python working/extract.py
"""
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

MODELLO = "gpt-4o-mini"
DATASET = Path(__file__).parent.parent / "dataset"

client = OpenAI()


# --------------------------------------------------- TODO 1 · col docente 🎤
def carica(nome_file):
    """La fattura è già testo pulito (.txt): basta una lettura diretta.
    Per un PDF si riuserebbe aikit.load() di L16 — qui non serve."""
    raise NotImplementedError


# --------------------------------------------------- TODO 2 · col docente 🎤
class RigaFattura(BaseModel):
    """Una riga della fattura: prodotto, quantità, prezzo unitario.

    TODO: aggiungere i campi.
    """


# --------------------------------------------------- TODO 2 · col docente 🎤
class Fattura(BaseModel):
    """Lo schema della serata. Due campi NULLABLE — sconto e note possono
    mancare, e allora tornano None, non un valore inventato.

    TODO: aggiungere i campi (due nullable: sconto, note).
    """


# --------------------------------------------------- TODO 2 · col docente 🎤
def estrai_fattura(testo):
    """Stesso pattern di L25 (estrai_persona): structured outputs su un
    documento vero invece che su un testo scritto per l'occasione."""
    raise NotImplementedError


# ---------------------------------------------------------------------------
# ESERCIZIO BREVE (⌨️ da soli) — TODO 3
#
# Un CV diverso dalla fattura: un altro schema, con almeno un campo
# nullable per un'informazione che il CV potrebbe non menzionare (qui:
# le certificazioni — il testo di Marta non ne cita nessuna).
# ---------------------------------------------------------------------------

# TODO 3 · da soli
class EsperienzaLavorativa(BaseModel):
    """TODO: azienda, ruolo, anni."""


# TODO 3 · da soli
class PersonaCV(BaseModel):
    """TODO: nome, cognome, esperienze (list[EsperienzaLavorativa]),
    competenze (list[str]), certificazioni (nullable)."""


# TODO 3 · da soli
def estrai_cv(testo):
    """Stesso pattern di estrai_fattura, sul nuovo schema PersonaCV."""
    raise NotImplementedError


if __name__ == "__main__":
    # Tappa 1: carico la fattura — testo grezzo, intestazione e footer visibili.
    testo1 = carica("fattura_2026-0143.txt")
    print(testo1[:160], "...\n", sep="")

    # Tappa 2: schema + estrazione.
    fattura1 = estrai_fattura(testo1)
    print(fattura1)
    conto = fattura1.imponibile + fattura1.iva - (fattura1.sconto or 0)
    print(f"verifica: {fattura1.imponibile} + {fattura1.iva} - "
          f"{fattura1.sconto or 0} = {conto:.2f} (totale: {fattura1.totale})")

    # Tappa 3: seconda fattura, senza sconto e senza nota.
    print()
    testo2 = carica("fattura_2026-0158.txt")
    fattura2 = estrai_fattura(testo2)
    print(fattura2)
    print(f"sconto={fattura2.sconto} · note={fattura2.note}")

    # Tappa 4: il caso impreciso — la riga in omaggio.
    print()
    testo3 = carica("fattura_2026-0171.txt")
    fattura3 = estrai_fattura(testo3)
    print(fattura3)

    # Esercizio breve: il CV di Marta.
    print()
    testo_cv = carica("cv_marta_colombo.txt")
    persona = estrai_cv(testo_cv)
    print(persona)
