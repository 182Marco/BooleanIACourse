"""aikit — il toolkit del corso, un modulo riusabile per lezione.

Dieci moduli in tutto, costruiti nel corso delle lezioni:
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
  - hybrid.py (Modulo 3 · Lezione 4): BM25 accanto al semantico, fusi con
    RRF — costruisci_indice_bm25(), cerca_bm25(), rrf(), cerca_hybrid().
  - rerank.py (Modulo 3 · Lezione 5): il secondo stadio — rerank_cohere(),
    rerank_llm(), cerca_due_stadi(). Promosso oggi.

Oggi (Modulo 3 · Lezione 6) `working/debug.py` ne richiama QUATTRO: rag
(rag.recupera() per il semantico, rag.genera() per la risposta, rag.CONFIG
e rag.ISTRUZIONI per le leve chunk size e prompt), hybrid (cerca_hybrid()
e INDICE, la lista di tutti i chunk in memoria), rerank (cerca_due_stadi()
per il retrieval a due stadi) e vectorstore (apri_collection() per sapere
se la collection va indicizzata). Sono le leve della giornata: si girano
da CONFIG in debug.py, i moduli NON si toccano. llm_client e search
restano per continuità e non servono. chat.py di Modulo 3 · Lezione 3
resta fuori: oggi si diagnostica single-turn (l'aikit non è cumulativo).

Le docstring dei singoli moduli raccontano la lezione in cui sono nati: i
riferimenti a file o TODO di quelle lezioni (cerca_chunk,
prepara_collection.py, "Lab 2", "TODO 1") non riguardano questa cartella.
"""
