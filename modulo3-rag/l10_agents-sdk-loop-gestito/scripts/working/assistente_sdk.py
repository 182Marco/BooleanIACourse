"""assistente_sdk.py — l'assistente della lezione scorsa, con il giro gestito dall'OpenAI Agents SDK.

A Modulo 3 · Lezione 9 il giro del tool calling era scritto a mano: chiedi()
chiamava il modello, TOOLS era la lista che il modello vedeva, esegui()
smistava le function_call, e un ciclo rimandava i risultati con lo stesso
call_id. Stasera quel giro lo fa una libreria, openai-agents. I due tool
restano funzioni nostre; cambia solo chi li cabla.

La corrispondenza, pezzo per pezzo:

  la lezione scorsa                        stasera
  ISTRUZIONI                            →  Agent(instructions=...)
  definisci_tool(schema) + TOOLS        →  @function_tool sopra la funzione, e tools=[...]
  esegui() + il ciclo dentro chiedi()   →  Runner.run_sync(agente, domanda)
  MAX_CHIAMATE                          →  max_turns
  usati (il log della strada)           →  result.new_items (la traccia del run)

Il file, dall'alto in basso:

  costanti             MODELLO, K (quanti chunk rimanda cerca_documenti),
                       MAX_TURNI; DOMANDE (una per strada, più una senza
                       risposta), SOLO
  cerca_documenti      il RAG come tool, già scritto: la docstring è la
                       descrizione che il modello legge
  TODO 1               query_db come tool: stessa forma, la funzione vera è
                       in aikit/tools.py
  ISTRUZIONI + agente  le istruzioni della lezione scorsa, e l'Agent con i
                       due tool
  TODO 2               strada(result): dalla traccia del run alla strada presa
  dato                 stampa_traccia(), stampa_tabella(), il main

Uso (dalla cartella scripts/):
    python working/assistente_sdk.py
"""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))   # il solito prologo del modulo: rende importabile aikit/

from dotenv import load_dotenv                   # noqa: E402

load_dotenv(SCRIPTS / ".env")                    # OPENAI_API_KEY (e, se c'è, OPENAI_AGENTS_DISABLE_TRACING): PRIMA di importare agents, che la legge la prima volta che gli serve e poi la tiene

from agents import Agent, Runner, function_tool, MaxTurnsExceeded   # noqa: E402 — i tre oggetti dell'SDK, e l'eccezione del tetto
from agents import ToolCallItem, ToolCallOutputItem, MessageOutputItem   # noqa: E402 — i tipi di item della traccia: tool chiesto, suo output, risposta

from aikit import rag                            # noqa: E402 — Modulo 3 · Lezione 2: recupera()
from aikit import tools                          # noqa: E402 — Modulo 3 · Lezione 8: query_db(sql), la funzione vera
from aikit import vectorstore                    # noqa: E402 — Modulo 2 · Lezione 9: la collection
from aikit.llm_client import cost_usd            # noqa: E402 — Modulo 2 · Lezione 3

MODELLO = "gpt-5.6-luna"                         # lo stesso della lezione scorsa; è in PRICING di llm_client
K = 4                                            # quanti chunk cerca_documenti rimanda al modello
MAX_TURNI = 10                                   # il tetto al giro: un turno è una chiamata al modello (era MAX_CHIAMATE)

# Le domande del main, ognuna con la STRADA ATTESA, come la lezione scorsa.
DOMANDE = [
    ("Entro quanti giorni posso restituire un prodotto comprato online?", "documenti"),
    ("Quanti ordini ha fatto Giulia Moretti?", "dati"),
    ("Lorenzo Rossi può montare il braccio LMX-4400 sulle scrivanie che ha ordinato?", "documenti+dati"),
    ("Che tempo fa oggi a Padova?", "nessuna"),
]
SOLO = None              # una domanda sola al posto delle altre: SOLO = "Quanti ordini ha fatto Giulia Moretti?"


# ------------------------------------------- il RAG come tool · già scritto
# @function_tool trasforma la funzione in un tool: il nome è quello della
# funzione, la descrizione è la docstring, i parametri escono dalla firma
# (domanda: str) e dalla sezione Args. È la stessa definizione che la
# lezione scorsa costruiva definisci_tool() da una classe Pydantic. Dopo il
# decoratore cerca_documenti non è più una funzione da chiamare: è un oggetto
# tool, e lo chiama Runner dentro il giro.
@function_tool
def cerca_documenti(domanda: str) -> str:
    """Cerca nei documenti aziendali di Lumen (manuale della scrivania LumaDesk,
    policy resi e garanzia, guida allo smart working, listino e catalogo
    prodotti, ticket di supporto, changelog dei rilasci firmware) e ritorna i
    passaggi più pertinenti alla domanda, ognuno preceduto dal suo id da citare.
    I passaggi possono non contenere la risposta.

    Args:
        domanda: la domanda da cercare nei documenti.
    """
    chunks = rag.recupera(domanda, K)            # i K chunk più pertinenti: dict con id, testo, score, source
    testo = ""
    for c in chunks:
        testo += f"[{c['id']}]\n{c['testo']}\n\n"
    return testo.strip()


# ------------------------------------------- TODO 1 · query_db come tool · ⌨️
# La funzione vera esiste già: tools.query_db(sql), di Modulo 3 · Lezione 8
# (solo SELECT, sola lettura, errori come testo). Qui va scritto il tool
# nella forma di cerca_documenti: @function_tool, una docstring con lo schema
# del database (le quattro righe di QueryDb in aikit/tools.py: è quello che
# il modello legge per scrivere la query) e la sezione Args, e dentro la
# chiamata a tools.query_db(sql). Poi il tool va nella lista tools=[...]
# dell'agente, qui sotto.
def query_db(sql: str) -> str:
    """TODO 1"""
    raise NotImplementedError("TODO 1")


# ------------------------------------------- le istruzioni e l'agente
# Le ISTRUZIONI sono quelle della lezione scorsa, parola per parola.
ISTRUZIONI = """Sei l'assistente di Lumen, un'azienda che vende scrivanie regolabili LumaDesk e accessori. Rispondi in italiano, in poche frasi.
Per rispondere hai due strade:
- domande su prodotti, procedure, resi, garanzia, smart working, ticket e rilasci firmware: usa cerca_documenti e cita i passaggi che usi con il loro id tra parentesi quadre, per esempio [policy-resi-garanzia-001];
- domande su ordini, clienti e prezzi: usa query_db.
Se una domanda ha bisogno di tutte e due, usa tutti e due i tool.
Rispondi SOLO con quello che i tool ti restituiscono. Se i passaggi trovati non contengono la risposta, o i dati non ce l'hanno, di' che non hai trovato la risposta e dove hai cercato. Se una domanda non riguarda Lumen, di' che non puoi rispondere, senza usare i tool. Se un tool ritorna un errore due volte di fila, fermati e di' che il dato non è disponibile. Non inventare mai."""

# L'Agent tiene insieme le tre cose che il modello vede a ogni chiamata:
# le istruzioni, la lista dei tool e il modello. Non chiama niente: è
# Runner a fare il giro.
agente = Agent(
    name="Assistente Lumen",                     # l'etichetta dell'agente, si vede nella dashboard di tracing
    instructions=ISTRUZIONI,
    tools=[cerca_documenti],                     # TODO 1: qui va anche query_db (l'oggetto tool, cioè la funzione con il decoratore sopra)
    model=MODELLO,
)


# ------------------------------------------- TODO 2 · la strada, dalla traccia · ⌨️
# result.new_items è la traccia del run: un item per ogni cosa successa,
# nell'ordine. Le richieste di tool sono ToolCallItem; dentro, raw_item è la
# function_call dell'API (quella della lezione scorsa: name, arguments,
# call_id), quindi il nome del tool sta in item.raw_item.name. Dai nomi dei tool chiamati alla strada, come
# la lezione scorsa: "documenti" se ha usato cerca_documenti, "dati" se
# query_db, "documenti+dati" se tutti e due, "nessuna" se nessun tool.
def strada(result):
    """Ritorna la strada presa nel run: "documenti", "dati",
    "documenti+dati" o "nessuna", leggendo i ToolCallItem in
    result.new_items."""
    raise NotImplementedError("TODO 2")


# ------------------------------------------------- helper di stampa (dati)
def stampa_traccia(result):
    """La traccia del run, un rigo per item: i tool chiesti (con gli
    argomenti), i loro output (le prime righe: il modello riceve tutto),
    la risposta. In fondo le chiamate al modello, i token e il costo,
    da result.context_wrapper.usage."""
    for item in result.new_items:
        if isinstance(item, ToolCallItem):
            print(f"   tool     {item.raw_item.name}({item.raw_item.arguments})")   # arguments è una stringa JSON, come la lezione scorsa: qui si stampa e basta
        elif isinstance(item, ToolCallOutputItem):
            righe = str(item.output).split("\n")
            print(f"   output   {righe[0]}")
            for riga in righe[1:4]:
                print(f"            {riga}")
            if len(righe) > 4:
                print(f"            … altre {len(righe) - 4} righe")
        elif isinstance(item, MessageOutputItem):
            print("   risposta")
    u = result.context_wrapper.usage             # context_wrapper è il contesto del run; dentro, usage tiene i conti di tutte le chiamate
    costo = cost_usd(MODELLO, u.input_tokens, u.output_tokens)
    print(f"   {u.requests} chiamat{'a' if u.requests == 1 else 'e'} · {u.input_tokens} token in, {u.output_tokens} out · ${costo:.5f}")


def stampa_tabella(esiti):
    """La tabella del giro: una riga per domanda con la strada attesa e
    quella presa. esiti è una lista di (domanda, attesa, presa)."""
    print("\n\n" + "#" * 78)
    print(f"# RIASSUNTO · {MODELLO} · strada attesa / strada presa")
    print("#" * 78)
    print(f"  {'domanda':<46} {'attesa':<15} {'presa':<15} uguale?")
    uguali = 0
    for domanda, attesa, presa in esiti:
        uguali += attesa == presa
        print(f"  {domanda[:46]:<46} {attesa:<15} {presa:<15} {'sì' if attesa == presa else 'NO'}")
    print(f"\n  strada giusta: {uguali}/{len(esiti)}")


if __name__ == "__main__":
    # La collection del modulo: si indicizza solo se manca (la prima volta:
    # 82 chunk, un paio di minuti, meno di un centesimo).
    if vectorstore.apri_collection(rag.CONFIG["collection"]).count() == 0:
        rag.indicizza()

    domande = [(SOLO, None)] if SOLO else DOMANDE
    esiti = []
    for domanda, attesa in domande:
        print("\n" + "=" * 78)
        print(f"D: {domanda}")
        try:
            result = Runner.run_sync(agente, domanda, max_turns=MAX_TURNI)   # il giro: chiama, esegue, rimanda, finché arriva testo (run_sync: la versione per gli script; in un notebook sarebbe await Runner.run())
        except MaxTurnsExceeded as e:                # il giro non ha finito entro il tetto: niente risposta, in tabella un ?
            print(f"   (mi fermo: {MAX_TURNI} turni senza una risposta; {len(e.run_data.new_items)} item eseguiti prima, in e.run_data)")
            esiti.append((domanda, attesa, "?"))
            continue
        stampa_traccia(result)
        print(f"→ {result.final_output}")
        try:
            presa = strada(result)
        except NotImplementedError:
            presa = "(TODO 2)"                   # finché strada() non è scritta, la tabella lo dice
        print(f"   strada: {presa}")
        esiti.append((domanda, attesa, presa))
    if not SOLO:
        stampa_tabella(esiti)
