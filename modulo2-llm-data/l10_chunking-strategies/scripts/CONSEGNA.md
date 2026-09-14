# Modulo 2 · Lezione 10 — Chunking Strategies · consegna

Stasera arrivano i **documenti lunghi**: tre file di Lumen che non stanno
sensatamente in un embedding solo. Si spezzano (chunking), si embeddano, si
indicizzano e si interrogano — e a ogni configurazione il retrieval cambia
faccia. Un solo file per tutta la serata: `working/chunk.py`. Tutto si
lancia dalla cartella `scripts/`.

## Setup (una volta sola, nei primi minuti)

Ogni lezione ha la sua cartella `scripts/` col suo venv: quello di stasera
è **nuovo** (non si riusa quello di Modulo 2 · Lezione 9). Aprite il terminale nella cartella
della lezione (quella scaricata da Drive, che contiene `scripts/`), poi:

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # dentro: la STESSA chiave OpenAI di Modulo 2 · Lezione 1-9
```

> La chiave è quella che avete già: la trovate nel file `scripts/.env` della
> cartella di una lezione precedente, da copiare qui dentro.

> Il `pip install` si porta dietro di nuovo `chromadb`: se ci mette qualche
> minuto è normale, lasciatelo andare mentre il brief continua.

> Chiave persa? **Alzate la mano**: il docente ha una chiave di riserva.

**Setup finito quando:** `python working/chunk.py` stampa la riga `config:
fixed · size 500 …` e sotto `[--] ancora da scrivere — TODO 1: chunk_fixed`.
La riga `[--]` è normale: è il primo TODO della serata.

Niente corpus embeddato da copiare stasera: i documenti sono in `dataset/`
in chiaro e gli embedding si calcolano **a ogni giro** (backend `openai`
per tutti). La collection `lumen_chunks` si **ricrea da zero** a ogni
lancio: è il punto della serata.

## Live coding col docente (🎤 si replica) — `working/chunk.py`

| TODO | Cosa | Fatto quando |
|---|---|---|
| 1 | `chunk_fixed(testo, size, overlap)`: blocchi di `size` caratteri, ogni blocco riparte `overlap` caratteri indietro | lanciando lo script, i tagli stampati cadono ogni 500 caratteri esatti — anche in mezzo alle parole (solo l'ultimo pezzo di ogni documento è più corto: è il resto) |
| 2 | `chunk_recursive(testo, size)`: il taglio cade sull'ultimo separatore che ci sta (paragrafo → riga → frase), poi si riparte da lì. Per lanciarla mettete `STRATEGIA = "recursive"` in testa al file | i tagli stampati cadono su titoli e confini di frase, mai a metà parola |

`chunk_semantic(testo, soglia)` è **già scritta**: il docente la mostra in
demo (taglia dove la similarità tra frasi adiacenti cala: un calo = cambio
di argomento). Voi la **usate** negli esperimenti, non la scrivete.

## Esperimenti (⌨️ da soli) — le manopole in testa al file

In testa a `working/chunk.py` ci sono quattro costanti:

```python
STRATEGIA = "fixed"      # "fixed" | "recursive" | "semantic"
CHUNK_SIZE = 500         # caratteri (fixed e recursive)
OVERLAP = 0              # caratteri ripetuti tra chunk vicini (solo fixed);
                         # tenetelo sempre MINORE di CHUNK_SIZE
SOGLIA = 0.4             # sotto questa similarità si taglia (solo semantic)
```

> Avete chiuso il terminale o ne avete aperto uno nuovo (pausa, computer in
> sospensione)? Prima di rilanciare: `cd` nella cartella `scripts` e
> `source .venv/bin/activate` di nuovo. Un `ModuleNotFoundError: No module
> named 'chromadb'` — o un `python` che non risponde — vuol dire venv non
> attivo: non avete rotto niente.

Il giro è sempre lo stesso: **cambiate la config → rilanciate → leggete →
annotate** una riga nella tabella in fondo al file (è tutta commentata: scriverci
dentro non tocca il codice). Una manopola per volta
quando potete: è così che si sa a cosa attribuire la differenza. Lo script
rifà tutto da solo: ri-chunk, ri-embed, ri-indicizza (collection ricreata),
ri-cerca le tre query note.

Come si legge l'output: per ogni query lo script stampa la **risposta
attesa** e sotto il **1° risultato per intero**. Confrontateli:

- **OK** — la risposta è lì, tutta.
- **META** — c'è solo un pezzo: il testo si interrompe a metà.
- **FUORI** — quel testo non è la risposta: parla d'altro, o ve la fa
  cercare voi (è il caso del documento intero).

**Fatto quando:** avete provato **tutte e tre le strategie** (con almeno un
paio di taglie diverse su fixed) e trovato almeno una configurazione **OK su
tutte e tre** le query — e sapete dire quale manopola ha fatto la differenza.
La config vincente si azzecca anche al secondo lancio: è il confronto che
insegna qualcosa, non la riga giusta.
Occhio anche alla riga `[openai] … token → $…` che passa a ogni giro (la
stampa `embed()`, dal toolkit di Modulo 2 · Lezione 7): l'indicizzazione si
ri-paga ogni volta, e alcune configurazioni costano più di altre — con
`semantic` la riga passa **due volte**, perché prima si embeddano le frasi
per decidere i tagli e poi i chunk per l'indice.

**Se finite prima (facoltativo).** Rifate la prova dei **documenti interi**
vista in teoria: `fixed` con `CHUNK_SIZE = 6000` — più lungo del documento
più lungo, quindi un chunk per documento. Poi cercate il **punto di rottura**
di una configurazione che funziona: da `recursive` 500, scendete a 300, 200,
120 — a che taglia la risposta comincia a spezzarsi? E provate una query
vostra su un fatto che sapete essere nei documenti: la config che vince sulle
tre note vince anche sulla vostra?

```bash
python working/chunk.py     # un esperimento = un lancio (~$0.0001-0.0002 a giro)
```

**Prima di chiudere:** rimettete la configurazione che avete scelto e
rilanciate un'ultima volta. Su disco resta la collection dell'**ultimo
lancio**: è da lì che si riparte la prossima lezione. Non sapete quale
scegliere? `recursive` con size 500.

## Cosa portate a casa

`chunk.py` con le vostre due strategie scritte a mano, la **tabella
esperimenti** compilata (la vostra mappa di cosa funziona su questo corpus)
e la collection `lumen_chunks` su disco con la configurazione scelta: nella
prossima lezione (Modulo 2 · Lezione 11) quei chunk finiscono **dentro un
prompt** — il primo RAG completo del corso.
