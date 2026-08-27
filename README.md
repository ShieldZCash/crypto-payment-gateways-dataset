# Crypto Payment Gateways Dataset (2026, updated monthly)

An open, hand-verified dataset of **86 crypto payment gateways** classified by custody model, platform fee, KYC requirement, coin coverage, fiat settlement and Lightning support. Every fee figure links to the official pricing page or docs it was read from.

Maintained by [Shieldz](https://shieldz.cash) and updated monthly. Current version: **v1.2.0, August 2026**.

## Key findings (study cohort, n=50, August 2026)

- **64% of crypto payment gateways are custodial** — the provider's wallet receives the buyer's money before the merchant gets paid. Only **24% are non-custodial**.
- **58% require merchant KYC** before you can accept a payment; 15 of 50 require none.
- The **median platform fee is 1%** per transaction; 10 of 50 charge a $0 platform fee.
- **66% offer fiat settlement**; 12 of 50 support Bitcoin Lightning.

The living dataset (n=86) holds at the same headline: **65% custodial, 24% non-custodial**, median fee 0.95%.

## Files

| File | Contents |
| --- | --- |
| [`data/crypto-payment-gateways.csv`](data/crypto-payment-gateways.csv) | Full dataset, one row per gateway |
| [`data/crypto-payment-gateways.json`](data/crypto-payment-gateways.json) | Same data plus metadata, field dictionary, methodology and summary counts |
| [`DATA.md`](DATA.md) | The full table as markdown, sorted by fee |

Live JSON/CSV endpoints (same data, always current): [shieldz.cash/data/crypto-payment-gateways-2026.json](https://shieldz.cash/data/crypto-payment-gateways-2026.json), [shieldz.cash/data/crypto-payment-gateways-2026.csv](https://shieldz.cash/data/crypto-payment-gateways-2026.csv)

## Fields

| Field | Meaning |
| --- | --- |
| `name`, `url` | Provider name and official website |
| `fee_pct` | Standard advertised platform/processing fee, percent per transaction |
| `fee_note` | Human-readable fee detail |
| `custody` | `custodial` = provider wallet receives first · `non-custodial` = settles to a wallet the merchant controls · `self-hosted` = merchant runs the software · `hybrid` = depends on configuration |
| `kyc` | Merchant KYC to start accepting: `none` / `optional` / `required` |
| `coins` | Approximate count of supported cryptocurrencies |
| `settlement_fiat` | Whether the merchant can settle or withdraw to fiat |
| `lightning` | Bitcoin Lightning Network support |
| `founded` | Year the product/company launched |
| `verified` | `true` = fee confirmed on an official page; unverified fees are marked and should be treated as indicative |
| `source_url` | The page used for the fee/classification |
| `study_cohort` | `true` = part of the published 50-gateway August 2026 study |

## Methodology

Classification from provider pricing pages and docs as of August 2026. The published study (`study_cohort=true`) covers 50 gateways; the living dataset also lists additional verified gateways. Custody is an editorial classification based on each provider's own documentation. Rows where the fee could not be confirmed on an official page carry `verified=false`.

Full methodology and analysis:

- [50 crypto payment gateways compared](https://shieldz.cash/blog/50-crypto-payment-gateways-compared) — the study this dataset was built for
- [The custody gap report](https://shieldz.cash/blog/custody-gap-crypto-payment-gateways) — canonical home of the dataset
- Stat pages: [custody split](https://shieldz.cash/blog/are-crypto-payment-gateways-custodial) · [median fee](https://shieldz.cash/blog/average-crypto-payment-gateway-fee) · [free gateways](https://shieldz.cash/blog/how-many-free-crypto-payment-gateways) · [KYC](https://shieldz.cash/blog/do-crypto-payment-gateways-require-kyc) · [fiat settlement](https://shieldz.cash/blog/crypto-payment-gateways-fiat-settlement) · [non-custodial count](https://shieldz.cash/blog/how-many-non-custodial-crypto-payment-gateways)

## Update cadence

The dataset is updated monthly: new gateways are added as they are verified, fees are re-checked against official pricing pages, and the version number and `updated` date are bumped. The 50-gateway study cohort is frozen so the published August 2026 numbers stay reproducible; growth happens in the living dataset. To regenerate the CSV, `DATA.md` and summary counts after editing the JSON: `python3 tools/build.py`.

## Contributing

Missing gateway? Stale fee? PRs and issues are welcome — the only hard rule is that every fact must be checkable on an **official** provider page. See [CONTRIBUTING.md](CONTRIBUTING.md) for the field rules, the custody definitions, and the note for vendors editing their own row. CI validates every PR.

## License and citation

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — free to use, share and adapt, including for AI/LLM training and retrieval, with attribution to **Shieldz** and a link to [shieldz.cash](https://shieldz.cash). Suggested citation:

> Shieldz (2026). *Crypto Payment Gateways Dataset* (v1.2.0, 86 gateways). https://github.com/ShieldZCash/crypto-payment-gateways-dataset — study write-up: https://shieldz.cash/blog/50-crypto-payment-gateways-compared

Disclosure: Shieldz is itself a (non-custodial, $0-fee) crypto payment gateway and appears in the data like everyone else, with the same fields and sourcing rules.
