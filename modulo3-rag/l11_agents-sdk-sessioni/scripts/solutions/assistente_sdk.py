"""assistente_sdk.py — l'assistente della lezione scorsa, con una sessione: regge i follow-up e riprende la conversazione.

La lezione scorsa ogni run partiva da zero: il modello vedeva le istruzioni,
i tool e la domanda, nient'altro. A un follow-up («E per il secondo caso?»)
non sapeva di cosa si parlava. Stasera una SESSIONE dell'SDK salva gli item
di ogni run (la domanda, le function_call, i loro output, la risposta) e li
ripassa al modello al run dopo: è la storia di Modulo 3 · Lezione 3, tenuta
dall'SDK.

La corrispondenza con chat.py di Modulo 3 · Lezione 3:

  Modulo 3 · Lezione 3                     stasera
  storia (la lista dei messaggi)        →  la sessione: SQLiteSession(nome)
  salva_sessione / carica_sessione      →  SQLiteSession(nome, file): con lo stesso nome riprende
  tronca(storia), il buffer             →  SessionSettings(limit=...): gli ultimi N item
  condensa(storia, domanda)             →  l'argomento di cerca_documenti, lo scrive il modello con la storia davanti

Il file, dall'alto in basso:

  costanti             MODELLO, K, MAX_TURNI; SESSIONI (il file delle
                       sessioni), LIMITE (quanti item della storia vede il
                       modello)
  cerca_documenti      il RAG come tool
  query_db             il database come tool
  ISTRUZIONI + agente  le istruzioni e l'Agent con i due tool
  strada(result)       dalla traccia del run alla strada presa
  TODO 1               apri_sessione(): la sessione su file, con un nome
  TODO 2               in apri_sessione(): il tetto alla storia, LIMITE
  già scritto          stampa_traccia(), il main: la chat da terminale

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
from agents import SQLiteSession, SessionSettings   # noqa: E402 — la sessione, e le sue impostazioni (il tetto alla storia)

from aikit import rag                            # noqa: E402 — Modulo 3 · Lezione 2: recupera()
from aikit import tools                          # noqa: E402 — Modulo 3 · Lezione 8: query_db(sql), la funzione vera
from aikit import vectorstore                    # noqa: E402 — Modulo 2 · Lezione 9: la collection
from aikit.llm_client import cost_usd            # noqa: E402 — Modulo 2 · Lezione 3

MODELLO = "gpt-5.6-luna"                         # lo stesso della lezione scorsa; è in PRICING di llm_client
K = 4                                            # quanti chunk cerca_documenti rimanda al modello
MAX_TURNI = 10                                   # il tetto al giro: un turno è una chiamata al modello (era MAX_CHIAMATE)
SESSIONI = SCRIPTS / "sessioni.db"               # il file SQLite dove la sessione salva la storia (TODO 1): costruito da SCRIPTS, vale da qualunque cartella si lanci
LIMITE = None                                    # quanti item della storia si ripassano al modello: None = tutti (TODO 2)


# ------------------------------------------- il RAG come tool
# @function_tool trasforma la funzione in un tool: il nome è quello della
# funzione, la descrizione è la docstring, i parametri escono dalla firma
# (domanda: str) e dalla sezione Args. Dopo il decoratore cerca_documenti non
# è più una funzione da chiamare: è un oggetto tool, e lo chiama Runner
# dentro il giro. L'argomento domanda lo scrive il modello: con una sessione,
# lo scrive con la storia davanti.
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


# ------------------------------------------- il database come tool
# La funzione vera è tools.query_db(sql), di Modulo 3 · Lezione 8 (solo
# SELECT, sola lettura, errori come testo). La docstring porta lo schema del
# database: è quello che il modello legge per scrivere la query.
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
# Runner a fare il giro. La storia non sta qui: sta nella sessione.
agente = Agent(
    name="Assistente Lumen",                     # l'etichetta dell'agente, si vede nella dashboard di tracing
    instructions=ISTRUZIONI,
    tools=[cerca_documenti, query_db],           # i due tool: nella lista vanno gli oggetti tool, non le funzioni
    model=MODELLO,
)


# ------------------------------------------- la strada, dalla traccia
# result.new_items è la traccia del run: un item per ogni cosa successa,
# nell'ordine. Le richieste di tool sono ToolCallItem; il nome del tool sta
# in item.raw_item.name. In una chat dice se un follow-up ha cercato, e dove.
def strada(result):
    """Ritorna la strada presa nel run: "documenti", "dati",
    "documenti+dati" o "nessuna", leggendo i ToolCallItem in
    result.new_items."""
    usati = [item.raw_item.name for item in result.new_items if isinstance(item, ToolCallItem)]
    documenti = "cerca_documenti" in usati
    dati = "query_db" in usati
    if documenti and dati:
        return "documenti+dati"
    if documenti:
        return "documenti"
    if dati:
        return "dati"
    return "nessuna"


# ------------------------------------------- TODO 1 e TODO 2 · la sessione · ⌨️
# Una SQLiteSession ha un nome (session_id) e un file. Senza file la storia
# sta in memoria e si perde quando il programma si chiude; con un file, lo
# stesso nome ritrova la stessa conversazione anche dopo un riavvio.
# TODO 1: chiedere il nome con input() e aprire la sessione su SESSIONI.
# TODO 2: il tetto alla storia, con SessionSettings(limit=LIMITE): il modello
# vede solo gli ultimi LIMITE item (None = tutti). È il buffer di Modulo 3 ·
# Lezione 3, contato in item invece che in token.
def apri_sessione():
    """Chiede il nome della sessione e ritorna una SQLiteSession con quel
    nome, salvata nel file SESSIONI, che ripassa al modello solo gli ultimi
    LIMITE item della storia."""
    nome = input("Nome della sessione: ").strip()     # strip(): uno spazio in più sarebbe un nome diverso, cioè una conversazione nuova
    return SQLiteSession(nome, SESSIONI, session_settings=SessionSettings(limit=LIMITE))


# ------------------------------------------------- helper di stampa (già scritti)
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
    u = result.context_wrapper.usage             # context_wrapper è il contesto del run; dentro, usage tiene i conti di tutte le chiamate (con una sessione, i token in input contano anche la storia, riletta a ogni turno)
    costo = cost_usd(MODELLO, u.input_tokens, u.output_tokens)
    print(f"   {u.requests} chiamat{'a' if u.requests == 1 else 'e'} · {u.input_tokens} token in, {u.output_tokens} out · ${costo:.5f}")


if __name__ == "__main__":
    # La collection del modulo: si indicizza solo se manca (la prima volta:
    # 82 chunk, un paio di minuti, meno di un centesimo).
    if vectorstore.apri_collection(rag.CONFIG["collection"]).count() == 0:
        rag.indicizza()

    try:
        sessione = apri_sessione()
    except NotImplementedError:                  # finché il TODO 1 non è scritto: una sessione in memoria, che si perde alla chiusura
        sessione = SQLiteSession("aula")
    print(f"Sessione «{sessione.session_id}». Scrivi una domanda; invio a vuoto per uscire.")

    while True:
        domanda = input("\nTu> ").strip()
        if not domanda:
            break
        try:
            result = Runner.run_sync(agente, domanda, session=sessione, max_turns=MAX_TURNI)   # con session=: prima del run l'SDK ci mette davanti la storia, dopo il run ci salva gli item nuovi
        except MaxTurnsExceeded as e:            # il giro non ha finito entro il tetto: niente risposta, si passa alla domanda dopo
            print(f"   (mi fermo: {MAX_TURNI} turni senza una risposta; {len(e.run_data.new_items)} item eseguiti prima, in e.run_data)")
            continue
        stampa_traccia(result)
        print(f"→ {result.final_output}")
        print(f"   strada: {strada(result)}")
