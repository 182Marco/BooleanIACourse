# Modulo 3 · Lezione 10 — OpenAI Agents SDK: il loop gestito · consegna

Si lavora in `working/assistente_sdk.py`: è l'assistente della lezione
scorsa con il giro fatto dall'SDK. Dentro, nell'ordine: le costanti
(`MODELLO`, `K`, `MAX_TURNI`), le `DOMANDE` con la strada attesa, `SOLO`;
`cerca_documenti` già scritto come tool; **TODO 1**; le `ISTRUZIONI` della
lezione scorsa e l'`Agent`; **TODO 2**; `stampa_traccia()`,
`stampa_tabella()` e il main, che chiama `Runner.run_sync()` e in fondo
stampa la tabella **strada attesa / strada presa**.

## Setup (5')

Dalla cartella `scripts/` di questa lezione (una libreria nuova,
`openai-agents`; le altre sono quelle della lezione scorsa):

```bash
cd scripts            # dalla cartella della lezione; se sei già in scripts/, salta questa riga
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Se hai ancora il venv della lezione scorsa puoi riusarlo: `source
../../lezione-09-lab-rag-tools/scripts/.venv/bin/activate` e poi solo `pip
install openai-agents==0.22.3`.

Poi la chiave: copia il file `.env` dalla cartella `scripts/` della
lezione scorsa dentro questa cartella `scripts/` (se le cartelle sono
quelle del repo: `cp ../../lezione-09-lab-rag-tools/scripts/.env .env`).
Se non ce l'hai più: `cp .env.example .env`, alza la mano, e incolla
dentro la chiave che ti dà il docente (a voce o nella chat della classe). Se hai anche la cartella `chroma/`
della lezione scorsa, copiala dentro questa `scripts/` con `cp -r
<quella cartella>/chroma .` (diventa `scripts/chroma/`): risparmi
l'indicizzazione. Il `.env` copiato non ha la
riga `OPENAI_AGENTS_DISABLE_TRACING=1` di cui si parla in aula: se vorrai
spegnere il tracing, la aggiungi a mano (è in `.env.example`).

Si lancia tutto dalla cartella `scripts/`: `python working/assistente_sdk.py`.
Il primo lancio si fa dopo le demo, quando lo fa il docente. Al primo avvio, se `chroma/` manca, indicizza la collection (un paio di
minuti, meno di un centesimo). Quel primo lancio ha un tool solo,
`cerca_documenti`: la domanda sui resi risponde con la citazione, Giulia
Moretti dice che «lo strumento necessario non è disponibile», Lorenzo
Rossi cerca due volte nei documenti e dice che gli ordini non li trova,
Padova è un rifiuto senza tool come sempre, e la tabella dice `(TODO 2)`
su ogni riga. È la baseline, non è rotto. Un lancio
completo costa meno di un centesimo: rilancia quante volte vuoi.

## Cosa stampa il main

Per ogni domanda la **traccia del run**, poi la risposta e la strada:

```
==========================================================================
D: Quanti ordini ha fatto Giulia Moretti?
   tool     query_db({"sql":"SELECT COUNT(*) … WHERE c.nome = 'Giulia Moretti'"})
   output   numero_ordini
            13
   risposta
   2 chiamate · 1179 token in, 66 out · $0.00031
→ Giulia Moretti ha effettuato 13 ordini.
   strada: dati
```

Le righe `tool` / `output` / `risposta` sono gli item di
`result.new_items`, nell'ordine in cui sono successi. La riga dei token
viene da `result.context_wrapper.usage`.

## TODO 1 — query_db come tool (20')

La funzione vera esiste già: `tools.query_db(sql)`, quella di Modulo 3 ·
Lezione 8 (solo `SELECT`, sola lettura, errori come testo), importata in
cima con `from aikit import tools`. Manca il **tool**: va scritto nella
stessa forma di `cerca_documenti`, che è appena sopra:

1. `@function_tool` sopra la funzione `query_db(sql: str) -> str`.
2. La **docstring**: è la descrizione che il modello legge per decidere se
   usarlo e per scrivere la query. Copia **tutta** la docstring di `QueryDb` in `scaffolding/aikit/tools.py`
   (è il file della lezione scorsa promosso nel toolkit: le sue prime
   righe parlano di quella lezione, a te servono solo quelle della
   docstring): la frase iniziale («Esegue una query
   SQL (solo SELECT, dialetto SQLite)…») e le quattro righe dello schema
   `prodotti(...)`, `clienti(...)`, `ordini(...)`, `righe_ordine(...)`. Poi
   aggiungi la sezione `Args:` con `sql`, come in `cerca_documenti`.
3. Dentro, `return tools.query_db(sql)`.
4. Il tool nella lista dell'agente: `tools=[cerca_documenti, query_db]`.

Dalla firma (`sql: str`) e dalla docstring l'SDK costruisce nome,
descrizione e parametri del tool: gli stessi tre pezzi che la lezione
scorsa faceva `definisci_tool(QueryDb, "query_db")`. Dopo il decoratore
`query_db` non è più una funzione che puoi chiamare tu (`query_db("SELECT
1")` dà `TypeError: 'FunctionTool' object is not callable`): la chiama
`Runner` dentro il giro. Per provare la funzione vera a mano c'è
`tools.query_db("SELECT 1")`.

**Fatto quando:** `SOLO = "Quanti ordini ha fatto Giulia Moretti?"`
risponde 13, e nella traccia c'è `tool     query_db({"sql": …})`.

## TODO 2 — la strada, dalla traccia (15')

`strada(result)` deve ritornare `"documenti"`, `"dati"`,
`"documenti+dati"` o `"nessuna"`, come la lezione scorsa. Allora i tool usati li raccoglieva il ciclo in una lista; oggi sono nella
traccia: `result.new_items` è una lista di item, e le richieste di tool
sono quelli di tipo `ToolCallItem` (già importato in cima). Dentro,
`item.raw_item` è la `function_call` dell'API, la stessa che la lezione
scorsa leggevi a mano: il nome del tool è `item.raw_item.name`. Da lì la stessa logica di `strada(usati)` della
lezione scorsa.

**Fatto quando:** con `SOLO = None` la tabella in fondo dice `4/4`, e
sotto ogni risposta la riga `strada:` coincide con i tool nella traccia
(nessun tool → `nessuna`). Nelle nostre misure (quattro domande per tre giri) è 12 su 12: se una
riga dice NO, rilanciala in `SOLO` due volte prima di cercare l'errore nel
tuo codice.

## Se qualcosa non torna

| Cosa vedi | Cosa controllare |
|---|---|
| Giulia Moretti: «lo strumento necessario non è disponibile», nessun `tool` nella traccia | `query_db` non è nella lista `tools=[...]` dell'agente (TODO 1, punto 4) |
| al primo run, subito dopo la prima riga `D:`, `'function' object has no attribute 'name'` | `query_db` è nella lista `tools=[...]` ma non ha `@function_tool` sopra |
| `output   An error occurred while running the tool. … Error: TODO 1` | il tool è cablato, ma dentro c'è ancora `raise NotImplementedError`: l'SDK ha rimandato l'errore al modello come testo |
| il modello scrive query con colonne che non esistono (`no such column`) | la docstring di `query_db` non ha lo schema del database, o l'ha sbagliato: il modello lo legge da lì |
| `TypeError: 'FunctionTool' object is not callable` | hai chiamato `query_db(...)` o `cerca_documenti(...)` come funzione: dopo il decoratore sono tool, li chiama `Runner`; la funzione vera è `tools.query_db(...)` |
| `strada: (TODO 2)` su ogni riga | `strada()` non è ancora scritta |
| `AttributeError: … has no attribute 'name'` in `strada()` | stai leggendo `.name` su tutti gli item: solo i `ToolCallItem` ce l'hanno (`isinstance(item, ToolCallItem)`), gli output e la risposta no |
| `strada: nessuna` con un `tool` nella traccia | `strada()` guarda i nomi sbagliati: sono `cerca_documenti` e `query_db`, come le funzioni |
| `(mi fermo: 10 turni senza una risposta)` | il modello ha chiesto tool per dieci turni di fila: guarda la traccia, di solito lo stesso tool con lo stesso errore |
| `OPENAI_API_KEY` non impostata, subito all'avvio | hai lanciato da un'altra cartella: `cd scripts`, poi `python working/assistente_sdk.py` |
| la prima domanda ci mette due minuti | sta indicizzando `lumen_m3`: è normale, la seconda volta parte subito |

## Se finisci prima

- Prendi una domanda della tua lista `LE_MIE_QUERY` (in `working/debug.py`
  di Modulo 3 · Lezione 6: quelle che il RAG da solo sbagliava) e mettila
  in `SOLO`: nella traccia vedi se il
  modello cerca una volta o due, e con quali parole.
- Stampa lo schema che l'SDK ha costruito dal tuo `query_db`:
  `print(query_db.description)` e `print(query_db.params_json_schema)`
  subito sotto la definizione di `query_db` (così lo vedi senza aspettare
  le domande). Confrontalo con la docstring che hai scritto: è tutto
  quello che il modello vede del tool.
- Un terzo tool: `prezzo_prodotto(codice)` esiste già in
  `scaffolding/aikit/tools.py` (lo hai scritto tu a Modulo 3 · Lezione 8).
  Incartalo con `@function_tool` nella stessa forma di `query_db`, mettilo
  in `tools=[...]` e chiedi «Quanto costa la LMX-4400?»: nella traccia vedi
  se il modello preferisce il tool con la query fissa o `query_db`.
