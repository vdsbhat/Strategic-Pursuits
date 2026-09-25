# Strategic Pursuits
## AI-Assisted Account & Opportunity Intelligence

A self-contained analytics portfolio demo for investigating strategic account–product pursuits. All data is synthetic. This is Project 2; it is independent of the Account Growth Intelligence Workbench (Project 1).

## Open the demo

**Double-click `index.html`.** It contains the data, styles and application code. No Python, server, EXE, internet connection, API key or installation is required to view it. Enable JavaScript in your browser.

You may share **just `index.html`** for an offline demonstration. The full package includes the source data, analytical build, editable UI files, tests and documentation for portfolio review.

## Publish

Place `index.html` at the root of your GitHub Pages publishing folder, just as in Project 1. Upload the remaining files if you want interviewers to inspect the analytical implementation. The source folders are not needed to run the published demo. This package does not publish anything automatically and does not include the previous Windows executable workflows.

## What to explore

- Overview: summary and charts only. Click product bars, score bands or pursuit-type cards to filter the portfolio, then choose Explore these accounts. The Account Explorer preserves those filters and shows the detailed shortlist and evidence.
- Account Explorer: combine product, region, industry, pursuit-type and multiple signal-band filters. Search by account name or ID; matching account suggestions follow the other filters.
- Select an account–product row to see weighted contributions, a factual evidence brief and an inspection panel.
- Export the top 25, 50 or 100 currently matching rows. Export always ranks by priority score, even when the table is sorted differently.
- Methodology: review the calculation, assumptions, improvements and limitations.
- Strategic scope includes scores >=55. All signals includes the full analytical universe. All visible metrics and charts follow filters. Click an active chart filter again to clear it, or use Reset filters.

## Current synthetic demo snapshot (2.2)

3,000 synthetic accounts; 7 product families; 21,000 account–product combinations; 5,948 No Footprint records. Version 2.2 regenerates activity, product engagement, competition and open pipeline from deterministic buying-stage scenarios across the portfolio, without changing weights, thresholds, account demographics or product footprints. Stage assignments are illustrative demo assumptions, not observed customer behavior. The current distribution is 83 Very Strong, 2,665 Strong, 5,627 Moderate, 6,238 Emerging and 6,387 Not Prioritized: 8,375 strategic pursuits overall. See `data/audit.json` for current counts and `data/demo-scenarios.json` for the exact scenarios. Original CSVs remain intact in `data/source/`; the actual inputs used for scoring are also exported in `data/effective/`. All five bands have examples in All signals. All signals is the default when opening or resetting the dashboard. Switching to Strategic intentionally excludes scores below 55.

The revised effective portfolio contains $87,601,960,796 in open product pipeline before filters (see the build audit for exact current totals). These are synthetic, unweighted amounts—not incremental revenue, uplift or a forecast. USD is the inherited display assumption; the sources have no explicit currency column.

## Rebuild (optional)

Requires Python 3.10 or newer, standard library only:

```text
python build.py
python -m unittest discover -s tests -p "test_*.py"
node tests/test_client.cjs
```

Node is optional and needed only for the client tests. Edit source CSVs in `data/source/`, or UI files in `assets/`, then run `python build.py`. Do not edit the generated index if you intend to rebuild later. The fixed random seed makes scenario generation reproducible; identical inputs produce identical output.

## Files

```text
index.html                   Open or publish this standalone page
build.py                     Validated data preparation and scoring
demo_scenarios.py            Explicit, deterministic synthetic enrichment
assets/                      Editable HTML template, CSS and JavaScript
data/source/                 Six original source CSVs, unchanged
data/effective/              Actual enriched input CSVs used for scoring
data/demo-scenarios.json     Traceable synthetic scenario changes
data/account_product_scores.csv  Recomputed, ranked analytical output
data/audit.json               Counts, pipeline reconciliation and source hashes
tests/                       Analytics and client logic checks
docs/                        Methodology, improvements and interview notes
```

## Honest portfolio framing

This is an AI-assisted development project, not a trained AI recommendation engine. The runtime uses deterministic rules and template-generated briefs. Real-world predictive accuracy or revenue impact has not been established. See `docs/methodology.md` and `docs/review-notes.md` before presenting it.
