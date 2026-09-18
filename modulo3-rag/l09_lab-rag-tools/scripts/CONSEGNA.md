# Modulo 3 · Lezione 9 — Lab: RAG + Tools · consegna

Si lavora in `working/assistente.py`, e nel Lab 2 si annota in
`working/griglia.md`. Dentro il file ci sono, nell'ordine: le costanti
(`K`, `MAX_CHIAMATE`), le `DOMANDE` con la strada attesa, `LAB2` (nel Lab 2
si mette `True`: le domande stanno in `working/domande_lab2.py`),
`LE_MIE_DOMANDE` vuota, `SOLO`; **tre TODO**; il giro `chiedi()`, che è quello delle due
lezioni scorse con dentro il pezzo del TODO 1; `strada()`, gli helper di
stampa e il main, che in fondo stampa la tabella **strada attesa / strada
presa**.

L'assistente ha **due tool**: `query_db` (quello di Modulo 3 · Lezione 8,
importato da `scaffolding/aikit/tools.py`) e `cerca_documenti` (il RAG
come tool: lo scrivete oggi). Gli altri tool di `tools.py`
(`prezzo_prodotto`, `data_oggi`, `calcolatrice`) oggi restano fuori:
`strada()` conosce solo questi due. La giornata: il Lab 1 in tre parti (si
attacca un tool, si scrive il secondo, si scrivono le istruzioni), poi il
Lab 2 (si prova con le domande del docente e si sistema).

## Setup (10')

Dalla cartella `scripts/` di questa lezione (nessuna libreria nuova: sono le
stesse di Modulo 3 · Lezione 6):

```bash
cd scripts            # dalla cartella della lezione; se sei già in scripts/, salta questa riga
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Poi la chiave: copia il file `.env` dalla cartella `scripts/` della
lezione scorsa, ovunque tu l'abbia salvata, dentro questa cartella
`scripts/` (se le cartelle sono quelle del repo: `cp
../../lezione-08-tool-implementation/scripts/.env .env`). Se non ce l'hai
più: `cp .env.example .env`, alza la mano, e incolla dentro la chiave che
ti dà il docente.

Si lancia tutto dalla cartella `scripts/`: `python working/assistente.py`.
Lancialo subito: al primo avvio indicizza la collection dei documenti (una
riga per documento, la riga dell'embedding, un'attesa di un paio di
minuti, poi «indicizzati 82 chunk», meno di un centesimo). Le volte dopo
parte subito. Quel primo lancio risponde a tutto da sé, senza tool
(`TOOLS` è vuota): la tabella dice `nessuna` su tutte le righe, e in fondo
`strada giusta: 1/4`, perché solo Padova coincide. È la baseline, non è
rotto.

## Le strade

Ogni domanda ha una **strada attesa**, e il main stampa quella **presa**
(sotto ogni risposta, riga `strada:`):

| Strada | Tool | Esempio |
|---|---|---|
| documenti | `cerca_documenti` | «Entro quanti giorni posso restituire un prodotto?» |
| dati | `query_db` | «Quanti ordini ha fatto Giulia Moretti?» |
| documenti+dati | tutti e due | «Lorenzo Rossi può montare il braccio LMX-4400 sulle scrivanie che ha ordinato?» |
| nessuna | nessuno | «Che tempo fa oggi a Padova?»: la risposta non sta da nessuna parte, e l'assistente lo dice |

Si prova una domanda alla volta mettendola in `SOLO`, in cima al file:
`SOLO = "Quanti ordini ha fatto Giulia Moretti?"`. Con `SOLO = None` il
main fa tutte le `DOMANDE` e stampa la tabella.

## Lab 1a — attaccare un tool (45') · TODO 1

Il tool esiste già: `QueryDb` (lo schema, con lo schema del database nella
docstring) e `query_db(sql)` sono importati in cima al file da
`scaffolding/aikit/tools.py`. Quello che manca è il **cablaggio**, in tre
punti:

1. **La voce in `TOOLS`**: `definisci_tool(QueryDb, "query_db")`. Dalla
   classe Pydantic fa la definizione che il modello legge: la docstring
   come descrizione, i campi come parametri. `TOOLS` è la lista che il
   modello vede a ogni chiamata.
2. **Il ramo in `esegui()`**: se `nome` è `"query_db"`, ritorna
   `query_db(argomenti["sql"])`. La chiave `"sql"` è il campo di `QueryDb`.
3. **Il ciclo dentro `chiedi()`**, dove c'è scritto TODO 1. Il giro ha già
   chiamato il modello, ha messo l'output in `storia` e ha raccolto in
   `chiamate` gli item `function_call`. Per ognuna: gli argomenti con
   `json.loads(chiamata.arguments)` (è una stringa JSON), il risultato con
   `esegui(chiamata.name, argomenti)`, il nome in `usati` (il log della
   strada), la stampa con `stampa_esecuzione(nome, argomenti, risultato)`,
   e il risultato in `storia` come `{"type": "function_call_output",
   "call_id": chiamata.call_id, "output": str(risultato)}`. Il `call_id`
   è lo stesso della richiesta: così il modello sa a cosa stai rispondendo.
   Poi il `while` ricomincia e il modello riceve tutto.

**Fatto quando:** `SOLO = "Quanti ordini ha fatto Giulia Moretti?"`
risponde 13, e sotto la risposta c'è `strada: dati  (tool: query_db)`.

## Lab 1b — il RAG come tool (40') · TODO 2

La classe `CercaDocumenti` ha un solo campo, `domanda`; la sua docstring
è la **descrizione** che il modello legge per decidere se usare il tool:
scrivetela voi (cosa cerca, in quali documenti, cosa ritorna). La
funzione `cerca_documenti(domanda)` chiama `rag.recupera(domanda, K)`, che
ritorna i `K` chunk più pertinenti (dict con `id`, `testo`, `score`,
`source`), e li restituisce come **un solo testo** in cui ogni chunk ha
davanti il suo id tra parentesi quadre: così il modello può citarlo.
Ritorna una stringa. Non si passa `rag.rispondi()`: il modello deve vedere
i chunk, per citarli e per metterli insieme ai dati.

Poi lo attaccate come nel Lab 1a: la seconda voce in `TOOLS`
(`definisci_tool(CercaDocumenti, "cerca_documenti")`) e il secondo ramo in
`esegui()`. Il ciclo in `chiedi()` non cambia: vale per qualunque tool.

**Fatto quando:** la domanda sui resi risponde «30 giorni» citando un id
(`[policy-resi-garanzia-…]`), e la domanda su Lorenzo Rossi ha
`strada: documenti+dati`. Se esce `dati` da solo, rilanciala: il modello
può oscillare.
Al rientro il docente mostra la sua versione: chi non ha finito la
ricopia durante la pausa.

## Lab 1c — le istruzioni (25') · TODO 3

`ISTRUZIONI` valgono a ogni chiamata del giro. Adesso sono quelle di
Modulo 3 · Lezione 7 («Rispondi in italiano, in una frase»): devono dire
al modello chi è e di cosa parla (Lumen); **quando usare quale tool**
(documenti → `cerca_documenti`, ordini/clienti/prezzi → `query_db`, tutti e
due se servono); che **cita** i passaggi usati con l'id tra parentesi
quadre, per esempio `[policy-resi-garanzia-001]`; cosa fa quando **la
risposta non c'è**: dice di non averla trovata, e dove ha cercato, senza
inventare; e cosa fa con una domanda che non riguarda Lumen: lo dice,
senza usare i tool. Le regole di citazione e di rifiuto di `rag.py` da
oggi stanno qui: la costante `ISTRUZIONI` in cima a
`scaffolding/aikit/rag.py`. Di quella si riusa la forma della citazione
con l'id; il resto («usando SOLO le informazioni nei documenti», «Non lo
trovo nei documenti») parla di una fonte sola: copiato così com'è vieta il
database. Va riscritto per due fonti.

**Fatto quando:** con `SOLO = None` la tabella in fondo dice `4/4`, e la
domanda su Padova viene rifiutata senza chiamare tool. Al rientro il
docente mostra le sue istruzioni: chi non è a 4/4 le ricopia prima del
Lab 2. Se una riga dice
NO, rilancia quella domanda in `SOLO` due volte: se almeno una volta passa
a sì, conta come fatta (il modello oscilla); se resta NO tutte e due le
volte, è una cosa da sistemare nelle istruzioni.

## Se qualcosa non torna

| Cosa vedi | Cosa controllare |
|---|---|
| `ancora da scrivere: TODO 1` | il modello ha chiesto un tool e il ciclo che lo esegue non c'è ancora |
| `ValueError: tool sconosciuto: query_db` | il tool è in `TOOLS` ma manca il ramo in `esegui()` (o il nome è scritto diverso) |
| `KeyError: 'sql'` o `KeyError: 'domanda'` in `esegui()` | il campo dello schema e la chiave letta in `esegui()` non hanno lo stesso nome |
| il modello chiede lo stesso tool a ogni chiamata, fino a `(mi fermo: 6 chiamate…)` | il risultato non torna al modello: manca la `function_call_output` in `storia`, o il `call_id` non è quello della richiesta |
| `ancora da scrivere: TODO 2` | il modello ha chiesto `cerca_documenti` e la funzione non c'è ancora |
| il modello non usa mai `cerca_documenti`, o lo usa a caso | la docstring di `CercaDocumenti` è ancora quella del TODO 2: il modello la legge così com'è, senza errori |
| strada `nessuna` su tutte le domande | `TOOLS` è vuota: il modello non ha niente da chiamare |
| il tool si esegue (`eseguo query_db: …`) e risponde, ma `strada: nessuna` | manca `usati.append(chiamata.name)` nel ciclo: il log della strada è vuoto |
| `OPENAI_API_KEY` non impostata, subito all'avvio | hai lanciato da un'altra cartella: `cd scripts`, poi `python working/assistente.py` |
| risponde dai documenti ma senza `[id]` | le `ISTRUZIONI` non dicono di citare, o `cerca_documenti` non mette gli id davanti ai chunk |
| «Non ho trovato…» su una domanda che nei documenti c'è | guarda i chunk stampati sotto `eseguo cerca_documenti`: se il passaggio giusto c'è, sono le istruzioni; se non c'è, è il retrieval (Modulo 3 · Lezione 6) |
| la prima domanda ci mette due minuti | sta indicizzando `lumen_m3`: è normale, la seconda volta parte subito |
| `ValueError: too many values to unpack` (o `not enough values`) nel main | una voce di `LE_MIE_DOMANDE` non è una tupla `("domanda", "strada attesa")`: manca la strada, o le parentesi |

## Lab 2 — provare e sistemare (45')

Le domande sono **le vostre di Modulo 3 · Lezione 6**: quelle che avete
scritto voi e che il RAG da solo sbagliava (la risposta stava in un
ticket o in un changelog, e il retrieval portava altro), più una doppia.
Oggi le fate all'assistente. La differenza è che il RAG è un tool: il
modello può leggere i passaggi, decidere che non rispondono, e chiamare
`cerca_documenti` **di nuovo con altre parole**. Nel log si vede: `tool:
cerca_documenti → cerca_documenti`, e sopra ogni chiamata la domanda che
ha usato.

Le dieci domande sono in `working/domande_lab2.py`, già con la strada
attesa: non si copiano. In cima ad `assistente.py` mettete `LAB2 = True`
e lanciate con `SOLO = None`: il main fa le quattro `DOMANDE` più queste
dieci, due o tre minuti. Le domande vostre vanno in `LE_MIE_DOMANDE`
(stessa forma: tuple `("domanda", "strada attesa")`, con la virgola).

Per ogni domanda una riga in `working/griglia.md`: strada presa (dal
log), quante volte ha cercato e con quali parole, e l'**esito**: giusta ·
strada sbagliata · risposta sbagliata · inventata (la legenda è nella
griglia). Qui la strada è quasi sempre giusta: quello che conta è la
risposta. Per sapere la risposta vera si leggono i documenti in
`dataset/lumen_m3/`: i ticket sono in `ticket-supporto.txt`, i rilasci
in `changelog-rilasci.txt`. Per la doppia, il database con
`scaffolding/sql.py`:

```bash
python scaffolding/sql.py
python scaffolding/sql.py "SELECT o.id, SUM(r.quantita * r.prezzo_unitario) AS totale, o.spese_spedizione FROM ordini o JOIN righe_ordine r ON r.ordine_id = o.id WHERE o.id = 1296"
```

Una risposta che dice «non ho trovato» quando la risposta nei documenti
c'è è «risposta sbagliata». Una che cita un passaggio che non c'entra è
«inventata».

Poi si sistema. Per ogni domanda sbagliata scegli **una** leva, tutte e
due nel vostro file (`K` oggi resta 4: non è una leva, il retrieval
l'avete curato a Modulo 3 · Lezione 6):

| Leva | Dove | Quando serve |
|---|---|---|
| le istruzioni | `ISTRUZIONI` | ha risposto con i primi passaggi senza cercare ancora; ha citato un passaggio fuori tema; ha risposto dal manuale quando la risposta era in un ticket. Per esempio: «se i passaggi trovati non contengono la risposta, chiama di nuovo cerca_documenti con parole diverse», «se un passaggio è un ticket di supporto, cita il suo codice TCK» |
| la descrizione del tool | la docstring di `CercaDocumenti` | il modello non entra nei documenti, o non sa che ci sono i ticket con i casi risolti: dirglielo nella descrizione (cosa c'è, cosa non c'è) |

Cambi la leva, rilanci il main con **tutte** le domande e scrivi «dopo» in
griglia: se una domanda che era giusta ora non lo è più, va scritto. Il
modello non è deterministico: prima di dire che una leva ha rotto
qualcosa, rimetti quella domanda in `SOLO` e rilanciala due volte. Un
giro completo sono quattordici domande, 4-10 secondi l'una: prima di ogni
rilancio pensa se ti serve tutto o basta `SOLO`.

**Fatto quando:** almeno **due domande sbagliate** sono sistemate senza
romperne altre.

**Se finisci prima:** scrivi domande tue, e provale dove pensi che
sbagli: una doppia («il cliente X ha comprato Y: ha diritto a Z?»), una su
un dato che il database non ha, una fuori da tutto.
