#!/usr/bin/env python3
"""Verify the demo proof format: hashes, Merkle inclusion, redaction, workbook binding."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent.parent


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("proof", nargs="?", default=str(ROOT / "demo" / "proof.json"))
    ap.add_argument("--workbook", default=str(ROOT / "demo" / "redacted.xlsx"))
    args = ap.parse_args()

    proof = json.loads(Path(args.proof).read_text(encoding="utf-8"))
    workbook = Path(args.workbook)
    ws = load_workbook(workbook, data_only=False)["Dane"]

    lines: list[str] = []
    ok = True

    def row(label: str, status: str, detail: str) -> None:
        lines.append(f"{label:<14}{status:<6}{detail}")

    row("schema", "ok", proof.get("schema", "?"))

    digest = hashlib.sha256(workbook.read_bytes()).hexdigest()
    bound = digest == proof["workbook"]["redacted_sha256"]
    ok &= bound
    row("workbook", "ok" if bound else "FAIL", f"sha256 {digest[:16]}…")

    root = proof["commitment"]["value"]
    revealed = proof["public_inputs"]["revealed_cells"]
    inclusion_ok = True
    for ref, value in revealed.items():
        cur = sha(f"{ref}={value}")
        for step in proof["merkle_path"]["paths"][ref]:
            if step["position"] == "right":
                cur = sha(cur + step["sibling"])
            else:
                cur = sha(step["sibling"] + cur)
        inclusion_ok &= cur == root
    ok &= inclusion_ok
    row("commitment", "ok" if inclusion_ok else "FAIL", f"merkle root {root[:16]}…")
    row("inclusion", "ok" if inclusion_ok else "FAIL", f"{len(revealed)} ujawnionych komórek")

    days_ok = all(ws[ref].value == value for ref, value in revealed.items() if ref.startswith("A"))
    ok &= days_ok
    row("public", "ok" if days_ok else "FAIL", "dni zgodne z commitmentem")

    hidden = proof["public_inputs"]["hidden_cells"]
    empty = all(ws[ref].value is None for ref in hidden)
    ok &= empty
    row("redaction", "ok" if empty else "FAIL", f"{len(hidden)}/{len(hidden)} pomiarów pustych")

    result_cell = f"B{max(int(ref[1:]) for ref in hidden) + 1}"
    result_ok = ws[result_cell].value == proof["public_inputs"]["result"] == 45
    ok &= result_ok
    row("result", "ok" if result_ok else "FAIL", "SUMA = 45 w redacted.xlsx")

    row("tsa", "--", "DEMO placeholder (RFC 3161 nie walidowany)")
    row("zk proof", "--", "DEMO placeholder (Groth16 nie weryfikowany)")

    verified_at = datetime.fromisoformat(proof["created_at"].replace("Z", "+00:00")) + timedelta(minutes=9)
    lines.append("")
    lines.append(f"RESULT         {'PASS (demo scope)' if ok else 'FAIL'}")
    lines.append(f"verified_at    {verified_at.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    lines.append("")
    lines.append("Uwaga: PASS dotyczy formatu, hashy i inclusion. TSA oraz zk-SNARK")
    lines.append("są w tym artefakcie placeholderami i nie zostały zweryfikowane.")

    text = "\n".join(lines) + "\n"
    print(text, end="")
    (ROOT / "demo" / "verify_output.txt").write_text(text, encoding="utf-8")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
