"""benchmark_scala.py — il brute-force misurato a scala (il perché di L21).

Genera corpora sintetici di vettori float32 a 1536 dimensioni (come il corpus
vero) e misura UNA query: lo stesso lavoro di search.py — la cosine con TUTTI
i vettori + l'ordinamento — scritto in forma vettoriale (numpy fa il ciclo in
C) per poterlo misurare anche su centinaia di migliaia di vettori. Il tempo
cresce LINEARMENTE con n: è O(n·d), e ogni query lo ripaga per intero. La
proiezione a 10 milioni di vettori è il numero da portare in slide: il motivo
per cui esiste l'indice (ANN, → L21).

Uso (dalla cartella scripts/):

    python scaffolding/benchmark_scala.py

Per provare taglie diverse si cambia TAGLIE qui sotto. RAM: n vettori ≈
n × 1536 × 4 byte (200'000 ≈ 1.2 GB). Un tetto di sicurezza (RAM_TETTO_GB)
salta le taglie che rischiano di piantare il laptop: NON serve misurare
10 milioni per crederci — la retta è lineare, la proiezione basta.
"""
import sys
import time

import numpy as np

DIM = 1536            # le dimensioni di text-embedding-3-small (il corpus vero)
RIPETIZIONI = 5       # si tiene il tempo MIGLIORE: misura il costo, non il rumore
TAGLIE = [48, 5_000, 50_000, 200_000]
PROIEZIONE_A = 10_000_000
RAM_TETTO_GB = 2.5    # oltre: rischio OOM/freeze su un laptop d'aula


def misura(n: int) -> float:
    """ms per UNA query su n vettori: il lavoro di search(), in forma vettoriale."""
    rng = np.random.default_rng(20)
    vectors = rng.standard_normal((n, DIM), dtype=np.float32)
    q = rng.standard_normal(DIM, dtype=np.float32)
    tempi = []
    for _ in range(RIPETIZIONI):
        inizio = time.perf_counter()
        scores = vectors @ q / (np.linalg.norm(vectors, axis=1) * np.linalg.norm(q))
        np.argsort(scores)[::-1][:5]
        tempi.append(time.perf_counter() - inizio)
    return min(tempi) * 1000


if __name__ == "__main__":
    print(f"brute-force: cosine con tutti + argsort, {DIM} dim, float32 "
          f"(migliore di {RIPETIZIONI} giri)\n")
    print(f"{'n vettori':>12} {'RAM corpus':>12} {'ms/query':>10}")
    ultima = None
    for n in TAGLIE:
        ram = n * DIM * 4 / 1024**2
        if ram / 1024 > RAM_TETTO_GB:
            print(f"{n:>12,} {ram / 1024:>10.1f} GB    SALTATO: oltre il tetto di "
                  f"{RAM_TETTO_GB} GB (rischio OOM). La retta è lineare: proiezione.")
            continue
        ms = misura(n)
        print(f"{n:>12,} {ram:>10.0f} MB {ms:>10.1f}")
        ultima = (n, ms)
    if ultima is None:
        sys.exit("nessuna taglia sotto il tetto di RAM: riprova con n più piccoli.")
    n, ms = ultima
    proiezione = ms * PROIEZIONE_A / n
    print(f"\nproiezione lineare a {PROIEZIONE_A:,} vettori: "
          f"~{proiezione / 1000:.1f} s per UNA query (e ogni query ripaga tutto).")
    print("Sabato (L21) la stessa ricerca la fa un indice ANN: è il suo mestiere.")
