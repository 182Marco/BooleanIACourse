# Modulo 3 · Lezione 8 — Tool Implementation · consegna

Si lavora in **un solo file**: `working/tools.py`, lo stesso della lezione
scorsa con un tool nuovo. Dentro ci sono, nell'ordine: `DB`, `LIMITE` e
`MAX_CHIAMATE` in cima; la calcolatrice e la data; **`QueryDb` e
`query_db()`, già scritti**; **il TODO** (`prezzo_prodotto`);
`definisci_tool()` e `TOOLS`; `esegui()`; il giro `chiedi()`; gli helper di
stampa e il main con le tre `DOMANDE`. Tutto tranne il TODO è già scritto:
il docente lo spiega, voi seguite sul file, non si ricopia niente.

Il database è `dataset/lumen.db`: quattro tabelle (`prodotti`, `clienti`,
`ordini`, `righe_ordine`). Per guardarci dentro senza modello:

```bash
python scaffolding/sql.py                                  # le tabelle, le colonne, quante righe
python scaffolding/sql.py "SELECT * FROM prodotti LIMIT 5"  # una query, in sola lettura
```

Serve `OPENAI_API_KEY` in `.env`: la più semplice è copiare il file `.env`
della lezione scorsa (la cartella `scripts/` di Modulo 3 · Lezione 7) in
questa cartella `scripts/`. Setup (venv, `requirements.txt`, `.env`): in
`README.md`, sezione Setup; nessuna
libreria nuova, `sqlite3` è già in Python. Si lancia tutto dalla cartella
`scripts/`: `python working/tools.py`. Ogni lancio sono tre domande e sei
chiamate al modello, circa un decimo di centesimo.

Per provare una domanda sola si mette in `SOLO`, in cima al file:
`SOLO = "Quanto costa la LMX-4400?"`. In `scaffolding/` c'è anche
`check_lab08.py`: è uno strumento del docente, non va lanciato; il «fatto
quando» si vede a schermo.

## Codice spiegato — query_db (già nel file)

1. `QueryDb` ha un solo campo, `sql`. La sua docstring è la descrizione del
   tool, e contiene lo **schema** del database: tabelle, colonne e tipi. Il
   modello vede questo, non i dati.
2. `query_db(sql)` esegue la query del modello: rifiuta tutto ciò che non è
   un `SELECT`, apre il database **in sola lettura** (`mode=ro`), rimanda al
   massimo `LIMITE` righe, e se qualcosa va storto **ritorna l'errore come
   testo** invece di sollevarlo: il modello lo legge e può correggersi.
3. In `esegui()` c'è il ramo `query_db`; in `chiedi()` il tetto
   `MAX_CHIAMATE`.

Lanciato così com'è, il main risponde bene a «Quanti ordini ha fatto Giulia
Moretti?» (13) e **male** alle altre due: «Quanti ordini sono ancora in
viaggio?» dice che non ce ne sono (sono 5: il modello non sa che lo stato si
chiama `spedito`), e «Quanto costa la LMX-4400?» di solito cerca il codice
nella colonna `nome` e non lo trova.

## Esercizio — prezzo_prodotto e i tre casi rotti (⌨️ da soli)

Un'ora, così: 20 minuti il TODO, 10 la domanda sul prezzo, 20 i tre casi
rotti, il resto per «se finisci prima».

### TODO — `prezzo_prodotto`

Un tool che ritorna **nome e prezzo di listino** di un prodotto, dato il
suo codice (per esempio `LD-210`). La differenza con `query_db`: qui il
modello passa **solo il codice**, la query la scrivete voi, fissa, con il
**segnaposto** `?` e il valore passato a parte:

```python
con.execute("SELECT nome, prezzo FROM prodotti WHERE codice = ?", (codice,))
```

Mai il codice incollato nella stringa con un f-string: è testo che arriva
dal modello, e incollato può cambiare la query. Tre cose, nei tre punti segnati `TODO` nel file:

1. La **classe** `PrezzoProdotto` e la **funzione** `prezzo_prodotto(codice)`:
   nel file sono già abbozzate. Scrivi la docstring della classe (è la
   descrizione che il modello legge) e il corpo della funzione, che ritorna
   una **stringa**. La riga si legge con `fetchone()`, che ritorna `None` se
   il codice non c'è.
2. La **voce in `TOOLS`**.
3. Il **ramo in `esegui()`**.

Poi rilancia con `SOLO = "Quanto costa la LMX-4400?"`: quale tool usa
adesso il modello? E perché? Basta un lancio.

### I tre casi rotti

Uno alla volta, con `SOLO`. Se il programma muore, sistema
`prezzo_prodotto` e rilancia.

1. **Un codice che non esiste**: `SOLO = "Quanto costa la LMX-9999?"` →
   risposta attesa: il prodotto non è nel listino.
2. **Un codice scritto male**: `SOLO = "Quanto costa il codice lmx-4400,
   scritto esattamente così?"` → risposta attesa: **89 euro** (il codice va
   sistemato: maiuscolo, senza spazi ai lati). La domanda dice «esattamente
   così» perché altrimenti il modello spesso corregge il codice da solo:
   controlla che nella riga `function_call prezzo_prodotto(...)` arrivi
   davvero `lmx-4400` minuscolo.
3. **Il database che non c'è**: rinomina `dataset/lumen.db` in
   `dataset/lumen-vecchio.db` (in VS Code: tasto destro sul file, Rinomina)
   e rilancia la domanda sulla LMX-4400 → risposta attesa: il listino non
   si raggiunge. Poi rimetti a posto, in quest'ordine:
   - se nella cartella `dataset/` è comparso un nuovo `lumen.db` vuoto,
     **prima** cancellalo (lo crea `sqlite3.connect()` quando il file non
     c'è, a meno di aprirlo in sola lettura come fa `query_db`);
   - **poi** rinomina `lumen-vecchio.db` di nuovo in `lumen.db`.

   Se per sbaglio hai cancellato il database vero: `python
   scaffolding/make_dataset.py` lo rigenera identico.

**Fatto quando:** sui tre casi rotti il programma non muore e il modello dà
la risposta attesa (non è nel listino · 89 euro, con `prezzo_prodotto` che
riceve `lmx-4400` minuscolo · il listino non si raggiunge); e su «Quanto
costa la LMX-4400?» sai dire quale tool ha usato il modello, e perché.

### Se qualcosa non torna

| Cosa vedi | Cosa controllare |
|---|---|
| `ModuleNotFoundError: No module named 'openai'` (o `dotenv`, `pydantic`) | il venv non è attivo o manca `pip install -r requirements.txt`: README, sezione Setup |
| `TypeError: 'NoneType' object is not subscriptable` | `fetchone()` ha restituito `None`: il codice non è nel database. Controlla `None` prima di leggere la riga |
| `sqlite3.OperationalError: no such table: prodotti` | il file del database non è quello giusto (o non c'è, e `connect()` ne ha creato uno vuoto) |
| `no such table` anche dopo aver sistemato il caso 3 | è rimasto il `lumen.db` vuoto di una prova precedente: cancellalo e rilancia. Una query dentro un `try`/`except`, come in `query_db`, regge anche questo caso |
| `sqlite3.OperationalError: unable to open database file` | il file non c'è e la connessione è in sola lettura: è il caso 3, va gestito |
| `ValueError: tool sconosciuto: prezzo_prodotto` | il modello ha chiesto il tool, ma in `esegui()` manca il ramo (o il nome è scritto diverso da `TOOLS`) |
| `KeyError: 'codice'` in `esegui()` | il campo di `PrezzoProdotto` e la chiave letta in `esegui()` non hanno lo stesso nome |
| `KeyError: 'operazione'` (o un altro nome storpiato) in `esegui()` | il modello ha sbagliato il nome di un argomento di un altro tool: non è il vostro codice, si rilancia |
| `sqlite3.ProgrammingError: Incorrect number of bindings` | il parametro va passato come tupla: `(codice,)`, con la virgola |
| Il modello usa ancora `query_db` sul prezzo | `prezzo_prodotto` non è in `TOOLS`, o nome e descrizione non dicono che dà il prezzo dato il codice |
| Il modello risponde con una domanda di cortesia in coda | `ISTRUZIONI` è stata cambiata; non è un errore |

## Se finisci prima

Un secondo tool con la query fissa: `stato_ordine(id)`, che ritorna lo
stato di un ordine e la data di consegna (o «non ancora»), e un messaggio
chiaro se l'ordine non c'è. Domande: «A che punto è l'ordine 1297?» e «A che
punto è l'ordine 9999?». **Fatto quando:** la 1297 risulta spedita e non
ancora consegnata, la 9999 dà un messaggio chiaro. Poi rilancia «Quanti
ordini sono ancora in viaggio?»: cambia qualcosa?
