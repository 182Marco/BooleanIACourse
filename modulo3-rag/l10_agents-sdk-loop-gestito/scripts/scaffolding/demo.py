"""demo.py — le cinque dimostrazioni del docente sull'OpenAI Agents SDK (Modulo 3 · Lezione 10).

Strumento del docente, si lancia copiando un comando dalle slide. Ogni
dimostrazione è a sé e costa una o due chiamate al modello. L'agente è lo
stesso della soluzione (i due tool di Modulo 3 · Lezione 9, le stesse
ISTRUZIONI), ridefinito qui perché la demo deve girare anche prima che gli
studenti abbiano scritto i TODO.

Uso (dalla cartella scripts/, con la chiave in .env):
    python scaffolding/demo.py schema     # 1 · lo schema che l'SDK ricava da firma e docstring, accanto a quello Pydantic
    python scaffolding/demo.py traccia    # 2 · la traccia di un run a due tool: gli item, le chiamate, i token
    python scaffolding/demo.py tetto      # 3 · max_turns=1: il giro non può finire, e l'eccezione che esce
    python scaffolding/demo.py tetto 2    #     (se lo chiedono: con 2 turni le quattro domande passano)
    python scaffolding/demo.py rotto      # 4 · un tool che solleva un'eccezione: cosa fa l'SDK di default, e senza rete
    python scaffolding/demo.py tracing    # 5 · l'id della traccia mandata alla dashboard, e come si spegne
"""
import json
import os
import sqlite3
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from dotenv import load_dotenv                   # noqa: E402

load_dotenv(SCRIPTS / ".env")

from agents import Agent, Runner, function_tool, MaxTurnsExceeded, ToolCallItem, ToolCallOutputItem, MessageOutputItem   # noqa: E402
from agents.tracing import trace                 # noqa: E402

from aikit import rag, tools, vectorstore        # noqa: E402
from aikit.llm_client import cost_usd            # noqa: E402

MODELLO = "gpt-5.6-luna"
K = 4
DOMANDA_DOPPIA = "Lorenzo Rossi può montare il braccio LMX-4400 sulle scrivanie che ha ordinato?"
DOMANDA_DATI = "Quanti ordini ha fatto Giulia Moretti?"
DOMANDA_PREZZO = "Quanto costa la LMX-4400?"
DOMANDE = [                                      # le quattro della lezione scorsa, per «tetto 2»
    "Entro quanti giorni posso restituire un prodotto comprato online?",
    DOMANDA_DATI,
    DOMANDA_DOPPIA,
    "Che tempo fa oggi a Padova?",
]


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
    chunks = rag.recupera(domanda, K)
    return "\n\n".join(f"[{c['id']}]\n{c['testo']}" for c in chunks)


@function_tool
def query_db(sql: str) -> str:
    """Esegue una query SQL (solo SELECT, dialetto SQLite) sul database degli
    ordini Lumen e ritorna le righe trovate. Tabelle e colonne:
    prodotti(codice TEXT, nome TEXT, categoria TEXT, prezzo REAL)
    clienti(id INTEGER, nome TEXT, tipo TEXT, citta TEXT, data_registrazione TEXT)
    ordini(id INTEGER, cliente_id INTEGER, data TEXT, stato TEXT, data_consegna TEXT, spese_spedizione REAL)
    righe_ordine(id INTEGER, ordine_id INTEGER, codice_prodotto TEXT, quantita INTEGER, prezzo_unitario REAL)

    Args:
        sql: la query SELECT da eseguire.
    """
    return tools.query_db(sql)


ISTRUZIONI = """Sei l'assistente di Lumen, un'azienda che vende scrivanie regolabili LumaDesk e accessori. Rispondi in italiano, in poche frasi.
Per rispondere hai due strade:
- domande su prodotti, procedure, resi, garanzia, smart working, ticket e rilasci firmware: usa cerca_documenti e cita i passaggi che usi con il loro id tra parentesi quadre, per esempio [policy-resi-garanzia-001];
- domande su ordini, clienti e prezzi: usa query_db.
Se una domanda ha bisogno di tutte e due, usa tutti e due i tool.
Rispondi SOLO con quello che i tool ti restituiscono. Se i passaggi trovati non contengono la risposta, o i dati non ce l'hanno, di' che non hai trovato la risposta e dove hai cercato. Se una domanda non riguarda Lumen, di' che non puoi rispondere, senza usare i tool. Se un tool ritorna un errore due volte di fila, fermati e di' che il dato non è disponibile. Non inventare mai."""

agente = Agent(name="Assistente Lumen", instructions=ISTRUZIONI, tools=[cerca_documenti, query_db], model=MODELLO)


def stampa_traccia(result):
    """Come in assistente_sdk.py, con in più il tipo di ogni item."""
    for item in result.new_items:
        if isinstance(item, ToolCallItem):
            print(f"   ToolCallItem        {item.raw_item.name}({item.raw_item.arguments})   call_id {item.raw_item.call_id}")
        elif isinstance(item, ToolCallOutputItem):
            prima = str(item.output).split("\n")[0]
            print(f"   ToolCallOutputItem  {prima[:90]}")
        elif isinstance(item, MessageOutputItem):
            print("   MessageOutputItem   la risposta")
        else:
            print(f"   {type(item).__name__}")
    u = result.context_wrapper.usage
    print(f"   {u.requests} chiamate al modello · {u.input_tokens} token in, {u.output_tokens} out · ${cost_usd(MODELLO, u.input_tokens, u.output_tokens):.5f}")


def demo_schema():
    print("La lezione scorsa: definisci_tool(QueryDb, \"query_db\") dalla classe Pydantic\n")
    print(json.dumps(tools.definisci_tool(tools.QueryDb, "query_db"), indent=2, ensure_ascii=False))
    print("\n\nStasera: @function_tool sopra query_db(sql), da firma e docstring\n")
    print(json.dumps({"name": query_db.name, "description": query_db.description, "parameters": query_db.params_json_schema}, indent=2, ensure_ascii=False))
    print("\nStessi tre pezzi: nome, descrizione, parametri. È tutto ciò che il modello vede del tool.")


def demo_traccia():
    print(f"D: {DOMANDA_DOPPIA}\n")
    result = Runner.run_sync(agente, DOMANDA_DOPPIA)
    print("result.new_items, nell'ordine:")
    stampa_traccia(result)
    print(f"\nresult.final_output:\n→ {result.final_output}")
    print(f"\nresult.raw_responses: {len(result.raw_responses)} risposte del modello, una per turno")
    for n, r in enumerate(result.raw_responses, start=1):
        print(f"   turno {n}: output {[o.type for o in r.output]} · {r.usage.input_tokens} token in, {r.usage.output_tokens} out")


def demo_tetto(turni=1):
    """Con 1 (il default della demo) il giro non può finire. Se qualcuno chiede
    «e con 2?»: python scaffolding/demo.py tetto 2 passa le quattro DOMANDE."""
    domande = [DOMANDA_DATI] if turni == 1 else DOMANDE
    if turni == 1:
        print("Un turno è una chiamata al modello. Con 1 turno può solo rispondere; se chiede un tool, il giro non può finire.\n")
    for domanda in domande:
        print(f"D: {domanda}   con max_turns={turni}")
        try:
            result = Runner.run_sync(agente, domanda, max_turns=turni)
            print(f"→ {result.final_output}   ({result.context_wrapper.usage.requests} chiamate)\n")
        except MaxTurnsExceeded as e:
            print(f"MaxTurnsExceeded: {e}")
            print("cosa era successo prima di fermarsi (e.run_data.new_items):")
            for item in e.run_data.new_items:
                print(f"   {type(item).__name__}")
            print()
    print("Senza max_turns il tetto è 10. Il while senza limite della lezione scorsa qui ha un numero, e un'eccezione quando lo supera.")


def _query_nuda(sql):
    """query_db SENZA il try/except di Modulo 3 · Lezione 8: un errore SQL solleva un'eccezione."""
    con = sqlite3.connect(tools.DB.as_uri() + "?mode=ro", uri=True)
    cursore = con.execute(sql)
    colonne = [c[0] for c in cursore.description]
    righe = cursore.fetchmany(51)
    con.close()
    return " | ".join(colonne) + "".join("\n" + " | ".join(str(v) for v in riga) for riga in righe[:50])


# Lo schema nella docstring è VECCHIO di proposito (prezzo_listino invece di
# prezzo): il modello scrive una query che SQLite rifiuta, e l'eccezione
# arriva all'SDK.
@function_tool
def query_db_rotto(sql: str) -> str:
    """Esegue una query SQL (solo SELECT, dialetto SQLite) sul database degli
    ordini Lumen e ritorna le righe trovate. Tabelle e colonne:
    prodotti(codice TEXT, nome TEXT, categoria TEXT, prezzo_listino REAL)

    Args:
        sql: la query SELECT da eseguire.
    """
    return _query_nuda(sql)


@function_tool(failure_error_function=None)      # None: l'eccezione NON torna al modello, esce dal run
def query_db_rotto_senza_rete(sql: str) -> str:
    """Esegue una query SQL (solo SELECT, dialetto SQLite) sul database degli
    ordini Lumen e ritorna le righe trovate. Tabelle e colonne:
    prodotti(codice TEXT, nome TEXT, categoria TEXT, prezzo_listino REAL)

    Args:
        sql: la query SELECT da eseguire.
    """
    return _query_nuda(sql)


def demo_rotto():
    print(f"D: {DOMANDA_PREZZO}   con un query_db senza try/except e uno schema vecchio nella descrizione (prezzo_listino)\n")
    print("1 · di default: l'eccezione del tool torna al modello come testo\n")
    ag = Agent(name="Assistente Lumen", instructions=ISTRUZIONI, tools=[query_db_rotto], model=MODELLO)
    result = Runner.run_sync(ag, DOMANDA_PREZZO)
    stampa_traccia(result)
    print(f"→ {result.final_output}")
    print("\n   (la lezione scorsa lo facevamo noi: except Exception as e: return f\"Errore: {e}\")")
    print("   (se ha risposto «non disponibile» è per le ISTRUZIONI: «se un tool ritorna un errore due volte di fila, fermati»)")
    print("\n2 · con failure_error_function=None: l'eccezione esce dal run e il programma muore\n")
    ag = Agent(name="Assistente Lumen", instructions=ISTRUZIONI, tools=[query_db_rotto_senza_rete], model=MODELLO)
    try:
        result = Runner.run_sync(ag, DOMANDA_PREZZO)
        print(f"→ {result.final_output}")
    except Exception as e:                       # solo per stampare pulito: senza questo try il programma muore qui, con il traceback
        print(f"   {type(e).__name__}: {e}")
        print("   (senza try/except intorno a Runner.run_sync il programma muore qui)")


def demo_tracing():
    with trace("Modulo 3 · Lezione 10 · demo") as t:
        result = Runner.run_sync(agente, DOMANDA_DATI)
    print(f"→ {result.final_output}")
    if t.trace_id == "no-op":
        print("\ntracing spento: OPENAI_AGENTS_DISABLE_TRACING=1 nel .env (o nell'ambiente). Niente è partito verso la dashboard.")
    else:
        print(f"\ntrace_id: {t.trace_id}")
        print(f"la traccia è qui: https://platform.openai.com/traces/trace?trace_id={t.trace_id}")
        print("dentro: l'agente, ogni chiamata al modello (input e output completi), ogni tool con argomenti e risultato, i tempi.")
        print("per spegnerlo: OPENAI_AGENTS_DISABLE_TRACING=1 nel .env")


if __name__ == "__main__":
    demo = sys.argv[1] if len(sys.argv) > 1 else ""
    demos = {"schema": demo_schema, "traccia": demo_traccia, "tetto": demo_tetto, "rotto": demo_rotto, "tracing": demo_tracing}
    if demo not in demos:
        raise SystemExit("uso: python scaffolding/demo.py schema | traccia | tetto | rotto | tracing")
    if demo != "schema" and vectorstore.apri_collection(rag.CONFIG["collection"]).count() == 0:
        rag.indicizza()
    if demo == "tetto" and len(sys.argv) > 2:
        demo_tetto(int(sys.argv[2]))
    else:
        demos[demo]()
