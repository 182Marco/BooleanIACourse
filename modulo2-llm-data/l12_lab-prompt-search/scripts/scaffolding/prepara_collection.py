"""prepara_collection.py — la riserva: ricostruisce `lumen_chunks` da zero.

Per chi non ha la propria collection di L22 (o l'ha cancellata): spezza i 3
documenti di Lumen con la configurazione di riferimento di L22 (recursive,
500 caratteri) e li indicizza in chroma/. Una chiamata embed (~$0.0001).

    python scaffolding/prepara_collection.py
"""
import sys

from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from aikit.embeddings import embed        # noqa: E402 — L19
from aikit import vectorstore             # noqa: E402 — L21-L22
from aikit.chunk import chunk_recursive   # noqa: E402 — L22, da oggi in aikit

DATASET = SCRIPTS / "dataset"
CHUNK_SIZE = 500                          # la configurazione di riferimento di L22


if __name__ == "__main__":
    ids, testi, metadati = [], [], []
    for percorso in sorted(DATASET.glob("*.txt")):
        pezzi = chunk_recursive(percorso.read_text(encoding="utf-8"), CHUNK_SIZE)
        for numero, pezzo in enumerate(pezzi):
            ids.append(f"{percorso.stem}-{numero:03d}")
            testi.append(pezzo)
            metadati.append({"doc": percorso.stem})
        print(f"{percorso.stem}: {len(pezzi)} chunk")

    print(f"\nembeddo e indicizzo {len(testi)} chunk in `lumen_chunks`:")
    vettori = embed(testi)
    collection = vectorstore.crea_collection("lumen_chunks")
    vectorstore.indicizza(collection, ids, testi, vettori, metadati)
    print("fatto: la collection è pronta in chroma/")
