# Scheda esperimenti — Lab Prompt & Search

Versione COMPLETA (riferimento docente): i giri sono stati eseguiti davvero
(gpt-4.1-mini, 09-16/07/2026) con la collection di riserva `recursive/500`.
Una soluzione possibile: gli studenti possono trovare esiti diversi sulle
proprie varianti di prompt.

Esito: ✔ corretta e fondata · ✂ incompleta/parziale · ✗ sbagliata o
inventata · ∅ rifiuto (corretto solo per la query fuori-corpus)

## Lab 1 — A/B di prompt

| # | GROUNDING | CON_COT | CITAZIONE | facile | trappola | fuori-corpus | facile-2 | token out (tot.) | costo (tot.) | note |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | morbido | no | breve | ✔ | ✔ | ∅ | ✗ | 211 | $0.00133 | baseline |
| 2 | severo | no | breve | ✔ | ✔ | ∅ | ✗ | 232 | $0.00142 | risposte un po' più lunghe (+41 token input dal system prompt più lungo), esito IDENTICO al morbido su tutte e 4 |
| 3 | morbido | sì | breve | ✔ | ✔ | ✗ | ✗ | 483 (3 query) | $0.00155 (3 query) | +129% output: il modello VERBALIZZA il ragionamento; sulla query fuori-corpus rompe il rifiuto fisso e scrive un rifiuto discorsivo — il CoT peggiora l'aderenza al formato |
| 4 | morbido | no | estesa | ✔ | ✔ | ∅ | ✗ | 269 (3 query) | $0.00121 (3 query) | citazione con frase esatta tra virgolette, verificabile a colpo d'occhio; +27% token vs baseline |
| 5 | severo | no | estesa | ✔ | ✔ | ∅ | ✗ | 237 (3 query) | $0.00121 (3 query) | combinazione: stesso esito delle singole varianti, costo in linea con estesa da sola |

**Quale variante vince, e su quali query si stacca?** Nessuna variante di
prompt cambia l'esito su NESSUNA delle 4 query: severo/estesa cambiano solo
forma (più lunghe, citazione più verificabile) a costo moderato; CoT è
l'unica che PEGGIORA qualcosa (rompe il formato di rifiuto) e costa il
doppio. **facile-2 fallisce in ogni variante**: il prompt non può risolvere
un problema che nasce prima, nel retrieval.

## Lab 2 — tuning del retrieval

| # | K | SOGLIA | strategia/size collection | facile | trappola | fuori-corpus | facile-2 | note |
|---|---|---|---|---|---|---|---|---|
| 1 | 4 | 0.0 | recursive/500 (45 chunk) | ✔ | ✔ | ∅ | ✗ | baseline — vedi diagnosi sotto |
| 2 | 6 | 0.0 | recursive/500 | ✔ | ✔ | ∅ | ✗ | ancora niente: il chunk mancante è 8° per score (0.396), fuori anche da k=6 |
| 3 | 8 | 0.0 | recursive/500 | ✔ | ✔ | ∅ | ✔ | risolto: entrano ENTRAMBI i chunk (0.639 e 0.396), risposta completa con doppia fonte — ma +70% token input vs k=4 |
| 4 | 4 | 0.0 | recursive/800 (reindicizza_chunks, 29 chunk) | ✔ | ✔ | ∅ | ✔ | risolto anche così: a 800 caratteri i due dettagli (importo + scadenza) stanno nello STESSO chunk, una sola fonte citata, costa meno di k=8 |

**Diagnosi facile-2** (`aikit.vectorstore.search`, 8 risultati): il
documento sulla postazione ha l'importo (250€) in un chunk e la scadenza
(60 giorni) nel chunk SUCCESSIVO — la frase è tagliata a metà dal
`recursive/500`. A k=4 arriva solo il secondo chunk (score 0.639), il primo
resta fuori a 0.396 (8° posto): il modello ha la scadenza ma non l'importo,
e con `costruisci_prompt` che vieta di aggiungere ciò che non è scritto,
rifiuta l'intera risposta invece di rispondere a metà.

**Soglia**: non è una manopola che risolve QUESTO caso. Le query
genuinamente fuori corpus (fuori-corpus: contrassegno) hanno score 0.50-0.57
— PIÙ ALTI del chunk mancante di facile-2 (0.396). Una soglia abbastanza
bassa da includere 0.396 include anche rumore vero; una soglia che esclude
il rumore esclude anche l'informazione buona. Qui il fix è k o il chunk
size, non lo score minimo.

**Quale modifica ha cambiato visibilmente la risposta?** k 4→8 e il
re-chunking a 800 caratteri, **entrambi** risolvono facile-2 — con
compromessi diversi (k=8: più contesto, +70% input token, due fonti da
riconciliare; size=800: un chunk solo, risposta più pulita, ma tocca TUTTA
la collection, non solo questa query).

## Conclusione della giornata

Prompt vincente: **severo + citazione estesa** — nessun guadagno di
correttezza sulle query di questa sessione, ma citazioni verificabili a
un costo ancora modesto (~$0.0005/risposta). CoT scartato: costa il doppio
e rompe il formato di rifiuto.

Configurazione di retrieval vincente: **recursive/800 chunk-size** (non
k=8): stesso esito, risposta con una sola fonte invece di due, meno token
per risposta.

Perché: il prompt regola COME si risponde coi documenti che arrivano;
quando il problema è che il documento giusto non arriva (o arriva a metà),
nessun prompt lo ripara — bisogna cambiare cosa il retrieval porta in
tavola. È la stessa lezione del wrap-up di L23, misurata oggi.
