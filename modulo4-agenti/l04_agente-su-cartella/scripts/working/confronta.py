"""confronta.py — la stessa domanda con i tool di Modulo 3 e con i tool di cartella.

Per ogni giro stampa i tool chiamati, le chiamate al modello, i token e la risposta. Serve strumenti_cartella.py finito: con le sole firme i tool di cartella rimandano al
modello l'errore «da scrivere», e l'assistente risponde che non trova niente.
Costa meno di un centesimo.

Uso:  python confronta.py
"""
import asyncio

from agents import Agent, Runner, ToolCallItem

import assistente
from strumenti_cartella import elenca_file, cerca, leggi_file

DOMANDA = "Quali documenti devo consegnare il primo giorno di lavoro?"
GIRI = 3

STRADE = [
    ("tool di Modulo 3", assistente.ISTRUZIONI, [assistente.cerca_documenti, assistente.query_db]),
    ("tool di cartella", assistente.ISTRUZIONI_CARTELLA, [elenca_file, cerca, leggi_file]),
]


async def main():
    print(f"Domanda: {DOMANDA}")
    for nome, istruzioni, tools in STRADE:
        agente = Agent(name="Assistente Valtesa", instructions=istruzioni, tools=tools, model=assistente.MODELLO)
        print(f"\n== {nome}")
        for giro in range(1, GIRI + 1):
            result = await Runner.run(agente, DOMANDA, max_turns=assistente.MAX_TURNI)
            chiamati = [item.raw_item.name for item in result.new_items if isinstance(item, ToolCallItem)]
            u = result.context_wrapper.usage
            print(f"giro {giro}: {u.requests} chiamate, {u.input_tokens} token in, {u.output_tokens} out; tool: {', '.join(chiamati)}")
            print(f"   {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
