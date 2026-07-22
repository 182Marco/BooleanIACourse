# L24 — Lab Prompt & Search · guida agli script

Sabato (⌨️, 4h): **A/B testing di prompt e tuning del retrieval** sul RAG
scritto a L23. Niente codice nuovo dal docente — è il metodo sperimentale
che conta: una manopola alla volta, stessa query set, tutto annotato in
`scheda_esperimenti.md`, il vero deliverable della giornata. Niente
notebook, solo script `.py`.

Il `check_lab24.py` è **strumento del docente**, fuori dal percorso
studente: preparazione, regressione e diagnosi rapida di uno studente
bloccato.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · ⌨️ da completare dagli studenti ·
📄 documenti/dati di esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Dipendenze (`openai`, `chromadb`, `numpy`, `python-dotenv`) — stesse di L21-L23. |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` — la **stessa chiave di L13-L23**. |
| `CONSEGNA.md` | 🧰 | Promemoria operativo della giornata per gli studenti. |
| `scaffolding/aikit/` | 🧰 | Il toolkit completo: `llm_client.py` (L15), `embeddings.py` (L19), `search.py` (L20), `vectorstore.py` (L21-L22). **Da oggi si aggiunge `chunk.py`** (L22, promosso): le tre strategie di chunking, riusate nel Lab 2. Non si tocca, si importa. |
| `scaffolding/prepara_collection.py` | 🧰 | La riserva: ricostruisce `lumen_chunks` da zero (recursive 500, 45 chunk, ~$0.0001) per chi non ha la propria collection di L22-L23. |
| `scaffolding/check_lab24.py` | 🧰 | **Strumento del docente**: base zero costi (le 3 varianti di prompt e `reindicizza_chunks` esistono); `--live` i giri veri (~$0.004, verifica anche il caso studio k=4 vs k=8); `--solutions`. Non compare nel percorso studente. |
| `dataset/*.txt` | 📄 | I 3 documenti lunghi di Lumen (manuale, policy resi, guida smart working), gli stessi di L22-L23. |
| `working/rag.py` | ⌨️ | L'unico file di codice della giornata. Include già `cerca_chunk`/`costruisci_prompt`/`rispondi` di L23 più le manopole di oggi (non si sovrascrive col proprio file di L23: si riportano solo le eventuali personalizzazioni). **TODO 1-3** (Lab 1): la variante `SYSTEM_PROMPTS["severo"]`, l'istruzione di citazione "estesa", l'istruzione di CoT. **TODO 4** (Lab 2): `reindicizza_chunks(strategia, size, overlap=0)`. Le manopole `GROUNDING` / `CON_COT` / `CITAZIONE` / `K` / `SOGLIA` / `REINDICIZZA` si girano rilanciando lo script, senza altro codice da scrivere. Riferimento in `solutions/`. |
| `working/scheda_esperimenti.md` | ⌨️ | Il **deliverable vero** della giornata: due tabelle (Lab 1 prompt, Lab 2 retrieval) da compilare un giro alla volta. Riferimento compilato in `solutions/`. |
| `solutions/rag.py` | — | La versione **completa** (stessi nomi, stessi import): i TODO sono UNA soluzione possibile. |
| `solutions/scheda_esperimenti.md` | — | La scheda compilata coi giri **davvero eseguiti** (gpt-4.1-mini, 09-16/07/2026): numeri di riferimento per il docente, non un risultato "giusto" da copiare. |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # dentro: la stessa chiave OpenAI di L13-L23
```

Poi la collection: la propria `chroma/` di L22-L23 copiata qui, oppure
`python scaffolding/prepara_collection.py` (riserva identica).

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env`, `.venv` e `chroma/` (git non li versiona).

## Come si prova

```bash
python working/rag.py                          # un giro sulle 4 query del main
python scaffolding/prepara_collection.py       # la riserva della collection (45 chunk)
python scaffolding/check_lab24.py              # docente: base, zero costi
python scaffolding/check_lab24.py --live       # docente: i giri veri (~$0.004)
python scaffolding/check_lab24.py --solutions  # docente: verifica solutions/
```

## Il caso studio della giornata (numeri misurati, 16/07/2026)

La query `facile-2` del main ("Quanto vale il contributo per la postazione e
entro quanti giorni va presentata la richiesta?") **fallisce a k=4** su
QUALSIASI variante di prompt (morbido/severo/CoT/estesa: sempre "non lo
trovo"): l'importo (250€) e la scadenza (60 giorni) stanno in due chunk
`recursive/500` consecutivi, e a k=4 arriva solo il secondo (score 0.639),
il primo resta 8° (score 0.396). **Si risolve nel retrieval**, non nel
prompt: k=8 recupera entrambi (+70% token input, due fonti citate);
`reindicizza_chunks("recursive", 800)` li fonde in un chunk solo (stesso
esito, una fonte, meno token). La soglia da sola non basta: i chunk
genuinamente fuori corpus scorano 0.50-0.57, PIÙ ALTI dello 0.396 mancante.

Le varianti di prompt (Lab 1) non cambiano l'esito su nessuna delle 4
query: severo/estesa costano il 10-27% in più senza guadagno di
correttezza; il CoT costa +129% e ROMPE il formato di rifiuto fisso sulla
query fuori-corpus. Dettaglio completo in `solutions/scheda_esperimenti.md`.
