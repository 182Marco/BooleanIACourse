"""aikit — il toolkit del corso, un modulo riusabile per lezione.

Sette moduli in tutto, costruiti nel corso del modulo:
  - loaders/ (Modulo 2 · Lezione 4): load(path) -> list[Document], dispatch per formato.
  - clean.py (Modulo 2 · Lezione 5): pipeline di pulizia componibile, pipeline_for(path).
  - llm_client.py (Modulo 2 · Lezione 3): LLMClient, il pattern prompt-as-function.
  - embeddings.py (Modulo 2 · Lezione 7): embed() con backend selezionabile, cosine.
  - search.py (Modulo 2 · Lezione 8): la ricerca brute-force scritta da voi.
  - vectorstore.py (Modulo 2 · Lezione 9-10): la collection ChromaDB.
  - chunk.py (Modulo 2 · Lezione 10): le tre strategie di chunking.

Oggi (Modulo 2 · Lezione 15) `working/app.py` ne richiama attivamente CINQUE:
loaders e clean, dormienti da Modulo 2 · Lezione 6 (il corpus del blocco
retrieval arrivava sempre già pulito), tornano perché oggi il corpus è vero;
insieme a chunk, embeddings, vectorstore, che non hanno mai smesso di
servire. llm_client e search restano nel toolkit ma non servono in questa
lezione: structured outputs usa il client OpenAI diretto, la ricerca reale
passa dal vector DB dalla Lezione 9 in poi. NON si toccano, si importano.
"""
