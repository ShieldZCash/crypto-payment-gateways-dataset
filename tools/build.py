#!/usr/bin/env python3
"""Rebuild everything derived from data/crypto-payment-gateways.json.

Edit ONLY the `gateways` array (and bump `version`/`updated`), then run this.
It recomputes `counts` and `summary.full_dataset`, and regenerates the CSV and
DATA.md. `summary.study_cohort` is frozen: it is the published August 2026
study (n=50) and is never recomputed.
"""
import csv
import json
import statistics
from pathlib import Path

root = Path(__file__).resolve().parent.parent
json_path = root / "data" / "crypto-payment-gateways.json"
d = json.loads(json_path.read_text())
gws = d["gateways"]

FIELDS = ["name", "url", "fee_pct", "fee_note", "custody", "kyc", "coins",
          "settlement_fiat", "lightning", "founded", "notable", "verified",
          "source_url", "study_cohort"]

n = len(gws)
study = [g for g in gws if g["study_cohort"]]
d["counts"] = {"total": n, "study_cohort": len(study), "additional": n - len(study)}

by = lambda k, v: sum(1 for g in gws if g[k] == v)
fees = [g["fee_pct"] for g in gws if isinstance(g["fee_pct"], (int, float))]
d["summary"]["full_dataset"] = {
    "n": n,
    "custodial": by("custody", "custodial"),
    "non_custodial": by("custody", "non-custodial"),
    "self_hosted": by("custody", "self-hosted"),
    "hybrid": by("custody", "hybrid"),
    "pct_custodial": round(by("custody", "custodial") / n * 100),
    "pct_non_custodial": round(by("custody", "non-custodial") / n * 100),
    "kyc_required": by("kyc", "required"),
    "kyc_optional": by("kyc", "optional"),
    "kyc_none": by("kyc", "none"),
    "pct_kyc_required": round(by("kyc", "required") / n * 100),
    "median_fee_pct": round(statistics.median(fees), 2),
    "zero_platform_fee": sum(1 for f in fees if f == 0),
    "fiat_settlement": sum(1 for g in gws if g["settlement_fiat"]),
    "pct_fiat_settlement": round(sum(1 for g in gws if g["settlement_fiat"]) / n * 100),
    "lightning": sum(1 for g in gws if g["lightning"]),
    "verified": sum(1 for g in gws if g["verified"]),
}
json_path.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")

with (root / "data" / "crypto-payment-gateways.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    for g in sorted(gws, key=lambda g: g["name"].lower()):
        w.writerow({k: (str(v).lower() if isinstance(v, bool) else v) for k, v in g.items()})

rows = sorted(gws, key=lambda g: (g["fee_pct"] if isinstance(g["fee_pct"], (int, float)) else 99, g["name"].lower()))
yn = lambda v: "yes" if v else "no"
lines = [
    f"# {d['dataset']}: full table",
    "",
    f"{n} gateways, v{d['version']}, updated {d['updated']}. "
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
    fee = f"{g['fee_pct']}" + ("" if g["verified"] else "\\*")
    lines.append(
        f"| [{g['name']}]({g['url']}) | {fee} | {g['custody']} | {g['kyc']} | {g['coins']} "
        f"| {yn(g['settlement_fiat'])} | {yn(g['lightning'])} | {g['founded']} | {yn(g['study_cohort'])} "
        f"| {g['notable']} |"
    )
lines.append("")
(root / "DATA.md").write_text("\n".join(lines))
print(f"built: {n} gateways -> JSON summary, CSV, DATA.md")
