# Version 2.2 — broader synthetic buying stages

This revision is an illustrative demo design, not an estimate of a real sales portfolio. No weights, thresholds, account demographics, product footprints or product taxonomy were changed. The original six CSVs remain in `data/source/`; current scoring uses `data/effective/`.

## Generation assumptions

Fixed seed: 20260924. Account stages are drawn from Quiet 22%, Exploring 33%, Evaluating 34%, Advanced evaluation 11%. To include high-end enterprise examples, accounts with fit >=94 have a 65% chance of being assigned advanced evaluation before the remaining stage draw. This deliberate sampling overrepresents engaged high-fit accounts; it is not a learned relationship.

Account activity varies from 3–10 older records for Quiet to 26–28 recent records for Advanced evaluation. High-fit advanced examples use 28 records aged 1–6 relative days. Channels are drawn from the existing taxonomy. Activity is account-wide, not evidence of individual people or product-specific events.

Product stages are correlated but not identical to account stages. Quiet accounts mostly have Quiet products; Evaluating accounts mostly have Evaluating products. Each stage can contain other stages. High-fit On-Premise examples have an 85% chance of an advanced product scenario. This produces late-stage modernization examples while retaining the original footprint.

| Product stage | Engagement index | Competitor-record probability | Intensity when present | Open-pipeline probability | Amount as fraction of $15.5M |
|---|---|---|---|---|---|
| Quiet | 10–42 | 15% | 10–40 | 5% | 0.005–0.05 |
| Exploring | 45–73 | 45% | 35–67 | 28% | 0.04–0.22 |
| Evaluating | 76–94 | 78% | 68–93 | 75% | 0.22–0.72 |
| Advanced evaluation | 97–100 | 97% | 97–100 | 97% | 0.94–1.00 |

These strong correlations and large late-stage deal amounts are demonstration assumptions chosen to make upper score bands inspectable. They should not be described as statistically validated buying behavior. Existing non-open opportunities are preserved; original Open rows are replaced, not added on top. Competitor and product-engagement inputs are regenerated. Since intent and pipeline are normalized across the effective portfolio, every score is rebuilt.

## Resulting distribution

| Band | Count | Share of 21,000 |
|---|---:|---:|
| Very Strong | 83 | 0.4% |
| Strong | 2,665 | 12.7% |
| Moderate | 5,627 | 26.8% |
| Emerging | 6,238 | 29.7% |
| Not Prioritized | 6,387 | 30.4% |

Strategic scope contains 8,375 combinations (score >=55); maximum score 87.6. Full effective open pipeline is $87,601,960,796. This total is synthetic and intentionally different from earlier editions; it is not a revenue forecast or an increase achieved by the project.

The very strongest scores remain rare because whitespace and modernization cannot both contribute their maximum, and only certain deployment/fit combinations can reach 85 under the unchanged scoring formula. Narrow filters can still leave a band empty. Select All signals to see all five bands; Strategic scope intentionally hides scores below 55.

## Interface change and rollback

Overview now contains summary cards and charts only. Account Explorer contains the shortlist, exports and account evidence. Region, industry, product, band and scope filters carry across both views. The Overview action “Explore these accounts” opens the currently filtered shortlist.

The version 2.1 ZIP and standalone HTML were saved alongside this package in the deliverables directory before making this revision. Restore that ZIP to roll back both data and interface; the original source CSVs have also been preserved here.
