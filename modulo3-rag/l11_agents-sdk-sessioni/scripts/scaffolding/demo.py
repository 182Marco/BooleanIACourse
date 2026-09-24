"""demo.py — le due dimostrazioni del docente sulle sessioni dell'Agents SDK (Modulo 3 · Lezione 11).

Strumento del docente, si lancia copiando un comando dalle slide. Ogni
dimostrazione fa due scambi del dialogo 1 di Modulo 3 · Lezione 3 (quattro
chiamate al modello, meno di un centesimo). L'agente è lo stesso della
soluzione (i due tool, le stesse ISTRUZIONI), ridefinito qui perché la demo
deve girare anche prima che gli studenti abbiano scritto i TODO.

Uso (dalla cartella scripts/, con la chiave in .env):
    python scaffolding/demo.py senza      # apertura · il follow-up senza sessione: ogni run parte da zero
    python scaffolding/demo.py storia     # teoria · gli stessi due scambi con una sessione, e cosa c'è dentro
"""
import asyncio
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from dotenv import load_dotenv                   # noqa: E402

load_dotenv(SCRIPTS / ".env")

from agents import Agent, Runner, function_tool, SQLiteSession, ToolCallItem   # noqa: E402

from aikit import rag, tools, vectorstore        # noqa: E402
from aikit.llm_client import cost_usd            # noqa: E402

MODELLO = "gpt-5.6-luna"
K = 4
DIALOGO = ["Perché il piano si ferma sempre a metà corsa?", "E per il secondo caso?"]   # il dialogo 1 di Modulo 3 · Lezione 3


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


def scambio(domanda, sessione=None):
    """Un run: la domanda, i tool con i loro argomenti, la risposta, i token."""
    print(f"\nTu> {domanda}")
    result = Runner.run_sync(agente, domanda, session=sessione)
    usati = [item for item in result.new_items if isinstance(item, ToolCallItem)]
    for item in usati:
        print(f"   tool     {item.raw_item.name}({item.raw_item.arguments})")
    if not usati:
        print("   nessun tool")
    u = result.context_wrapper.usage
    print(f"   {u.requests} chiamat{'a' if u.requests == 1 else 'e'} · {u.input_tokens} token in, {u.output_tokens} out · ${cost_usd(MODELLO, u.input_tokens, u.output_tokens):.5f}")
    print(f"→ {result.final_output}")


def demo_senza():
    print("L'assistente della lezione scorsa, senza sessione: ogni run parte da zero.")
    for domanda in DIALOGO:
        scambio(domanda)
    print("\nAl secondo run il modello ha visto le istruzioni, i tool e «E per il secondo caso?». Nient'altro.")


def demo_storia():
    sessione = SQLiteSession("demo")             # senza file: in memoria, sparisce alla fine del programma
    print("Gli stessi due scambi, con una sessione.")
    for domanda in DIALOGO:
        scambio(domanda, sessione)
    # get_items() è async: si esegue sullo stesso event loop di run_sync.
    # asyncio.run() ne aprirebbe un altro, e un run dopo morirebbe.
    items = asyncio.get_event_loop().run_until_complete(sessione.get_items())
    print(f"\nCosa c'è nella sessione: {len(items)} item, nell'ordine in cui sono successi")
    for item in items:
        tipo = item.get("type", "message")
        if tipo == "message" and item.get("role") == "user":
            print(f"   message (user)        {item['content'][:70]}")
        elif tipo == "message":
            testo = item["content"][0].get("text", "") if isinstance(item["content"], list) else str(item["content"])
            print(f"   message (assistant)   {' '.join(testo.split())[:70]}…")
        elif tipo == "function_call":
            print(f"   function_call         {item['name']}({item['arguments'][:60]}…)")
        elif tipo == "function_call_output":
            caratteri = len(str(item["output"]))
            print(f"   function_call_output  {str(item['output']).splitlines()[0][:60]} … ({caratteri} caratteri, circa {round(caratteri / 3.4, -1):.0f} token)")   # 3,4 caratteri per token: misurato su tre output
        else:
            print(f"   {tipo}")
    print("\nAl prossimo run l'SDK mette questi item davanti alla domanda nuova. Anche i passaggi dei documenti.")


if __name__ == "__main__":
    demo = sys.argv[1] if len(sys.argv) > 1 else ""
    demos = {"senza": demo_senza, "storia": demo_storia}
    if demo not in demos:
        raise SystemExit("uso: python scaffolding/demo.py senza | storia")
    if vectorstore.apri_collection(rag.CONFIG["collection"]).count() == 0:
        rag.indicizza()
    demos[demo]()
