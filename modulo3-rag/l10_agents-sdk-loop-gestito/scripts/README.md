# Modulo 3 · Lezione 10 — OpenAI Agents SDK: il loop gestito · guida agli script

Lezione da 2 ore (📊 teoria con cinque dimostrazioni dal vivo + 🎤 codice
spiegato + ⌨️ esercizio): l'assistente di Modulo 3 · Lezione 9, con gli
stessi due tool e le stesse istruzioni, ma il giro del tool calling lo fa
l'**OpenAI Agents SDK** (`openai-agents`). Il file della serata è
`working/assistente_sdk.py`: `cerca_documenti` è già un tool dell'SDK,
l'`Agent` e `Runner.run_sync()` sono già scritti; gli studenti scrivono
`query_db` come tool (TODO 1) e `strada()` dalla traccia del run (TODO 2).
Le cinque dimostrazioni del docente si lanciano da `scaffolding/demo.py`.

> **Per gli studenti:** servono la sezione **Setup** e le prime due righe
> di **Come si prova**. Il resto, da «Prima di entrare in aula» in poi, è
> per il docente.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 codice di riferimento che il
docente spiega · ⌨️ da completare dagli studenti · 📄 documenti/dati di
esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Le dipendenze di Modulo 3 · Lezione 9 più `openai-agents==0.22.3` (versione fissata: l'SDK cambia spesso). |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` (la stessa del Modulo 2) e la riga commentata `OPENAI_AGENTS_DISABLE_TRACING=1` per spegnere il tracing. |
| `CONSEGNA.md` | ⌨️ | Il setup, cosa stampa il main, i TODO 1-2 con i criteri di «fatto» e gli errori tipici, cosa fare se si finisce prima. |
| `scaffolding/aikit/` | 🧰 | Il toolkit, identico a Modulo 3 · Lezione 9. Di `tools.py` stasera si usa `tools.query_db(sql)`, la funzione vera (e `QueryDb`, `definisci_tool` nella Demo 1 per il confronto). `rag.recupera()`, `rag.CONFIG`, `rag.indicizza()`, `vectorstore.apri_collection()`, `cost_usd()` come sempre. Non si tocca. |
| `scaffolding/demo.py` | 🎤 | **Le cinque dimostrazioni del docente**, una per comando: `schema`, `traccia`, `tetto`, `rotto`, `tracing` (`tetto 2` se chiedono «e con due turni?»). Ha un agente suo, identico alla soluzione, tranne nella Demo 4 dove il tool è uno solo, quello rotto: gira anche prima dei TODO. |
| `scaffolding/check_lab10.py` | 🧰 | **Strumento del docente**: base istantaneo senza rete (struttura, scaffolding intatto, versione fissata; TODO 1: `query_db` è un `FunctionTool` con nome, schema del database nella descrizione, parametro `sql`, eseguito risponde 300, è nei `tools` dell'agente; TODO 2: `strada()` su un run finto); `--solutions`; `--live` con la chiave (le quattro `DOMANDE` prendono la strada attesa). Spegne il tracing da solo. Non compare nel percorso studente. |
| `scaffolding/make_dataset.py`, `make_db.py` | 🧰 | I generatori del corpus e del database (seed fisso). Servono al check; non si lanciano in aula. |
| `scaffolding/sql.py` | 🧰 | Una query a mano in sola lettura; senza argomenti stampa lo schema. |
| `working/assistente_sdk.py` | ⌨️ | **Il file della serata**: `MODELLO` (`gpt-5.6-luna`), `K`, `MAX_TURNI`, `DOMANDE` con la strada attesa, `SOLO`; `cerca_documenti` con `@function_tool` (già scritto); TODO 1 (`query_db`); `ISTRUZIONI` e `agente = Agent(...)`; TODO 2 (`strada(result)`); `stampa_traccia()`, `stampa_tabella()`, il main con `Runner.run_sync(agente, domanda, max_turns=MAX_TURNI)`. Si continua a Modulo 3 · Lezione 11. |
| `solutions/assistente_sdk.py` | 🧰 | La versione completa, stesso nome: differisce solo nei TODO 1-2. |
| `dataset/lumen_m3/` | 📄 | I sei documenti Lumen (82 chunk), identici a Modulo 3 · Lezione 2. |
| `dataset/lumen.db` | 📄 | Il database degli ordini Lumen, lo stesso di Modulo 3 · Lezione 8. |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../../lezione-09-lab-rag-tools/scripts/.env .env   # la chiave della lezione scorsa (oppure: cp .env.example .env e incollala dentro)
cp -r ../../lezione-09-lab-rag-tools/scripts/chroma .  # facoltativo: la collection già indicizzata
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env`, `.venv` e `chroma/` (git non li versiona). La chiave
> OpenAI è quella del corso. Chi non copia `chroma/` la ricostruisce al
> primo lancio (82 chunk, un paio di minuti, meno di un centesimo). Il
> database arriva già pronto.

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/assistente_sdk.py                          # il file della serata: le DOMANDE, o la domanda in SOLO

python scaffolding/demo.py schema                         # le demo del docente (1-5), una per volta
python scaffolding/demo.py traccia
python scaffolding/demo.py tetto
python scaffolding/demo.py tetto 2                        # se lo chiedono: con 2 turni le quattro domande passano
python scaffolding/demo.py rotto
python scaffolding/demo.py tracing

# solo docente, non fa parte del percorso studente
python scaffolding/check_lab10.py                         # istantaneo, zero costi
python scaffolding/check_lab10.py --file working/assistente_sdk_studente.py   # il file di uno studente, copiato in working/
python scaffolding/check_lab10.py --solutions             # regressione sulla versione completa
python scaffolding/check_lab10.py --solutions --live      # chiamate vere (~30 secondi, meno di un centesimo)
```

Un lancio del main sono quattro domande, 1-2 chiamate a `gpt-5.6-luna`
l'una più un embedding per ogni `cerca_documenti`: un quinto di centesimo,
3-4 secondi a domanda. Sul `working/` intonso il check dà **2 FAIL per
costruzione** (i due TODO): è la baseline.

## Cosa si vede a schermo

Per ogni domanda la traccia del run (gli item di `result.new_items`
nell'ordine: `tool` con gli argomenti, `output` con le prime righe,
`risposta`), la riga delle chiamate e dei token da
`result.context_wrapper.usage`, la risposta, la strada; in fondo la
tabella attesa/presa. Con la soluzione:

```
D: Lorenzo Rossi può montare il braccio LMX-4400 sulle scrivanie che ha ordinato?
   tool     query_db({"sql":"SELECT o.id AS ordine_id, … WHERE c.nome = 'Lorenzo Rossi'"})
   tool     cerca_documenti({"domanda":"Compatibilità del braccio LMX-4400 con le scrivanie LumaDesk …"})
   output   ordine_id | data | stato | codice_prodotto | quantita | nome | categoria
            1039 | 2026-02-11 | consegnato | LD-210 | 1 | LumaDesk piano 140x80 cm, doppio motore | scrivanie
            … altre 15 righe
   output   [manuale-lumadesk-000]
            … altre 11 righe
   risposta
   2 chiamate · 2573 token in, 215 out · $0.00077
→ Sì. Lorenzo Rossi ha ordinato scrivanie LD-200, LD-210 e LD-210W: il braccio LMX-4400 è compatibile con tutti i piani LD tranne LD-115 [listino-catalogo-004].
   strada: documenti+dati
```

I due tool nello stesso turno: il modello li chiede insieme, l'SDK li
esegue tutti e due e rimanda i due output in una chiamata sola. (È un
altro giro rispetto a quello in slide: i numeri cambiano a ogni run.)

## Prima di entrare in aula (docente, cinque righe)

1. Venv fatto, `.env` copiato, `chroma/` già indicizzata (è gitignored: su
   un clone fresco manca, e la Demo 2 resterebbe muta due minuti): un
   lancio di `python scaffolding/demo.py traccia` la sera prima sistema
   tutto.
2. Il file da proiettare nell'apertura e nel codice spiegato è la versione
   **finita** di Modulo 3 · Lezione 9:
   `../../lezione-09-lab-rag-tools/scripts/solutions/assistente.py` (263
   righe). Le 71 righe del giro sono `TOOLS` + `esegui()` (100-120) e
   `chiedi()` (133-182). Il `working/` di quella lezione è lo stub con i
   TODO: non torna né il conteggio né le `ISTRUZIONI`.
3. Login su `platform.openai.com/traces` con l'account della chiave del
   corso (chi la gestisce nel team ha anche l'accesso alla dashboard):
   serve alla Demo 5. Se il login non passa, la Demo 5 si riduce al
   `trace_id` stampato e alla riga del `.env`.
4. I numeri nelle slide 10 e 21 (token, citazioni, «2 chiamate, non 3»)
   sono di un giro: dal vivo cambiano, e lo si dice. Se il modello chiede
   i due tool in due turni, sono 3 chiamate.
5. La chiave di riserva per chi ha perso il `.env`: a voce o nella chat
   della classe, durante il setup.
6. Il conto delle righe (slide 2 e 8), detto onesto: delle 71 del giro,
   50 (`chiedi()`) spariscono e 21 (`TOOLS`, `esegui()`) cambiano forma nel
   decoratore e in `tools=[…]`; il file nuovo è 221 righe e non 199
   perché `query_db` ora è scritto qui e prima era importato.
7. Demo 1 stampa due JSON interi: a schermo si guardano `description` e
   `properties`, il resto scorre. Demo 4: il «non disponibile» viene dalle
   `ISTRUZIONI` («se un tool ritorna un errore due volte di fila,
   fermati»), è la domanda più probabile. Se dal vivo esce un terzo esito, il punto
   resta lo stesso: il run non è morto, il testo dell'errore è tornato al
   modello.

## La serata (docente)

1. **Apertura (📊, 5')**: la versione finita di `assistente.py` della
   lezione scorsa a schermo (vedi la checklist): 263 righe, 71 sono il
   giro. Agenda.
2. **Setup (⌨️, 5')**: venv, `pip install -r requirements.txt`, il `.env`
   della lezione scorsa, `chroma/` copiata o no. Non si lancia niente:
   pip finisce durante la teoria.
3. **Teoria con le demo (📊, 40')**: i tre oggetti; **Demo 1**
   `demo.py schema`; la corrispondenza; **Demo 2** `demo.py traccia`;
   `max_turns` e **Demo 3** `demo.py tetto`; **Demo 4** `demo.py rotto`;
   cosa resta nostro; il nome; **Demo 5** `demo.py tracing` (apri il link
   stampato nel browser, con l'account del corso). Ogni demo ha la sua
   slide di switch con il comando; la slide dopo dice cosa si è visto.
4. **Codice spiegato (🎤, 20')**: i due file affiancati, dall'alto in
   basso; nel file di sinistra (la soluzione di Modulo 3 · Lezione 9) i
   sei punti da indicare: `cerca_documenti` (righe 78-99), `TOOLS` ed
   `esegui()` (100-120), le `ISTRUZIONI` (121-132), `chiedi()` con il ciclo
   (133-182), `strada()` (183-198), le stampe (199 in poi). Poi il lancio
   di `working/assistente_sdk.py` (con un tool solo: la baseline), e
   lanciano anche gli studenti.
5. **Esercizio (⌨️, 35' + 5')**: TODO 1 (20'), TODO 2 (15'), poi la slide
   di rientro con la soluzione dei due TODO: chi è indietro ricopia.
6. **Wrap-up (📊, 10')**: recap e ponte a Modulo 3 · Lezione 11.

Se si va lunghi: la Demo 5 si fa sulla traccia della Demo 2 (il
`trace_id` è stampato anche lì, aprendo la dashboard) senza rilanciare; la
slide sul nome si dice a voce; nell'esercizio il TODO 2 si mostra dalla
slide di rientro.

## Diagnosi rapida in aula (docente; gli studenti possono leggerla)

- Studente bloccato → copia il suo file **dentro `scripts/working/`**
  della tua copia con un altro nome, poi `python scaffolding/check_lab10.py
  --file working/assistente_sdk_giulia.py`. Dice quale dei due TODO manca
  e perché.
- Giulia Moretti «lo strumento necessario non è disponibile», nessun
  `tool` nella traccia → `query_db` non è in `tools=[...]`.
- `'function' object has no attribute 'name'` al primo run (subito dopo la
  prima riga `D:`; l'`Agent` si costruisce senza lamentarsi) → `query_db` è
  nella lista senza `@function_tool`.
- `output   An error occurred while running the tool. … Error: TODO 1` →
  il tool è cablato, dentro c'è ancora lo stub: è la Demo 4 dal vivo,
  l'SDK ha rimandato l'eccezione al modello.
- `no such column` nella traccia → la docstring di `query_db` non ha lo
  schema, o ce l'ha sbagliato.
- `AttributeError … 'name'` in `strada()` → legge `.name` su tutti gli
  item: solo i `ToolCallItem` ce l'hanno.
- `strada: nessuna` con un tool nella traccia → nomi sbagliati in
  `strada()`.
- `(mi fermo: 10 turni senza una risposta)` → `MaxTurnsExceeded`: il main
  lo cattura; nella traccia di solito lo stesso tool con lo stesso errore.
- `ModuleNotFoundError: No module named 'agents'` → `pip install -r
  requirements.txt` non è stato fatto in questo venv (il pacchetto si
  chiama `openai-agents`, il modulo `agents`).
- `OPENAI_API_KEY` non impostata → lanciato da un'altra cartella: `cd
  scripts`.
- La prima domanda ci mette due minuti → sta indicizzando; con `chroma/`
  copiata parte subito.

## Note tecniche (docente)

- **Versioni:** `openai-agents` 0.22.3, `openai` 3.16 (21/09/2026). Il
  modulo si importa come `agents`. `Runner.run_sync()` va bene in uno
  script; in un notebook o dentro un loop asyncio serve `await
  Runner.run()`.
- **`@function_tool`** trasforma la funzione in un oggetto `FunctionTool`:
  chiamarla a mano dà `TypeError: 'FunctionTool' object is not callable`
  (la funzione vera resta `tools.query_db`). Legge la docstring (stile
  Google: la sezione `Args:` dà la descrizione di ogni parametro) e la firma con i type
  hint: senza `sql: str` il parametro non ha tipo e lo schema è sbagliato.
  Lo schema generato è `strict` (`additionalProperties: false`): se
  chiedono cosa vuol dire, il modello non può passare parametri che non
  sono nella firma. `name="Assistente Lumen"` è l'etichetta dell'agente
  nella dashboard di tracing. Si
  stampa con `query_db.description` e `query_db.params_json_schema`.
- **Misure con la chiave vera (21/09/2026, tre giri, `misura_sdk.py
  --ripeti 3`: strumento di preparazione nella cartella della lezione, un
  livello sopra `scripts/`, non arriva agli studenti):** strade 12/12 sia a mano che con
  l'SDK; stesse chiamate; l'SDK manda in input 1.430 token in media
  contro 1.811 a mano, perché la definizione del tool è più corta
  (`definisci_tool` ripeteva la docstring dentro `parameters`); tempi
  uguali, 3-4 secondi a domanda.
- **Un turno è una chiamata al modello.** Lorenzo Rossi chiede i due tool
  nello stesso turno: 2 chiamate, non 3. `max_turns` default 10; con 1
  qualunque domanda con tool dà `MaxTurnsExceeded`, e `e.run_data.new_items`
  ha quello che era successo prima; con 2 le quattro `DOMANDE` passano
  (`demo.py tetto 2`, 21/09/2026). Il main lo cattura e scrive `?` in
  tabella.
- **Eccezioni nei tool:** di default l'SDK le rimanda al modello come
  «An error occurred while running the tool. Please try again. Error: …»
  (`failure_error_function`); con `failure_error_function=None`
  l'eccezione esce dal run come `UserError` e il programma muore. Il
  nostro `tools.query_db` cattura già tutto da solo (Modulo 3 · Lezione
  8): la Demo 4 usa una copia senza `try/except` e con `prezzo_listino`
  nello schema, apposta, ed è l'unico tool di quell'agente. Tre giri il
  21/09/2026, sempre 3 chiamate: due volte riscrive `SELECT *` e risponde
  89 euro, una volta riprova la stessa query e dice «non disponibile». Dal
  vivo può uscire l'uno o l'altro.
- **Reasoning:** con Luna la Responses API nuda emette item `reasoning`
  (il ciclo della lezione scorsa li rimandava); nel run dell'SDK non
  compaiono né in `new_items` né in `raw_responses`. Se uno chiede «e i
  reasoning?»: li gestisce l'SDK.
- **Tracing:** acceso di default, ogni run manda la traccia a
  `platform.openai.com/traces` (l'account della chiave): agente, chiamate
  al modello con input e output completi, tool con argomenti e risultato,
  tempi. Si spegne con `OPENAI_AGENTS_DISABLE_TRACING=1` nel `.env`: l'SDK legge
  la variabile la prima volta che gli serve e poi la tiene in cache, quindi
  la regola sicura è `load_dotenv` **prima** di `from agents import …`
  (il file lo fa). Il check e
  `misura_sdk.py` lo spengono da soli.
- **`output_type`** (se lo chiedono): `Agent(..., output_type=Risposta)`
  con un modello Pydantic dà `final_output` già come oggetto; provato con i
  due tool il 21/09/2026, quattro strade su quattro. Non è in slide: il
  codice della serata non lo usa.
- **Cosa non si dice stasera** (dal piano): sessioni (Modulo 3 · Lezione
  11), la misura sul query set (Modulo 3 · Lezione 12), handoff, agenti
  come tool, guardrail, approvazioni, MCP (Modulo 4).
