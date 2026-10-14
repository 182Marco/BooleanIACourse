"""confronta.py — il compito da approvare con SandboxAgent, l'agente su cartella dell'SDK che ha
già la shell.

Per l'estensione dell'esercizio: stampa i comandi che lancia, chiamate al modello, token e
risposta, da mettere accanto alla traccia del vostro assistente con esegui_python. SandboxAgent
lavora su una copia di ufficio/ e lancia i comandi senza chiedere. Solo macOS, Linux e WSL: su
Windows il client locale non parte. Costa circa un centesimo.

Uso:  python confronta.py
"""
import asyncio
import platform
from pathlib import Path

CARTELLA = Path(__file__).parent

from dotenv import load_dotenv
load_dotenv(CARTELLA / ".env")                      # la chiave, prima di importare agents

from agents import MaxTurnsExceeded, Runner, ToolCallItem
from agents.run import RunConfig
from agents.sandbox import Manifest, SandboxAgent, SandboxRunConfig
from agents.sandbox.entries import LocalDir
from agents.sandbox.sandboxes import UnixLocalSandboxClient

MAX_TURNI = 10
DOMANDA = ("Quanto hanno speso in note spese approvate i dipendenti della sede di Padova? "
           "Guarda nella cartella ufficio.")

agente = SandboxAgent(
    name="Assistente Valtesa",
    instructions="Sei l'assistente dell'ufficio del personale di Valtesa. Rispondi in italiano, in poche frasi.",
    model="gpt-6-luna",
    default_manifest=Manifest(entries={"ufficio": LocalDir(src=CARTELLA / "ufficio")}),
)


async def main():
    if platform.system() == "Windows":
        print("Su Windows il client locale di SandboxAgent non parte: provate in WSL.")
        return
    config = RunConfig(sandbox=SandboxRunConfig(client=UnixLocalSandboxClient()))
    try:
        result = await Runner.run(agente, DOMANDA, max_turns=MAX_TURNI, run_config=config)
    except MaxTurnsExceeded:
        print(f"   nessuna risposta dopo {MAX_TURNI} chiamate")
        return
    for item in result.new_items:
        if isinstance(item, ToolCallItem):
            print(f"   comando  {item.raw_item.arguments[:300]}")
    u = result.context_wrapper.usage
    print(f"   {u.requests} chiamate · {u.input_tokens} token in, {u.output_tokens} out")
    print(f"→ {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
