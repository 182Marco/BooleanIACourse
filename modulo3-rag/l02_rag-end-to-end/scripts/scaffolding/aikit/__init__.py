"""aikit — il toolkit del corso, un modulo riusabile per lezione.

Sette moduli in tutto, costruiti nel corso del modulo:
  - loaders/ (Modulo 2 · Lezione 4): load(path) -> list[Document], dispatch per formato.
  - clean.py (Modulo 2 · Lezione 5): pipeline di pulizia componibile, pipeline_for(path).
  - llm_client.py (Modulo 2 · Lezione 3): LLMClient, il pattern prompt-as-function.
  - embeddings.py (Modulo 2 · Lezione 7): embed() con backend selezionabile, cosine.
  - search.py (Modulo 2 · Lezione 8): la ricerca brute-force scritta da voi.
  - vectorstore.py (Modulo 2 · Lezione 9-10): la collection ChromaDB.
  - chunk.py (Modulo 2 · Lezione 10): le tre strategie di chunking.

Oggi (Modulo 3 · Lezione 2) `working/rag.py` ne richiama CINQUE: loaders,
clean, chunk, embeddings e vectorstore — la filiera dell'ingest e la
ricerca sul vector DB. llm_client e search restano nel toolkit per
continuità col Modulo 2 ma non servono in questa lezione: rag.py parla col
client OpenAI diretto, e la ricerca brute-force di Modulo 2 · Lezione 8 è
superata dal vector DB. NON si toccano, si importano.

Le docstring dei singoli moduli raccontano la lezione del Modulo 2 in cui
sono nati: i riferimenti a file o TODO di quelle lezioni (cerca_chunk,
prepara_collection.py, "Lab 2") non riguardano questa cartella.
"""
