---
name: report-mensile
description: Prepara il report mensile delle note spese per l'ufficio del personale di Valtesa - la pagina HTML con totali, sedi, voci e note fuori massimale, e una sintesi di poche righe da mandare all'ufficio, con i numeri controllati. Da usare quando si chiede il report, il riepilogo o i numeri delle note spese di un mese.
---

# Report mensile delle note spese

Per il mese chiesto (AAAA-MM) servono due file, con numeri di cui sei sicuro:
`output/report-AAAA-MM.html` e `output/sintesi-AAAA-MM.md`.

1. **Trova i dati del mese.** Lancia, dalla cartella del progetto,
   `python .claude/skills/report-mensile/scripts/dati_del_mese.py AAAA-MM`.
   Dice in quali file di `dati/` ci sono note di quel mese, quante, il
   totale, e cosa manca rispetto a `note_spese.csv`. Se il mese non è in
   nessun file, fermati e dillo.
2. **Fai il report.** `python report.py AAAA-MM` legge solo
   `dati/note_spese.csv`. Se le note del mese stanno in un altro file (un
   export appena arrivato), aggiungi a `report.py` un'opzione per leggerlo,
   senza cambiare il comportamento di oggi. Se lo script si ferma con un
   errore, leggilo e cerca la causa nei dati: se è un caso che il report deve
   reggere, correggi lo script; se mancano dati, fermati e chiedi. Ogni
   modifica a `report.py` ha il suo test in `tests/test_report.py`: i test
   nuovi chiamano `riepilogo()` e `pagina()` con note scritte nel test, e non
   lanciano `report.py`, che scriverebbe sopra i file di `output/`.
3. **Controlla i numeri.** Note e totale del report devono essere quelli di
   `dati_del_mese.py`. Se non tornano, non andare avanti: cerca il perché.
4. **Spiega quello che i dati non dicono.** Per una città senza massimale
   leggi l'art. 3 della policy trasferte in `ufficio-completo/`. Se mancano
   le notti degli hotel, `rimborsi.py` ne conta una per riga: i soggiorni
   lunghi risultano fuori massimale. Non correggere i dati: segnala.
5. **Scrivi la sintesi** in `output/sintesi-AAAA-MM.md`, al massimo sei
   righe per l'ufficio: note e totale, la sede che spende di più, le note
   fuori massimale, e cosa va verificato, con i numeri. Solo quello che dicono
   i file.
6. **Chiudi** con `pytest`, poi riapri `output/report-AAAA-MM.html` e
   controlla che dica ancora le note giuste. Infine un riepilogo: i file
   prodotti, cosa hai cambiato negli script e perché.

Non modificare i file di `dati/` e di `ufficio-completo/`.
