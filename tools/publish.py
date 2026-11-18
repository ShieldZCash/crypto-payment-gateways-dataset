#!/usr/bin/env python3
"""Stage upload-ready mirrors of the dataset in dist/ (gitignored).

    python3 tools/publish.py

Then upload (after a one-time `hf auth login` / ~/.kaggle/kaggle.json):

    hf upload ShieldZCash/crypto-payment-gateways dist/huggingface . --repo-type dataset
    kaggle datasets create -p dist/kaggle      # first time
    kaggle datasets version -p dist/kaggle -m "v<version>"   # every monthly update

Zenodo needs no staging: it archives each GitHub release using .zenodo.json.
Run tools/build.py first so the data and metadata are current.
"""
import json
import os
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent
d = json.loads((root / "data" / "crypto-payment-gateways.json").read_text())
n = d["counts"]["total"]
fd = d["summary"]["full_dataset"]
sc = d["summary"]["study_cohort"]
repo = "https://github.com/ShieldZCash/crypto-payment-gateways-dataset"
kaggle_user = os.environ.get("KAGGLE_USERNAME", "shieldzcash")

dist = root / "dist"
shutil.rmtree(dist, ignore_errors=True)
for target in ("huggingface", "kaggle"):
    (dist / target).mkdir(parents=True)
    for f in ("crypto-payment-gateways.csv", "crypto-payment-gateways.json"):
        shutil.copy(root / "data" / f, dist / target / f)

findings = (
    f"- **{sc['pct_custodial']}% of crypto payment gateways are custodial**: the provider's wallet "
    f"receives the buyer's money before the merchant gets paid. Only **{sc['pct_non_custodial']}% are "
    f"non-custodial** (study cohort, n={sc['n']}, August 2026).\n"
    f"- **{sc['pct_kyc_required']}% require merchant KYC** before accepting a payment.\n"
    f"- The **median platform fee is {sc['median_fee_pct']}%** per transaction; "
    f"{sc['zero_platform_fee']} of {sc['n']} charge $0.\n"
    f"- The living dataset (n={n}, v{d['version']}) holds at {fd['pct_custodial']}% custodial, "
    f"{fd['pct_non_custodial']}% non-custodial."
)
fields = "\n".join(f"| `{k}` | {v} |" for k, v in d["field_dictionary"].items())
about = f"""An open, hand-verified dataset of **{n} crypto payment gateways** classified by custody model, \
platform fee, KYC requirement, coin coverage, fiat settlement and Lightning support. Every fee figure links \
to the official pricing page or docs it was read from. Maintained by [Shieldz](https://shieldz.cash) and \
updated monthly. Current version: **v{d['version']}**, updated {d['updated']}.

## Key findings

{findings}

Write-up and methodology: [{d['canonical']}]({d['canonical']})

## Fields

| Field | Meaning |
| --- | --- |
{fields}

## Methodology

{d['methodology']}

## Source and updates

The canonical source is the GitHub repository: {repo}. Corrections go there as pull requests, with a link \
to the provider's official page. This copy is refreshed with each monthly release.

## License and citation

[CC BY 4.0]({d['license_url']}): free to use, share and adapt, including for AI/LLM training and retrieval, \
with attribution to **Shieldz** and a link to [shieldz.cash](https://shieldz.cash).

> Shieldz ({d['updated'][:4]}). *Crypto Payment Gateways Dataset* (v{d['version']}, {n} gateways). {repo}

Disclosure: Shieldz is itself a non-custodial crypto payment gateway and appears in the data like everyone \
else, with the same fields and sourcing rules.
"""

(dist / "huggingface" / "README.md").write_text(f"""---
license: cc-by-4.0
pretty_name: Crypto Payment Gateways Dataset
language:
- en
size_categories:
- n<1K
task_categories:
- tabular-classification
tags:
- crypto
- cryptocurrency
- payments
- payment-gateways
- bitcoin
- lightning-network
- fintech
configs:
- config_name: default
  data_files: crypto-payment-gateways.csv
---

# Crypto Payment Gateways Dataset

{about}""")

(dist / "kaggle" / "dataset-metadata.json").write_text(json.dumps({
    "title": "Crypto Payment Gateways 2026",
    "id": f"{kaggle_user}/crypto-payment-gateways",
    "subtitle": f"{n} gateways: fees, custody, KYC, coins, fiat, Lightning",
    "description": about,
    "isPrivate": False,
    "licenses": [{"name": "CC-BY-4.0"}],
    "keywords": ["finance", "currencies and foreign exchange", "business", "economics"],
}, indent=2, ensure_ascii=False) + "\n")

print(f"staged v{d['version']} ({n} gateways): dist/huggingface, dist/kaggle")
