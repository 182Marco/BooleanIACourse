"""Soluzione di riferimento (docente) — remove_urls.

Una volta scritto lo step, si aggancia alla pipeline come tutti gli altri:

    from aikit.clean import clean, normalize_whitespace
    from esercizio.soluzione import remove_urls

    pulito = clean(text, [remove_urls, normalize_whitespace])
"""
import re

URL = re.compile(r"(https?://\S+|www\.\S+)")


def remove_urls(text: str) -> str:
    return URL.sub("", text)


if __name__ == "__main__":
    esempio = "Vedi https://www.gutenberg.org per il testo completo. Fine."
    print(remove_urls(esempio))
