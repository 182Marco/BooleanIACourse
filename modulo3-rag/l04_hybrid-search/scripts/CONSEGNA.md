# Modulo 3 · Lezione 4 — Advanced Retrieval I: Hybrid Search · consegna

Si lavora in **un solo file**: `working/hybrid.py`. Dentro ci sono la
`CONFIG` in cima, il `QUERY_SET` (le tredici domande del modulo),
`tokenizza()` già scritto, le due funzioni dell'indice BM25 **già
scritte** (il docente le spiega, voi seguite sul file: non si ricopia
niente), due TODO e un main già pronto: lancia la demo del codice spiegato
e poi tutto il query set nelle tre modalità. Se mancano i TODO 3-4 il main
prosegue e nella colonna hybrid stampa «(ancora da scrivere)».

## Codice spiegato — l'indice BM25 (già nel file)

### 1 — `costruisci_indice_bm25()` (🎤 già scritta, il docente la spiega)

Legge tutti i chunk della collection `lumen_m3` (gli stessi 82 di
`rag.py`, stessi id) e costruisce l'indice `BM25Okapi` sui loro token.
Riempie `INDICE["bm25"]` e `INDICE["chunks"]`, ritorna quanti chunk ha
indicizzato.

### 2 — `cerca_bm25(query, k)` (🎤 già scritta, il docente la spiega)

I `k` chunk con lo score BM25 più alto, nella stessa forma di
`rag.recupera()` (dict con `id`, `testo`, `score`, `source`). Le due funzioni sono già
nel vostro file: durante la spiegazione si segue sul proprio
`working/hybrid.py`, non si ricopia. Se per sbaglio le rompete, la
versione buona è in `solutions/hybrid.py`.

## Esercizio — la fusione

### TODO 3 — `rrf(liste, k)` (⌨️ da soli)

Reciprocal Rank Fusion: da più liste ordinate di chunk a una sola. Ogni
chunk vale `1 / (CONFIG["rrf_costante"] + posizione)` in ogni lista in cui
compare (posizione a partire da 1), e i contributi si sommano. Ritorna i
`k` chunk con la somma più alta, con `score` = la somma. Degli score
originali (coseno, BM25) non si usa niente: conta solo il rango.

### TODO 4 — `cerca_hybrid(query, k)` (⌨️ da soli)

`CONFIG["candidati"]` chunk dal semantico (`rag.recupera`) e altrettanti da
BM25 (`cerca_bm25`), fusi con `rrf()`. Ritorna i `k` chunk in testa alla
fusione.

## Quando è fatto

Lancia `python working/hybrid.py` dalla cartella `scripts/`: il main
stampa, per ogni domanda del query set, le tre modalità fianco a fianco
(semantico / bm25 / hybrid). Compila la **tabella in fondo al file**: per
ogni domanda qual è il chunk giusto e in che posizione sta nelle tre
modalità. Il main stampa i primi `CONFIG["k"]` (3) di ogni modalità: se
il chunk giusto non è tra quelli, per sapere dove sta davvero alza
`CONFIG["k"]` a 10 e rilancia: vale per tutte le domande insieme, quindi
basta un solo rilancio (frazioni di centesimo); oltre il decimo posto si
scrive «—». Per capire qual è il chunk giusto basta di solito l'inizio del
testo stampato accanto a ogni id; se non basta, il testo intero sta nel
documento in `dataset/lumen_m3/` (l'id dice quale: `ticket-supporto-008` è
nel file `ticket-supporto.txt`) — si cerca lì la frase dell'anteprima.

È fatto quando la tabella dice due cose:

- sulle domande **con un codice** l'hybrid non è mai dietro al semantico:
  su alcune porta in testa il chunk che il semantico teneva dietro, su
  altre lo porta più in alto senza arrivare al primo posto (succede, e non
  è un errore: se ne parla al reveal), su altre ancora non cambia nulla
  perché il semantico era già primo;
- sulle domande **concettuali** (il contributo, l'estero, il monitor che
  scende) il chunk giusto **resta in top-3** con l'hybrid: la fusione non
  ha peggiorato quello che funzionava.

La seconda metà è il punto: un miglioramento che rompe il resto non è un
miglioramento.

Un errore **si vede** nell'output, se lo si guarda: lo stesso id due
volte nella colonna hybrid. Vuol dire che `rrf()` ricostruisce i chunk
male (di solito due cicli annidati e un `break` che chiude solo quello
interno). Due errori invece **non si vedono a occhio**: usare lo score al
posto della posizione in `rrf()`, e chiedere `k` chunk invece di
`candidati` in `cerca_hybrid()`. In entrambi i casi il programma gira e
stampa numeri plausibili. Per questi due, e solo per questi, c'è una
verifica secca:

```bash
python scaffolding/check_lab04.py
```

stampa `[OK]`/`[FAIL]` per ogni TODO senza chiamate a servizi.

## Se finisci prima

Porta `CONFIG["candidati"]` a 3 e poi a 30 e rilancia: cosa cambia
nell'hybrid quando le due liste sono corte, e quando sono lunghe? Poi
`CONFIG["rrf_costante"]` a 1: la fusione premia di più chi sta primo in una
sola lista, e si vede su quali domande. Prima di consegnare la tabella
rimetti `CONFIG` com'era (k 3, candidati 10, costante 60): la tabella vale
con quei valori. Rilanciare non è un problema di
costi: un giro del query set embedda tredici domande, frazioni di centesimo.
