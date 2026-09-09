# Modulo 3 · Lezione 5 — Advanced Retrieval II: Re-ranking · consegna

Si lavora in **un solo file**: `working/rerank.py`. Dentro ci sono la
`CONFIG` in cima, il `QUERY_SET` (le stesse tredici domande della lezione
scorsa), la funzione `rerank_cohere()` **già scritta** (il docente la
spiega, voi seguite sul file: non si ricopia niente), due TODO e un main
già pronto: lancia la demo del codice spiegato e poi tutto il query set
con e senza rerank. Se mancano i TODO 2-3 il main prosegue e nelle
colonne cohere e llm stampa «(ancora da scrivere)».

Serve `OPENAI_API_KEY` in `.env` (la stessa del Modulo 2; il file si apre
con l'editor che usi per il codice, è un file di testo). `COHERE_API_KEY`
è **facoltativa**: se hai fatto la chiave Trial, il main riempie anche la
colonna cohere; se non ce l'hai, la salta da solo («senza COHERE_API_KEY
in .env: si salta») e lavori col backend LLM, che è quello che scrivi tu.
Se invece la chiave c'è ma è copiata male, il primo lancio si ferma con
un errore `401` di Cohere: si ricontrolla la riga in `.env`.

## Codice spiegato — Cohere Rerank (già nel file)

### 1 — `rerank_cohere(query, chunks)` (🎤 già scritta, il docente la spiega)

Una chiamata a Cohere Rerank con la domanda e i testi di tutti i chunk:
il modello legge ogni coppia domanda + chunk e dà un punteggio di
pertinenza. Ritorna gli stessi chunk dal più pertinente in giù, nella
forma di `rag.recupera()` (dict con `id`, `testo`, `score`, `source`),
con `score` = relevance score tra 0 e 1. Se per sbaglio la rompete, la
versione buona è in `solutions/rerank.py`.

## Esercizio — il secondo backend e i due stadi

### TODO 2 — `rerank_llm(query, chunks)` (⌨️ da soli)

Lo stesso lavoro fatto dal modello generico. Un prompt con la domanda e
i chunk numerati (`[0]`, `[1]`, …), e `client.responses.parse()` con
`text_format=Ordine` (il modello Pydantic è già nel file: una lista di
indici) per farsi restituire gli indici dal più al meno pertinente, come
a Modulo 2 · Lezione 13. Ritorna gli stessi chunk in quell'ordine, con
`score` = quanti ne restano dietro (il primo vale `len(chunks)`, l'ultimo
1): il modello dà un ordine, non un punteggio. Stampa i token usati
(`risposta.usage.input_tokens` e `output_tokens`), come fa `embed()` con
gli embedding: servono per la tabella.

Attenzione a due cose che il modello può fare: ripetere un indice, o
saltarne uno. Nel risultato ogni chunk deve tornare **una volta sola**, e
**tutti**: come garantirlo lo decidi tu.

### TODO 3 — `cerca_due_stadi(query, k_largo, k_finale, backend)` (⌨️ da soli)

Primo stadio `hybrid.cerca_hybrid(query, k_largo)`; secondo stadio
`rerank_cohere()` oppure `rerank_llm()` a seconda di `backend` (`"cohere"`
o `"llm"`); ritorna i primi `k_finale` chunk riordinati.

## Quando è fatto

Lancia `python working/rerank.py` dalla cartella `scripts/`. Al primo
lancio ricostruisce la collection `lumen_m3` (82 chunk: stampa un conteggio
per documento, poi una chiamata di embedding; un paio di minuti, meno di
un centesimo): è normale. Poi il main stampa, per ogni domanda del query set, le tre modalità fianco a fianco
(hybrid / cohere / llm) con i secondi di ogni chiamata, e per l'LLM i
token. Tra una domanda e l'altra aspetta sei secondi (il free tier Cohere
fa dieci chiamate al minuto): il giro completo dura circa due minuti.
Compila la **tabella in fondo al file**: la colonna del chunk giusto è
già scritta (è la tabella della lezione scorsa); per ogni domanda la sua
posizione nelle tre modalità (il main stampa i primi 3: oltre si scrive
«—») e i secondi delle due chiamate.

È fatto quando la tabella dice tre cose:

- sulle tre domande che la lezione scorsa l'hybrid teneva **seconde**
  (SRV-02, il codice sconto, il piano che si ferma a metà corsa) il chunk
  giusto è **primo** col backend che hai scritto tu, e con Cohere se l'hai
  provato;
- sulle domande che l'hybrid aveva già prime, **nessuna** esce dalla
  top-3: il rerank non ha rotto quello che funzionava (con l'LLM una può
  cambiare posto: succede, e non è un vostro errore — se ne parla al
  reveal);
- hai annotato secondi e token: quanto costa in tempo il giro LLM rispetto
  a quello Cohere si legge dalla tua tabella, non dalle slide.

Un errore **si vede** nell'output: lo stesso id due volte nella colonna
llm, o una colonna con meno chunk delle altre. Vuol dire che
`rerank_llm()` prende gli indici del modello così come arrivano, senza
togliere i doppi né aggiungere i mancanti. Per gli altri errori tipici
(`429` da Cohere, `ValidationError`, colonne identiche all'hybrid) c'è la
lista in fondo a `README.md`: è per il docente, ma potete leggerla anche
voi.

## Se finisci prima

Porta `CONFIG["k_largo"]` a 30 e rilancia: «La scrivania non sta ferma»
adesso è tra i candidati? E il rerank la porta in top-3? Guarda anche
cosa succede ai token dell'LLM con trenta chunk invece di dieci. Prima
di consegnare la tabella rimetti `CONFIG` com'era (k_largo 10, k_finale
3): la tabella vale con quei valori. Un giro in più costa frazioni di
centesimo e quattordici chiamate Cohere sulle mille del mese. Non
rilanciare il main due volte di fila senza aspettare: le dieci chiamate
al minuto del free tier sono per tutta la tua chiave, e la undicesima
risponde `429`; basta aspettare un minuto.
