# Modulo 2 · Lezione 15 — Progetto Modulo 2 · consegna

Oggi non si impara niente di nuovo: si mette in fila tutto il modulo in
un'unica app, sul corpus che scegliete voi. Un solo file per tutta la
giornata: `working/app.py`. Tutto si lancia dalla cartella `scripts/`.
`aikit/` vive in `scaffolding/aikit/` (non serve pensarci: `app.py` lo importa
già da lì) — se volete guardare una firma o una docstring, è quella la
cartella da aprire.

## Setup (una volta sola, nei primi minuti)

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # dentro: la STESSA chiave OpenAI di Modulo 2 · Lezioni 1-14
```

> Chiave persa? **Alzate la mano**: il docente ha una chiave di riserva.

## Il corpus: libero

Mettete **3-10 file** vostri (PDF, DOCX, HTML, Markdown o testo semplice) in
`dataset/mio_corpus/`. Se non avete nulla di pronto, copiate lì il contenuto
di `dataset/riserva_lumen/` (i tre documenti lunghi già noti da Modulo 2 ·
Lezione 10-12):

```bash
cp dataset/riserva_lumen/* dataset/mio_corpus/
```

Le fatture di `dataset/fatture_lumen/` sono invece **fisse e uguali per
tutti**: non si toccano, servono solo al blocco di estrazione.

## Build (⌨️ 170') — `working/app.py`

| TODO | Cosa | Fatto quando |
|---|---|---|
| 1 | `indicizza_corpus()`: load (Modulo 2 · Lezione 4) + clean (Modulo 2 · Lezione 5) + chunk (Modulo 2 · Lezione 10) + embed (Modulo 2 · Lezione 7) + index (Modulo 2 · Lezione 9) su tutti i file di `dataset/mio_corpus/` | stampa un numero di chunk indicizzati coerente col numero di file |
| 2 | `cerca_chunk(query, k)`: riapre la collection e cerca (Modulo 2 · Lezione 11, quasi identico) | su una query di prova tornano `k` risultati con score |
| 3 | `genera_risposta(query, chunks)`: prompt RAG (Modulo 2 · Lezione 11) + structured outputs su `RispostaRAG` (Modulo 2 · Lezione 13) | su una domanda nel corpus `trovato=True` con una fonte vera; su una fuori corpus `trovato=False`, senza inventare |
| 4 | `estrai_fattura(path)`: schema `Fattura` di Modulo 2 · Lezione 14 (già in cima al file, non si riscrive) | sulla fattura senza sconto, `sconto`/`note` tornano `None`, non un valore inventato |

**Se un file del vostro corpus dà un errore di encoding o di parsing**:
passate alla riserva Lumen e tornateci dopo — non restate bloccati sul TODO 1
per tutta la mattina. Attenzione anche al caso silenzioso: un PDF scansionato
(pagina-immagine) non dà errore, ma produce testo vuoto — se il conteggio
chunk vi sembra basso rispetto ai file caricati, controllate se è per questo.

Prima di lanciare, ricordatevi di riempire `QUERY_DI_PROVA` in fondo al file
(è vuota apposta) con 2-3 domande sul vostro corpus: senza, l'app indicizza ma
non stampa nessuna risposta.

```bash
python working/app.py
```

## Demo & valutazione (⌨️ 45')

Mostrate la vostra pipeline su 2-3 query del vostro corpus più l'estrazione
delle tre fatture Lumen. Nessuna scheda da compilare oggi: il deliverable è
l'app che gira.

## Cosa portate a casa

`app.py` con la pipeline completa `load → clean → chunk → embed → search →
generate` (risposta strutturata) più l'estrattore fatture — tutto il Modulo 2
in un unico file. Settimana di pausa, poi Modulo 3 riparte esattamente da qui.
