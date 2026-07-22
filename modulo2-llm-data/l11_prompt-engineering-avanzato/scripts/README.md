# L23 — Prompt Engineering Avanzato · guida agli script

Infrasettimanale (📊 + ⌨️, 2h): **il primo RAG completo del corso**. Col
docente si scrive solo il retrieval (`cerca_chunk`, live coding 15'); poi
gli studenti scrivono DA SOLI il prompt RAG (`costruisci_prompt`: sezioni
marcate, grounding, citazioni, rifiuto) e il giro completo (`rispondi`),
esercizio 1 — e personalizzano il `SYSTEM_PROMPT` (esercizio 2). Il momento
della serata — la domanda E07 che senza documenti era una procedura
inventata e diventa quella vera, citata — succede sulle macchine degli
studenti. Niente notebook, solo script `.py`.

Il `check_lab23.py` è **strumento del docente**, fuori dal percorso studente
(il "fatto quando" degli esercizi è l'output osservabile): preparazione,
regressione e diagnosi rapida di uno studente bloccato.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 codice di riferimento che il docente
live-coda · ⌨️ da completare dagli studenti · 📄 documenti/dati di esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Dipendenze (`openai`, `chromadb`, `numpy`, `python-dotenv`). |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` — la **stessa chiave di L13-L22**. |
| `CONSEGNA.md` | 🧰 | Promemoria operativo della serata per gli studenti. |
| `scaffolding/aikit/` | 🧰 | Il toolkit completo: `llm_client.py` (L15, **promosso stasera** coi prezzi inclusi), `embeddings.py` (L19), `search.py` (L20), `vectorstore.py` (L21-L22). **Non si tocca**: si importa. |
| `scaffolding/prepara_collection.py` | 🧰 | La **riserva**: ricostruisce `lumen_chunks` da zero (recursive 500, la configurazione di riferimento di L22 — 45 chunk, ~$0.0001) per chi non ha la propria collection. |
| `dataset/*.txt` | 📄 | I 3 documenti lunghi di Lumen (manuale, policy resi, guida smart working), gli stessi di L22. |
| `working/rag.py` | 🎤⌨️ | L'unico file della serata. **TODO 1 col docente** (`cerca_chunk`); **TODO 2-3 da soli** (`costruisci_prompt` e `rispondi` — prescritti solo nomi, variabili del main e scopo); **TODO 4** (`SYSTEM_PROMPT`, esercizio 2). Fornita: `rispondi_senza_documenti` (il confronto). Riferimento in `solutions/`. |
| `scaffolding/check_lab23.py` | 🧰 | **Strumento del docente**: base zero costi (collection presente, il prompt contiene domanda e chunk); `--live` fa il giro vero (~$0.001); `--solutions`. Non compare nel percorso studente. |
| `solutions/rag.py` | 🎤 | La versione **completa** (stesso nome, stessi import): il main e il prompt sono UNA soluzione possibile. |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # dentro: la stessa chiave OpenAI di L13-L22
```

Poi la collection: la propria `chroma/` di L22 copiata qui, oppure
`python scaffolding/prepara_collection.py` (riserva identica).

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env`, `.venv` e `chroma/` (git non li versiona); la collection
> se la portano da L22 o la rigenerano con la riserva.

## Come si prova

```bash
python working/rag.py                         # le prove sulle 2 domande del main
python scaffolding/prepara_collection.py      # la riserva della collection (45 chunk)
python scaffolding/check_lab23.py             # docente: base, zero costi
python scaffolding/check_lab23.py --live      # docente: il giro vero (~$0.001)
python scaffolding/check_lab23.py --solutions # docente: verifica solutions/
```

## Le idee da trasmettere (coi numeri misurati, 09/07/2026)

1. **Il nuovo della serata è UNA funzione.** Retrieval e generazione sono
   import da `aikit/`: il codice che si scrive stasera è il prompt. Per
   questo il prompt engineering conta: è l'unico pezzo che scrivi ogni volta.
2. **Il modello risponde sempre, con o senza fondamento.** La E07 senza
   documenti: una procedura plausibile ma sbagliata, tono sicurissimo (a
   temperature 0.7 i dettagli cambiano a ogni run — mai la stessa frase due
   volte, verificato — la sicurezza del tono no). Col RAG: la procedura
   vera del manuale, con la fonte. La sicurezza del tono non è un segnale
   di verità.
3. **Il rifiuto è una risposta giusta.** Sul contrassegno (che nei documenti
   non c'è) il modello da solo inventa i metodi di pagamento; il RAG con
   grounding dice "Non lo trovo nei documenti" — ed è la risposta migliore.
4. **Few-shot, onestamente**: il formato ticket a 3 righe è rispettato sia
   con istruzioni chiare sia con 2 esempi (38 vs 60 token out). Gli esempi
   sono l'attrezzo in più quando mostrare batte descrivere — non un dogma.
5. **CoT, onestamente**: col contesto giusto la risposta è corretta con e
   senza (out 79 → 191 token, $0.000315 → $0.000499): compra trasparenza,
   non correttezza. Il ragionamento vero oggi si compra coi reasoning model.
6. **Il ponte a L24**: query vaga sui saldi → chunk sbagliato → "30 giorni"
   sbagliato con e senza CoT. Quando il RAG sbaglia, spesso è il retrieval,
   non il prompt: sabato si misura.

## Percorso in aula (le slide sono la regia: ogni switch ha la sua slide)

1. **Teoria (📊, 50')**: system prompt, struttura e delimitatori, few-shot
   onesto, CoT coi numeri + reasoning model, panorama in una slide,
   anatomia del prompt RAG.
2. **Live coding (🎤, 15')**: `cerca_chunk` col docente (TODO 1) + la
   demo-shock `rispondi_senza_documenti` sulla E07.
3. **Esercizio 1 (⌨️, 35')**: `costruisci_prompt` e `rispondi` da soli
   (TODO 2-3); fatto quando la E07 risponde con la procedura vera e la
   fonte, e il contrassegno ottiene il rifiuto pulito.
4. **Esercizio 2 (⌨️, 15')**: il `SYSTEM_PROMPT` (TODO 4), prima/dopo sulle
   stesse domande.
5. **Wrap-up (📊, 5')**: recap + il teaser del retrieval miss → sabato
   (L24) si misura. Collection e `rag.py` non si cancellano.
