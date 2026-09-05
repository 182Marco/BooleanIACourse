"""aikit — il toolkit del corso, un modulo riusabile per lezione.

Otto moduli in tutto, costruiti nel corso delle lezioni:
  - loaders/ (Modulo 2 · Lezione 4): load(path) -> list[Document], dispatch per formato.
  - clean.py (Modulo 2 · Lezione 5): pipeline di pulizia componibile, pipeline_for(path).
  - llm_client.py (Modulo 2 · Lezione 3): LLMClient, il pattern prompt-as-function.
  - embeddings.py (Modulo 2 · Lezione 7): embed() con backend selezionabile, cosine.
  - search.py (Modulo 2 · Lezione 8): la ricerca brute-force scritta da voi.
  - vectorstore.py (Modulo 2 · Lezione 9-10): la collection ChromaDB.
  - chunk.py (Modulo 2 · Lezione 10): le tre strategie di chunking.
  - rag.py (Modulo 3 · Lezione 2): la pipeline del modulo — indicizza(),
    recupera(), rispondi() e CONFIG. Promosso OGGI (Modulo 3 · Lezione 3),
    identico alla soluzione della lezione scorsa salvo il percorso al corpus.

Oggi (Modulo 3 · Lezione 3) rag.py si MODIFICA una volta, in aula, nel
live coding di apertura: rispondi() si spacca in genera(chunks, domanda,
storia) + rispondi(query, storia), con le regole del prompt in ISTRUZIONI.
La versione finita è in solutions/aikit/rag.py. È l'eccezione dichiarata
alla regola del toolkit: un modulo di aikit/ si modifica in aula, mai in
silenzio. Poi `working/chat.py` ne richiama UNO: rag — rag.recupera() per
il retrieval, rag.genera() per la risposta con la storia davanti,
rag.CONFIG per il modello. rag.py a sua volta importa loaders, clean,
chunk, embeddings e vectorstore per l'ingest, che il main di chat.py
lancia solo se la collection `lumen_m3` è vuota. llm_client e search
restano per continuità e non servono. Gli altri moduli NON si toccano,
si importano.

Le docstring dei singoli moduli raccontano la lezione in cui sono nati: i
riferimenti a file o TODO di quelle lezioni (cerca_chunk,
prepara_collection.py, "Lab 2", "TODO 4 di rag.py" in vectorstore.py) non
riguardano questa cartella. I TODO di oggi sono solo in working/chat.py.
"""
