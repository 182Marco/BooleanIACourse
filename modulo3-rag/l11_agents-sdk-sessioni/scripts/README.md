# Modulo 3 · Lezione 11 — Agents SDK: sessioni e conversazione · guida agli script

Lezione da 2 ore (📊 apertura con una dimostrazione + ⌨️ setup + 📊 teoria
con una dimostrazione + 🎤 codice spiegato + ⌨️ esercizio): l'assistente di
Modulo 3 · Lezione 10, con gli stessi due tool, le stesse istruzioni e
`strada()`, più una **sessione** dell'SDK che tiene la storia. Il file della
serata è `working/assistente_sdk.py`: è la soluzione della lezione scorsa
con il main trasformato in una chat da terminale; gli studenti scrivono solo
`apri_sessione()`, la sessione su file con un nome (TODO 1) e il tetto alla
storia (TODO 2). Le due dimostrazioni del docente si lanciano da
`scaffolding/demo.py`. I dialoghi misurati da dare a voce sono fuori da
`scripts/`, in `../dialoghi-docente.md` (e `.pdf`).

> **Per gli studenti:** servono la sezione **Setup** e la prima riga di
> **Come si prova**. Il resto è per il docente.

## Prima di entrare in aula (docente)

1. **Ambiente pronto**: venv in `scripts/` con `pip install -r
   requirements.txt`, `.env` copiato, `chroma/` già indicizzata (è
   gitignored: su un clone fresco manca, e la prima demo resterebbe muta due
   minuti). Un lancio di `python scaffolding/demo.py senza` prima dell'aula
   indicizza e prova la chiave.
2. **`python scaffolding/check_lab11.py --solutions --live`** → `tutto OK`:
   struttura, i due TODO della soluzione, e la ripresa in due processi
   (la domanda sul braccio LMX-4400, poi «Perché no?» con lo stesso nome).
   Meno di un centesimo.
3. **Le due demo provate**: `python scaffolding/demo.py senza` e `python
   scaffolding/demo.py storia`. Quattro chiamate ciascuna, meno di un
   centesimo.
4. **`sessioni.db`**: se hai provato la soluzione, in `scripts/` c'è un
   `sessioni.db` con le tue conversazioni. Cancellalo (`rm sessioni.db*`: con il file ci sono a volte `sessioni.db-wal` e `-shm`)
   per partire pulito, oppure in aula usa nomi che non hai mai usato.
5. **`../dialoghi-docente.pdf`** a portata di mano: cosa aspettarsi a ogni
   follow-up, e i dialoghi per chi finisce prima.
6. **La chiave di riserva** per chi ha perso il `.env`: a voce o nella chat
   della classe, durante il setup.
7. I numeri e le tracce nelle slide 3, 8, 11, 12, 13 e 19 sono misurati: dal vivo
   cambiano, e lo si dice. Nella demo `storia` il secondo scambio a volte
   risponde senza tool (1 giro su 5): gli item sono 6 e non 8.
8. Il «fatto quando» del TODO 1 distingue la sessione su file da quella in
   memoria: senza storia «Perché no?» non chiama tool e risponde «Non ho
   abbastanza contesto» (5 giri su 5). Una prima versione usava «E la
   versione wide?» dopo il prezzo della LD-210: scartata, perché il 949 esce
   anche senza storia.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 codice di riferimento che il
docente spiega · ⌨️ da completare dagli studenti · 📄 documenti/dati di
esempio.

| File | Ruolo | Cosa fa |
|------------------|----|--------------------------------------------------|
| `requirements.txt` | 🧰 | Le stesse dipendenze di Modulo 3 · Lezione 10, con `openai-agents==0.22.3`: `SQLiteSession` e `SessionSettings` sono già nel pacchetto. |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` (la stessa del Modulo 2) e la riga commentata `OPENAI_AGENTS_DISABLE_TRACING=1`. |
| `.gitignore` | 🧰 | `.env`, `.venv/`, `chroma/`, `__pycache__/` e `sessioni.db`: le conversazioni salvate non si versionano. |
| `CONSEGNA.md` | ⌨️ | Il setup, come si usa la chat, i TODO 1-2 con la prova e il criterio di «fatto», le sette domande del dialogo lungo, gli errori tipici, cosa fare se si finisce prima. |
| `README.md` | 📄 | Questa guida; `README.pdf` è l'export. |
| `scaffolding/aikit/` | 🧰 | Il toolkit di Modulo 3 · Lezione 10. Cambiano solo tre default, che passano a `gpt-5.6-luna`: il generator in `rag.py`, `modello_llm` in `rerank.py`, `MODELLO` in `tools.py`; `LLMClient` in `llm_client.py` resta `gpt-4.1-mini` (vedi le note tecniche). Stasera si usano `rag.recupera()`, `rag.CONFIG`, `rag.indicizza()`, `vectorstore.apri_collection()`, `tools.query_db()`, `cost_usd()`: nessuno dei default cambiati. Non si tocca. |
| `scaffolding/demo.py` | 🎤 | **Le due dimostrazioni del docente**: `senza` (apertura: le prime due domande del dialogo 1 di Modulo 3 · Lezione 3, ogni run senza sessione) e `storia` (teoria: le stesse due domande con una sessione in memoria, poi la stampa degli item salvati). Ha un agente suo, identico alla soluzione: gira anche prima dei TODO. |
| `scaffolding/check_lab11.py` | 🧰 | **Strumento del docente**: base istantaneo senza rete (struttura, scaffolding intatto, versione fissata, l'agente con i due tool; TODO 1: `apri_sessione()`, con `input()` simulato, ritorna una `SQLiteSession` con quel nome sul file `SESSIONI` e non in memoria; TODO 2: con `LIMITE = 5` la sessione ha `limit` 5); `--solutions`; `--file`; `--live` con la chiave (la domanda sul braccio LMX-4400 in un processo, «Perché no?» in un secondo processo con lo stesso nome). Usa file di sessione temporanei, non tocca `scripts/sessioni.db`, spegne il tracing. Non compare nel percorso studente. |
| `scaffolding/make_dataset.py`, `make_db.py` | 🧰 | I generatori del corpus e del database (seed fisso), identici alla lezione scorsa. Servono al check; non si lanciano in aula. |
| `scaffolding/sql.py` | 🧰 | Una query a mano in sola lettura su `lumen.db`; senza argomenti stampa lo schema. |
| `working/assistente_sdk.py` | ⌨️ | **Il file della serata**: la soluzione di Modulo 3 · Lezione 10 con `SESSIONI` e `LIMITE` tra le costanti, `apri_sessione()` da scrivere (TODO 1 e 2, riga 152) e il main a chat: `input()`, poi `Runner.run_sync(...)` con `session=sessione`, e sotto ogni risposta traccia e strada. Finché il TODO 1 manca, il main usa `SQLiteSession("aula")`, in memoria. |
| `solutions/assistente_sdk.py` | 🧰 | La versione completa, stesso nome: differisce solo nelle due righe di `apri_sessione()`. |
| `dataset/lumen_m3/` | 📄 | I sei documenti Lumen (82 chunk), identici a Modulo 3 · Lezione 2. |
| `dataset/lumen.db` | 📄 | Il database degli ordini Lumen, lo stesso di Modulo 3 · Lezione 8. |

`sessioni.db` non è nella tabella perché non si distribuisce: lo crea la
chat, in `scripts/`, al primo lancio dopo il TODO 1.

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt                        # le stesse della lezione scorsa
cp ../../l10_agents-sdk-loop-gestito/scripts/.env .env   # la chiave della lezione scorsa (oppure: cp .env.example .env e incollala dentro)
cp -r ../../l10_agents-sdk-loop-gestito/scripts/chroma . # facoltativo: la collection già indicizzata
```

Chi ha ancora il venv della lezione scorsa può attivare quello (`source
../../l10_agents-sdk-loop-gestito/scripts/.venv/bin/activate`) e non installare niente. I path
sono quelli della repo che hanno gli studenti (`modulo3-rag/l10_…`,
`modulo3-rag/l11_…`); nel repo di lavorazione le cartelle si chiamano
`lezione-10-…` e `lezione-11-…`.

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env`, `.venv`, `chroma/` e `sessioni.db` (git non li
> versiona). La chiave OpenAI è quella del corso. Chi non copia `chroma/` la
> ricostruisce al primo lancio (82 chunk, un paio di minuti, meno di un
> centesimo). Il database arriva già pronto.

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/assistente_sdk.py                  # la chat della serata; Invio a vuoto per uscire

python scaffolding/demo.py senza                  # apertura: il follow-up senza sessione
python scaffolding/demo.py storia                 # teoria: gli stessi due scambi con la sessione, e cosa c'è dentro

# solo docente, non fa parte del percorso studente
python scaffolding/check_lab11.py                 # istantaneo, zero costi
python scaffolding/check_lab11.py --file working/assistente_sdk_studente.py   # il file di uno studente, copiato in working/
python scaffolding/check_lab11.py --solutions     # regressione sulla versione completa
python scaffolding/check_lab11.py --solutions --live   # chiamate vere: due processi, lo stesso nome

rm sessioni.db*                                   # per ripartire senza conversazioni salvate (Windows: del sessioni.db*)
```

Uno scambio sono di solito due chiamate a `gpt-5.6-luna` (una se risponde
senza tool), più un embedding per ogni `cerca_documenti`. Un dialogo di tre scambi con la sessione costa circa
$0,002, il dialogo lungo senza tetto circa $0,007: l'esercizio intero sta
sotto i due centesimi a testa. Sul `working/` intonso il check dà **2 FAIL
per costruzione** (i due TODO): è la baseline.

## Cosa si vede a schermo

Con la soluzione, la prova del TODO 1: la prima domanda del dialogo 6,
Invio a vuoto, un nuovo lancio con lo stesso nome e il follow-up (misurato il
24/09/2026: dal vivo token e testo cambiano):

```
Nome della sessione: prova
Sessione «prova». Scrivi una domanda; invio a vuoto per uscire.

Tu> Il braccio LMX-4400 è compatibile con il piano fisso LD-115?
   tool     cerca_documenti({"domanda":"Il braccio LMX-4400 è compatibile con il piano fisso LD-115?"})
   output   [ticket-supporto-008]
            TCK-1152 · LD-115 · morsetto del braccio che non chiude — Sintomo: …
            [listino-catalogo-004]
            … altre 7 righe
   risposta
   2 chiamate · 1695 token in, 88 out · $0.00044
→ No. Il braccio LMX-4400 non è compatibile con il piano fisso LD-115 perché lo spessore è insufficiente per il morsetto. [listino-catalogo-004]
   strada: documenti

Tu>

Nome della sessione: prova
Sessione «prova». Scrivi una domanda; invio a vuoto per uscire.

Tu> Perché no?
   risposta
   1 chiamata · 1187 token in, 42 out · $0.00029
→ Perché il piano LD-115 è troppo sottile per consentire al morsetto del LMX-4400 di chiudersi correttamente. [ticket-supporto-008]
   strada: nessuna
```

Dopo il riavvio il modello ha la storia davanti: qui risponde senza tool,
con il passaggio del primo scambio (`[ticket-supporto-008]` era già
nell'output di `cerca_documenti`). Nelle altre tre misure del riavvio ha
chiamato `cerca_documenti` con la domanda riscritta («Perché il braccio
LMX-4400 non è compatibile con il piano fisso LD-115?»): le due tracce
vanno bene tutte e due. Senza storia la risposta è «Non ho abbastanza
contesto per rispondere».

## La serata (docente)

1. **Apertura (📊 + demo, 5')**: `python scaffolding/demo.py senza`. Al
   secondo run nessun tool e «Non ho abbastanza contesto per capire a quale
   "secondo caso" ti riferisci», 552 token in (6 giri su 6). Poi l'agenda.
2. **Setup (⌨️, 5')**: venv (o quello della lezione scorsa), `.env` e
   `chroma/` copiati. Non si lancia niente: pip finisce durante la teoria.
3. **Teoria con una demo (📊, 25')**: cosa fa una sessione; **demo**
   `demo.py storia` e gli item nella sessione; turno e scambio; la
   corrispondenza con `chat.py` di Modulo 3 · Lezione 3; cosa entra nella
   storia e i token; la domanda per il retrieval la scrive il modello; i
   follow-up misurati; il tetto, `SessionSettings(limit=N)`.
4. **Codice spiegato (🎤, 15')**: `working/assistente_sdk.py` dall'alto in
   basso, solo quello che cambia rispetto alla lezione scorsa: l'import di
   `SQLiteSession` e `SessionSettings` (riga 46), `SESSIONI` e `LIMITE`
   (56-57), `apri_sessione()` con i due TODO (144-156), il main a chat
   (182-205: il `try` su `apri_sessione()` con il ripiego su «aula», il
   ciclo `input()`, `session=sessione` in `run_sync`). Poi il lancio con le
   due domande dell'apertura: il follow-up passa. Invio a vuoto, nuovo
   lancio, «E per il secondo caso?»: la sessione «aula» era in memoria, ed
   è di nuovo «non ho abbastanza contesto». Poi lanciano gli studenti. Per
   chi vuole il confronto riga per riga: la soluzione della lezione scorsa è
   `../../lezione-10-agents-sdk-loop-gestito/scripts/solutions/assistente_sdk.py`
   (221 righe; il file di stasera 205: escono `DOMANDE`, `SOLO` e
   `stampa_tabella()`).
5. **Esercizio (⌨️, 55' + 5')**: TODO 1 (25'), TODO 2 (30'), il resto per
   chi finisce prima (dialoghi da `../dialoghi-docente.md`, a voce); poi la
   slide di rientro con la soluzione e i numeri: chi è indietro ricopia.
6. **Wrap-up (📊, 10')**: recap e ponte a Modulo 3 · Lezione 12: gli
   studenti portano il proprio `assistente.py` di Modulo 3 · Lezione 9, e il
   passaggio all'SDK si fa in aula (Lab 1). Alla slide 17 si dice anche che
   `aikit/` ha Luna come default in `rag.py`, `rerank.py` e `tools.py`:
   stasera non si usano, ma il toolkit non cambia mai in silenzio.

Se si va lunghi: la demo `storia` si salta (la slide dopo mostra gli stessi
item); le slide 12 e 13 si danno in un minuto ciascuna (la tabella degli
argomenti e i due numeri grandi); il riavvio nel codice spiegato si dice a voce, senza rilanciare; il
TODO 2 si fa con una prova sola, `LIMITE = 16`, e i numeri di `None` si
danno dalla slide di rientro.

Se si è in anticipo (chi finisce i due TODO in 20-25'): gli extra di
`CONSEGNA.md` (il dialogo 5 con e senza storia, `LIMITE = 24` e `LIMITE =
10`), poi gli altri dialoghi dall'elenco in fondo a
`../dialoghi-docente.md`, da incollare nella chat della classe. A fine
esercizio si può aprire `sessioni.db` con `sqlite3 sessioni.db "select
count(*) from agent_messages"`: la storia di tutte le sessioni della
serata, in un file.

## Diagnosi rapida in aula (docente; gli studenti possono leggerla)

- **Studente bloccato** → copia il suo file **dentro `scripts/working/`**
  della tua copia con un altro nome, poi `python scaffolding/check_lab11.py
  --file working/assistente_sdk_giulia.py`. Dice quale TODO manca e perché
  (sessione in memoria, file sbagliato, tetto mancante).
- **All'avvio non chiede il nome e scrive `Sessione «aula»`** → il TODO 1
  non è scritto: in `apri_sessione()` c'è ancora `raise
  NotImplementedError`, e il main ripiega su `SQLiteSession("aula")`, in
  memoria.
- **I follow-up reggono, ma dopo il riavvio la storia non c'è** → tre
  cause, in ordine di frequenza probabile:
  - sessione in memoria: `SQLiteSession(nome)` senza file. In `scripts/`
    non c'è `sessioni.db`; il check dice `db_path è ':memory:'`;
  - nome diverso al secondo lancio: una maiuscola, o uno spazio in più se
    manca `.strip()`. Un nome nuovo è una conversazione nuova, nello stesso
    file;
  - file diverso: `SQLiteSession(nome, "sessioni.db")` con un path relativo
    al posto di `SESSIONI`. Il file finisce nella cartella da cui si lancia,
    e da due cartelle diverse sono due file. `SESSIONI` è costruito dalla
    posizione del file e non ha questo problema; il check stampa il
    `db_path` che trova.
- **«Perché no?» dopo il riavvio risponde «non ho abbastanza contesto»**
  → la storia non c'è: nome diverso da quello del primo lancio, o sessione
  in memoria (manca `SESSIONI`). Si controllano `sessioni.db` e il nome.
- **Invio a vuoto al prompt del nome** (a Modulo 3 · Lezione 3 voleva dire
  «non salvare») → la sessione si chiama `""`, sta sul file ed è condivisa
  da tutti i lanci con Invio a vuoto: la prima domanda ha già migliaia di
  token. Si rilancia con un nome vero.
- **`exit` scritto per abitudine** (a Modulo 3 · Lezione 3 si usciva così) →
  diventa una domanda al modello e finisce nella storia. Si esce con Invio a
  vuoto.
- **`SQLiteSession(nome, SESSIONI, SessionSettings(limit=LIMITE))`**, senza
  `session_settings=` → il terzo argomento posizionale è il nome della
  tabella, e SQLite dà un `OperationalError` alla creazione. Serve il nome:
  `session_settings=SessionSettings(limit=LIMITE)`.
- **`AttributeError: 'NoneType' object has no attribute 'session_id'`** →
  `apri_sessione()` non ritorna la sessione.
- **`TypeError: … unexpected keyword argument 'limit'`** → `limit=` passato
  a `SQLiteSession`: il costruttore non ce l'ha, va in
  `session_settings=SessionSettings(limit=LIMITE)`.
- **Con `LIMITE = 16` gli ultimi scambi hanno gli stessi token di `None`**
  → il tetto non arriva alla sessione (il check lo dice: `limit` è `None`).
  Fino al quinto scambio i due giri sono comunque simili: prima della quinta
  domanda la storia ha 16 item, e il tetto non taglia niente.
- **La prima domanda del dialogo lungo parte già con migliaia di token** →
  nome riusato: la sessione ha dentro la conversazione di prima.
- **Con 16 l'ultima domanda trova lo stesso il peso** → controllare che il
  tetto ci sia; se c'è, è la variabilità: in 1 giro su 4 il modello ha
  cercato «… probabilmente LD-200 o LD-210» e ha dato tutti e due i pesi (34
  e 39 kg). Non sa quale delle due: vale come «non si trova più».
- **Domande 4 e 6 del dialogo lungo: «non ho trovato»** → normale: 11 giri
  su 12 per ciascuna, con e senza tetto. Non è il punto del dialogo.
- **`RuntimeError: <asyncio.locks.Event object at 0x…> is bound to a
  different event loop`** → lo studente ha aggiunto un
  `asyncio.run(sessione.get_items())` per stampare la storia: il run dopo
  muore. Si toglie, o si usa
  `asyncio.get_event_loop().run_until_complete(sessione.get_items())`, come
  `scaffolding/demo.py`.
- **`ModuleNotFoundError: No module named 'agents'`** → nel venv attivo non
  è stato fatto `pip install -r requirements.txt` (il pacchetto si chiama
  `openai-agents`, il modulo `agents`).
- **Errore su `OPENAI_API_KEY` o `api_key`** → manca `scripts/.env`.
- **La prima domanda ci mette due minuti** → sta indicizzando; con `chroma/`
  copiata parte subito.

## Note tecniche (docente)

- **Due «tetti» nel file.** `MAX_TURNI` (i commenti del file lo chiamano «il
  tetto al giro», come la lezione scorsa) limita i turni dentro un run;
  `LIMITE` limita la storia che la sessione ripassa tra un run e l'altro. Al
  codice spiegato conviene dirlo, perché in slide «tetto» è `LIMITE`.
- **La slide 17** si mostra dopo il lancio del codice spiegato: è il
  rientro, con quello che si è appena visto (il follow-up che passa, la
  sessione «aula» vuota dopo il riavvio).
- **Domande 4 e 6 del dialogo lungo, «non ho trovato» 11 volte su 12.** Le
  risposte sono nel corpus (le esclusioni in `policy-resi-garanzia-010`, i
  codici di errore in `manuale-lumadesk-008`), e con la domanda così com'è il
  retrieval le trova al terzo posto. Il modello però la riscrive
  aggiungendo il marchio («Cosa non copre la garanzia Lumen o LumaDesk?»,
  «Codici di errore della LumaDesk e relativo significato»), e il passaggio
  giusto scende al 10°-16° posto, fuori dai 4 di `cerca_documenti` (misurato
  il 24/09/2026). Il marchio il modello lo aggiunge anche senza sessione
  (slide 3: «Perché il piano della scrivania LumaDesk…»): una domanda
  riscritta non è sempre migliore di quella dell'utente. È un caso da
  diagnosi di Modulo 3 · Lezione 6 (il chunk giusto non è nel top-k), non un
  difetto della sessione.

- **Versioni:** `openai-agents` 0.22.3, `openai` 3.16, come la lezione
  scorsa. Tutte le misure sono del 24/09/2026 con la chiave vera, modello
  `gpt-5.6-luna`, K 4: `misura_sessioni.py` (strumento di preparazione
  nella cartella della lezione, un livello sopra `scripts/`, non arriva agli
  studenti), `scaffolding/demo.py`, `check_lab11.py --live`. Il dettaglio
  dialogo per dialogo è in `../dialoghi-docente.md`.
- **Sessione in memoria e su file.** `SQLiteSession(nome)` ha `db_path`
  `":memory:"`: la storia vive finché vive il processo. `SQLiteSession(nome,
  SESSIONI)` apre (e crea, se manca) il file SQLite già nel costruttore: in
  `scripts/sessioni.db` compaiono le tabelle `agent_sessions` e
  `agent_messages`. Nello stesso file stanno tante conversazioni, una per
  nome (`session_id`): lo stesso nome riprende, un nome nuovo parte da zero.
- **`sessioni.db`** è nel `.gitignore`. Per ripartire pulito si cancella:
  la sessione lo ricrea al lancio dopo.
- **Cosa salva la sessione:** tutti gli item del run, nell'ordine: la
  domanda (`message` user), `function_call`, `function_call_output`, la
  risposta (`message` assistant). Quattro item per scambio con un tool, due
  senza tool, sei con due tool nello stesso turno. Nessun item `reasoning`.
  Un `function_call_output` di `cerca_documenti` è circa 400 token (330-510
  su tre output misurati, circa 1.300 caratteri: i quattro passaggi). Ogni
  scambio aggiunge alla storia circa 500 token, e uno scambio con un tool
  sono due turni che la rileggono tutti e due: per questo i token in input
  della riga sotto la traccia crescono di circa mille a scambio.
- **Il tetto:** `SessionSettings(limit=N)` non cancella niente. La sessione
  salva tutto; `get_items()` ritorna gli ultimi N item, ed è quello che
  l'SDK mette davanti alla domanda nuova. `limit=None` = tutti. Il taglio
  conta item, non scambi: può cadere tra una `function_call` e il suo
  output. L'SDK toglie i pezzi rimasti senza coppia prima di chiamare il
  modello (`drop_orphan_function_calls` in `agents/run_internal/items.py`):
  misurato con `limit` 6 e 10, che tagliano a metà scambio, nessun errore
  (token dell'ultimo scambio 2.747 e 3.842; la scrivania non si trova).
- **Perché i passaggi entrano nella storia** (la domanda più probabile: a
  Modulo 3 · Lezione 3 `chat.py` diceva «mai i chunk in storia»). La
  sessione salva gli item del run così come sono, e la `function_call` e il
  suo output per l'API vanno in coppia: l'SDK non ha un'opzione per salvare
  la richiesta del tool senza il risultato. Il conto: `condensa()` costava
  una chiamata in più a ogni scambio e teneva la storia corta; la sessione
  non fa chiamate in più, ma porta circa 500 token a scambio, letti due
  volte. Filtrare la storia prima del run si può (`session_input_callback`
  di `RunConfig`), ma è fuori dal corso: qui la risposta è il tetto.
- **`asyncio.run()` accanto a `run_sync()`:** `get_items()` è async. Un
  `asyncio.run(sessione.get_items())` apre un event loop nuovo e lo chiude;
  il `run_sync()` successivo nello stesso processo muore con `RuntimeError:
  … is bound to a different event loop` (misurato). `run_sync()` riusa
  l'event loop del thread, quindi la lettura va fatta su quello:
  `asyncio.get_event_loop().run_until_complete(sessione.get_items())`, come
  in `demo.py`. Il file degli studenti non legge la sessione.
- **Luna nei default di `aikit`, tranne `LLMClient`.** `rag.py` (generator),
  `rerank.py` (LLM-as-reranker) e `tools.py` girano con Luna e da questa
  lezione ce l'hanno come default (decisione del 22/09/2026; nessuno di
  questi default si usa stasera, e gli hash del check sono aggiornati).
  `LLMClient` resta `gpt-4.1-mini`: passa sempre `temperature=0.7`, e Luna
  risponde `BadRequestError` (400). Se uno studente prova
  `LLMClient(model="gpt-5.6-luna")`, l'errore è quello.
- **Il riassunto della storia** (`OpenAIResponsesCompactionSession`
  nell'SDK) è fuori dal modulo. Se lo chiedono, una riga a voce: esiste una
  sessione dell'SDK che compatta la parte vecchia della storia; nel corso
  non la usiamo.
- **Tracing:** come la lezione scorsa, acceso di default; si spegne con
  `OPENAI_AGENTS_DISABLE_TRACING=1` nel `.env`, letto prima di `from agents
  import …`. Il check e `misura_sessioni.py` lo spengono da soli.
- **Cosa non si dice stasera** (dal piano): la misura sul query set con i
  follow-up (Modulo 3 · Lezione 12); il riassunto della storia (una riga se
  chiesto) e la memoria oltre la conversazione (Modulo 4 · Lezione 8);
  handoff e più agenti (Modulo 4).
