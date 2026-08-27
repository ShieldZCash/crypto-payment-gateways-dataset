#!/usr/bin/env python3
"""Regenerate DATA.md (full markdown table) from data/crypto-payment-gateways.json."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
d = json.loads((root / "data" / "crypto-payment-gateways.json").read_text())
rows = sorted(d["gateways"], key=lambda g: (g["fee_pct"] if isinstance(g["fee_pct"], (int, float)) else 99, g["name"].lower()))

def yn(v):
    return "yes" if v else "no"

lines = [
    f"# {d['dataset']} — full table",
    "",
    f"{d['counts']['total']} gateways, v{d['version']}, updated {d['updated']}. "
    f"License: [{d['license']}]({d['license_url']}), attribution: [Shieldz]({d['publisher_url']}). "
    f"Canonical write-up: {d['canonical']}",
    "",
    "An asterisk on the fee marks rows where the fee could not be confirmed on an official pricing page "
    "(`verified=false`). `study` marks the 50-gateway cohort of the published August 2026 study.",
    "",
    "| Provider | Fee % | Custody | KYC | Coins | Fiat | Lightning | Founded | Study | Notable |",
    "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
]
for g in rows:
    fee = f"{g['fee_pct']}" + ("" if g.get("verified") else "\\*")
    lines.append(
        f"| [{g['name']}]({g['url']}) | {fee} | {g['custody']} | {g['kyc']} | {g['coins']} "
        f"| {yn(g['settlement_fiat'])} | {yn(g['lightning'])} | {g['founded']} | {yn(g['study_cohort'])} "
        f"| {g['notable']} |"
    )
lines.append("")
(root / "DATA.md").write_text("\n".join(lines))
print(f"DATA.md written: {len(rows)} rows")
