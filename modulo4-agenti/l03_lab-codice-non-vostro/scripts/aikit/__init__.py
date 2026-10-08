"""aikit — il toolkit del corso, nella parte che serve al progetto Valtesa.

Sei moduli, gli stessi dei Moduli 2 e 3:
  - loaders/ (Modulo 2 · Lezione 4): load(path) -> list[Document], dispatch per formato.
  - clean.py (Modulo 2 · Lezione 5): pipeline di pulizia componibile, pipeline_for(path).
  - chunk.py (Modulo 2 · Lezione 10): le strategie di chunking.
  - embeddings.py (Modulo 2 · Lezione 7): embed() con backend selezionabile, cosine.
  - vectorstore.py (Modulo 2 · Lezione 9-10): la collection ChromaDB, salvata in indice/.
  - llm_client.py (Modulo 2 · Lezione 3): LLMClient, il pattern prompt-as-function; cost_usd().

Nel progetto li usano indicizza.py (loaders, clean, chunk, embeddings,
vectorstore: costruisce l'indice dei documenti di ufficio/) e assistente.py
(vectorstore, dentro il tool cerca_documenti). llm_client non lo usa nessuno
dei due. Rispetto all'aikit di Modulo 3 · Lezione 12 cambia solo la cartella
dell'indice (CHROMA_DIR in vectorstore.py); rag, tools, hybrid, rerank e
search restano nelle cartelle di Modulo 3.

Le docstring dei singoli moduli raccontano la lezione in cui sono nati: i
riferimenti a file di quelle lezioni (cerca_chunk, prepara_collection.py,
lumen_chunks, dataset/) non riguardano questo progetto.
"""
