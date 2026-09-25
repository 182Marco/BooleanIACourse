# Griglia delle domande — versione del docente

Il tema: Valtesa (`temi/valtesa/`), con la collection di
`obiettivo2_documenti.py`, il database di `scaffolding/tabelle_in_db.py` e
l'agente di `obiettivo4_assistente.py`, modello `gpt-5.6-luna`.
`obiettivo4_assistente.py` è la colonna «Prima»: le due cure qui sotto il
docente le fa a lezione, su quel file.

Ogni domanda è stata lanciata tre volte (tre giri): la stessa domanda non dà
sempre la stessa risposta, e una domanda che passa una volta su tre non è
sistemata. Il follow-up (9) è lanciato nella stessa sessione della 1.

La **risposta vera** è stata cercata prima: nei documenti, o con una SELECT
scritta a mano (`python scaffolding/sql.py temi/valtesa/valtesa.db "SELECT …"`).

| # | Tipo | Domanda | Risposta vera | Strada presa | Prima | Cura 1 | Cura 2 |
|---|---|---|---|---|---|---|---|
| 1 | documenti | Qual è il massimale per una cena in trasferta a Milano? | 35 € per le cene fino al 30 giugno 2026, 40 € dal 1° luglio (Circolare 7/2026) | documenti | 3/3 | 3/3 | 3/3 |
| 2 | documenti | Se sono in trasferta mi spetta il buono pasto? | Sì, con almeno 6 ore di lavoro, se non si chiede il rimborso del pranzo | documenti | 3/3 | 3/3 | 3/3 |
| 3 | documenti | Sono appena stato assunto: entro quando devo fare i corsi sulla sicurezza? | Formazione generale entro 30 giorni; la specifica dipende dal reparto | documenti | 0/3, «non trovato» | 0/3 | 3/3 |
| 4 | dati | Quanti giorni di ferie ha preso Sara Conti nel 2026? | Due Sara Conti: 15 (Brescia) e 21 (Padova) | dati | 0/3, «36» | 3/3 | 3/3 |
| 5 | dati | Quante note spese sono ancora in attesa di approvazione, e per quale importo? | 56, per 2.184,40 € | dati | 0/3, «0» | 1/3 | 3/3 |
| 6 | dati | Quante ore di permesso hanno preso i dipendenti del reparto IT nel 2026? | 31 | dati | 3/3 | 3/3 | 2/3 |
| 7 | tutte e due | La nota spese 1043 rispetta il massimale? | Sì: cena a Milano del 15 luglio 2026, 38,50 €, massimale 40 € | documenti+dati | 2/3 | 0/3 | 1/3 |
| 8 | senza risposta | Quando viene pagato il premio di produzione? | Non c'è in nessun documento né tabella | documenti | 3/3, «non trovato» | 3/3 | 3/3 |
| 9 | follow-up della 1 | E per il pranzo? | 25 €, invariato | documenti | 3/3 | 3/3 | 3/3 |
| | | | | **totale** | **17/27** | **19/27** | **24/27** |

**Cura 1:** una riga nelle istruzioni sui nomi uguali. **Cura 2:** K da 4 a 8,
con la cura 1 già fatta. Le misure sono in `misure_valtesa_*.json`, nella
cartella della lezione.

## Cura 1: le istruzioni sui nomi uguali (domanda 4)

**Cosa succedeva.** La query filtra `nome = 'Sara' AND cognome = 'Conti'` e
fa `SUM(quantita)`: le Sara Conti sono due, e la risposta «36» è la somma di
15 e 21, un numero che non riguarda nessuna delle due. Si vede nella traccia,
e con `sql.py` (due righe in `dipendenti`).

**Cosa ho cambiato.** Una riga nelle istruzioni. La prima versione:

> Se un nome corrisponde a più persone, non sommare i loro dati: dai il
> risultato di ognuna, con la sede, e chiedi di quale si parla.

Sara Conti è passata a 3/3, ma la domanda 6 è scesa a 2/3: l'agente elencava
le ore persona per persona, e in un giro ha dimenticato il totale. La
seconda versione, più stretta:

> Se la domanda nomina una persona e nel database ci sono più dipendenti con
> quel nome, non sommare i loro dati: dai il dato di ognuno, con la sede, e
> chiedi di quale si parla.

Sara Conti 3/3, domanda 6 di nuovo 3/3 (colonna «Cura 1»).

**Le altre dopo la modifica.** La 5 e la 7 si muovono da un giro all'altro
anche senza cambiare niente che le riguardi (vedi sotto). La lista delle ore
persona per persona è rimasta: nella misura con K 8 un giro su tre è di
nuovo senza totale.

## Cura 2: K da 4 a 8 (domanda 3)

**Cosa succedeva.** «Non ho trovato entro quando completare i corsi.» Il
chunk con la tabella dei corsi c'è, ma per la domanda è 6° e 8° nella
ricerca: con K 4 non arriva al modello. È il caso comune di Modulo 3 ·
Lezione 6.

**Cosa ho cambiato.** `K = 8` in `obiettivo4_assistente.py` (era 4). La domanda 3 è
passata a 3/3. I token in input per domanda, in media, sono saliti da 1.881
a 2.330 (+24%).

**Le altre dopo la modifica.** Come prima, tranne la 6 (2/3, la lista della
cura 1). La 5 in questa misura è 3/3, ma K non la riguarda: è una domanda
sui dati.

## Rimaste

- **La 7, nota spese 1043: 5 giri giusti su 12**, contando tutte e quattro
  le misure. La traccia dice perché: l'argomento di `cerca_documenti`. Quando
  il modello cerca «il massimale per la voce cena», il passaggio della
  Circolare 7/2026 con i 40 € è tra il 1° e il 6° posto; quando cerca «il
  massimale applicabile alle note spese», tra il 6° e il 12°, e l'agente
  risponde che il massimale non l'ha trovato. Non sistemata.
- **La 5, note in attesa: 6 giri giusti su 12.** Il modello riprende le
  parole della domanda e filtra `stato = 'in attesa di approvazione'`;
  nella tabella il valore è `in attesa`. È la materia di Modulo 3 ·
  Lezione 13.
