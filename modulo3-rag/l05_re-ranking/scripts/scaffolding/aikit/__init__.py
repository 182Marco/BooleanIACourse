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
    recupera(), genera(), rispondi() e CONFIG. Promosso a Modulo 3 ·
    Lezione 3 e lì modificato in aula: la generazione è genera(chunks,
    domanda, storia=None), le regole del prompt stanno in ISTRUZIONI.

Oggi (Modulo 3 · Lezione 4) `working/hybrid.py` ne richiama DUE: rag
(rag.recupera() per la ricerca semantica, rag.CONFIG per il nome della
collection) e vectorstore (apri_collection() per leggere tutti i chunk su
cui costruire l'indice BM25). rag.py a sua volta importa loaders, clean,
chunk, embeddings e vectorstore per l'ingest, che il main di hybrid.py
lancia solo se la collection `lumen_m3` è vuota. llm_client e search
restano per continuità e non servono. NON si toccano, si importano.
chat.py di Modulo 3 · Lezione 3 resta fuori: stasera si lavora
single-turn (l'aikit non è cumulativo).

Le docstring dei singoli moduli raccontano la lezione in cui sono nati: i
riferimenti a file o TODO di quelle lezioni (cerca_chunk,
prepara_collection.py, "Lab 2", "TODO 1") non riguardano questa cartella.
"""

