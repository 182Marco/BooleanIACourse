"""skill_agente.py — la lettura progressiva delle skill, costruita a mano nell'assistente.

Le skill dell'assistente stanno in skill-assistente/, una cartella per skill con il suo
SKILL.md, nello stesso formato del coding agent. Nelle istruzioni va solo l'indice: nome e
descrizione di ogni skill. Il corpo il modello lo apre con il tool apri_skill, quando una
domanda corrisponde a una descrizione: come il tool Skill di Claude Code.

Uso:  python skill_agente.py "Vado a Milano il 14 luglio per due notti: quanto posso spendere?"
      python skill_agente.py --istruzioni       solo il testo che riceve il modello
"""
import asyncio
import sys
from pathlib import Path

from agents import Agent, Runner, SQLiteSession, function_tool

from assistente import CARTELLA, MAX_TURNI, MODELLO, stampa_traccia
from assistente import agente as assistente_base       # l'assistente di Modulo 4 · Lezione 6, così com'è

SKILL = CARTELLA / "skill-assistente"


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

agente = Agent(name="Assistente Valtesa", instructions=assistente_base.instructions + "\n\n" + ISTRUZIONI_SKILL,
               tools=assistente_base.tools + [apri_skill], model=MODELLO)


async def main():
    if sys.argv[1:] == ["--istruzioni"]:
        print(agente.instructions)
        return
    domanda = " ".join(sys.argv[1:]) or input("Tu> ")
    result = await Runner.run(agente, domanda, session=SQLiteSession("skill"), max_turns=MAX_TURNI)
    stampa_traccia(result)
    print(f"→ {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
