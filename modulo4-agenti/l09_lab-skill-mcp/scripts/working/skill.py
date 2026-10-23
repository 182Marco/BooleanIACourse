"""skill.py — le skill dell'assistente, con la lettura progressiva costruita a mano.

Le skill stanno in skill-assistente/, una cartella per skill con il suo SKILL.md, nello stesso
formato del coding agent. Nelle istruzioni va solo l'indice: nome e descrizione di ogni skill
(ISTRUZIONI_SKILL). Il corpo il modello lo apre con il tool apri_skill, quando una domanda
corrisponde a una descrizione: come il tool Skill di Claude Code.

Era skill_agente.py (Modulo 4 · Lezione 7), senza l'agente e il main: dalla versione 0.9
l'agente è uno solo, in assistente.py.
"""
from pathlib import Path

from agents import function_tool

SKILL = Path(__file__).parent / "skill-assistente"


def leggi_skill(file):
    """Il frontmatter (name, description) e il corpo di un SKILL.md. Un campo per riga:
    una riga dell'intestazione senza «: » (per esempio il seguito di una descrizione
    su più righe) si salta."""
    _, testa, corpo = file.read_text(encoding="utf-8").split("---", 2)
    campi = dict(riga.split(": ", 1) for riga in testa.strip().splitlines() if ": " in riga)
    return campi, corpo.strip()


def indice():
    """Una riga per skill, solo nome e descrizione: è tutto quello che il modello vede all'inizio."""
    righe = []
    for file in sorted(SKILL.glob("*/SKILL.md")):
        campi, _ = leggi_skill(file)
        righe.append(f"- {campi['name']}: {campi['description']}")
    return "\n".join(righe)


@function_tool
def apri_skill(nome: str) -> str:
    """Apre una skill dell'elenco e rimanda le sue istruzioni, da seguire per rispondere.

    Args:
        nome: il nome della skill, come nell'elenco.
    """
    file = SKILL / nome / "SKILL.md"
    if Path(nome).name != nome or not file.exists():     # solo un nome, niente percorsi come ../
        return f"Nessuna skill «{nome}». Le skill sono:\n{indice()}"
    return leggi_skill(file)[1]


ISTRUZIONI_SKILL = f"""Hai delle skill: istruzioni scritte per alcuni compiti. Qui sotto c'è solo l'elenco, con nome e descrizione.
Se la domanda corrisponde alla descrizione di una skill, prima di tutto aprila con apri_skill e segui le sue istruzioni. Altrimenti non aprirla.
{indice()}"""
