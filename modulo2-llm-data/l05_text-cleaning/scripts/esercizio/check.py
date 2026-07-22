"""check.py — verifica l'esercizio SENZA chiamare il modello (niente chiave API).

    python check.py        # nella cartella esercizio/

Prova a importare la TUA `remove_urls` da mia_pulizia.py; se non è ancora fatta,
lo dice. Ogni requisito stampa [OK]/[FAIL].
"""
import sys

try:
    from mia_pulizia import remove_urls
except (ImportError, NotImplementedError):
    print("[FAIL] remove_urls non ancora implementata in mia_pulizia.py")
    sys.exit(1)

CASI = [
    ("Vedi https://www.gutenberg.org per il testo. Fine.", "gutenberg.org", False),
    ("Link http://example.com/x?y=1 qui.", "example.com", False),
    ("Scrivi a www.sito.it adesso", "www.sito", False),
    ("Nessun url in questa frase.", "Nessun url in questa frase.", True),
]


def main() -> int:
    ok = True
    for testo, atteso, deve_restare in CASI:
        try:
            out = remove_urls(testo)
        except NotImplementedError:
            print("[FAIL] remove_urls solleva NotImplementedError")
            return 1
        presente = atteso in out
        passato = presente if deve_restare else not presente
        stato = "[OK]  " if passato else "[FAIL]"
        print(f"{stato} {testo!r} -> {out!r}")
        ok = ok and passato
    print("\nTutto a posto ✔" if ok else "\nCi sono ancora [FAIL] da sistemare.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
