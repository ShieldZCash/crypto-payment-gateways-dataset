#!/usr/bin/env python3
"""Rebuild everything derived from data/crypto-payment-gateways.json.

Edit ONLY the `gateways` array (and bump `version`/`updated`), then run this.
It recomputes `counts` and `summary.full_dataset`, and regenerates the CSV,
DATA.md and the citation metadata (CITATION.cff, .zenodo.json). `summary.study_cohort` is frozen: it is the published August 2026
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

# Citation metadata. Zenodo reads .zenodo.json on each GitHub release and mints
# a new DOI version; GitHub's "Cite this repository" reads CITATION.cff.
fd = d["summary"]["full_dataset"]
sc = d["summary"]["study_cohort"]
repo = "https://github.com/ShieldZCash/crypto-payment-gateways-dataset"
title = "Crypto Payment Gateways Dataset"
abstract = (
    f"An open, hand-verified dataset of {n} crypto payment gateways classified by custody model, "
    f"platform fee, KYC requirement, coin coverage, fiat settlement and Lightning support, every fee "
    f"linked to the official pricing page or docs it was read from. Updated monthly. "
    f"Headline finding: {sc['pct_custodial']}% of gateways are custodial and {sc['pct_non_custodial']}% "
    f"non-custodial (study cohort, n={sc['n']}); the living dataset (n={n}) holds at "
    f"{fd['pct_custodial']}% custodial, {fd['pct_non_custodial']}% non-custodial."
)
keywords = ["crypto payment gateways", "cryptocurrency", "payments", "custody", "non-custodial",
            "KYC", "fees", "Bitcoin", "Lightning Network", "dataset"]
(root / "CITATION.cff").write_text(
    "cff-version: 1.2.0\n"
    'message: "If you use this dataset, please cite it as below."\n'
    f'title: "{title}"\n'
    "type: dataset\n"
    f"version: {d['version']}\n"
    f"date-released: {d['updated']}\n"
    "license: CC-BY-4.0\n"
    f'url: "{repo}"\n'
    f'repository-code: "{repo}"\n'
    f"abstract: {json.dumps(abstract)}\n"
    "keywords:\n" + "".join(f"  - {json.dumps(k)}\n" for k in keywords) +
    "authors:\n"
    '  - name: "Shieldz"\n'
    '    website: "https://shieldz.cash"\n'
    '  - family-names: "Yanbollu"\n'
    '    given-names: "Deniz"\n'
    "references:\n"
    "  - type: article\n"
    '    title: "The Custody Gap: Only 1 in 4 Crypto Payment Gateways Is Non-Custodial"\n'
    f'    url: "{d["canonical"]}"\n'
    "    authors:\n"
    '      - name: "Shieldz"\n'
)
zenodo = {
    "title": f"{title} (v{d['version']}, {n} gateways)",
    "upload_type": "dataset",
    "version": d["version"],
    "publication_date": d["updated"],
    "description": f"<p>{abstract}</p><p>Methodology: {d['methodology']}</p>"
                   f"<p>Write-up and live JSON/CSV: <a href=\"{d['canonical']}\">{d['canonical']}</a></p>",
    "creators": [{"name": "Yanbollu, Deniz", "affiliation": "Shieldz"}],
    "license": "cc-by-4.0",
    "access_right": "open",
    "keywords": keywords,
    "related_identifiers": [
        {"identifier": d["canonical"], "relation": "isDocumentedBy", "resource_type": "publication-article"},
        {"identifier": repo, "relation": "isSupplementTo", "resource_type": "dataset"},
    ],
}
(root / ".zenodo.json").write_text(json.dumps(zenodo, indent=2, ensure_ascii=False) + "\n")
print(f"built: {n} gateways -> JSON summary, CSV, DATA.md, CITATION.cff, .zenodo.json")
