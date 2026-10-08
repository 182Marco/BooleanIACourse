# Ticket 214 — Riepilogo mensile delle note spese

**Da:** Ufficio del personale · **Per:** IT · **Priorità:** normale

Ogni mese la Direzione Amministrativa ci chiede un riepilogo delle note
spese. Oggi lo facciamo a mano, con un foglio di calcolo. Ci serve un
comando che lo prepari:

```
python report.py 2026-07
```

scrive `output/report-2026-07.html`, una pagina con:

- il numero delle note del mese e l'importo totale. Le note del mese sono
  quelle con il giorno nel mese, in qualsiasi stato;
- i totali per sede, Brescia e Padova (la sede di chi ha presentato la
  nota), e per voce (pranzo, cena, hotel, taxi), con un grafico degli
  importi per voce;
- le note fuori massimale, una per riga, con il massimale applicato e di
  quanto lo superano: è la parte che resta a carico del dipendente (policy
  trasferte, art. 7).

La pagina la apriamo anche dal portatile in trasferta, senza rete: deve
essere un file solo, senza niente da scaricare da internet.

## Criteri di accettazione

I numeri di luglio li abbiamo controllati noi, a mano.

1. `python report.py 2026-07` scrive `output/report-2026-07.html`.
2. Luglio: 164 note, 8.963,53 €. Brescia 105 note per 5.141,74 €, Padova
   59 note per 3.821,79 €.
3. Luglio, per voce: pranzo 767,14 €, cena 1.389,97 €, hotel 5.863,40 €,
   taxi 943,02 €.
4. Luglio: 20 note fuori massimale.
5. Un mese senza note (`python report.py 2026-12`) dà una pagina con zero
   note, senza errori.
6. La pagina si apre senza connessione: dentro non c'è nessun indirizzo
   `http://` o `https://`.
7. I test stanno in `tests/test_report.py` e non modificano i file in
   `dati/`.
