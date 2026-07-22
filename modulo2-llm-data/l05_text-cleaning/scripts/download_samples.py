"""download_samples.py — (ri)scarica i tre documenti reali della lezione.

I file sono già versionati in sample_docs/; questo script serve a rigenerarli o a
capire da dove vengono (trasparenza sulla fonte/licenza). Girano tutti offline in
aula: si scaricano una volta.

    python download_samples.py

Fonti:
- frankenstein.txt   Project Gutenberg #84 — pubblico dominio
- arxiv_1905.00075.pdf   arXiv:1905.00075 — "On the Use of arXiv as a Dataset"
- wikipedia_nlp.html   it.wikipedia.org — CC BY-SA
"""
import urllib.request
from pathlib import Path

FONTI = {
    "sample_docs/frankenstein.txt": "https://www.gutenberg.org/cache/epub/84/pg84.txt",
    "sample_docs/arxiv_1905.00075.pdf": "https://arxiv.org/pdf/1905.00075",
    "sample_docs/wikipedia_nlp.html": "https://it.wikipedia.org/wiki/Elaborazione_del_linguaggio_naturale",
}

if __name__ == "__main__":
    Path("sample_docs").mkdir(exist_ok=True)
    for dest, url in FONTI.items():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (aidea-boolean-master)"})
        with urllib.request.urlopen(req) as r:
            Path(dest).write_bytes(r.read())
        print(f"scaricato {dest}  <-  {url}")
