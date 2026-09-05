# Modulo 3 · Lezione 3 — Lab: RAG Conversazionale (memoria & sessioni) · guida agli script

Lab da 4h (📊 brief compatto + 🎤 live coding breve + ⌨️ tre lab): il
`rag.py` della lezione scorsa regge una sola domanda alla volta; oggi regge
una **conversazione**, follow-up compresi, con **sessioni** che sopravvivono
alla chiusura del programma. Niente `ConversationBufferMemory`: la memoria
è codice esplicito, scritto dagli studenti in **un solo file di lavoro**,
`working/chat.py`, in tre passi — storia + troncamento (Lab 1), query
condensation (Lab 2), summary memory + sessioni su JSON (Lab 3).

`rag.py` entra oggi in `scaffolding/aikit/` (il rito della promozione) e
**si modifica una volta, in aula**, nel live coding di apertura:
`rispondi()` faceva tre cose in una (recupera, prompt, modello) e non si
poteva riusare con una storia; si spacca in `genera(chunks, domanda,
storia=None)` + `rispondi(query, storia=None)`, con le regole del prompt in
`ISTRUZIONI`. La versione finita è `solutions/aikit/rag.py`. Poi `chat.py`
chiama `rag.recupera()` e `rag.genera()` e `rag.py` non si tocca più. Il
corpus è lo stesso Lumen esteso della lezione scorsa (82 chunk nella
collection `lumen_m3`).

I dialoghi da provare **non sono in questa cartella**: li dà il docente, un
dialogo alla volta (`dialoghi-docente.md`, nella cartella della lezione).

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 live coding del docente ·
⌨️ da completare dagli studenti · 📄 documenti/dati di esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Le dipendenze di Modulo 3 · Lezione 2 più `tiktoken` (il conteggio dei token di Modulo 2 · Lezione 3). |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` — la stessa chiave del Modulo 2. |
| `CONSEGNA.md` | ⌨️ | La consegna dei tre lab (TODO 1-5) e il criterio di "fatto" di ognuno. |
| `scaffolding/aikit/` | 🧰 | Il toolkit: i sette moduli del Modulo 2 **+ `rag.py`** di Modulo 3 · Lezione 2, promosso oggi (identico alla soluzione della lezione scorsa salvo la riga del percorso al corpus e la docstring). Gli altri sette moduli non si toccano. |
| `scaffolding/aikit/rag.py` | 🎤 | **Il file del live coding di apertura** (10'): arriva nella forma di partenza (`indicizza()` · `recupera()` · `rispondi()`), in aula diventa `ISTRUZIONI` + `genera(chunks, domanda, storia=None)` + `rispondi(query, storia=None)`. Il docente scrive, gli studenti replicano. Dopo, `chat.py` usa `rag.recupera()`, `rag.genera()` e `rag.CONFIG`; il main lancia `rag.indicizza()` solo se la collection è vuota. |
| `solutions/aikit/rag.py` | 🎤 | La **versione finita** del live coding: il codice di riferimento che il docente legge mentre scrive (commenti compresi). Stesso percorso relativo di `scaffolding/aikit/rag.py`, così gli import restano identici. Chi resta indietro lo copia al posto del proprio. È il `rag.py` che le lezioni successive trovano in `aikit/`. |
| `scaffolding/make_dataset.py` | 🧰 | Il generatore del corpus (Modulo 3 · Lezione 2). Il corpus è già generato e non cambia: serve al check per verificare che lo scaffolding sia intatto. |
| `scaffolding/check_lab03.py` | 🧰 | **Strumento del docente**: base istantaneo senza rete (struttura, wiring di `genera()` e dei cinque TODO, tutto mockato); accetta `rag.py` nelle due forme (partenza / finito) e dice in quale è; `--solutions` verifica la versione completa caricando da solo il `rag.py` finito; `--live` fa chiamate vere sul dialogo del reveal della lezione scorsa (follow-up senza e con condensation) e sul riassunto. Non compare nel percorso studente. |
| `scaffolding/demo_brief.py` | 🧰 | **Strumento del docente** per il brief: la coppia domanda + follow-up sul `rag.py` single-turn, con pausa `[invio]` tra le due. Si rilancia anche dopo il live coding: stesse risposte, la baseline non è cambiata. Non compare nel percorso studente. |
| `working/chat.py` | ⌨️ | **L'unico file di lavoro dei lab**: `CONFIG` (budget token, memoria, cartella sessioni — il modello è quello di `rag.CONFIG`), `conta_token()` dato, TODO 1-2 (Lab 1), TODO 3 (Lab 2), TODO 4-5 (Lab 3), il loop `Tu>` nel main. |
| `solutions/chat.py` | 🧰 | La versione completa di `working/chat.py`, stesso nome file. Ha bisogno del `rag.py` finito (vedi «Come si prova»). |
| `dataset/lumen_m3/` | 📄 | I sei documenti Lumen, identici a Modulo 3 · Lezione 2 (82 chunk). |
| `sessioni/` | 📄 | Nasce a runtime (Lab 3): un file JSON per sessione. Non è versionata. |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # dentro: la stessa chiave OpenAI del Modulo 2
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env`, `.venv`, `chroma/` e `sessioni/` (git non li versiona), e
> con `scaffolding/aikit/rag.py` nella **forma di partenza** (quella del
> repo): il live coding lo fanno in aula. La collection `lumen_m3` NON
> viaggia con la cartella: al primo avvio `chat.py` la ricostruisce da solo
> (82 chunk, ~2 minuti, meno di un centesimo).

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/chat.py           # il file dei lab: chiede il nome sessione, poi il loop Tu> (al primo avvio indicizza: ~2 min, costo irrisorio)

# solo docente, non fa parte del percorso studente
python scaffolding/check_lab03.py                       # struttura + wiring (rag.genera e i TODO): istantaneo, zero costi
python scaffolding/check_lab03.py --solutions           # regressione sulla versione completa (carica da solo solutions/aikit/rag.py)
python scaffolding/check_lab03.py --solutions --live    # chiamate vere: follow-up senza/con condensation, riassunto
python scaffolding/demo_brief.py                        # la demo del follow-up per il brief (blocco 1) — e dopo il live coding, per il rilancio
```

`python solutions/chat.py` chiama `rag.genera()`, quindi vuole il `rag.py`
**finito** in `scaffolding/aikit/`: o si fa il live coding, o si copia
`solutions/aikit/rag.py` al suo posto. Prima di distribuire la cartella si
rimette la forma di partenza (`git checkout scaffolding/aikit/rag.py`).
`check_lab03.py --solutions` e `prova_dialoghi.py` non hanno questo
problema: caricano il `rag.py` finito da soli.

Numeri di riferimento (misurati con chiamate reali): un turno completo
(condensation + risposta) costa circa $0,0002; un dialogo di tre turni
resta sotto il millesimo di dollaro ($0,0004-0,0006, 5 chiamate); il dialogo
lungo di sette turni costa $0,0014 col buffer e $0,0020 col riassunto. Il
budget della storia in `CONFIG` è **350 token**, stretto apposta: con
risposte lunghe il troncamento (o il riassunto) scatta già al terzo-quinto
turno, così si vede in aula.

> **Prima dell'aula (docente):** lancia `python scaffolding/check_lab03.py
> --solutions --live` (indicizza la collection se manca, verifica tutto con
> chiave vera) e poi `python scaffolding/demo_brief.py`. Leggi
> `solutions/aikit/rag.py`: è quello che scrivi a schermo nel live coding,
> commenti compresi. Prova almeno il primo dialogo di `dialoghi-docente.md`
> con `prova_dialoghi.py 1` (nella cartella della lezione): il follow-up
> deve produrre la riga `↳ cercato:` e il chunk giusto. Se hai sessioni di
> prova in `sessioni/`, cancella la cartella: in aula le sessioni le creano
> gli studenti.

## Percorso in aula (le slide sono la regia: ogni switch ha la sua slide)

1. **Brief (📊, 25')**: il follow-up che fallisce, dal vivo
   (`python scaffolding/demo_brief.py`, esegue il docente); cosa entra nel
   modello con una storia; query condensation; buffer vs summary memory;
   sessioni; perché `rispondi()` com'è non si riusa.
2. **Live coding (🎤, 10')**: `scaffolding/aikit/rag.py` — `ISTRUZIONI`,
   `genera()`, `rispondi()` con la storia. Riferimento:
   `solutions/aikit/rag.py`. Rilancio di `demo_brief.py`: stesse risposte.
3. **Lab 1 (⌨️, 45')**: TODO 1-2 in `working/chat.py` — `rag.recupera()` +
   `rag.genera(…, storia)`, il troncamento. Fatto quando cinque turni restano
   sotto budget e le citazioni ci sono ancora; il follow-up fallisce ancora.
4. **Lab 2 (⌨️, 60')**: TODO 3 — `condensa()` davanti al retrieval, provata
   sui dialoghi del docente. Fatto quando compare `↳ cercato:` ed esce il
   chunk giusto.
5. **☕ Pausa (15')**.
6. **Lab 3 (⌨️, 50')**: TODO 4-5 — `riassumi()` con
   `CONFIG["memoria"] = "riassunto"`, sessioni su JSON. Fatto quando si
   riapre la stessa sessione e il follow-up funziona ancora.
7. **Blocco flessibile (📊⌨️, 35')**: a scelta del docente — buffer vs
   riassunto sul dialogo lungo di `dialoghi-docente.md`, Q&A, o esercizio
   extra (budget stretto).

## Diagnosi rapida in aula (docente)

- Studente bloccato → `python scaffolding/check_lab03.py` dice se `rag.py`
  è nella forma di partenza o finita, se `genera()` è cablata, e quale TODO
  non è cablato e perché.
- `AttributeError: module 'aikit.rag' has no attribute 'genera'` all'avvio
  di `chat.py` → il live coding non è stato fatto o salvato: si copia
  `solutions/aikit/rag.py` su `scaffolding/aikit/rag.py` e si riparte.
- `rag.py` modificato oltre il live coding (il check lo dice) → confronto
  con `solutions/aikit/rag.py`, o si copia quello.
- Il follow-up risponde ancora «Non lo trovo» dopo il Lab 2 → guardare la
  riga `↳ cercato:`: se non compare, `condensa()` non è innestata in
  `rispondi_in_chat()` davanti a `rag.recupera()`; se compare ma la domanda
  riscritta è ancora vaga, è il prompt di `condensa()` (chiedere
  esplicitamente di sostituire pronomi e riferimenti).
- Il modello «non ricorda» nemmeno nel prompt (al follow-up «E dall'estero?»
  non sa di cosa si parla) → a `rag.genera()` non viene passata la storia
  (terzo argomento).
- La storia cresce senza mai troncare → `tronca()` (o `riassumi()`) non è
  chiamata a fine turno in `rispondi_in_chat()`, o il budget in `CONFIG` è
  stato alzato.
- La sessione riparte vuota → il nome all'avvio è diverso, oppure
  `salva_sessione()` non viene chiamata (la chiama il main: basta che non
  alzi `NotImplementedError`). I file stanno in `scripts/sessioni/`.
- Risposta giusta ma citazione sbagliata → succede quando il modello
  risponde dalla storia invece che dai chunk: è un limite noto, si discute
  nel brief (il generatore ricorda, il retrieval no).
