# Contributing

Contributions are welcome: new gateways, fee corrections, custody reclassifications, dead-link fixes. The bar is simple: **every fact must be checkable on an official page**.

## Adding a gateway

1. Edit **only** `data/crypto-payment-gateways.json`, adding an object to the `gateways` array. The CSV and `DATA.md` are generated; don't edit them by hand.
2. Fill every field (see the field dictionary in the [README](README.md#fields)). Rules:
   - `source_url` is **required** and must be an official pricing/docs page of the provider, not a review site, not a blog, not ours.
   - `fee_pct` is the standard advertised per-transaction platform fee. If you cannot confirm it on an official page, set `verified: false` and say so in `fee_note`.
   - `custody` follows the definitions below. When in doubt, open an issue first.
   - `notable` is one neutral, factual sentence. Marketing language ("best", "leading", "revolutionary") will be asked to change.
   - `study_cohort` must be `false`: the published 50-gateway August 2026 study is frozen so its numbers stay reproducible.
3. Run `python3 tools/build.py` (regenerates CSV, DATA.md and the summary counts) and `python3 tools/validate.py` (must print OK).
4. Open a PR. CI runs the same validation.

## Custody definitions (the load-bearing column)

- **custodial**: the provider's wallet receives the buyer's funds first; the merchant is paid out later from a provider-held balance.
- **non-custodial**: funds settle to an address the merchant controls; the provider never holds a spendable balance.
- **self-hosted**: the merchant runs the software; custody is wherever the merchant points it.
- **hybrid**: genuinely depends on configuration (both modes are first-class, documented options).

A provider that advertises "non-custodial" but routes funds through provider-generated deposit addresses before payout is classified **custodial** (or **hybrid** if a true direct-settlement mode also exists). Classification follows the provider's own documentation, not its marketing. Disagreements are settled in an issue with links to the provider's docs.

## Vendors editing their own row

Welcome, with two conditions: say so in the PR ("I work for X"), and bring `source_url` evidence like everyone else. Self-serving reclassifications without documentation are closed.

## Corrections

Fees and terms change. If a row is stale, a PR with the new `source_url` beats an issue, but either is appreciated. The dataset is re-checked monthly; the `updated` date and `version` are bumped by the maintainers on release.
