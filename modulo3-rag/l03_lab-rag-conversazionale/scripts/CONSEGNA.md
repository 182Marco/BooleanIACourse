# Modulo 3 · Lezione 3 — Lab: RAG Conversazionale · consegna

Si lavora in **un solo file**: `working/chat.py`. Dentro ci sono la `CONFIG`
in cima, `conta_token()` già scritto, cinque TODO e un main già pronto: il
loop `Tu>` della chat. Il main si ferma al primo TODO mancante e lo dice.

Retrieval e generazione sono in `rag.py`, in `scaffolding/aikit/`, che dopo
il live coding di apertura ha tre funzioni da chiamare: `rag.recupera(domanda)`
ritorna i chunk, `rag.genera(chunks, domanda, storia)` ritorna la risposta
(la storia, se c'è, va davanti al prompt), `rag.CONFIG["modello"]` è il
modello. Dopo il live coding **non si tocca più**. Se il vostro `rag.py`
non ha `genera()` (all'avvio: `AttributeError: … has no attribute 'genera'`),
la versione finita è `solutions/aikit/rag.py`: si copia al posto di
`scaffolding/aikit/rag.py` e si va avanti.

Le domande da provare le dà il docente, un dialogo alla volta: si battono
nel loop così come sono, follow-up compresi.

Setup (venv, `requirements.txt`, `.env` con la chiave del Modulo 2): in
`README.md`, sezione Setup. Si lancia tutto dalla cartella `scripts/`:
`python working/chat.py`. Al **primo avvio** indicizza il corpus da zero
(82 chunk, un paio di minuti, meno di un centesimo): è normale, dalla
seconda volta parte subito. All'avvio chiede il **nome della sessione**:
nei Lab 1 e 2 basta premere invio (senza nome non salva niente); serve nel
Lab 3.

## Lab 1 — la memoria si aggancia al RAG

### TODO 1 — `tronca(storia)`

Il troncamento di Modulo 2 · Lezione 3 (`_tronca` della classe `Chatbot`
del vostro `chatbot.py`, qui riscritto da zero), come funzione: toglie i
messaggi più vecchi finché la storia sta in `CONFIG["budget_token"]`.
Modifica la lista sul posto e ritorna quanti messaggi ha tolto.

### TODO 2 — `rispondi_in_chat(storia, domanda)`

Un turno di conversazione: recupera i chunk con `rag.recupera()`, genera la
risposta con `rag.genera(chunks, domanda, storia)` — la **storia davanti** al
prompt la mette `genera()`, è quello che avete scritto nel live coding —,
aggiunge alla storia la domanda e la risposta — **mai i chunk** — e alla
fine tiene la storia nel budget con `tronca()`. Ritorna
`(risposta, chunks, domanda_cercata)`: nel Lab 1 la domanda cercata è la
domanda stessa.

`rag.rispondi(domanda, storia)` fa le due chiamate in una riga e va bene
anche così; qui si tengono separate per vedere cosa entra nel retrieval e
cosa nella generazione — nel Lab 2 è il punto.

**Fatto quando:** su una conversazione di cinque turni la riga `[storia: …]`
resta sotto il budget (a un certo punto compare `[buffer] tolti …`) e il
chatbot risponde ancora con le citazioni. Sul follow-up («E per il secondo
caso?») **fallisce ancora** — «Non lo trovo nei documenti.», oppure una
risposta con la fonte sbagliata: è atteso, si cura nel Lab 2.

Per verificarlo da soli, senza aspettare il prossimo dialogo del docente,
la coppia della slide del brief è già vostra: «Perché il piano si ferma
sempre a metà corsa?» e poi «E per il secondo caso?». Se finite in
anticipo: domande vostre sui sei documenti, ognuna seguita da un follow-up
con un pronome — indovinate prima quale fallirà.

## Lab 2 — query condensation

### TODO 3 — `condensa(storia, domanda)`

Una chiamata al modello che riscrive la domanda usando la storia, in una
domanda che sta in piedi da sola (nomi al posto dei pronomi, il tema della
conversazione dentro la domanda). Ritorna la domanda riscritta. Se la
domanda è già autonoma, il modello la lascia com'è. Un solo messaggio
`user` col prompt di riscrittura (la conversazione e la nuova domanda),
senza `instructions` e senza storia; modello `rag.CONFIG["modello"]`;
`r.output_text.strip()` di ritorno. Il prompt, lo stesso della slide:

```
Qui sotto c'è una conversazione e una nuova domanda dell'utente.
Riscrivi la nuova domanda in modo che sia comprensibile DA SOLA, senza la
conversazione: sostituisci pronomi e riferimenti ("quello", "il secondo
caso", "e per la wide?") con ciò a cui si riferiscono. Se la domanda è già
autonoma, ricopiala uguale. Rispondi SOLO con la domanda riscritta.

<conversazione>
Utente: …
Assistente: …
</conversazione>

<nuova_domanda>
…
</nuova_domanda>
```

Poi si innesta in `rispondi_in_chat()` **davanti al retrieval**: la domanda
che va a `rag.recupera()` e a `rag.genera()` è quella riscritta; in storia
resta quella originale.

**Fatto quando:** sullo stesso dialogo dove prima usciva il chunk sbagliato,
ora compare la riga `↳ cercato: …` con la domanda riscritta, tra i chunk c'è
quello giusto e la risposta lo cita. Anche qui la coppia della slide del
brief basta per verificarlo da soli. Se finite in anticipo: follow-up
vostri sempre più vaghi («e quello?», «e prima?») e leggete cosa ne fa la
riga `↳ cercato:`.

## Lab 3 — summary memory e sessioni

### TODO 4 — `riassumi(storia)`

Se la storia sfora il budget, tutti i messaggi tranne gli ultimi due
(l'ultimo turno) vengono sostituiti da **un** messaggio di riassunto scritto
dal modello: un messaggio `user` che inizia con «Riassunto della
conversazione finora: …» (seguito da un `assistant` di presa d'atto, così
l'alternanza user/assistant resta), davanti all'ultimo turno. Un riassunto
precedente, se c'è, viene assorbito nel nuovo. Ritorna il riassunto (o
`None` se non serviva). La chiamata è come quella di `condensa()`: un solo
messaggio `user` con la conversazione da riassumere e la richiesta di un
riassunto in poche righe che conservi i fatti concreti (prodotti, codici,
cifre, tempi) e le fonti citate tra parentesi quadre.

In `rispondi_in_chat()` lavora al posto di `tronca()` quando
`CONFIG["memoria"]` vale `"riassunto"`: per provarlo si esce dalla chat
(`exit`), si cambia **a mano** quella riga in cima al file (`"buffer"` →
`"riassunto"`) e si rilancia `python working/chat.py`. È l'unica riga fuori
dai TODO che si tocca oggi.

### TODO 5 — `salva_sessione(nome, storia)` e `carica_sessione(nome)`

La storia su file JSON in `CONFIG["sessioni_dir"]/<nome>.json`: si salva a
ogni turno (lo fa già il main), si ricarica all'avvio se la sessione esiste,
altrimenti si parte da una lista vuota. Il main chiede il nome della
sessione all'avvio.

**Fatto quando:** con `CONFIG["memoria"] = "riassunto"` la riga
`[riassunto] …` compare quando la storia sfora e la chat continua; poi si
chiude il programma, lo si riapre **con lo stesso nome di sessione**, e un
follow-up sul turno di prima funziona ancora.

## Se finisci prima

Stringi `CONFIG["budget_token"]` (150) e confronta `"buffer"` e
`"riassunto"` sullo stesso dialogo: a quale turno il buffer dimentica il
primo argomento, e cosa manca nel riassunto. Rilanciare non è un problema
di costi: un turno completo (condensation + risposta) resta sotto il
millesimo di dollaro.
