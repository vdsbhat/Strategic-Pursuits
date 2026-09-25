# Scoring methodology — build 2.2

Grain: one account × product-family row. Universe: all seven products for each supplied account. Original source CSVs are unchanged from the upload. Before scoring, version 2.2 applies documented buying-stage scenarios across the full portfolio in `demo_scenarios.py`. Effective input CSVs and the manifest are supplied. Weights and thresholds are unchanged; account activity, product engagement, competition and open pipeline inputs are regenerated while demographics, footprints and non-open opportunities are preserved. This intentionally increases upper-band coverage and must not be presented as observed customer behavior or validation of the model.

| Signal | Maximum contribution | Calculation |
|---|---:|---|
| Customer fit | 20 | Revenue score ×40% + employee score ×30% + industry score ×30%, then ×20% |
| Customer intent | 20 | 70% normalized age-weighted account activity +30% normalized event count, then ×20% |
| Product engagement | 15 | Supplied synthetic product index ×15% |
| Product whitespace | 10 | 100 if No Footprint, otherwise 0; then ×10% |
| Modernization | 15 | Deployment/engagement rule, then ×15% |
| Competitive intensity | 10 | Maximum recorded intensity for account/product ×10% |
| Product pipeline | 10 | Normalized open account/product amount ×10% |

Fit revenue scores: >=$5B:100; >=$1B:85; >=$500M:65; otherwise45. Employee scores: >=25,000:100; >=10,000:85; >=5,000:65; otherwise45. Target industries score100; other industries55. Targets: Manufacturing, Financial Services, Telecommunications, Healthcare, Energy. Currency display assumes USD.

Intent age multiplier: max(0.2, 1 − days_ago/365 × 0.8). All provided source event records are counted. Min–max normalization = (x−minimum)/(maximum−minimum) ×100; a constant series receives0. Normalization is fixed at build time over the entire portfolio. Account intent is shared across products.

Modernization: On-Premise with engagement>=60 receives85; other On-Premise55; Hybrid65; Cloud20; No Footprint0.

Sum unrounded weighted contributions; scale by ten, round ties to even, then divide by ten, following the original pandas one-decimal rounding convention. Displayed component rounding may sum slightly differently. Bands use the rounded total: >=85 Very Strong; >=70 Strong; >=55 Moderate; >=40 Emerging; otherwise Not Prioritized. Strategic shortlist threshold55.

Pursuit classification, in precedence order: No Footprint → Whitespace; modernization>=65 → Modernization; competition>=60 → Competitive; otherwise Expansion. A classification is a proposed investigation angle, not proven buyer need.

Only Open opportunities contribute pipeline. Won/Lost/Closed and the original arbitrary 75% weighted_amount are not used. Competition without a record contributes0; absence of a record does not prove absence of competition. The supplied snapshot has complete footprint and product-engagement coverage. Missing required account–product rows cause a build failure, rather than silently creating confident recommendations.

## Validation before real-world use

Replace synthetic inputs with governed sources and explicit snapshot dates, currency, lineage and missingness. Establish event identity before deduplication. Reassess the meaning of fit, competition and pipeline by pursuit type. Evaluate overlap between signals and min–max outlier sensitivity. Compare top-N ranking quality with simple baselines using time-separated historical outcomes and account-owner review. Do not equate prioritization with causal uplift.
