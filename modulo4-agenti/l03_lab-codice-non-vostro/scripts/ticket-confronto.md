# Ticket 215 — Il confronto con il mese prima

**Da:** Ufficio del personale · **Per:** IT · **Priorità:** bassa

Il riepilogo mensile funziona. Adesso la Direzione Amministrativa vuole
vedere anche come cambiano i numeri rispetto al mese prima. Nella stessa
pagina che scrive `python report.py 2026-07`:

- accanto al numero delle note e all'importo totale del mese, quelli del
  mese prima e la differenza;
- lo stesso per i totali per sede, Brescia e Padova;
- il numero delle note fuori massimale del mese, quello del mese prima e
  la differenza.

Il resto della pagina non cambia.

## Criteri di accettazione

I numeri di giugno li abbiamo controllati noi, a mano.

1. `python report.py 2026-07` mostra luglio e giugno: 164 e 193 note,
   8.963,53 € e 10.836,01 €. La differenza è −29 note e −1.872,48 €.
2. Per sede, giugno: Brescia 127 note per 6.395,67 €, Padova 66 note per
   4.440,34 €.
3. Note fuori massimale: 20 a luglio, 42 a giugno.
4. Per gennaio (`python report.py 2026-01`) il mese prima è dicembre 2025,
   che non ha note: la pagina lo mostra con zero note, senza errori.
5. I criteri del ticket 214 valgono ancora: i numeri di luglio sono gli
   stessi, e i test che c'erano passano.
