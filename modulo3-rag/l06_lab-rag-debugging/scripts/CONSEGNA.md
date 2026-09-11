# Modulo 3 · Lezione 6 — Lab RAG: debugging del retrieval · consegna

Si lavora in `working/debug.py`, e si annota in `working/griglia.md`.
Dove sta il resto (i documenti, il toolkit, il database): `MAPPA.md`. Dentro ci sono la
`CONFIG` con tutte le leve in cima, il `QUERY_SET` (le tredici domande
delle lezioni scorse, oggi con accanto a ognuna una **frase attesa**),
una lista `LE_MIE_QUERY` vuota, due funzioni già scritte (`prepara()`,
che applica le leve, e `cerca()`, il retrieval secondo `CONFIG`), **tre
TODO** — le tre domande del metodo —, gli helper di stampa e il main. Il
main si ferma al primo TODO mancante e lo dice. `working/griglia.md` è
la scheda da compilare: una riga per failure nel Lab 2, la cura nel
Lab 3, e in fondo la `CONFIG` con cui si chiude.

La giornata ha tre blocchi pratici: si scrive lo strumento (Lab 1), lo
si usa per trovare i failure (Lab 2), si cerca la cura (Lab 3).

Serve `OPENAI_API_KEY` in `.env` (la stessa del Modulo 2). `COHERE_API_KEY`
è facoltativa: è la chiave Trial fatta a Modulo 3 · Lezione 5, se l'hai
fatta. Se ce l'hai, nel Lab 3 il rerank
Cohere si accende con **due** chiavi di `CONFIG` insieme, `"retrieval":
"rerank"` e `"backend": "cohere"`; se non ce l'hai lasci `"backend":
"llm"` (con `"cohere"` e la chiave vuota il primo giro si ferma con un
errore `401` di Cohere: si rimette `"llm"`). Setup (venv,
`requirements.txt`, `.env`): in `README.md`, sezione Setup. Si lancia
tutto dalla cartella `scripts/`: `python working/debug.py`. Al primo
avvio, se la collection `lumen_m3` manca, la indicizza (82 chunk, un paio
di minuti, meno di un centesimo).

`rerank.py` della lezione scorsa è passato in `scaffolding/aikit/` e si
importa; con `rag.py` e `hybrid.py` **non si tocca**: oggi le leve si
girano tutte da `CONFIG`.

## La frase attesa

Per sapere se una risposta è giusta serve sapere qual è il chunk giusto.
Invece dell'id (che cambia se si cambia il chunk size) si usa una **frase
attesa**: un pezzo di testo che sta **solo** nel chunk giusto, per esempio
`TCK-1152`, `ESTATE15`, `scollega l'alimentazione per 30 secondi`. Per
le tredici domande del set è già scritta; per le domande vostre la
trovate voi leggendo i documenti in `dataset/lumen_m3/` (o con
`trova_nel_corpus()`, appena l'avete scritta). **Copiatela dal file**,
non riscrivetela a mano: un accento o un trattino diverso e la frase
«non c'è». `None` vuol dire: la
risposta non è nel corpus, il sistema deve dire «Non lo trovo nei
documenti.»

## Lab 1 — il banco di prova (i tre TODO)

Le tre domande del metodo, in codice. Si prova una domanda alla volta
mettendo la coppia in `SOLO`, in cima al file, per esempio
`SOLO = ("Cosa copre SRV-02?", "SRV-02 — ritiro")`: il main la usa al
posto del giro completo.

### TODO 1 — `trova_nel_corpus(frase)` · esiste?

Ritorna gli id dei chunk che contengono la frase (maiuscole e minuscole
non contano); lista vuota se non c'è. Tutti i chunk sono in
`hybrid.INDICE["chunks"]`, una lista di dict con `id`, `testo` e
`source`, riempita da `prepara()`: il main la chiama per primo, quindi
si prova la funzione dal main (con `SOLO`), non da sola.

### TODO 2 — `diagnostica(query, frase_attesa)` · le tre domande

Con la `CONFIG` corrente, stampa (1) se la frase attesa esiste nel
corpus e in quali chunk; (2) se il primo di quei chunk è nel top-k, cioè
tra i primi `CONFIG["k"]` dei candidati di `cerca(query)`, e a che
posizione sta (`cerca()` ne ritorna `CONFIG["candidati"]`, di più, per
dire quanto è lontano); (3) la risposta di `rag.genera()` sui primi k, e
se **la usa**, cioè se cita uno dei chunk attesi (le citazioni sono tra
parentesi quadre, `[id]`). Se la frase attesa è `None`, la risposta è
giusta quando dice «Non lo trovo nei documenti.». Ritorna
`(posizione, nel_topk, giusta)`: posizione `None` se il chunk non è tra
i candidati. È il TODO lungo della giornata: prenditi il tempo, e provalo
con `SOLO` man mano che lo scrivi, senza aspettare di averlo finito.

### TODO 3 — `giro()`

`diagnostica()` su tutto `QUERY_SET + LE_MIE_QUERY`, poi la tabella
riassuntiva con `stampa_tabella()` (già scritta): una riga per domanda con
posizione, nel top-k, giusta, e in fondo quante risposte sono giuste.

**Fatto quando:** con `SOLO = None` il giro gira su tutto il set e
stampa la tabella: sulla baseline (semantico, k 4) sono **10 risposte
giuste su 13**. Se esce 9/13 o 11/13 non è per forza un errore vostro:
la generazione oscilla, si rilancia una volta e si guarda quale riga è
cambiata.

## Lab 2 — caccia ai failure (le query vostre)

Lo strumento c'è: ora si usa. Guarda le tre risposte che mancano sulla
baseline e per ognuna rispondi alle tre domande. Poi scrivi domande **tue** sui sei
documenti — almeno tre, con codici, con parole diverse da quelle del
documento, su cose che nel documento non ci sono — e mettile in
`LE_MIE_QUERY` con la loro frase attesa; scambiale col vicino.

Ogni failure va nella **prima tabella di `working/griglia.md`**, una riga
ciascuno: la domanda, la frase attesa, le tre risposte della diagnostica
e la **lettera del caso**, cioè dove si ferma la catena delle tre domande
e dove sta il chunk. La legenda dei sei casi è nella griglia stessa: A e
B sono fuori dal top-k, vicino o lontano; C e D la domanda senza
risposta, detta o inventata; E il chunk nel prompt e ignorato; F la
risposta giusta ma costosa.

**Fatto quando:** la griglia ha almeno sei failure con la lettera del
caso, di almeno due casi diversi. Il caso C (la domanda non ha risposta
e il sistema lo dice) si annota ma non conta tra i sei. Se una domanda
vostra viene risposta bene, non è un failure: si scarta e se ne scrive
un'altra.

## Lab 3 — cura mirata (nessun TODO: si lavora su CONFIG)

Per ogni failure della prima tabella scegli **una** leva coerente con il
caso, e riempi la **seconda tabella** di `working/griglia.md` (stesso
numero di riga):

| Caso | Leve |
|---|---|
| A (fuori dal top-k, vicino) | `k` più alto · `retrieval` → `"rerank"` (riordina i candidati prima del taglio) · `"hybrid"` (le parole esatte, i codici) |
| B (fuori dal top-k, lontano) | `"hybrid"` se nella domanda c'è un codice; altrimenti nessuna leva di oggi, si annota |
| D (non esiste, risponde lo stesso) | `soglia` (solo col semantico o con rerank Cohere: lì lo score è una pertinenza) · `istruzioni` |
| E (nel top-k, ignorato) | `"rerank"` per metterlo primo + `k` basso (meno distrattori) · `istruzioni` |
| F (giusta ma costosa) | `k` più basso, verificando che resti giusta |

Un esempio del ciclo, lo stesso della slide sull'anti-regressione (è
già fatto: **non conta** tra i vostri due failure curati): TCK-1152 è 10°, k 4:
caso A → provo `retrieval = "hybrid"` →
rilancio il giro → TCK-1152 è 1° e giusta, ma «metà corsa» è passata da
1° a 2° → nella seconda tabella scrivo leva `hybrid`, dopo `1 / sì`,
regressioni «metà corsa 1° → 2°, ancora nel prompt» → rimetto
`"semantico"` e passo al failure successivo.

Un giro costa frazioni di centesimo (13 chiamate a `gpt-4o-mini`, più
13 al reranker se `"rerank"`); con `"cohere"` il giro dura un minuto e
mezzo per il free tier (10 chiamate al minuto) e due giri di fila danno
`429`: si aspetta un minuto.

Cambi la leva in `CONFIG`, rilanci il giro, annoti nella griglia «dopo» e
le **regressioni**: le query che prima erano giuste e ora non lo sono —
le tredici del set, e anche le vostre se erano giuste. Una leva alla volta: prima della prova successiva riporti `CONFIG`
alla baseline. Se una leva da sola non basta, ne provi una seconda
**insieme** alla prima, e in griglia scrivi tutte e due: lo sai che
servono entrambe solo perché le hai misurate una per una. La generazione
non è deterministica: se una risposta cambia da sola tra un giro e
l'altro non è una regressione, e lo vedi rilanciando.

**Fatto quando:** almeno due failure sono curati (TCK-1152 con hybrid,
l'esempio del brief, non conta), almeno una cura usa `"hybrid"` o
`"rerank"`, e per ogni query del set che è peggiorata sai dire perché.

## Se finisci prima

Gli esiti li vedi anche al rientro del Lab 3: qui li misuri con le tue
mani, ed è il punto, e al rientro li racconti. La scrivania («non sta ferma», caso
B) non si cura con nessuna leva di oggi: prova `candidati = 30` e guarda
a che posizione sta, poi prova `"rerank"`. Cerca nel corpus la portata massima
della LD-210: ci sono **due** risposte, e nessuna leva sceglie quella
giusta. Prova le leve del caso E su «Posso usare un alimentatore da 4A
al posto di quello in dotazione?» (frase attesa `TCK-1201`): il chunk è
primo e il modello rifiuta con tutte. E prova `k = 20`: quante risposte
giuste, e quanti token in più per ogni domanda? Fatto quando le quattro
cose sono in griglia, una riga ciascuna, con posizione o conteggio
annotati.
