"""domande_lab2.py — le domande del Lab 2, una per riga con la strada attesa.

Sono le vostre di Modulo 3 · Lezione 6: le nove che il RAG da solo
sbagliava (la risposta stava in un ticket o nel changelog, e il retrieval
portava altro), più una doppia sui dati e sui documenti insieme.

Non si modifica: assistente.py le legge quando LAB2 = True. Le domande
vostre vanno in LE_MIE_DOMANDE, in assistente.py.
"""

DOMANDE_LAB2 = [
    ("Un fulmine ha colpito casa mia e da quel momento non mi funziona più il sollevamento della scrivania. Qual è il problema?", "documenti"),
    ("Come mai non ho ricevuto un rimborso totale per il mio reso?", "documenti"),
    ("Come mai un mio amico riesce a impostare dei profili sulla sua LumaDesk e io no?", "documenti"),
    ("Posso utilizzare un doppio monitor nativamente sulla mia LumaDesk LD-200?", "documenti"),
    ("Quali altri requisiti servono, oltre al fatto che non sia scaduto il termine, per esercitare il diritto alla garanzia?", "documenti"),
    ("Devo reimpostare le mie memorie di posizione preferite della scrivania ad ogni accensione", "documenti"),
    ("Non vedo la scrivania sul telefono. Cosa devo fare?", "documenti"),
    ("Non riesco a salvare la posizione della scrivania, cosa faccio?", "documenti"),
    ("Sento un rumore metallico durante la regolazione della scrivania, come intervenire?", "documenti"),
    ("Lorenzo Rossi ha diritto alla spedizione gratuita sull'ordine 1296?", "documenti+dati"),
]
