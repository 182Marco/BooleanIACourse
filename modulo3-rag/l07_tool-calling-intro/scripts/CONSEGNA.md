# Modulo 3 · Lezione 7 — Tool Calling Intro · consegna

Si lavora in **un solo file**: `working/tools.py`. Dentro ci sono, nell'ordine:
la calcolatrice (schema Pydantic + funzione), **il TODO** (il secondo tool),
`definisci_tool()` e la lista `TOOLS`, `esegui()`, il giro `chiedi()`, gli
helper di stampa e il main con le quattro `DOMANDE`. Tutto tranne il TODO è
**già scritto**: il docente lo spiega, voi seguite sul file, non si ricopia
niente.

Serve `OPENAI_API_KEY` in `.env` (la stessa del Modulo 2). Setup (venv,
`requirements.txt`, `.env`): in `README.md`, sezione Setup. Si lancia tutto
dalla cartella `scripts/`: `python working/tools.py`. Ogni lancio sono
quattro domande e sei chiamate al modello (sette con il secondo tool),
meno di un decimo di centesimo.

Per provare una domanda sola si mette in `SOLO`, in cima al file:
`SOLO = "Che giorno è oggi?"`. In `scaffolding/` c'è anche
`check_lab07.py`: è uno strumento del docente, non va lanciato; il «fatto
quando» si vede a schermo.

## Codice spiegato — il giro con la calcolatrice (già nel file)

1. `Calcolatrice` è lo schema Pydantic degli **argomenti** (`a`, `b`,
   `operazione`) e `calcolatrice()` la funzione che li esegue.
2. `definisci_tool(schema, nome)` trasforma lo schema nella definizione che
   l'API si aspetta: nome, descrizione (la docstring), parametri
   (`model_json_schema()`). `TOOLS` è la lista che il modello vede.
3. `esegui(nome, argomenti)` esegue il tool che il modello ha chiesto: un
   `if` sul nome.
4. `chiedi(domanda)` è il giro: chiama il modello con la conversazione
   (`storia`, che parte dalla domanda) e `TOOLS`; se nell'output ci sono
   item `function_call`, esegue ognuno e rimanda il risultato come
   `function_call_output` con lo stesso `call_id`; ripete finché arriva
   testo.

Lanciato così com'è, il main risponde bene a «Quanto fa 849 diviso 1,22?»
(695,90, con il tool) e **male** a «Che giorno è oggi?» (una data del 2024):
non ha un tool per saperlo.

## Esercizio — il secondo tool (⌨️ da soli)

Un'ora, così: 20 minuti il TODO, 10 le quattro domande, 15 la prova, il
resto per «se finisci prima».

### TODO — `data_oggi`

Tre cose, nei tre punti segnati `TODO` nel file:

1. Lo **schema** `DataOggi` (una classe senza campi: il tool non ha
   argomenti, e la docstring è la descrizione che il modello legge) e la
   **funzione** `data_oggi()`, che ritorna la data di oggi come stringa
   (`date.today().isoformat()`, `date` è già importato).
2. La **voce in `TOOLS`**: `definisci_tool(DataOggi, "data_oggi")`.
3. Il **ramo in `esegui()`**: `if nome == "data_oggi": return data_oggi()`.

Poi rilancia il file e guarda le quattro domande: quali tool chiama il
modello per ognuna? La terza di solito ne chiede **due nella stessa
risposta** (se li chiede uno alla volta va bene lo stesso); la quarta
nessuno.

### La prova: nome e descrizione generici

Quando le quattro domande vanno bene, rendi il secondo tool illeggibile
per il modello: cambia il nome in `TOOLS` in `"strumento_2"` (e nell'`if`
di `esegui()`, che deve combaciare) e la docstring di `DataOggi` in
`"Uno strumento utile."`. Rilancia: «Che giorno è oggi?» torna a una data
inventata, perché il modello non ha più modo di capire a cosa serve il
tool e non lo chiama. Basta **un lancio per configurazione**: i «5 su 5»
delle slide li abbiamo misurati noi. Poi rimetti a posto nome e
descrizione.

Prova anche a cambiarne **uno solo** dei due: con il nome buono e la
descrizione generica il modello lo chiama lo stesso, e viceversa: basta
che uno dei due dica a cosa serve il tool. La prova si giudica sulla **seconda** domanda,
quella sola sulla data: sulla terza, avendo già deciso di usare la
calcolatrice, il modello di solito chiama anche il tool generico.

**Fatto quando:** con nome e descrizione buoni le quattro domande usano i
tool giusti (calcolatrice · data · entrambi · nessuno) e la seconda dà la
data di oggi; con nome e descrizione generici la seconda torna a una data
del 2024, e l'hai visto sul tuo schermo.

### Se qualcosa non torna

| Cosa vedi | Cosa controllare |
|---|---|
| `ModuleNotFoundError: No module named 'openai'` (o `dotenv`, `pydantic`) | il venv non è attivo (`source .venv/bin/activate`, su Windows `.venv\Scripts\activate`) o manca `pip install -r requirements.txt`: README, sezione Setup |
| `400 … No tool output found for function call call_…` | manca il `function_call_output` per una delle `function_call`, o il `call_id` non è quello della richiesta |
| `400 … No tool call found for function call output` | nell'input della seconda chiamata manca la `function_call` originale: `storia += r.output` deve rimandare tutto l'output |
| `400 … Invalid type for 'input[…].output'` | `output` deve essere una stringa: `str(risultato)` |
| `ValueError: tool sconosciuto: data_oggi` | il modello ha chiesto il tool, ma in `esegui()` manca il ramo con quel nome (o il nome è scritto diverso da `TOOLS`) |
| `TypeError: … not subscriptable` su `chiamata.arguments` | `arguments` è una stringa JSON: prima `json.loads()`, poi `argomenti["a"]` |
| `400 … 'additionalProperties' is required to be supplied and to be false` | hai messo `strict: True`: con lo schema di `model_json_schema()` serve `False` |
| «Che giorno è oggi?» dà ancora una data del 2024 | il tool non è in `TOOLS`, o nome e descrizione non dicono cosa fa |

## Se finisci prima

Un **terzo tool con parametri**: la conversione di valuta a tasso fisso
(schema con `importo`, `da`, `a`; un dizionario di tassi nella funzione).
Domande: «Quanti sono 120 euro in dollari?». Poi la stessa prova di prima:
con nome `strumento_3` e descrizione «Uno strumento utile.» il modello lo
chiama **lo stesso**, perché i nomi dei parametri gli bastano; con i
parametri rinominati `x`, `y`, `z` non lo chiama più. Di un tool il modello
conosce solo nome, descrizione e parametri: se nessuno dei tre dice a cosa
serve, non ha altro modo di capirlo.
