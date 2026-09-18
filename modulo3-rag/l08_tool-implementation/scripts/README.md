# Modulo 3 · Lezione 8 — Tool Implementation · guida agli script

Lezione da 2 ore (📊 slide + 🎤 demo a mano e codice spiegato + ⌨️
esercizio): un tool che tocca dati veri. Il modello scrive una query SQL,
il nostro codice la esegue in sola lettura sul database degli ordini Lumen
(`dataset/lumen.db`) e gli rimanda il risultato; gli errori tornano al
modello come testo invece di far morire il programma. Il codice sta tutto
in **un file**, `working/tools.py`, lo stesso della lezione scorsa:
`query_db` è già scritto (il docente lo spiega); l'esercizio è
`prezzo_prodotto`, un tool con la query fissa, e i tre casi rotti.

> **Per gli studenti:** servono la sezione **Setup** e **Come si prova**
> (le prime tre righe). Il resto, da «Note tecniche», è per il docente.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 codice spiegato o demo del
docente · ⌨️ da completare dagli studenti · 📄 documenti e dati.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | `python-dotenv`, `openai`, `pydantic`: come Modulo 3 · Lezione 7 (`sqlite3` è nella libreria standard). |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` (la stessa del Modulo 2). |
| `CONSEGNA.md` | ⌨️ | Il TODO in tre punti, i tre casi rotti, il criterio di «fatto», gli errori tipici, `stato_ordine` per chi finisce prima. |
| `dataset/lumen.db` | 📄 | Il database degli ordini Lumen (SQLite): `prodotti` 16, `clienti` 40, `ordini` 300 (gennaio–agosto 2026), `righe_ordine` 781. Serve fino alla fine del modulo. |
| `scaffolding/make_dataset.py` | 🧰 | Genera `dataset/lumen.db` con seed fisso (si rigenera identico); le scelte fatte per le lezioni sono nel docstring. Non si lancia in aula. |
| `scaffolding/sql.py` | 🎤 | Una query a mano, in sola lettura: senza argomenti stampa lo schema. È la demo del docente sul database, e gli studenti lo usano per guardare i dati. |
| `scaffolding/aikit/llm_client.py` | 🧰 | Il client di Modulo 2 · Lezione 3: serve solo `cost_usd()`. |
| `scaffolding/check_lab08.py` | 🧰 | **Strumento del docente**: base istantaneo senza rete (struttura e database, `query_db` su scrittura, colonna sbagliata, due query in una e output lungo, `prezzo_prodotto` sui tre casi rotti, il tetto di `chiedi()`); `--solutions` per la versione completa; `--live` con la chiave vera. Non compare nel percorso studente. |
| `working/tools.py` | 🎤 ⌨️ | **Il file della serata**: la calcolatrice e la data della lezione scorsa; `QueryDb` + `query_db()`, `DB`, `LIMITE`, `MAX_CHIAMATE` già scritti; il **TODO** `prezzo_prodotto` in tre punti. |
| `solutions/tools.py` | 🧰 | La versione completa, stesso nome file: differisce da `working/` solo nel TODO. |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../../lezione-07-tool-calling-intro/scripts/.env .env   # la chiave della lezione scorsa (oppure: cp .env.example .env e incollala dentro)
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env` e `.venv` (git non li versiona). Il setup va fatto prima
> del codice spiegato: il momento giusto è la demo a mano sul database, che
> non ne ha bisogno (`sql.py` usa solo la libreria standard). Il database invece
> arriva già pronto: non va rigenerato.

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python scaffolding/sql.py                                   # lo schema del database
python scaffolding/sql.py "SELECT * FROM ordini LIMIT 5"     # una query a mano
python working/tools.py                                     # le tre domande, ogni passo del giro, token e costo

# solo docente, non fa parte del percorso studente
python scaffolding/check_lab08.py                           # istantaneo, zero costi
python scaffolding/check_lab08.py --file working/tools_studente.py  # il file di uno studente, copiato in working/
python scaffolding/check_lab08.py --solutions               # regressione sulla versione completa
python scaffolding/check_lab08.py --solutions --live        # chiamate vere (~15 s)
python scaffolding/make_dataset.py                          # rigenera lumen.db (identico)
```

Un lancio del main sono sei chiamate a `gpt-4.1-mini`, circa $0,0013. Sul
`working/` intonso il check dà **6 FAIL per costruzione** (`prezzo_prodotto`
è solo abbozzata, non è in `TOOLS` né in `esegui()`) e una `[NOTA]`: è la
baseline, non un guasto.

## Le tre query della demo a mano

```sql
SELECT * FROM ordini LIMIT 5
SELECT r.codice_prodotto, p.nome, r.quantita FROM righe_ordine r JOIN prodotti p ON p.codice = r.codice_prodotto WHERE r.ordine_id = 1286
SELECT COUNT(*) FROM ordini o JOIN clienti c ON c.id = o.cliente_id WHERE c.nome = 'Giulia Moretti'
```

La terza dà 13: è la risposta alla domanda dell'apertura.

## Cosa si vede a schermo

Con il file così com'è (senza `prezzo_prodotto`):

```
D: Quanti ordini ha fatto Giulia Moretti?
   chiamata 1  [432 token in, 45 out]  output: function_call query_db({"sql":"SELECT COUNT(*) AS numero_ordini FROM ordini JOIN clienti ON ordini.cliente_id = clienti.id WHERE clienti.nome = 'Giulia Moretti';"})
      eseguo query_db: numero_ordini
         13
   chiamata 2  [490 token in, 13 out]  output: message
   2 chiamate · $0.00046
→ Giulia Moretti ha fatto 13 ordini.

D: Quanti ordini sono ancora in viaggio?
   chiamata 1  [430 token in, 33 out]  output: function_call query_db({"sql":"SELECT COUNT(*) AS ordini_in_viaggio FROM ordini WHERE stato = 'in viaggio'"})
      eseguo query_db: ordini_in_viaggio
         0
   chiamata 2  [478 token in, 12 out]  output: message
   2 chiamate · $0.00044
→ Non ci sono ordini attualmente in viaggio.

D: Quanto costa la LMX-4400?
   chiamata 1  [430 token in, 28 out]  output: function_call query_db({"sql":"SELECT prezzo FROM prodotti WHERE nome = 'LMX-4400'"})
      eseguo query_db: prezzo
   chiamata 2  [468 token in, 19 out]  output: message
   2 chiamate · $0.00043
→ Non risulta un prezzo associato al prodotto LMX-4400 nel database.
```

La prima è giusta. La seconda è sbagliata **senza nessun errore**: gli
ordini in viaggio sono 5, ma il valore di `stato` è `spedito`, e il modello
non vede i valori delle colonne (10 giri su 10 così). La terza cerca il
codice nella colonna `nome` in circa 7 giri su 10; negli altri usa
`codice` e risponde 89 euro: se in aula esce giusta, si rilancia una volta.

Con `prezzo_prodotto` (la soluzione) la terza domanda chiama
`prezzo_prodotto` in tutti i giri misurati (10 su 10) e risponde 89 euro;
le prime due restano uguali, con un centinaio di token in più a chiamata
per la definizione del quarto tool.

## Note tecniche (docente)

- **Perché `query_db` intercetta `Exception` e non `sqlite3.Error`**: due
  istruzioni in una (`SELECT …; DELETE …`) fanno sollevare a `sqlite3`
  «You can only execute one statement at a time». Su Python 3.10 e 3.11 è
  un `sqlite3.Warning`, che non è una sottoclasse di `sqlite3.Error`: con
  `except sqlite3.Error` il programma morirebbe. Da Python 3.12 è un
  `ProgrammingError` (sottoclasse di `sqlite3.Error`). `Exception` regge
  tutte le versioni che gli studenti possono avere.
- **Le domande del 15 su 15** (slide sullo schema) sono cinque
  domande che contengono il valore come sta nel database: gli ordini di
  Giulia Moretti, i clienti aziende, i prodotti sotto i 50 euro, i pezzi
  di LMX-4400 venduti, la città del cliente dell'ordine 1100; tre lanci
  ciascuna. **423 contro 153**: i token in input di una chiamata con la
  sola parola «Ciao» e le `ISTRUZIONI`, con calcolatrice, data e `query_db`
  in `TOOLS` contro calcolatrice e data: la differenza, circa 270, è la
  definizione di `query_db`. Con le domande vere la prima chiamata ne
  mostra 430-432.
- **«Il modello potrebbe fare `SELECT DISTINCT stato`»**: vero, il tool glielo
  permette, ma nelle misure non lo fa da solo. È l'argomento giusto per
  Modulo 3 · Lezione 13 (lo schema descritto).
- **`mode=ro` e il file vuoto**: `sqlite3.connect("dataset/lumen.db")` su
  un file che non esiste **crea** un database vuoto, e la query dopo dà
  `no such table`. Con `sqlite3.connect(DB.as_uri() + "?mode=ro", uri=True)` il
  file non si crea (`unable to open database file`) e una scrittura dà
  `attempt to write a readonly database`. È il caso 3 dell'esercizio.
- **Il controllo sul `SELECT`** guarda solo l'inizio della query: una
  `WITH … SELECT` viene rifiutata. Va bene così: la sola lettura la
  garantisce `mode=ro`, il controllo dà un messaggio chiaro al modello.
- **Il round di correzione** («no such column» → query giusta) nelle
  misure è raro: sulle domande che contengono il valore mai (15 su 15
  giuste al primo colpo). Per questo la slide mostra un giro registrato («Quanti giorni ci
  vogliono in media tra ordine e consegna?», con il solo `query_db` tra i
  tool) e non una demo dal vivo. Chi vuole provarlo in aula: con i tre
  tool esce circa una volta su due su quella domanda, ma il modello tende
  a sottrarre le date con la calcolatrice una riga alla volta, e in un
  giro su cinque chiama la calcolatrice con un argomento sbagliato e il
  programma muore di `KeyError` in `esegui()`. Non è in slide: stasera gli
  errori si gestiscono dentro i tool (`query_db`, `prezzo_prodotto`), e
  `esegui()` resta com'era la lezione scorsa. Se uno studente lo incontra,
  la risposta è che lo stesso `try`/`except` si potrebbe mettere attorno a
  `esegui()` in `chiedi()`.
- **I numeri della slide sul costo** (15.350 contro 1.432 token): la
  chiamata dopo un `SELECT * FROM righe_ordine` (781 righe) con il
  risultato intero e con il taglio a 50 righe, a parità di domanda; su
  «Mostrami tutte le righe d'ordine.» il modello ha scritto `SELECT *`
  senza `LIMIT` in 3 lanci su 3.
- **«Maiuscolo, senza spazi»**: la soluzione fa `strip().upper()`, cioè toglie
  gli spazi ai lati. Un codice con uno spazio in mezzo («lmx 4400») non si
  trova, e va bene così: il caso dell'esercizio non ce l'ha.
- **Il modello non prova a scrivere**: su «Cancella l'ordine 1001» e simili
  risponde che può solo leggere (15 su 15, anche togliendo «solo SELECT»
  dalla descrizione). I controlli servono lo stesso: la descrizione il
  modello può ignorarla, il codice no.
- **Le query valide con la risposta sbagliata** (slide 14): «in viaggio»,
  «cancellati» (`'annullato'`), «il cliente Rossi» (due clienti, 15
  ordini; il modello scrive `nome = 'Rossi'`), «Quali clienti hanno
  ordinato la LMX-4400 a giugno?» (cerca nel 2023). Non si curano stasera: lo schema descritto è Modulo 3 · Lezione
  13. Se uno studente propone di scrivere i valori di `stato` nella
  descrizione, è la risposta giusta, e la si rimanda lì.
- **Materiale solo per il docente** (la soluzione di `stato_ordine` del «se
  finisci prima», da dove vengono i numeri delle slide, cosa rispondere su
  alcune domande che anticipano lezioni future): `conduzione-docente.md`,
  nella cartella della lezione, fuori da `scripts/`.

## Percorso in aula (le slide sono la regia: ogni switch ha la sua slide)

1. **Apertura (📊, 5')**: «Quanti ordini ha fatto Giulia Moretti?» al file
   della lezione scorsa: chiede i dati. Agenda.
2. **Il database (📊 10' + 🎤 5')**: tabelle, righe vere, quattro dettagli
   delle colonne, tre query da leggere; poi `scaffolding/sql.py` con le tre
   query.
3. **Teoria (📊, 20')**: text-to-SQL; lo schema, non i dati; gli errori
   tornano al modello; sicurezza nel codice; output compatti; query valide
   con la risposta sbagliata; la mappa del file.
4. **Codice spiegato (🎤, 15')**: `query_db` riga per riga, poi il lancio:
   la prima domanda giusta, le altre due sbagliate.
5. **Esercizio (⌨️, 60')**: `prezzo_prodotto`, la domanda sul prezzo, i tre
   casi rotti. Rientro sulle slide.
6. **Wrap-up (📊, 5')**: la query fissa e i casi rotti prima e dopo; recap;
   la prossima lezione.

Se si va lunghi: la demo a mano si riduce alla terza query (−3'); in
teoria il costo senza limite si dice a voce nel codice spiegato (−3');
codice spiegato ed esercizio non si accorciano (il nucleo dell'esercizio,
TODO e casi rotti, sono ~45'); nel wrap-up si salta la slide del recap e
si chiude sulla slide «Cosa si è visto: la query fissa e i casi rotti»
(−2').
Se si va corti: il «se finisci prima» di `CONSEGNA.md` per tutti.

## Diagnosi rapida in aula (docente; gli studenti possono leggerla)

- Studente bloccato → copia il suo file **dentro `scripts/working/`** della
  tua copia con un altro nome (per esempio `working/tools_giulia.py`: il
  file calcola `scripts/` da dove si trova, e fuori da lì non trova né
  `aikit` né il database), poi `python scaffolding/check_lab08.py --file
  working/tools_giulia.py`. Dice quale punto manca: la funzione, la voce in
  `TOOLS`, il ramo in `esegui()`, o quale dei tre casi rotti solleva ancora
  un'eccezione.
- In alternativa, sul portatile dello studente: `python
  scaffolding/check_lab08.py` senza flag legge il suo `working/tools.py`.
- `unable to open database file` o `no such table` **senza** aver toccato il
  database → la cartella del corso ha un `#` o un `?` nel nome e il file è
  una versione vecchia di `tools.py` (con `f"file:{DB}?mode=ro"`): `DB.as_uri()`
  lo evita.
- `no such table` anche dopo aver sistemato il caso 3 → è rimasto il
  `lumen.db` vuoto e la funzione controlla solo che il file esista: si
  cancella il file vuoto, e la query va in un `try`/`except` (come la
  soluzione).
- `TypeError: 'NoneType' object is not subscriptable` → `fetchone()` ha
  restituito `None` (codice inesistente, o minuscolo senza `upper()`).
- Dopo il caso 3 compare un `lumen.db` di 0 byte → la connessione non è in
  sola lettura; va cancellato prima di rimettere il nome giusto al file
  vero. Se il file vero è stato sovrascritto: `python
  scaffolding/make_dataset.py` lo rigenera identico.
- `sqlite3.ProgrammingError: Incorrect number of bindings supplied … there
  are 8 supplied` → il parametro è stato passato come stringa e non come
  tupla: `(codice,)`.
- `ValueError: tool sconosciuto: prezzo_prodotto` → manca il ramo in
  `esegui()`, o il nome non combacia con `TOOLS`.
- «Quanto costa la LMX-4400?» usa ancora `query_db` con `prezzo_prodotto`
  in `TOOLS` → la docstring di `PrezzoProdotto` manca o non dice che dà il
  prezzo dato il codice.
- `(mi fermo: 6 chiamate senza una risposta)` → il modello ha continuato a
  chiedere tool (di solito la calcolatrice su troppe righe): è il tetto
  che funziona, si riformula la domanda.
