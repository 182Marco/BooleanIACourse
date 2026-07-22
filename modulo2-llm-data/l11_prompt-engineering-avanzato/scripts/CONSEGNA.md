# L23 — Prompt Engineering Avanzato · consegna

Stasera si chiude il cerchio: col docente si scrive il retrieval
(`cerca_chunk`), poi scrivete VOI il prompt RAG e il giro completo — la
prima risposta fondata sui VOSTRI documenti, con la fonte citata. Tutto si
lancia dalla cartella `scripts/`.

## Setup (una volta sola, nei primi minuti della teoria)

Ogni lezione ha la sua cartella `scripts/` col suo venv: quello di stasera
è **nuovo**. Se `scripts/.venv` esiste già, il setup l'avete già fatto.

Aprite il terminale **nella cartella della lezione** (quella scaricata da
Drive, che contiene `scripts/` — un `ls` deve mostrarvela), poi:

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # dentro: la STESSA chiave OpenAI di L13-L22
```

**Fatto quando:** il prompt del terminale mostra `(.venv)` davanti (il venv è
attivo); `pip install` finisce con `Successfully installed ...` (nessun
`ERROR` sopra); `.env` esiste in `scripts/` e la riga `OPENAI_API_KEY=` ha
davvero la chiave dopo l'`=`, non vuota.

> Chiave persa? **Alzate la mano**: il docente ha una chiave di riserva.

## La collection: la VOSTRA, di sabato scorso

Il RAG cerca nella collection `lumen_chunks` di L22. Chi ha la propria
cartella `chroma/` di L22 la **copia qui dentro** (in `scripts/`):

```bash
cp -r ../../lezione-22-chunking-strategies/scripts/chroma .
```

(non trovate la cartella? `ls ../..` da `scripts/` mostra le cartelle delle
lezioni: cercate quella di L22 e adattate il percorso). **Per tutti gli
altri** — a L22 non c'eravate, non
avete finito, o semplicemente non siete sicuri di averla — la riserva è
identica e non richiede permesso: un decimo di centesimo, si rigenera
sempre da qui:

```bash
python scaffolding/prepara_collection.py
```

## Live coding col docente (🎤 si replica) — `working/rag.py`

| TODO | Cosa | Fatto quando |
|---|---|---|
| 1 | `cerca_chunk(query, k)`: la collection `lumen_chunks` interrogata via `aikit.vectorstore` | il docente la prova a schermo — 4 chunk con score per la domanda E07 — e la vostra fa lo stesso |

In chiusura del blocco, la demo col modello **da solo**
(`rispondi_senza_documenti`, fornita): tenete a mente quella risposta.

## Esercizio 1 (⌨️ da soli) — sempre `working/rag.py`

Scrivete il prompt RAG e il giro completo. **Prescritti solo i nomi, le
variabili del main e lo scopo**: il come — e le parole del prompt — sono
vostri.

| TODO | Cosa | Fatto quando |
|---|---|---|
| 2 | `costruisci_prompt(query, chunks)`: sezioni marcate (istruzioni / documenti con fonte / domanda), grounding («SOLO dai documenti»), citazione della fonte, rifiuto esplicito quando la risposta non c'è | su `DOMANDA_NEI_DOCUMENTI` (E07) la risposta è la **procedura vera del manuale, con la fonte** — non quella inventata di prima |
| 3 | `rispondi(query, k)`: cerca_chunk → costruisci_prompt → `llm.chat(..., instructions=SYSTEM_PROMPT)` | su `DOMANDA_FUORI` (contrassegno) esce il **rifiuto pulito**, non metodi di pagamento inventati |

```bash
python working/rag.py                     # le vostre prove (~$0.0004 a risposta)
```

## Esercizio 2 (⌨️ da soli) — il `SYSTEM_PROMPT`

Riscrivete il `SYSTEM_PROMPT` in cima al file: CHI è l'assistente, il TONO,
il FORMATO delle citazioni (potete comprarlo con 2 esempi few-shot), come
deve SUONARE il "non c'è". Poi le stesse due domande, **prima e dopo**:
fatto quando la risposta cambia nel modo che avevate deciso e il rifiuto
resta pulito.

## Cosa portate a casa

Fatto il TODO 4 col rifiuto ancora pulito? **Avete finito quello che serve
stasera** — il resto (altre prove, altre domande) è curiosità, non
necessario.

`rag.py` — il **primo RAG end-to-end del corso, scritto da voi** — più la
collection. **Non cancellate niente**: sabato (L24, Lab Prompt & Search) si
misura e si fa tuning proprio su questo.
