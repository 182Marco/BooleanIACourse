"""ESERCIZIO (10') — uno step di cleaning in più, per il chatbot.

Prima di dare un testo al chatbot (`ask()`), lo ripuliamo. Molti documenti reali
contengono URL (link nei footer, nelle note, nelle pagine web) che non servono a
rispondere e sprecano spazio nel prompt. Manca lo step che li toglie.

Compito: completa `remove_urls` perché, dato un testo, rimuova gli URL
(http://…, https://…, www…) lasciando intatto il resto. Poi verifica con:

    python check.py

Suggerimento: una regex. Gli URL iniziano con `http://`, `https://` o `www.`
e finiscono dove inizia uno spazio. Usa `re.sub(...)`.
"""
import re


def remove_urls(text: str) -> str:
    # TODO: sostituisci gli URL con "" (stringa vuota).
    # pattern indicativo: r"(https?://\S+|www\.\S+)"
    raise NotImplementedError("Completa remove_urls")


if __name__ == "__main__":
    esempio = "Vedi https://www.gutenberg.org per il testo completo. Fine."
    print(remove_urls(esempio))
