"""Il riepilogo mensile delle note spese per la Direzione Amministrativa (ticket-report.md),
con il confronto con il mese prima (ticket-confronto.md, il ticket 215).

Uso:  python report.py 2026-07   -> scrive output/report-2026-07.html

Le note del mese sono quelle con il giorno nel mese, in qualsiasi stato. La sede è quella di
chi ha presentato la nota, da dati/dipendenti.csv (per id: ci sono due Sara Conti). Il controllo
dei massimali è quello di rimborsi.py, non riscritto qui. Il mese prima di gennaio è dicembre
dell'anno prima.
"""
import argparse
import csv
import html
from collections import Counter
from pathlib import Path

from rimborsi import CARTELLA, NOTE_SPESE, controlla, limite_nota, notti

DIPENDENTI = CARTELLA / "dati" / "dipendenti.csv"
OUTPUT = CARTELLA / "output"
VOCI = ["pranzo", "cena", "hotel", "taxi"]


def carica(percorso):
    with open(percorso, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def mese_prima(mese):
    """«2026-07» -> «2026-06»; gennaio -> dicembre dell'anno prima."""
    anno, numero = int(mese[:4]), int(mese[5:])
    if numero == 1:
        return f"{anno - 1}-12"
    return f"{anno}-{numero - 1:02d}"


def riepilogo(note, sede_di):
    """I numeri del report: totali, per sede, per voce, e le note fuori massimale."""
    per_sede = Counter()
    note_per_sede = Counter()
    per_voce = Counter()
    fuori = []
    for nota in note:
        importo = float(nota["importo"])
        sede = sede_di[nota["dipendente_id"]]
        per_sede[sede] += importo
        note_per_sede[sede] += 1
        per_voce[nota["voce"]] += importo
        if not controlla(nota):
            riga = dict(nota)                       # la nota, più massimale ed eccedenza
            riga["limite"] = limite_nota(nota)
            riga["eccedenza"] = importo - riga["limite"]
            fuori.append(riga)
    return {
        "note": len(note),
        "totale": sum(float(nota["importo"]) for nota in note),
        "per_sede": per_sede,
        "note_per_sede": note_per_sede,
        "per_voce": per_voce,
        "fuori": fuori,
    }


def euro(valore):
    """1234.5 -> «1.234,50 €», come nei documenti dell'ufficio."""
    return f"{valore:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def differenza(adesso, prima, formato=str):
    """La differenza con il segno davanti: +5, −29, −1.872,48 €."""
    d = adesso - prima
    segno = "+" if d > 0 else "−" if d < 0 else ""
    return segno + formato(abs(d))


def grafico(per_voce):
    """Un grafico a barre degli importi per voce, in SVG dentro la pagina: niente librerie da internet."""
    massimo = max(per_voce.values(), default=0) or 1
    barre = ""
    for i, voce in enumerate(VOCI):
        larghezza = 360 * per_voce[voce] / massimo
        y = 10 + i * 34
        barre += (f'<text x="0" y="{y + 17}">{voce}</text>'
                  f'<rect x="70" y="{y}" width="{larghezza:.1f}" height="24" fill="#6d28d9"/>'
                  f'<text x="{76 + larghezza:.1f}" y="{y + 17}">{euro(per_voce[voce])}</text>')
    return f'<svg width="560" height="150" font-family="sans-serif" font-size="13">{barre}</svg>'


def pagina(mese, r, prima, r_prima):
    """La pagina HTML del report, un file solo, con il confronto con il mese prima."""
    e = html.escape
    righe_sede = "".join(f"<tr><td>{e(sede)}</td><td>{r['note_per_sede'][sede]}</td><td>{euro(r['per_sede'][sede])}</td></tr>"
                         for sede in sorted(r["per_sede"]))
    righe_voce = "".join(f"<tr><td>{voce}</td><td>{euro(r['per_voce'][voce])}</td></tr>" for voce in VOCI)
    righe_fuori = ""
    for n in r["fuori"]:
        voce = n["voce"] if notti(n) == 1 else f"{n['voce']} ({notti(n)} notti)"
        righe_fuori += (f"<tr><td>{n['id']}</td><td>{e(n['dipendente'])}</td><td>{voce}</td><td>{e(n['citta'])}</td>"
                        f"<td>{n['giorno']}</td><td>{euro(float(n['importo']))}</td><td>{euro(n['limite'])}</td>"
                        f"<td>{euro(n['eccedenza'])}</td></tr>")
    sedi = sorted(set(r["per_sede"]) | set(r_prima["per_sede"]))
    righe_confronto = (
        f"<tr><td>Note</td><td>{r['note']}</td><td>{r_prima['note']}</td>"
        f"<td>{differenza(r['note'], r_prima['note'])}</td></tr>"
        f"<tr><td>Importo</td><td>{euro(r['totale'])}</td><td>{euro(r_prima['totale'])}</td>"
        f"<td>{differenza(r['totale'], r_prima['totale'], euro)}</td></tr>")
    for sede in sedi:
        righe_confronto += (
            f"<tr><td>{e(sede)}, note</td><td>{r['note_per_sede'][sede]}</td><td>{r_prima['note_per_sede'][sede]}</td>"
            f"<td>{differenza(r['note_per_sede'][sede], r_prima['note_per_sede'][sede])}</td></tr>"
            f"<tr><td>{e(sede)}, importo</td><td>{euro(r['per_sede'][sede])}</td><td>{euro(r_prima['per_sede'][sede])}</td>"
            f"<td>{differenza(r['per_sede'][sede], r_prima['per_sede'][sede], euro)}</td></tr>")
    righe_confronto += (
        f"<tr><td>Fuori massimale</td><td>{len(r['fuori'])}</td><td>{len(r_prima['fuori'])}</td>"
        f"<td>{differenza(len(r['fuori']), len(r_prima['fuori']))}</td></tr>")
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>Note spese {mese} — Valtesa S.r.l.</title>
<style>
body {{ font-family: sans-serif; margin: 2em; color: #222; }}
table {{ border-collapse: collapse; margin-bottom: 1.5em; }}
td, th {{ border: 1px solid #ccc; padding: 4px 10px; text-align: left; }}
th {{ background: #eee; }}
</style>
</head>
<body>
<h1>Note spese di {mese}</h1>
<p>{r['note']} note spese, per un totale di {euro(r['totale'])}. {len(r['fuori'])} fuori massimale.</p>
<h2>Il confronto con il mese prima</h2>
<table><tr><th></th><th>{mese}</th><th>{prima}</th><th>Differenza</th></tr>{righe_confronto}</table>
<h2>Per sede</h2>
<table><tr><th>Sede</th><th>Note</th><th>Importo</th></tr>{righe_sede}</table>
<h2>Per voce</h2>
<table><tr><th>Voce</th><th>Importo</th></tr>{righe_voce}</table>
{grafico(r['per_voce'])}
<h2>Note fuori massimale</h2>
<p>La differenza tra importo e massimale resta a carico del dipendente (policy trasferte, art. 7).</p>
<table><tr><th>Id</th><th>Dipendente</th><th>Voce</th><th>Città</th><th>Giorno</th><th>Importo</th><th>Massimale</th><th>Eccedenza</th></tr>{righe_fuori}</table>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Il riepilogo mensile delle note spese.")
    parser.add_argument("mese", help="il mese, AAAA-MM (per esempio 2026-07)")
    args = parser.parse_args()

    sede_di = {d["id"]: d["sede"] for d in carica(DIPENDENTI)}
    tutte = carica(NOTE_SPESE)
    note = [nota for nota in tutte if nota["giorno"].startswith(args.mese + "-")]
    prima = mese_prima(args.mese)
    note_prima = [nota for nota in tutte if nota["giorno"].startswith(prima + "-")]
    r = riepilogo(note, sede_di)
    r_prima = riepilogo(note_prima, sede_di)
    OUTPUT.mkdir(exist_ok=True)
    percorso = OUTPUT / f"report-{args.mese}.html"
    percorso.write_text(pagina(args.mese, r, prima, r_prima), encoding="utf-8")
    print(f"{r['note']} note spese, {euro(r['totale'])}, {len(r['fuori'])} fuori massimale -> {percorso}")


if __name__ == "__main__":
    main()
