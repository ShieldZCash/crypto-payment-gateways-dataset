#!/usr/bin/env python3
"""Validate data/crypto-payment-gateways.json. Exits non-zero on any error."""
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

root = Path(__file__).resolve().parent.parent
d = json.loads((root / "data" / "crypto-payment-gateways.json").read_text())
errors = []

REQUIRED = {
    "name": str, "url": str, "fee_pct": (int, float), "fee_note": str,
    "custody": str, "kyc": str, "coins": int, "settlement_fiat": bool,
    "lightning": bool, "founded": int, "notable": str, "verified": bool,
    "source_url": str, "study_cohort": bool,
}
CUSTODY = {"custodial", "non-custodial", "self-hosted", "hybrid"}
KYC = {"none", "optional", "required"}

def is_url(u):
    p = urlparse(u)
    return p.scheme in ("http", "https") and p.netloc

seen = set()
for i, g in enumerate(d["gateways"]):
    who = f"gateways[{i}] ({g.get('name', '?')})"
    for k, t in REQUIRED.items():
        if k not in g:
            errors.append(f"{who}: missing field '{k}'")
        elif not isinstance(g[k], t) or (t != bool and isinstance(g[k], bool) and k != "fee_pct"):
            errors.append(f"{who}: field '{k}' has wrong type {type(g[k]).__name__}")
    extra = set(g) - set(REQUIRED)
    if extra:
        errors.append(f"{who}: unknown fields {sorted(extra)}")
    if g.get("custody") not in CUSTODY:
        errors.append(f"{who}: custody must be one of {sorted(CUSTODY)}")
    if g.get("kyc") not in KYC:
        errors.append(f"{who}: kyc must be one of {sorted(KYC)}")
    for k in ("url", "source_url"):
        if isinstance(g.get(k), str) and not is_url(g[k]):
            errors.append(f"{who}: {k} is not a valid http(s) URL")
    if isinstance(g.get("fee_pct"), (int, float)) and not 0 <= g["fee_pct"] <= 10:
        errors.append(f"{who}: fee_pct {g['fee_pct']} out of range 0-10")
    if isinstance(g.get("founded"), int) and not 2008 <= g["founded"] <= 2027:
        errors.append(f"{who}: founded {g['founded']} looks wrong")
    key = g.get("name", "").strip().lower()
    if key in seen:
        errors.append(f"{who}: duplicate provider name")
    seen.add(key)

study_n = sum(1 for g in d["gateways"] if g.get("study_cohort"))
if study_n != 50:
    errors.append(f"study cohort must stay frozen at 50 entries, found {study_n}")
if d["counts"]["total"] != len(d["gateways"]):
    errors.append("counts.total does not match gateways length — run tools/build.py")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(d['gateways'])} gateways valid")
