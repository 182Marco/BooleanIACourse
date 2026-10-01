# Modulo 4 · Lezione 1 — Cosa fa una harness: i file

La lezione è quasi tutta di teoria. L'unica attività è la lettura di una
trace (20 minuti), senza codice e senza installazioni: basta aprire due file.

| File | Ruolo | Cosa contiene |
|---|---|---|
| `dataset/trace-claude-code.md` | 📄 dati | La trace di una sessione vera di Claude Code su un piccolo progetto inventato (il controllo delle note spese di un'azienda). In testa la prima chiamata: il system prompt blocco per blocco, i tool con i loro parametri, i promemoria della harness. Poi ogni chiamata con i token, i tool chiesti (con i parametri) e i risultati. Ripulita da percorsi e identificativi; i risultati lunghi sono tagliati e lo dice il testo. |
| `dataset/trace-claude-code-completa.md` | 📄 dati | La stessa sessione, senza tagli, scritta per essere letta: tool, system prompt e promemoria nell'ordine in cui li riceve il modello, poi ogni chiamata con i token, i tool chiesti e i risultati per intero. I pezzi lunghi sono blocchi chiusi, che si aprono con un clic. Non serve per l'esercizio: è per chi vuole vedere tutto. |
| `dataset/trace-claude-code-completa.jsonl` | 📄 dati | La stessa sessione nel formato originale in cui Claude Code la salva: una riga JSON per record, nell'ordine in cui li ha scritti, con system prompt, definizioni dei tool, promemoria e risultati completi. Ripulita da percorsi e identificativi. La versione `.md` qui sopra dice a quali righe sta ogni cosa. |
| `working/scheda.md` | ⌨️ da compilare | Le sei domande dell'esercizio. Per ognuna: la risposta, il pezzo della harness, dove ne avete scritto la versione di base (lezione e nome nel codice). |
| `solutions/scheda.md` | 🎤 soluzione del docente | La scheda compilata. |

## Come si lavora

Aprite `dataset/trace-claude-code.md` (in VS Code: tasto destro, «Open
Preview», per leggerla formattata) e accanto `working/scheda.md`.
Rispondete nella scheda. Fatto quando le sei domande hanno risposta, pezzo e
«Voi» (la tabella delle lezioni è in fondo alla scheda).
