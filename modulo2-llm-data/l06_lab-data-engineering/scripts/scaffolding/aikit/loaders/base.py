"""Il formato interno unico: ogni loader normalizza qui dentro.

text     — il contenuto estratto dal file
metadata — da dove arriva (source, page, type): servirà per citazioni (L23) e
           per filtrare le ricerche nel vector DB (L21)

È volutamente minimale: più è sottile, meno somiglia a un framework. La scegliamo
`dataclass` (e non un `dict`) per type hint, autocomplete e un posto naturale dove
appendere validazione più avanti.
"""
from dataclasses import dataclass, field


@dataclass
class Document:
    text: str
    metadata: dict = field(default_factory=dict)

    def __repr__(self):
        anteprima = " ".join(self.text.split())[:60]
        return f"Document({self.metadata}, text={anteprima!r}…)"
