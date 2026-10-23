---
name: rimborso-trasferta
description: Prepara le indicazioni per una trasferta di lavoro - quanto si può spendere per pasti, albergo e taxi nella città e nei giorni della trasferta, cosa fare prima di partire e come chiedere il rimborso. Da usare quando un dipendente chiede quanto può spendere in trasferta, cosa gli viene rimborsato o come presentare la nota spese di un viaggio.
---

# Indicazioni per una trasferta

1. **I dati della trasferta.** Dalla domanda: città, giorno di partenza,
   notti. Se manca la città o il giorno, chiedilo in una riga e fermati. Se
   manca l'anno, usa quello dei massimali più recenti di `massimali.csv` e
   scrivilo nella risposta; se mancano le notti, è una trasferta in giornata.
2. **I massimali.** Leggi `massimali.csv` (è corto). Per ogni voce (pranzo,
   cena, hotel, taxi) vale la riga della città con il `valido_dal` più
   recente, uguale o precedente al giorno di partenza. Per l'hotel il
   massimale è per notte: moltiplicalo per le notti. Se la città non è
   Milano, Torino o Roma, non ci sono massimali in tabella: lo dice l'art. 3
   della policy, si indicano nell'autorizzazione della trasferta.
3. **Le regole.** Con `cerca`, nella policy trasferte e nelle FAQ:
   l'autorizzazione prima della partenza (e del direttore di funzione oltre
   tre notti), quando spettano pranzo e cena, il treno che non va in nota
   spese, come si inserisce l'hotel, il termine per presentare la nota.
4. **La risposta**, in questo formato, con i file tra parentesi quadre:

   **Trasferta a <città>, dal <giorno>, <notti> notti**
   - Massimali: pranzo X €, cena X €, taxi X € a corsa, hotel X € a notte
     (X € in tutto).
   - Prima di partire: …
   - Al rientro: …

Non inventare massimali o regole che i file non dicono.
