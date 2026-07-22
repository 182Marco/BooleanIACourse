"""Soluzione esercizio — loader .txt e .csv (riferimento docente).

Una delle tante soluzioni valide. Il punto è: stessa interfaccia `Document`, i
metadata giusti, e per il CSV una scelta consapevole di granularità.
"""
import csv

from loaders.base import Document


def load_txt(path: str) -> list[Document]:
    with open(path, encoding="utf-8") as f:
        return [Document(f.read(), {"source": path, "type": "txt"})]


def load_csv(path: str, una_riga_per_doc: bool = True) -> list[Document]:
    with open(path, encoding="utf-8", newline="") as f:
        righe = list(csv.DictReader(f))

    if una_riga_per_doc:
        # una riga = un Document: comodo se ogni record è un'unità di retrieval
        return [
            Document(
                "\n".join(f"{k}: {v}" for k, v in riga.items()),
                {"source": path, "type": "csv", "row": i + 1},
            )
            for i, riga in enumerate(righe)
        ]

    # tutto insieme: un solo Document con tutte le righe
    testo = "\n".join("; ".join(f"{k}: {v}" for k, v in r.items()) for r in righe)
    return [Document(testo, {"source": path, "type": "csv"})]


if __name__ == "__main__":
    # mini-prova senza dipendenze esterne
    import tempfile, os
    with tempfile.TemporaryDirectory() as d:
        t = os.path.join(d, "note.txt")
        open(t, "w", encoding="utf-8").write("riga uno\nriga due")
        print(load_txt(t))

        c = os.path.join(d, "clienti.csv")
        open(c, "w", encoding="utf-8").write("nome,citta\nAcme,Milano\nFoo,Roma\n")
        print(load_csv(c))
        print(load_csv(c, una_riga_per_doc=False))
