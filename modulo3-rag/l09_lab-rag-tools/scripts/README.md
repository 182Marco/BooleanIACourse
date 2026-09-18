# Modulo 3 · Lezione 9 — Lab: RAG + Tools · guida agli script

Lab da 4 ore (📊 brief + ⌨️ il Lab 1 in tre parti + ⌨️ Lab 2): il RAG del
modulo e il giro del tool calling delle due lezioni scorse diventano **un
assistente solo** con **due tool**, `query_db` (di Modulo 3 · Lezione 8) e
`cerca_documenti` (il RAG come tool, che ritorna i chunk con i loro id).
L'assistente sceglie se cercare nei documenti Lumen, interrogare il
database degli ordini, o tutti e due; e quando la risposta non sta da
nessuna parte lo dice invece di inventare. Il codice sta tutto in **un
file**, `working/assistente.py`: tre TODO, uno per parte del Lab 1 (il
cablaggio di `query_db`, compreso il ciclo del giro che esegue le
`function_call`; il tool RAG; le `ISTRUZIONI`), il resto del giro già
scritto con il **log della strada presa**, e in fondo la tabella strada
attesa / strada presa. Nel Lab 2 si prova con le domande degli studenti di
Modulo 3 · Lezione 6, quelle che il RAG da solo sbagliava, e si sistema
con due leve. Le domande e gli esiti si annotano in
`working/griglia.md`.

Le domande del Lab 2 sono in `working/domande_lab2.py`; le risposte vere e gli esiti
misurati **non sono in questa cartella**: stanno in
`domande-lab2-docente.md`, un livello sopra `scripts/`.

> **Per gli studenti:** servono la sezione **Setup** e le prime due righe
> di **Come si prova**. Il resto, da «La giornata» in poi, è per il
> docente.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · ⌨️ da completare dagli studenti
· 📄 documenti/dati di esempio. (Oggi non c'è live coding del docente:
tutti i blocchi pratici sono ⌨️; nei due rientri il docente mostra il suo
pezzo dalle slide.)

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Le stesse dipendenze di Modulo 3 · Lezione 6: nessuna libreria nuova. |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` (la stessa del Modulo 2). |
| `CONSEGNA.md` | ⌨️ | Il setup, le strade, i TODO 1-3 (Lab 1a, 1b, 1c) con i criteri di «fatto» e gli errori tipici, il Lab 2 con le due leve. |
| `scaffolding/aikit/` | 🧰 | Il toolkit: i sette moduli del Modulo 2 + `rag.py`, `hybrid.py`, `rerank.py` (identici a Modulo 3 · Lezione 6) + **`tools.py`**, la soluzione di Modulo 3 · Lezione 8 promossa (intatta: contiene ancora i quattro tool di quella lezione; oggi `assistente.py` importa solo `QueryDb`, `query_db` e `definisci_tool`). Usa anche `rag.recupera()` / `rag.CONFIG` / `rag.indicizza()`, `vectorstore.apri_collection()`, `cost_usd()` di `llm_client.py`. Non si toccano: le leve stanno tutte in `assistente.py`. |
| `scaffolding/make_dataset.py` | 🧰 | Il generatore del corpus (Modulo 3 · Lezione 2): serve al check per verificare che i documenti siano intatti. Non si lancia in aula. |
| `scaffolding/make_db.py` | 🧰 | Il generatore di `dataset/lumen.db` (seed fisso, si rigenera identico). Non si lancia in aula. |
| `scaffolding/sql.py` | 🧰 | Una query a mano in sola lettura: senza argomenti stampa lo schema. Gli studenti lo usano nel Lab 2 per sapere la risposta vera sui dati. |
| `scaffolding/check_lab09.py` | 🧰 | **Strumento del docente**: base istantaneo senza rete (struttura e scaffolding intatto; TODO 1 con un client finto: `TOOLS`, `esegui()`, il ciclo che rimanda la `function_call_output` con lo stesso `call_id`; TODO 2 con il retrieval finto; TODO 3; il tetto e `strada()`); `--solutions` per la versione completa; `--live` con la chiave vera (le quattro `DOMANDE` prendono la strada attesa, una domanda fuori corpus è rifiutata). Non compare nel percorso studente. |
| `working/assistente.py` | ⌨️ | **Il file della giornata**: `MODELLO` (`gpt-5.6-luna`), `K`, `MAX_CHIAMATE`, `DOMANDE` con la strada attesa, `LAB2`, `LE_MIE_DOMANDE`, `SOLO`; TODO 2 (`CercaDocumenti` + `cerca_documenti()`, sopra perché `TOOLS` ha bisogno della classe), TODO 1 (`TOOLS` + i rami di `esegui()` + il ciclo dentro `chiedi()`), TODO 3 (`ISTRUZIONI`); `strada()`, gli helper di stampa, il main con la tabella. |
| `working/domande_lab2.py` | 📄 | Le dieci domande del Lab 2 con la strada attesa (le nove degli studenti di Modulo 3 · Lezione 6 più una doppia): il main le legge con `LAB2 = True`. Non si modifica, nessuna copia in `solutions/`. |
| `working/griglia.md` | ⌨️ | **La scheda del Lab 2**, da compilare a mano: le strade, gli esiti, le due leve; una tabella (domanda, strada attesa, strada presa, esito, leva, dopo). Non ha una copia in `solutions/`: è personale. |
| `solutions/assistente.py` | 🧰 | La versione completa di `working/assistente.py`, stesso nome file: differisce solo nei TODO 1-3. |
| `dataset/lumen_m3/` | 📄 | I sei documenti Lumen, identici a Modulo 3 · Lezione 2 (82 chunk a chunk size 500). |
| `dataset/lumen.db` | 📄 | Il database degli ordini Lumen (SQLite): `prodotti` 16, `clienti` 40, `ordini` 300, `righe_ordine` 781. Lo stesso di Modulo 3 · Lezione 8. |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../../lezione-08-tool-implementation/scripts/.env .env   # la chiave della lezione scorsa (oppure: cp .env.example .env e incollala dentro)
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env`, `.venv` e `chroma/` (git non li versiona). La chiave
> OpenAI è quella del corso, la stessa di tutte le lezioni da Modulo 2 in
> poi: nel repo non c'è (è gitignored), sta nei `.env` locali delle lezioni
> già fatte e nel gestore delle chiavi del team. Arriva in aula con una
> chiave di riserva pronta da incollare per chi ha perso il `.env`. La
> collection `lumen_m3` NON viaggia con la cartella: al primo avvio
> `assistente.py` la ricostruisce da solo (82 chunk: una riga per
> documento, la riga `[openai] 82 testi …` dell'unica chiamata di
> embedding, poi «indicizzati 82 chunk»; un paio di minuti, meno di un
> centesimo); chi ha la cartella di Modulo 3 · Lezione 6 con `chroma/` può
> copiarla qui. Il database arriva già pronto: non va rigenerato.

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/assistente.py                              # il file della giornata: le DOMANDE (+ LE_MIE_DOMANDE), o la domanda in SOLO
python scaffolding/sql.py "SELECT * FROM ordini LIMIT 5"   # una query a mano, per verificare una risposta sui dati

# solo docente, non fa parte del percorso studente
python scaffolding/check_lab09.py                         # istantaneo, zero costi
python scaffolding/check_lab09.py --file working/assistente_studente.py   # il file di uno studente, copiato in working/
python scaffolding/check_lab09.py --solutions             # regressione sulla versione completa
python scaffolding/check_lab09.py --solutions --live      # chiamate vere (~1 minuto, pochi centesimi)
```

Un lancio del main sono quattro domande, ognuna da una a tre chiamate a
`gpt-4.1-mini` più un embedding per ogni `cerca_documenti`: frazioni di
centesimo, 2-5 secondi a domanda. Sul `working/` intonso il check dà **5
FAIL per costruzione** (i tre TODO non sono scritti): è la baseline, non
un guasto.

## Cosa si vede a schermo

Per ogni domanda il main stampa ogni passo del giro, come alle due lezioni
scorse, più la riga della strada; in fondo la tabella. La forma:

```
==========================================================================
D: Quanti ordini ha fatto Giulia Moretti?
   chiamata 1  [… token in, … out]  output: function_call query_db({"sql":"SELECT COUNT(*) …"})
      eseguo query_db: COUNT(*)
         13
   chiamata 2  [… token in, … out]  output: message
   2 chiamate · $0.000…
→ Giulia Moretti ha fatto 13 ordini.
   strada: dati  (tool: query_db)

##############################################################################
# RIASSUNTO · K 4 · strada attesa / strada presa
##############################################################################
  domanda                                        attesa          presa           uguale?
  Entro quanti giorni posso restituire un prodo  documenti       documenti       sì
  Quanti ordini ha fatto Giulia Moretti?         dati            dati            sì
  Lorenzo Rossi può montare il braccio LMX-4400  documenti+dati  documenti+dati  sì
  Che tempo fa oggi a Padova?                    nessuna         nessuna         sì

  strada giusta: 4/4
```

Sotto `eseguo cerca_documenti` si vedono le prime righe dei chunk
restituiti (il modello riceve tutto): è lì che si guarda, nel Lab 2, se
il passaggio giusto è entrato tra i `K`.

## La giornata (docente)

1. **Brief (📊, 35')**: le due fonti e le strade; il giro con il pezzo
   che scrivono loro; il RAG come tool; le due leve; due tool nello stesso
   giro; il rifiuto; il log della strada; il file.
2. **Setup (⌨️, 10')**: venv, chiave, primo lancio (indicizza e risponde
   da sé: la baseline).
3. **Lab 1a — attaccare un tool (⌨️, 45')**: TODO 1 su `query_db`: la voce
   in `TOOLS`, il ramo in `esegui()`, il ciclo in `chiedi()`. Fatto quando
   Giulia Moretti risponde 13 con `strada: dati`. **Rientro (5')**: la
   slide col ciclo; chi è indietro lo ricopia.
4. **Lab 1b — il RAG come tool (⌨️, 40')**: TODO 2: docstring di
   `CercaDocumenti`, `cerca_documenti()`, seconda voce e secondo ramo.
   Fatto quando i resi citano un id e Lorenzo Rossi ha `documenti+dati`.
   **Rientro (5')**: la slide con docstring e `cerca_documenti` della
   soluzione; chi è indietro ricopia durante la pausa.
5. **Pausa (☕, 15')**.
6. **Lab 1c — le istruzioni (⌨️, 25')**: TODO 3. Fatto quando la tabella
   dice 4/4 e Padova è rifiutata senza tool. **Rientro (5')**: due o tre
   istruzioni degli studenti (incollate in chat, lette dallo schermo del
   docente), poi la slide con quelle della soluzione.
7. **Lab 2 — provare e sistemare (⌨️, 45')**: `LAB2 = True`, le dieci
   domande di `working/domande_lab2.py`, un lancio (12'), la griglia (10'),
   poi si sistema con le due leve (23'). **Rientro finale (10')**: alla
   lavagna, chi vuole; recap e ponte.

Se si va lunghi: nel brief la slide sui due tool nello stesso giro si
dice a voce (−3'); nel Lab 2 si lanciano solo le prime cinque domande e
una sola cura è obbligatoria. Il Lab 1 non si taglia: i rientri
allineano tutti (chi non ha finito ricopia il pezzo dalla slide).

## Diagnosi rapida in aula (docente; gli studenti possono leggerla)

- Studente bloccato → copia il suo file **dentro `scripts/working/`**
  della tua copia con un altro nome (per esempio
  `working/assistente_giulia.py`: il file calcola `scripts/` da dove si
  trova), poi `python scaffolding/check_lab09.py --file
  working/assistente_giulia.py`. Dice quale dei tre punti del TODO 1
  manca, e poi i TODO 2 e 3.
- `ancora da scrivere: TODO 1` → il modello ha chiesto un tool e il ciclo
  che lo esegue non c'è.
- `tool sconosciuto: …: il tool è in TOOLS ma manca il ramo in esegui()` →
  il main lo dice da solo; il nome va scritto uguale in `TOOLS` e in
  `esegui()`.
- Il modello non usa mai `cerca_documenti`, o lo usa a caso, senza
  errori → la docstring di `CercaDocumenti` è ancora quella del TODO 2: il
  modello la legge così com'è.
- `KeyError: 'sql'` / `KeyError: 'domanda'` → il campo dello schema e la
  chiave letta in `esegui()` hanno nomi diversi.
- `ValueError: too many values to unpack` nel main → una voce di
  `LE_MIE_DOMANDE` non è una tupla `("domanda", "strada attesa")`. È la
  mano alzata più probabile del Lab 2.
- Il modello richiede lo stesso tool a ogni chiamata fino a `(mi fermo: 6
  chiamate senza una risposta)` → la `function_call_output` non è in
  `storia`, o il `call_id` non è quello della richiesta: il modello non
  vede la risposta e richiede. È l'errore più frequente del Lab 1a.
- `ancora da scrivere: TODO 2` → il modello ha chiesto `cerca_documenti` e
  la funzione non c'è ancora.
- Strada `nessuna` su tutte le domande → `TOOLS` è vuota (TODO 1), oppure
  le `ISTRUZIONI` dicono al modello di rispondere da sé.
- Il tool si esegue e la risposta è giusta, ma `strada: nessuna` → manca
  `usati.append(chiamata.name)` nel ciclo: il log della strada resta
  vuoto. Il check lo dice («ritorna (risposta, tool usati)» in FAIL).
- `OPENAI_API_KEY` non impostata all'avvio → lanciato da un'altra cartella
  (`rag.py` legge il `.env` dalla cartella corrente): `cd scripts`.
- Risposta dai documenti senza `[id]` → le `ISTRUZIONI` non chiedono la
  citazione, o `cerca_documenti` non mette gli id davanti ai chunk.
- «Ho riscritto la descrizione e non cambia niente» → ha modificato la
  docstring della funzione `cerca_documenti()`, che il modello non vede:
  la descrizione del tool è la docstring della **classe**
  `CercaDocumenti` (`definisci_tool` passa `schema.__doc__`).
- «Non ho trovato la risposta» su una domanda che nei documenti c'è →
  guardare i chunk sotto `eseguo cerca_documenti`: se il passaggio giusto
  c'è, sono le istruzioni («rispondi solo con quello che i tool
  restituiscono» può essere letto troppo alla lettera); se non c'è, è il
  retrieval, e la cura (`K`) è quella di Modulo 3 · Lezione 6: non si rifà
  oggi.
- `no such column: …` sotto `eseguo query_db` e poi una risposta
  sensata → è la seconda situazione di rifiuto: l'errore è tornato al
  modello, che ha detto che il dato non c'è. Giusto.
- La prima domanda ci mette due minuti → sta indicizzando `lumen_m3`; se
  compare `chroma/` accanto a `scaffolding/`, la seconda volta parte
  subito.
- `unable to open database file` → la cartella del corso ha un `#` o un
  `?` nel nome e il file `tools.py` è una versione vecchia; quella in
  `aikit/` usa `DB.as_uri()` e non ha il problema.

## Note tecniche (docente)

- **Modello: `gpt-5.6-luna`** (dal 18/09/2026; a Modulo 3 · Lezione 7-8 era
  gpt-4.1-mini). Sta in `PRICING` di `llm_client.py` con 0,20 / 1,20 dollari
  per milione di token (prezzi del 30/07/2026). Nell'output arrivano anche
  item `reasoning`: `stampa_chiamata` li elenca, il ciclo li rimanda con il
  resto, e non vanno letti. Con gpt-4.1-mini il ciclo funziona uguale, ma il
  modello fa una ricerca sola anche se le istruzioni dicono di cercare
  ancora (1 ricerca doppia su 18 giri): il Lab 2 come è pensato regge solo
  con Luna.
- **Misure con la chiave vera (18/09/2026, K 4, gpt-5.6-luna, tre giri):**
  `check_lab09.py --solutions --live` tutto `[OK]`; `misura_assistente.py
  --ripeti 3` (cartella della lezione) dà sulle quattro `DOMANDE` 3/3 su
  tutte, 4 secondi a domanda in media. Gli esiti misurati delle domande del
  Lab 2 stanno solo in `domande-lab2-docente.md`, fuori da questa cartella.
- **Perché il RAG entra come `cerca_documenti` e non come `rispondi()`.**
  Se il tool restituisse già la risposta, il modello non potrebbe citare
  i passaggi né combinarli con i dati (la domanda doppia su Lorenzo
  Rossi); e le regole di rifiuto starebbero in due posti. Con i chunk, le
  `ISTRUZIONI` dell'assistente sono l'unico posto delle regole.
- **Il retrieval restituisce sempre `K` chunk**, anche fuori tema: il
  rifiuto sulle domande fuori corpus dipende dalle `ISTRUZIONI` e dalla
  descrizione del tool («i passaggi possono non contenere la risposta»),
  non dal tool. È la prima delle tre situazioni di rifiuto del brief; la
  seconda è il dato che non c'è (la colonna `email` non esiste: il modello
  lo vede dallo schema, o dall'errore di `query_db`), la terza la domanda
  fuori da tutto.
- **La strada `nessuna`** vuol dire nessun tool chiamato: è la strada
  attesa della domanda su Padova, e quella del primo lancio con `TOOLS`
  vuota. `strada()` guarda solo `cerca_documenti` e `query_db`.
- **Perché nessuna chiamata che classifichi la domanda prima** (se lo
  chiedono): sarebbe una chiamata in più da pagare e un punto in più dove
  sbagliare, e il modello ha già davanti la lista dei tool; la scelta
  dentro il giro è quella che l'SDK gestisce dalla prossima lezione.
- **Domande su cose che anticipano lezioni future.** «Posso fare una
  domanda di seguito?» (follow-up): Modulo 3 · Lezione 11, ogni domanda
  oggi è a sé. «Perché scriviamo il giro a mano?»: dalla prossima lezione
  lo gestisce l'OpenAI Agents SDK, e questo file è ciò che l'SDK riscrive.
  Il proto-assistente non si chiama «agente»: il nome arriva con l'SDK.
  **Il titolo in calendario** di Modulo 3 · Lezione 10 è ancora «RAG
  Evaluation Intro» (il piano di modulo la fa diventare la lezione
  sull'SDK, in attesa di riallineamento): in slide la prossima lezione è
  nominata per numero e contenuto, senza titolo, e in aula si dice così.
- **`hybrid.py` e `rerank.py`** restano in `aikit/` ma non si usano; la
  chiave Cohere non serve (nessun file la legge finché non si importa
  `rerank`). I tool `calcolatrice`, `data_oggi` e `prezzo_prodotto` restano
  in `tools.py` per non toccare il toolkit, ma l'assistente non li vede.
