# Modulo 2 · Lezione 5 · Consegna — Text Cleaning & Pre-processing

> La consegna completa è nelle slide della lezione. Questo file è un promemoria
> operativo: cosa lanciare, dove si lavora, quando avete finito.

## In due righe

Il documento della serata è un manuale in PDF. Estratto com'è, fa rispondere
**male** al modello. Voi scrivete gli step che lo ripuliscono, dentro
**`working/clean.py`** — l'unico file su cui si lavora.

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # dentro: la stessa chiave di Modulo 2 · Lezione 1-4
```

Poi, dopo ogni pezzo:

```bash
python working/clean.py
```

Lo script gira anche coi TODO non ancora fatti: stampa quello che c'è e dice
quali mancano. **Non serve finire tutto per vedere qualcosa.**

## Cosa c'è intorno

`scaffolding/aikit/` è il toolkit: dentro c'è `loaders.py`, **quello che avete
scritto voi la lezione scorsa**, più il client per parlare col modello. Accanto,
`ask.py`: fa la domanda e stampa il confronto. Si importano, non si riscrivono.

In `scaffolding/` ci sono anche `check_lab05.py`, `make_dataset.py` e il
`manifest.json`: sono **attrezzi del docente** (verifica dei materiali,
rigenerazione del PDF). **Non lanciateli** — non vi dicono niente che non
vediate già a schermo. Se restate bloccati, chiamate il docente: ha lui lo
strumento per capire in dieci secondi cosa non torna.

## Il live coding (🎤 si replica) — `working/clean.py`

| TODO | Cosa | Fatto quando |
|---|---|---|
| 1 | `normalize_whitespace` | il main stampa il testo accorciato, senza spazi doppi |
| 2 | `dehyphenate` | le parole spezzate a fine riga tornano intere |
| 3 | `reflow_paragraphs` | il conteggio delle righe crolla: le frasi si ricuciono |

## L'esercizio (⌨️ tocca a voi) — stesso file

| TODO | Cosa | Fatto quando |
|---|---|---|
| 4 | `remove_repeated_lines` | il piede della **LumaDesk Mini** sparisce, e «120 kg» resta |
| 5 | `remove_page_numbers` | le righe `pagina N di 4` spariscono |
| 6 | `pulisci_pdf` | il main arriva in fondo e fa le due domande |

**Il momento che conta è il TODO 6.** Quando la ricetta è completa, il main
chiede al modello la stessa cosa due volte — sul testo sporco e sul vostro
testo pulito. Prima della vostra pulizia la risposta è **80 kg**. Dopo è
**120 kg**, che è quello che il manuale dice davvero.

Le firme non si toccano: `normalize_whitespace`, `dehyphenate`,
`reflow_paragraphs`, `remove_repeated_lines`, `remove_page_numbers`,
`pulisci_pdf`. Il *come* è vostro — soluzioni diverse vanno benissimo.
