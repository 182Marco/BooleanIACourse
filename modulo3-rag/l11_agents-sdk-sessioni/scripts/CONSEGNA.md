# Modulo 3 · Lezione 11 — Agents SDK: sessioni e conversazione · consegna

Si lavora in `working/assistente_sdk.py`: è la soluzione della lezione
scorsa, con i due tool e `strada()` già scritti, e al posto delle quattro
domande fisse una chat da terminale. Dentro, nell'ordine: le costanti
(`MODELLO`, `K`, `MAX_TURNI` e le due nuove, `SESSIONI` e `LIMITE`);
`cerca_documenti` e `query_db`; le `ISTRUZIONI` e l'`agente`; `strada()`;
**TODO 1 e TODO 2**, tutti e due dentro `apri_sessione()`;
`stampa_traccia()` e il main, cioè la chat.

## Setup (5')

Dalla cartella `scripts/` di questa lezione. Le dipendenze sono le stesse
della lezione scorsa: la sessione è già dentro `openai-agents`.

```bash
cd scripts            # dalla cartella della lezione; se sei già in scripts/, salta questa riga
python3 -m venv .venv && source .venv/bin/activate   # Windows: python -m venv .venv e poi .venv\Scripts\activate
pip install -r requirements.txt
```

Quando pip ha finito, una prova da un secondo:

```bash
python -c "import agents; print('ok')"
```

Se stampa `ok` l'installazione è a posto; se dice `No module named
'agents'`, il venv attivo non è quello giusto o pip non ha finito.

Se hai ancora il venv della lezione scorsa puoi attivare quello e non
installare niente: `source ../../l10_agents-sdk-loop-gestito/scripts/.venv/bin/activate`
(Windows: `..\..\l10_agents-sdk-loop-gestito\scripts\.venv\Scripts\activate`).

Poi la chiave e la collection: copia il file `.env` e la cartella `chroma/`
dalla cartella `scripts/` della lezione scorsa dentro questa `scripts/`. Con
le cartelle della repo del corso (`modulo3-rag/l10_agents-sdk-loop-gestito/` per la lezione
scorsa, `modulo3-rag/l11_agents-sdk-sessioni/` per questa):

```bash
cp ../../l10_agents-sdk-loop-gestito/scripts/.env .env
cp -r ../../l10_agents-sdk-loop-gestito/scripts/chroma .   # solo se hai chroma/ nella lezione scorsa
```

Su Windows (prompt dei comandi):

```bat
copy ..\..\l10_agents-sdk-loop-gestito\scripts\.env .env
xcopy /E /I ..\..\l10_agents-sdk-loop-gestito\scripts\chroma chroma
```

Se la tua cartella della lezione scorsa ha un altro nome o sta altrove,
nei comandi cambia solo il percorso fino a `scripts/`; oppure copia `.env`
e la cartella `chroma/` con l'esplora risorse. Attenzione: `.env` è un file
nascosto (il nome comincia col punto): su Mac nel Finder si vedono con
Cmd+Shift+punto, su Linux con Ctrl+H. In caso di dubbio, alza la mano.

Se il `.env` non ce l'hai più: `cp .env.example .env`, alza la mano, e
incolla dentro la chiave che ti dà il docente (a voce o nella chat della
classe). Senza `chroma/` la collection si indicizza al primo lancio: un paio
di minuti, meno di un centesimo.

L'assistente non si lancia adesso: il primo lancio si fa dopo il codice
spiegato, quando lo fa il docente, con le due domande dell'apertura:

1. Perché il piano si ferma sempre a metà corsa?
2. E per il secondo caso?

Poi Invio a vuoto per uscire, un nuovo lancio, e di nuovo «E per il
secondo caso?».

## Come si usa la chat

Si lancia dalla cartella `scripts/`:

```bash
python working/assistente_sdk.py
```

Compare il prompt `Tu>`: scrivi una domanda e premi Invio. **Invio a vuoto
per uscire.** Sotto ogni risposta:

- la traccia del run: una riga `tool` per ogni tool chiesto, con
  l'argomento che ha scritto il modello, le prime righe del suo `output`, e
  `risposta`;
- la riga `N chiamate · … token in, … out · $…`: i token in input sono
  tutto quello che il modello ha letto nel run, storia compresa;
- la risposta dopo `→`, e la `strada:` presa (`documenti`, `dati`,
  `documenti+dati` o `nessuna`).

Una domanda con la sua risposta è uno **scambio**. Ogni chiamata al modello
è un **turno**, quello che conta `MAX_TURNI`: uno scambio di solito sono due
turni (il modello chiede un tool, poi risponde), e la riga dei token dice
«2 chiamate».

Finché il TODO 1 non c'è, la chat non chiede nessun nome e scrive
`Sessione «aula»`: è una sessione **in memoria**. I follow-up reggono, ma
quando esci la storia è persa. È la baseline, non è rotto. Un dialogo di tre
scambi costa circa due decimi di centesimo: rilancia quante volte vuoi.

## TODO 1 — la sessione su file, con un nome (25')

`apri_sessione()` deve:

1. chiedere il nome della sessione con `input()`, per esempio
   `input("Nome della sessione: ")`;
2. ritornare una `SQLiteSession` con quel nome, salvata nel file
   `SESSIONI`: `SQLiteSession(nome, SESSIONI)`.

Le due righe vanno **al posto** della riga `raise NotImplementedError("TODO 1")`:
se la lasci, il programma si ferma lì e ripiega sulla sessione «aula» in
memoria.

`SQLiteSession` è già importata in cima, e `SESSIONI` è già definita: è
il file `scripts/sessioni.db`. Il main chiama `apri_sessione()` una volta
all'avvio e passa la sessione a ogni `Runner.run_sync(..., session=sessione)`:
non c'è altro da cambiare. Senza il file (`SQLiteSession(nome)`) la
sessione resterebbe in memoria, come «aula».

**Prova:** lancia, dai un nome (il tuo, per esempio) e chiedi «Il braccio
LMX-4400 è compatibile con il piano fisso LD-115?». Invio a vuoto per
uscire. Rilancia, dai **lo stesso nome**, e chiedi «Perché no?».

**Fatto quando:** dopo il riavvio «Perché no?» risponde col motivo: il
piano LD-115 è troppo sottile e il morsetto del braccio non si chiude.
Senza storia la stessa domanda risponde che non ha abbastanza contesto.

Dopo il primo lancio in `scripts/` compare il file `sessioni.db`: è lì che
sta la storia. Lo stesso nome riprende la stessa conversazione; un nome
nuovo ne apre una nuova, nello stesso file.

## TODO 2 — il tetto alla storia (30')

Nella stessa riga del TODO 1, aggiungi a `SQLiteSession(...)` il parametro
`session_settings=SessionSettings(limit=LIMITE)`. `LIMITE` è in cima al file:
quanti item della storia la sessione ripassa al modello, e `None` vuol dire
tutti. La sessione salva tutto lo stesso: il tetto decide cosa vede il
modello. Uno scambio con un tool sono quattro item (la domanda, la
richiesta del tool, il suo output, la risposta): 16 item sono gli ultimi
quattro scambi. Se uno scambio ha due tool (6 item) o nessuno (2), il taglio
può cadere a metà di uno scambio: l'SDK toglie da solo i pezzi rimasti senza
coppia, e non dà errori.

**Prova:** il dialogo lungo, sette domande da scrivere una alla volta nella
chat, in quest'ordine:

1. Quanto costa la LumaDesk LD-200?
2. Cosa mi serve per allestire la postazione di casa?
3. Entro quando devo chiedere il contributo?
4. Cosa non copre la garanzia?
5. Come faccio la calibrazione alla prima accensione?
6. Quali sono i codici di errore e cosa significano?
7. Tornando alla scrivania di cui abbiamo parlato all'inizio: quanto pesa?

Due prove: prima con `LIMITE = None`, poi con `LIMITE = 16` (si cambia la
riga `LIMITE = …` in cima al file e si rilancia). **Ogni prova con un nome
di sessione nuovo** (per esempio `lungo-none` e `lungo-16`): con un
nome già usato la chat riprende la conversazione di prima. A ogni risposta
guarda i token in input: senza tetto crescono a ogni scambio. Annota quelli
dell'ultima risposta della prima prova, per confrontarli con la seconda. Fino al
quinto scambio le due prove sono simili, perché la storia non ha ancora
superato i 16 item; la differenza si vede negli ultimi due.

Alle domande 4 e 6 l'assistente risponde spesso che non ha trovato la
risposta: non dipende dal tuo codice, e non è il punto della prova. Guarda
la riga `tool`: il modello aggiunge «LumaDesk» alla domanda, e il passaggio
giusto finisce oltre i quattro che `cerca_documenti` rimanda. Con la
domanda scritta così com'è, sarebbe il terzo.

**Fatto quando:** con `None` l'ultima domanda trova il peso, 34 kg; con 16
i token dell'ultimo scambio sono più bassi e la scrivania del primo
scambio non si trova più.

## Se qualcosa non torna

| Cosa vedi | Cosa controllare |
|------------------------|------------------------------------|
| all'avvio non ti chiede il nome e scrive `Sessione «aula»` | in `apri_sessione()` c'è ancora `raise NotImplementedError("TODO 1")`: il main ripiega sulla sessione in memoria |
| all'avvio hai premuto Invio al posto del nome | la sessione si chiama «» ed è la stessa per tutti i lanci senza nome: rilancia e scrivi un nome vero |
| `OperationalError` quando il programma parte | hai scritto `SessionSettings(limit=LIMITE)` senza `session_settings=` davanti: il terzo argomento senza nome è un'altra cosa |
| `AttributeError: 'NoneType' object has no attribute 'session_id'` | `apri_sessione()` non ritorna la sessione: manca il `return` |
| dopo il riavvio l'assistente non sa di cosa parli | il nome è diverso da quello di prima (basta una maiuscola), oppure in `SQLiteSession(...)` manca `SESSIONI` e la sessione è in memoria |
| `TypeError: … unexpected keyword argument 'limit'` | `limit` non va dentro `SQLiteSession(...)` ma dentro `SessionSettings(...)`: `session_settings=SessionSettings(limit=LIMITE)` |
| la prima domanda del dialogo lungo ha già più di 3.000 token in input (di solito sono circa 1.200) | hai riusato un nome: la sessione ha dentro la conversazione di prima. Rilancia con un nome nuovo |
| con `LIMITE = 16` gli ultimi scambi hanno gli stessi token di `None` | il tetto non arriva alla sessione: manca `session_settings=...`, o `LIMITE` è rimasto `None` |
| con 16 l'ultima risposta dà il peso di due scrivanie | il modello non sa più di quale scrivania si parlava e ha tirato a indovinare: vale come «non si trova più» |
| `ModuleNotFoundError: No module named 'agents'` | il venv attivo non ha le dipendenze: `pip install -r requirements.txt` |
| un errore su `OPENAI_API_KEY` o `api_key` | manca `scripts/.env`: vedi il Setup |
| la prima domanda ci mette due minuti | sta indicizzando la collection: è normale, la seconda volta parte subito |

## Se finisci prima

- Un dialogo di Modulo 3 · Lezione 3, in una sessione con un nome nuovo:
  «Quanti giorni a settimana posso lavorare da remoto?», poi «E
  dall'estero?», poi «Con quanto preavviso devo chiederlo?». Prima di ogni
  follow-up prova a indovinare: il modello cercherà, o risponderà dalla
  storia senza tool? Poi leggi nella traccia la riga `tool`: l'argomento
  l'ha scritto il modello, con la storia davanti. Poi rifai «E dall'estero?»
  in una sessione nuova, senza la prima domanda: cosa cerca adesso? Altri
  dialoghi li ha il docente.
- Il dialogo lungo con `LIMITE = 24`, con un nome nuovo: l'ultima domanda
  trova ancora la scrivania? Prima di lanciare, conta quanti item ci sono
  nella sessione quando arriva la settima domanda. Poi con `LIMITE = 10`,
  che taglia a metà di uno scambio: guarda i token degli ultimi scambi
  (restano sotto i 4.000) e la risposta all'ultima domanda. Nessun errore:
  il pezzo rimasto senza coppia lo toglie l'SDK.
- Scrivi tu la serie dei token: nel main, una lista vuota prima del ciclo;
  dopo ogni risposta ci aggiungi `result.context_wrapper.usage.input_tokens`;
  all'uscita (Invio a vuoto) la stampi. Con il dialogo lungo è la serie
  della slide 11, con i tuoi numeri; con `LIMITE = 16` vedi dove si ferma.
- I numeri in slide sono con `K = 4` e `MODELLO` di Luna: se li cambi, i
  tuoi numeri non si confrontano più.
