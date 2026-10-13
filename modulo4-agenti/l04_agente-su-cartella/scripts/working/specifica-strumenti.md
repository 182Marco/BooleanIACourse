# Specifica: i tool di cartella dell'assistente

Da scrivere in `strumenti_cartella.py`, che ha già le firme e le docstring:
le docstring sono quello che il modello legge, non si cambiano. Si lavora
solo in `strumenti_cartella.py` e in `tests/test_strumenti_cartella.py`.

## I quattro pezzi

- `dentro_la_radice(percorso)`: il percorso assoluto del file, risolto
  (`resolve()`: toglie i `..` e segue i link simbolici). Se non sta dentro
  `RADICE` (`is_relative_to()`), alza `ValueError` con un messaggio che
  dice quale percorso e perché.
- `elenca_file()`: i file di `RADICE`, anche nelle sottocartelle, uno per
  riga, con il percorso relativo a `RADICE`.
- `leggi_file(percorso)`: il testo del file (UTF-8; i caratteri che non si
  decodificano si sostituiscono, senza errore), al massimo `MAX_CARATTERI`.
- `cerca(testo)`: in tutti i file di `RADICE`, le righe che contengono il
  testo senza distinguere maiuscole e minuscole, nella forma
  `file:riga: testo`, al massimo `MAX_RISULTATI`. Se non trova niente lo
  dice in una frase.

## Come si lavora

- Le docstring e le firme restano quelle del file.
- Nessuna dipendenza nuova, nessun file fuori da quelli indicati.
- I test stanno in `tests/test_strumenti_cartella.py` e chiamano i tool con
  `chiama()` di `tests/test_assistente.py` (come fa l'SDK, senza modello);
  `pytest` verde, compresi i test che c'erano.
- Un test che ha bisogno di file o link creati apposta li crea in una
  cartella temporanea (`tmp_path` di pytest), mai in `ufficio/`, e ci fa
  puntare i tool cambiando `RADICE` con `monkeypatch.setattr`; un test che
  crea un link si salta con `pytest.skip` dove il sistema non lo permette
  (Windows senza modalità sviluppatore).

## Criteri di accettazione

Da scrivere da voi, prima di dare la specifica al coding agent: le
condizioni, verificabili, che il codice deve rispettare per essere
accettato. Ognuna avrà il suo test.

1.
