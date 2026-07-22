# L24 — Lab Prompt & Search · consegna

Oggi non si scrive un RAG nuovo: si **misura e migliora** quello di L23,
una manopola alla volta, annotando ogni esito in
`working/scheda_esperimenti.md`. Tutto si lancia dalla cartella `scripts/`.

## Setup (una volta sola, nei primi minuti del brief)

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # dentro: la STESSA chiave OpenAI di L13-L23
```

**Fatto quando:** `(.venv)` davanti al prompt, `pip install` senza `ERROR`,
`.env` con la chiave dopo l'`=`. Chiave persa? **Alzate la mano.**

## La collection: la VOSTRA, di L22-L23

Controllate prima di essere nella cartella giusta: `pwd` deve finire con
`lezione-24-lab-prompt-search/scripts`.

```bash
cp -r ../../lezione-23-prompt-engineering-avanzato/scripts/chroma .
```

Non ce l'avete? La riserva è identica, un decimo di centesimo:

```bash
python scaffolding/prepara_collection.py
```

## Il vostro `rag.py`

**Non sovrascrivete il file fornito**: `working/rag.py` di oggi include già
`cerca_chunk`/`costruisci_prompt`/`rispondi` di L23 PIÙ le manopole e i TODO
di oggi (sovrascriverlo col vostro di L23 li cancella). Se a L23 avevate
personalizzato qualcosa (es. il `SYSTEM_PROMPTS["morbido"]`, il formato delle
citazioni), riportate solo quelle righe dentro il file di oggi. Non c'eravate
o non avete personalizzato nulla? Il file fornito va bene così com'è.

## Lab 1 (⌨️ 90') — A/B di prompt

In cima a `working/rag.py` tre manopole: `GROUNDING`, `CON_COT`,
`CITAZIONE`. Completate le tre varianti mancanti (i `TODO` 1-3 nel file:
`SYSTEM_PROMPTS["severo"]`, l'istruzione di citazione estesa, l'istruzione
di CoT), poi per ogni combinazione che provate:

```bash
python working/rag.py
```

e trascrivete l'esito (per ognuna delle 4 query nel main) in
`working/scheda_esperimenti.md`, tabella Lab 1 — **una riga per giro**,
prima di cambiare la manopola successiva.

**Fatto quando:** la scheda dice quale prompt vince e su quali query si
stacca dalle altre.

## Lab 2 (⌨️ 80') — tuning del retrieval

Nel main dello stesso file, `K` e `SOGLIA`: cambiateli e rilanciate. Per il
chunking, completate `reindicizza_chunks(strategia, size, overlap=0)`
(combina `aikit.chunk` e `aikit.vectorstore`, come a L22): `strategia` è
`"fixed"` o `"recursive"` (`overlap` conta solo per `"fixed"`). Per
richiamarla, girate la manopola `REINDICIZZA` nel main — es.
`REINDICIZZA = ("recursive", 800)` — e rilanciate: la ricostruisce prima
delle query (`REINDICIZZA = None` non tocca la collection esistente). Per
tornare alla configurazione di riferimento, `REINDICIZZA = ("recursive", 500)`.

Ogni giro va in `working/scheda_esperimenti.md`, tabella Lab 2.

**Fatto quando:** almeno una modifica di retrieval cambia visibilmente la
risposta su una delle query — e sapete spiegare perché guardando i chunk
recuperati (`cerca_chunk`), non solo la risposta finale.

## Cosa portate a casa

`working/rag.py` esteso + `working/scheda_esperimenti.md` compilata: il
prompt vincente, la configurazione di retrieval vincente, i perché. È la
scheda il deliverable che conta.
