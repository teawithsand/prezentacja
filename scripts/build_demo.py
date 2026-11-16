#!/usr/bin/env python3
"""Build the five demo artefacts for the deck (illustrative proof format)."""
from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

ROOT = Path(__file__).resolve().parent.parent
DEMO = ROOT / "demo"
DEMO.mkdir(exist_ok=True)

# Seria: liczba wykiełkowanych siewek, dzień po dniu. Suma = 45.
COUNTS = [8, 6, 5, 7, 3, 4, 6, 2, 4]
RESULT = sum(COUNTS)
FIRST = 2
LAST = FIRST + len(COUNTS) - 1
SUM_ROW = LAST + 1

DAYS = {f"A{r}": r - FIRST + 1 for r in range(FIRST, LAST + 1)}
SEEDLINGS = {f"B{r}": v for r, v in zip(range(FIRST, LAST + 1), COUNTS)}
SUM_CELL = f"B{SUM_ROW}"

HIDDEN = list(SEEDLINGS)
REVEALED = list(DAYS) + [SUM_CELL]
VALUES = {**DAYS, **SEEDLINGS, SUM_CELL: RESULT}
FORMULA = f"SUM(B{FIRST}:B{LAST})"
TS = "2026-03-14T10:22:00Z"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def merkle_levels(leaves: list[str]) -> list[list[str]]:
    levels = [leaves]
    while len(levels[-1]) > 1:
        cur = levels[-1]
        nxt = []
        for i in range(0, len(cur), 2):
            left = cur[i]
            right = cur[i + 1] if i + 1 < len(cur) else cur[i]
            nxt.append(sha(left + right))
        levels.append(nxt)
    return levels


def build_sheet(ws, redacted: bool) -> None:
    thin = Side(style="thin", color="D1D5DB")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    black = PatternFill("solid", fgColor="1A1A1A")
    body = Font(name="Arial", size=12)
    head = Font(name="Arial", bold=True, size=10, color="6B7280")

    for col, title in (("A", "dzień"), ("B", "siewki")):
        cell = ws[f"{col}1"]
        cell.value = title
        cell.font = head
        cell.alignment = Alignment(horizontal="center")
        cell.border = border

    for row in range(FIRST, LAST + 1):
        day = ws[f"A{row}"]
        day.value = VALUES[f"A{row}"]
        day.font = body
        day.alignment = Alignment(horizontal="center")
        day.border = border

        cell = ws[f"B{row}"]
        cell.font = body
        cell.alignment = Alignment(horizontal="center")
        cell.border = border
        if redacted:
            cell.value = None
            cell.fill = black
        else:
            cell.value = VALUES[f"B{row}"]

    label = ws[f"A{SUM_ROW}"]
    label.value = "SUMA"
    label.font = head
    label.alignment = Alignment(horizontal="center")
    label.border = border

    result = ws[SUM_CELL]
    result.value = RESULT
    result.font = Font(name="Arial", bold=True, size=12, color="0F766E")
    result.alignment = Alignment(horizontal="center")
    result.border = border

    ws.column_dimensions["A"].width = 9
    ws.column_dimensions["B"].width = 11

    if redacted:
        note = ws[f"A{SUM_ROW + 2}"]
        note.value = "Wynik pochodzi z dowodu. Dziewięć pomiarów nie jest zapisanych w tym pliku."
        note.font = Font(name="Arial", size=9, italic=True, color="6B7280")


def build_source() -> Path:
    wb = Workbook()
    ws = wb.active
    ws.title = "Dane"
    build_sheet(ws, redacted=False)
    ws[SUM_CELL] = f"={FORMULA}"
    ws[SUM_CELL].font = Font(name="Arial", bold=True, size=12, color="0F766E")
    ws[SUM_CELL].alignment = Alignment(horizontal="center")
    path = DEMO / "source.xlsx"
    wb.save(path)
    return path


def build_redacted() -> Path:
    wb = Workbook()
    ws = wb.active
    ws.title = "Dane"
    build_sheet(ws, redacted=True)
    info = wb.create_sheet("Info")
    info["A1"] = "redacted.xlsx — artefakt demo Verixcel"
    info["A1"].font = Font(bold=True, size=14)
    info["A3"] = "9 z 9 pomiarów ukryto. Wynik SUMA = 45 jest odtwarzany z proof.json."
    info["A4"] = "Plik nie zawiera ukrytych wartości — to nie jest tylko czarna nakładka."
    info["A5"] = "TSA i zk-SNARK w proof.json są oznaczone jako warstwa demo."
    info.column_dimensions["A"].width = 100
    path = DEMO / "redacted.xlsx"
    wb.save(path)
    return path


def build_proof(source_path: Path, redacted_path: Path) -> dict:
    leaves = [sha(f"{ref}={VALUES[ref]}") for ref in VALUES]
    levels = merkle_levels(leaves)
    root = levels[-1][0]
    order = list(VALUES)
    paths = {}
    for ref in REVEALED:
        idx = order.index(ref)
        steps = []
        for level in levels[:-1]:
            sib = idx ^ 1
            if sib >= len(level):
                sib = idx
            steps.append({
                "sibling": level[sib],
                "position": "right" if idx % 2 == 0 else "left",
            })
            idx //= 2
        paths[ref] = steps

    proof = {
        "schema": "verixcel-proof/0.1-demo",
        "demo": True,
        "disclaimer": (
            "Artefakt ilustruje format dowodu. Commitment, drzewo Merkle i ścieżki "
            "inclusion są policzone realnie; TSA i zk-SNARK są placeholderami demo "
            "i nie zostały kryptograficznie zweryfikowane."
        ),
        "created_at": TS,
        "commitment": {
            "algorithm": "sha256",
            "scheme": "merkle-root",
            "canonical": "cell=value;" + ";".join(f"{ref}={VALUES[ref]}" for ref in VALUES),
            "value": root,
            "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        },
        "tsa_token": {
            "kind": "demo-placeholder",
            "protocol": "RFC 3161",
            "time": TS,
            "authority": "TSA (demo)",
            "token_b64": base64.b64encode(b"demo-rfc3161-token-not-valid").decode(),
        },
        "merkle_path": {
            "root": root,
            "leaf_count": len(leaves),
            "revealed": REVEALED,
            "paths": paths,
        },
        "zk_proof": {
            "kind": "demo-placeholder",
            "system": "Groth16",
            "curve": "BN254",
            "statement": f"SUM(B{FIRST}:B{LAST})=45",
            "proof": "0x" + "00" * 32,
        },
        "public_inputs": {
            "formula": FORMULA,
            "result": RESULT,
            "precision": "fixed-point 1e-6",
            "hidden_cells": HIDDEN,
            "revealed_cells": {ref: VALUES[ref] for ref in REVEALED},
        },
        "workbook": {
            "redacted_sha256": hashlib.sha256(redacted_path.read_bytes()).hexdigest(),
        },
    }
    (DEMO / "proof.json").write_text(json.dumps(proof, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return proof


def build_html(proof: dict) -> None:
    hidden = set(HIDDEN)
    rows = ['<tr><th>dzień</th><th>siewki</th></tr>']
    for row in range(FIRST, LAST + 1):
        ref = f"B{row}"
        cell = '<td class="hidden"></td>' if ref in hidden else f"<td>{VALUES[ref]}</td>"
        rows.append(f"<tr><td>{VALUES[f'A{row}']}</td>{cell}</tr>")
    rows.append(f'<tr class="sum"><td>SUMA</td><td class="result">{RESULT}</td></tr>')

    body = "".join(rows)
    html = f"""<!doctype html>
<html lang="pl"><head><meta charset="utf-8">
<style>
  @page {{ size: A4 portrait; margin: 16mm; }}
  body {{ font-family: 'IBM Plex Sans', 'DejaVu Sans', sans-serif; color: #1A1A1A; background: #FAFAFA; }}
  h1 {{ font-size: 18pt; margin: 0 0 4mm; }}
  .sub {{ font-family: 'IBM Plex Mono', monospace; font-size: 8.5pt; color: #6B7280; margin-bottom: 8mm; }}
  table {{ border-collapse: collapse; font-family: 'IBM Plex Mono', monospace; font-size: 13pt; background: #fff; }}
  th, td {{ border: 1px solid #D1D5DB; width: 22mm; height: 9mm; text-align: center; font-weight: 400; }}
  th {{ background: #F4F4F5; color: #6B7280; font-size: 8.5pt; }}
  td.hidden {{ background: #1A1A1A; }}
  td.result {{ color: #0F766E; font-weight: 600; }}
  tr.sum td {{ border-top: 2px solid #9CA3AF; font-weight: 600; }}
  .claim {{ font-family: 'IBM Plex Mono', monospace; font-size: 8.5pt; letter-spacing: 0.12em;
           text-transform: uppercase; color: #0F766E; margin-top: 8mm; }}
  .verdict {{ border-left: 3px solid #0F766E; background: #E9F5F2; padding: 4mm 5mm;
             font-size: 11pt; line-height: 1.45; margin-top: 3mm; max-width: 120mm; }}
  .note {{ font-size: 8.5pt; color: #6B7280; margin-top: 10mm; max-width: 140mm; line-height: 1.5; }}
</style></head><body>
<h1>redacted.xlsx — podgląd awaryjny · Verixcel</h1>
<div class="sub">demo · 9 z 9 pomiarów ukrytych · widoczna tylko suma</div>
<table>{body}</table>
<div class="claim">✓ Twierdzenie z dowodem kryptograficznym</div>
<div class="verdict">Formuła dała 45 na ukrytych danych, które nie zmieniły się od 14 marca.</div>
<div class="note">Wynik pochodzi z proof.json. Ukryte wartości nie są zapisane w pliku redacted.xlsx.
TSA i zk-SNARK są w warstwie demo. Ten PDF jest wyłącznie podglądem na wypadek braku Excela.</div>
</body></html>"""
    out = ROOT / "out"
    out.mkdir(exist_ok=True)
    (out / "redacted.html").write_text(html, encoding="utf-8")


def main() -> None:
    source = build_source()
    redacted = build_redacted()
    proof = build_proof(source, redacted)
    build_html(proof)
    print("commitment", proof["commitment"]["value"])
    print("source sha", proof["commitment"]["source_sha256"])
    print("files", sorted(p.name for p in DEMO.iterdir()))


if __name__ == "__main__":
    main()
