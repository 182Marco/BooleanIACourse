# Valtesa: rimborsi e assistente dell'ufficio del personale

Valtesa S.r.l. è un'azienda di 120 dipendenti con due sedi, Brescia e Padova.
Questo progetto è il software interno del suo ufficio del personale e
contiene due programmi:

- **`rimborsi.py`** controlla le note spese dei dipendenti in trasferta
  contro i massimali della policy aziendale. È il programma della trace di
  Modulo 4 · Lezione 1, già corretto: il massimale è quello in vigore nel
  giorno della spesa.
- **`assistente.py`** è l'assistente per i dipendenti costruito con l'OpenAI
  Agents SDK: risponde sui documenti dell'ufficio (con `cerca_documenti`)
  e sui dati di dipendenti, assenze e note spese (con `query_db`, in sola
  lettura). È l'assistente del docente di Modulo 3 · Lezione 12.

È il progetto di tutto il Modulo 4: ogni lezione ne ha una copia nella sua
cartella, che parte da quella della lezione prima.

## Primo avvio

Si fa una volta sola, prima di Modulo 4 · Lezione 2, e lo fa il coding agent
(la checklist del modulo dice come).

1. Il venv del modulo sta nella cartella del modulo, due cartelle sopra
   questa (`../../.venv`), ed è uno solo per tutte le lezioni. Si crea con
   Python 3.10 o più recente e si installa `requirements.txt`.
2. `.env.example` si copia in `.env` e si scrive la chiave OpenAI del corso.
3. `python indicizza.py` costruisce l'indice dei documenti in `indice/`
   (122 chunk, meno di un centesimo di dollaro).
4. `pytest` dalla cartella del progetto: tutti i test verdi.

Nelle lezioni dopo servono solo i punti 2 e 3 nella cartella nuova.

## I comandi

Dalla cartella del progetto, con il venv del modulo attivo:

```
python rimborsi.py        # l'esito di tutte le note spese; in fondo il totale
python assistente.py      # chiede il nome della sessione, poi le domande
python indicizza.py       # ricostruisce l'indice dei documenti
pytest                    # i test, senza chiamate alle API
```

## I file

| File | Cosa fa | Ruolo |
|---|---|---|
| `rimborsi.py` | Legge `dati/note_spese.csv` e `dati/massimali.csv` e stampa l'esito di ogni nota, poi il totale: 1.500 note, 293 fuori massimale | ⌨️ il programma su cui si lavora in Modulo 4 · Lezione 2 |
| `assistente.py` | L'agente con `cerca_documenti` e `query_db`; ricorda la conversazione in `sessioni.db` | 🧰 l'assistente del modulo |
| `indicizza.py` | Carica, pulisce e divide in chunk i documenti di `ufficio/`, calcola gli embedding e li salva in `indice/` | 🧰 |
| `aikit/` | Il toolkit del corso: loader, pulizia, chunking, embedding, collection Chroma, client LLM | 🧰 |
| `tests/test_rimborsi.py` | I sei test di `rimborsi.py`, tre con la data della circolare | 🧰 |
| `tests/test_assistente.py` | I test dell'assistente che non chiamano il modello: database, `query_db`, indice | 🧰 |
| `AGENTS.md` | Le istruzioni per il coding agent: le regole del corso, e la parte sul progetto che scrivete voi | ⌨️ |
| `requirements.txt` | Le dipendenze del modulo, con le versioni fissate | 🧰 |
| `.env.example` | Il modello del file con la chiave | 🧰 |
| `pytest.ini` | Dice a pytest dove stanno i test e da dove si importa | 🧰 |
| `dati/` | Gli export del gestionale: `note_spese.csv` (1.500 note, gennaio-agosto 2026), `massimali.csv`, `dipendenti.csv`, `assenze.csv`, `export-ottobre.csv` (le note di settembre), e `valtesa.db` con le prime quattro tabelle | 📄 |
| `ufficio/` | I sei documenti dell'ufficio del personale: policy trasferte, circolari 2026, regolamento ferie, regolamento welfare, procedura di ingresso, FAQ del portale | 📄 |
| `indice/` | L'indice dei documenti, fuori da git: lo costruisce `indicizza.py` | 📄 generato |

Ruoli: 🧰 ambiente e codice del progetto · ⌨️ su cui lavorate voi, con il
coding agent · 📄 documenti e dati.

## Le regole dei rimborsi, in breve

- I massimali sono per voce (pranzo, cena, hotel a notte, taxi a corsa) e per
  città: Milano, Torino e Roma. Sono nell'art. 6 della policy trasferte
  (`ufficio/policy-trasferte-note-spese.docx`) e in `dati/massimali.csv`.
- Dal 1° luglio 2026 a Milano la cena passa da 45 a 55 € e l'hotel da 130 a
  150 € a notte (circolare 7/2026, in `ufficio/circolari-personale-2026.html`).
  Vale il massimale in vigore nel giorno della spesa.
