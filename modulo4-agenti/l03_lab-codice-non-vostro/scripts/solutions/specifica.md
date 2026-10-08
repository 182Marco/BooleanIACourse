# Specifica: report.py

Dal ticket 214 (`ticket-report.md`).

**Cosa fa.** `python report.py AAAA-MM` scrive `output/report-AAAA-MM.html`,
il riepilogo delle note spese del mese per la Direzione Amministrativa, e
stampa una riga con il numero di note, il totale e il percorso del file.

**Da dove prende i dati.**

- Le note da `dati/note_spese.csv`: quelle del mese sono quelle con il
  giorno nel mese, in qualsiasi stato.
- La sede da `dati/dipendenti.csv`, con `dipendente_id` e non con il nome:
  ci sono due Sara Conti, una a Brescia e una a Padova.
- Il controllo dei massimali è `controlla()` di `rimborsi.py`, con le notti
  dell'obiettivo 2, e il massimale applicato è `limite_nota()` di
  `rimborsi.py`: il report non rifà il calcolo.

**Nella pagina.**

- Il numero di note e il totale del mese.
- I totali per sede (note e importo) e per voce (importo).
- Un grafico a barre degli importi per voce, disegnato nella pagina
  (SVG): niente librerie da internet.
- Le note fuori massimale, una per riga: id, dipendente, voce (con le
  notti, se più di una), città, giorno, importo, massimale applicato,
  eccedenza.

**Cosa non fa.** Non modifica niente in `dati/`, non cambia la regola di
`rimborsi.py` (usa `controlla()` e `limite_nota()`, che ci sono già),
non manda il report a nessuno, non considera lo stato delle note.

**Criteri di accettazione.** I sette del ticket, più:

8. `python rimborsi.py` ha ancora la stessa ultima riga (267 dopo
   l'obiettivo 2).
9. I test di `tests/test_report.py` usano note costruite nel test, tranne
   quello sui numeri di luglio, che legge l'export vero senza scriverci.
