# Modulo 2 · Lezione 4 — Data Loading · consegna

Stasera si insegna al codice a **leggere i file**: PDF, Word, pagine web,
Markdown — e poi due formati in più che aggiungete voi. Tutto in un unico
file, `working/loaders.py`, e tutto si lancia dalla cartella `scripts/`.

## Setup (una volta sola, nei primi minuti)

Ogni lezione ha la sua cartella `scripts/` con il suo venv. **Attenzione, una
cosa cambia rispetto alla lezione scorsa:** non c'è più una cartella
`starter/` — il venv si crea direttamente in `scripts/`.

Aprite il terminale **nella cartella della lezione**: è quella scaricata da
Drive, quella che contiene `scripts/`. Per esserne sicuri, prima di tutto
lanciate `ls` (su Windows `dir`): fra i nomi che escono deve esserci
`scripts`. Se non c'è, siete altrove — spostatevi con `cd` fino a vederlo.
Poi:

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # dentro: la STESSA chiave OpenAI di Modulo 2 · Lezione 1 – Modulo 2 · Lezione 3
```

> Chiave persa (laptop cambiato, `.env` cancellato)? **Alzate la mano**: il
> docente ha una chiave di riserva.

Il caricamento dei documenti gira anche **senza** chiave: senza, il file
carica e stampa tutto lo stesso, solo la domanda al modello viene saltata. In
quel caso il vostro «fatto quando» è la parte di caricamento — i Document e i
metadata stampati — e la risposta del modello la guardate su quella del
docente.

Tutto, per tutta la serata, si lancia **da `scripts/`**. Se vedete
`ModuleNotFoundError: aikit` quasi sempre è questo: siete dentro un'altra
cartella. Tornate in `scripts/` e rilanciate.

## Che cosa c'è già, e non si tocca

`scaffolding/aikit/` è il vostro toolkit: dentro ci sono `llm_client.py` e
`pricing.py`, **gli stessi file che avete scritto voi la lezione scorsa**.
Cambia la cartella, non il codice. Accanto c'è `ask.py`, il banco di prova:
fa la domanda al modello e stampa il risultato. Si importano, non si
riscrivono.

In `scaffolding/` trovate anche `check_lab04.py`, `make_dataset.py` e
`confronto_html.py`: sono **attrezzi del docente** (verifica dei materiali,
rigenerazione del dataset, misure per le slide). **Non lanciateli**: uno di
loro fa chiamate vere al modello, e nessuno vi dice niente che non vediate già
a schermo. Il vostro criterio di "fatto" è quello che stampa
`python working/loaders.py`. Se restate bloccati, chiamate il docente: ha lui
lo strumento per capire in dieci secondi che cosa non torna.

## Live coding col docente (🎤 si replica) — `working/loaders.py`

| TODO | Cosa | Fatto quando |
|---|---|---|
| 1 | `load_pdf` | il main stampa **3 Document** per `relazione-annuale.pdf`, uno per pagina, e il modello risponde sul fatturato |
| 2 | `load_docx` | un Document con tutto il verbale, e il modello sa dirvi la città del secondo showroom |
| 3 | `load_html` | la domanda sulla garanzia del telaio cambia risposta: **prima il modello dice 10 anni, dopo dice 5** |
| 4 | `load_markdown` | il testo della guida esce senza cancelletti né pipe della tabella |
| 5 | `load` | la porta unica: ogni file del `dataset/` passa dal loader giusto — tranne `.txt` e `.csv`, che danno `ValueError`. Quelli sono il vostro pezzo |

## Esercizio (⌨️ da soli) — sempre `working/loaders.py`

Avete visto il pattern quattro volte. Ora tocca a voi: due formati nuovi,
stessa interfaccia. **Prescritti solo i nomi, la firma e lo scopo**: il come è
vostro — soluzioni diverse sono benvenute.

| TODO | Cosa | Fatto quando |
|---|---|---|
| 6 | `load_txt` | il main stampa il Document delle note e il modello conta le segnalazioni E07 |
| 7 | `load_csv` + agganciare i due loader a `load()` | il main stampa i Document degli ordini e nessuna riga di `load()` dice più `ValueError` |

Per il CSV la scelta è vostra: **una riga = un Document**, oppure tutto il file
in uno solo? Non c'è una risposta giusta — ma pensate a che cosa ci farete
dopo, quando questi Document finiranno in un motore di ricerca. Alla fine ne
parliamo insieme: chi ha scelto diversamente racconta perché.

```bash
python working/loaders.py       # il vostro giro completo (~$0.002 a lancio)
```

**Finito prima?** Scrivete anche l'**altra** granularità del CSV — quella che
non avete scelto — e rilanciate: la risposta a «quanti ordini risultano
consegnati?» cambia? E se al posto di quella domanda ne mettete una su un
cliente solo? Portate al reveal quello che avete visto.

## Cosa portate a casa

`loaders.py` scritto in prima persona. Dalla prossima lezione entra nel
toolkit come `aikit/loaders.py`, e sopra ci si costruisce la pulizia del testo
(Modulo 2 · Lezione 5): il testo che avete estratto stasera è ancora sporco —
guardate le intestazioni ripetute in cima a ogni pagina del PDF.
