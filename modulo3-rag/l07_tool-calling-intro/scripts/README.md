# Modulo 3 · Lezione 7 — Tool Calling Intro · guida agli script

Lezione da 2 ore (📊 teoria + 🎤 codice spiegato + ⌨️ esercizio): il giro
minimo del tool calling, scritto a mano con la Responses API. Il modello
riceve una lista di funzioni **nostre** e, quando serve, restituisce una
richiesta (nome + argomenti); noi la eseguiamo e gli rimandiamo il
risultato; lui risponde. Il codice sta tutto in **un file**,
`working/tools.py`: la calcolatrice, la definizione dei tool, l'esecuzione
e il giro sono già scritti (il docente li spiega); l'esercizio è il secondo
tool, `data_oggi`, e la prova con nome e descrizione generici. Stasera
niente retrieval: `aikit/` è ridotto a `llm_client.py`.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 codice spiegato (già nel file
degli studenti) · ⌨️ da completare dagli studenti · 📄 documenti.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | `python-dotenv`, `openai`, `pydantic`: un sottoinsieme di Modulo 3 · Lezione 6. |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` (la stessa del Modulo 2). |
| `CONSEGNA.md` | ⌨️ | Il TODO in tre punti, la prova con nome e descrizione generici, il criterio di «fatto», gli errori tipici, il terzo tool per chi finisce prima. |
| `scaffolding/aikit/llm_client.py` | 🧰 | Il client di Modulo 2 · Lezione 3: stasera serve solo `cost_usd()`, per il costo del giro. La chiamata con i tool usa il client OpenAI direttamente. |
| `scaffolding/check_lab07.py` | 🧰 | **Strumento del docente**: base istantaneo senza rete (struttura, forma delle definizioni in `TOOLS`, `esegui()` sui due tool, il giro con un client finto); `--solutions` per la versione completa; `--live` con la chiave vera: le quattro domande usano i tool attesi. Non compare nel percorso studente. |
| `working/tools.py` | 🎤 ⌨️ | **Il file della serata**: `MODELLO`, `ISTRUZIONI`, le quattro `DOMANDE`, `SOLO`; la calcolatrice, `definisci_tool()`, `TOOLS`, `esegui()`, `chiedi()` e gli helper di stampa già scritti; il **TODO** del secondo tool in tre punti. |
| `solutions/tools.py` | 🧰 | La versione completa, stesso nome file: differisce da `working/` solo nel TODO. |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # dentro: la chiave OpenAI del Modulo 2
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env` e `.venv` (git non li versiona).

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/tools.py          # le quattro domande, ogni passo del giro a schermo, token e costo

# solo docente, non fa parte del percorso studente
python scaffolding/check_lab07.py                       # struttura + definizioni + giro con il client finto: istantaneo, zero costi
python scaffolding/check_lab07.py --file /percorso/tools.py   # il file di uno studente, senza copiarlo al posto del proprio
python scaffolding/check_lab07.py --solutions           # regressione sulla versione completa
python scaffolding/check_lab07.py --solutions --live    # chiamate vere (~10 s): le quattro domande con i tool attesi
```

Un lancio del main sono sei chiamate a `gpt-4.1-mini` con il solo
`working/`, sette con il secondo tool (un giro con tool sono due chiamate,
circa $0,0002): meno di un decimo di centesimo.

## Cosa si vede a schermo

Con il file così com'è (solo la calcolatrice):

```
D: Quanto fa 849 diviso 1,22?
   chiamata 1  [137 token in, 27 out]  output: function_call calcolatrice({"a":849,"b":1.22,"operazione":"/"})
      eseguo calcolatrice({'a': 849, 'b': 1.22, 'operazione': '/'}) = 695.9016393442623
   chiamata 2  [180 token in, 16 out]  output: message
   2 chiamate · $0.00020
→ 849 diviso 1,22 fa circa 695,90.

D: Che giorno è oggi?
   chiamata 1  [131 token in, 13 out]  output: message
   1 chiamata · $0.00007
→ Oggi è il 27 aprile 2024.

D: Che giorno è oggi, e quanto fa 849 per 7?
   chiamata 1  [140 token in, 41 out]  output: function_call calcolatrice({"a":849,"b":7,"operazione":"*"})
      eseguo calcolatrice({'a': 849, 'b': 7, 'operazione': '*'}) = 5943
   chiamata 2  [173 token in, 24 out]  output: message
   2 chiamate · $0.00023
→ Oggi è il 27 aprile 2024, e 849 per 7 fa 5943.

D: Cos'è una scrivania regolabile in altezza?
   chiamata 1  [138 token in, 42 out]  output: message
   1 chiamata · $0.00012
→ Una scrivania regolabile in altezza è un tavolo da lavoro che permette di modificare l'altezza del piano…
```

La terza domanda è il momento più utile del blocco: il conto giusto e la
data inventata nella stessa frase (5 giri su 5 con la sola calcolatrice,
`misura_tool_calling.py esercizio`; la data è sempre del 2024, non sempre
il 27 aprile). La quarta risponde senza tool e senza
documenti, da quello che il modello sa: stasera non c'è retrieval e
nessuno gli chiede di rifiutare (il lab di Modulo 3 · Lezione 9 rimette
il RAG tra i tool proprio per questo).

Con il secondo tool (la soluzione) la seconda domanda chiama `data_oggi`
e risponde con la data di oggi; la terza («Che giorno è oggi, e quanto fa
849 per 7?») chiede **due** `function_call` nella stessa risposta; la
quarta nessuno. I token della prima domanda salgono a 162 + 205 in: la
definizione del secondo tool sono 25 token in più a ogni chiamata, ed è
la riga in più nella tabella dei costi delle slide. Nelle slide la data
che esce dal tool è un segnaposto («la data di oggi»): a schermo esce
quella del giorno.

## Note tecniche (docente)

- **Forma dei tool nella Responses API**: `{"type": "function", "name",
  "description", "parameters", "strict"}`, piatta. L'helper
  `openai.pydantic_function_tool()` produce la forma di Chat Completions
  (`{"type": "function", "function": {...}}`): passata così alla Responses
  API dà `400 Missing required parameter: tools[0].name`. Per questo
  `definisci_tool()` costruisce il dict a mano da `model_json_schema()`.
- **`strict`**: con `True` l'API pretende `additionalProperties: false` e
  tutti i campi in `required` (400 altrimenti); `model_json_schema()` non
  li mette. Si tiene `False`: per i tool giocattolo di stasera basta, e
  Pydantic valida comunque gli argomenti se lo si vuole
  (`Calcolatrice(**argomenti)`). Strict e helper si citano in una riga.
- **Gli item di output tornano nell'input così come sono** (`storia +=
  r.output`, oggetti dell'SDK): l'SDK li serializza. Se si rimandano solo
  le `function_call_output`, l'API risponde `400 No tool call found for
  function call output`. La lista si chiama `storia` e non `input`
  perché `input` è una funzione di Python: ombreggiarla in aula porta a
  domande fuori tema.
- **Lo schema a schermo è più lungo di quello in slide**:
  `model_json_schema()` aggiunge `title` per la classe e per ogni campo e
  copia la docstring in `description` (che quindi compare due volte, nella
  definizione e dentro `parameters`). In slide sono tolti per leggibilità;
  chi stampa `TOOLS` in aula li vede.
- **Il `while True` di `chiedi()` non ha un limite di giri**: si ferma
  alla prima risposta in testo, e con questi tool il modello non chiede
  all'infinito. Se uno studente lo fa notare, la risposta è che un tetto
  di iterazioni è una delle cose che i tool veri (Modulo 3 · Lezione 8)
  e il loop gestito da un SDK aggiungono.
- **L'apertura non è deterministica al 100%**: «849 diviso 1,22» esce
  sbagliata in 19 giri su 21 (696,72 o 695,08); «Che giorno è oggi?» dà
  sempre una data del 2024. Se in aula la divisione esce giusta, si
  rilancia una volta, o si usa «Quanto fa 849 per 1,0731?» (sbagliata in
  tutti i 17 giri misurati, giusto 911,06). Le due risposte sbagliate in
  slide sono stampate, non rilanciate dal vivo.
- **La prova con nome e descrizione generici** si giudica sulla domanda
  singola: lì il tool generico non viene chiamato in nessun giro (0/5),
  misurato nella configurazione esatta dell'esercizio, `ISTRUZIONI`
  comprese (`misura_tool_calling.py esercizio`); le due configurazioni
  miste (uno solo dei due generico) chiamano il tool 5/5, sempre con le
  `ISTRUZIONI`. Sulla domanda doppia il
  modello, avendo già deciso di usare la calcolatrice, chiama anche il
  tool generico (5/5 con le `ISTRUZIONI` del file; senza istruzioni 0/5).
  Non è un errore dello studente, e la slide 17 lo dice.
- **`strict` e la forma piatta del tool**, le due domande che arrivano da
  chi legge un tutorial: la Responses API vuole `{"type": "function",
  "name", "description", "parameters", "strict"}` piatto, non
  `{"type": "function", "function": {...}}` di Chat Completions; e
  `strict: True` vuole `additionalProperties: false` e tutti i campi in
  `required`, che `model_json_schema()` non mette. Senza strict l'API
  non garantisce gli argomenti; con questi tool non è mai successo che
  uscissero fuori schema, e chi vuole la garanzia fa
  `Calcolatrice(**argomenti)`.
- **Modello**: `gpt-4.1-mini`, perché è in `PRICING` di `llm_client.py` e
  `cost_usd()` lo conosce (`rag.py` del modulo usa `gpt-4o-mini`; per
  usarlo qui andrebbe aggiunto a `PRICING`).
- **I numeri** in slide (token, costi, «5 giri su 5», date inventate) sono
  misurati il 14/09/2026 con `misura_tool_calling.py`, nella cartella
  della lezione: `schema`, `giro`, `apertura`, `scelta`, `vago`, `demo`,
  `demo2`, `errori`, `esercizio` (la configurazione esatta
  dell'esercizio e i token senza tool). I token delle slide sulle tappe
  sono quelli di `python working/tools.py` con la sola calcolatrice. Se
  cambiano modello o SDK, si rilancia.
- **Il terzo tool del «se finisci prima»** (conversione di valuta a tasso
  fisso) non ha una copia in `solutions/`: il riferimento è in
  `misura_tool_calling.py` (classe `Valuta` e il ramo `valuta` di
  `esegui()`, con i tassi). Per la prova dei parametri: nome
  `strumento_3` e descrizione generica → chiamato lo stesso 5/5;
  parametri `x`, `y`, `z` → mai chiamato.

## Percorso in aula (le slide sono la regia: ogni switch ha la sua slide)

1. **Apertura (📊, 5')**: «Che giorno è oggi?» e «Quanto fa 849 diviso
   1,22?» al modello senza tool: 27 aprile 2024 e 696,72. Agenda.
2. **Teoria (📊, 30')**: il modello chiede, non esegue; l'anatomia del
   giro sul JSON vero; lo schema da Pydantic; come sceglie il tool; due
   tool nella stessa risposta; il costo; la mappa del file.
3. **Codice spiegato (🎤, 15')**: `working/tools.py` dall'alto in basso, poi
   il lancio (del docente; chi ha `.env` pronto lancia anche lui): la prima
   domanda giusta col tool, la seconda sbagliata senza.
4. **Esercizio (⌨️, 60': 20' il TODO, 10' le quattro domande, 15' la
   prova, il resto l'extra)**: il TODO in tre punti, le quattro domande,
   la prova con nome e descrizione generici. Rientro sulle slide.
5. **Wrap-up (📊, 10')**: recap del giro; cosa non si è fatto apposta;
   la prossima lezione.

## Diagnosi rapida in aula (docente; gli studenti possono leggerla)

- Studente bloccato → `python scaffolding/check_lab07.py --file
  <il suo tools.py>` (sulla copia del docente: agli studenti il check non
  arriva) dice quale dei tre punti del TODO manca (voce in `TOOLS`, ramo
  in `esegui()`, valore ritornato). Sul `working/` intonso il check dà
  **2 FAIL per costruzione** (il secondo tool non c'è ancora): è la
  baseline, non un guasto.
- `400 No tool output found for function call` → una `function_call` è
  rimasta senza `function_call_output`: il ciclo `for` sulle chiamate è
  stato rotto, o il `call_id` non è quello della richiesta.
- `400 No tool call found for function call output` → `storia += r.output`
  manca o è stato sostituito con il solo testo: le `function_call` devono
  tornare nell'input insieme ai loro output.
- `TypeError: data_oggi() takes 0 positional arguments` → nel ramo di
  `esegui()` è stato scritto `data_oggi(argomenti)`: il tool non ha
  argomenti, si chiama senza.
- `TOOLS[1] ha type, name, description non vuota…` in `[FAIL]` dal check →
  quasi sempre manca la docstring di `DataOggi` (`schema.__doc__` è
  `None`).
- `400 Invalid type for 'input[…].output'` → `output` non è una stringa.
- `ValueError: tool sconosciuto: data_oggi` → il modello lo chiama (quindi
  `TOOLS` è a posto) ma in `esegui()` manca il ramo, o il nome non
  combacia con quello in `TOOLS`.
- `400 … 'additionalProperties' is required` → `strict: True` con lo schema
  di `model_json_schema()`: si rimette `False`.
- «Che giorno è oggi?» dà ancora una data del 2024 con il tool in `TOOLS`
  → nome o descrizione non dicono cosa fa (la docstring vuota o generica
  insieme a un nome generico); è la prova dell'esercizio, non un bug.
- La terza domanda fa due giri invece di due `function_call` nella stessa
  risposta → succede: il modello può chiederli uno alla volta. Non è un
  errore, si rilancia e si vede l'altra forma.
- Il modello risponde con una domanda di cortesia in coda («Vuoi che…?»)
  → `ISTRUZIONI` è stata cambiata; non è un errore.
