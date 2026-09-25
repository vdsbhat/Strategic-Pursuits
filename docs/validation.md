# Validation record

## Default-scope update

Opening and Reset filters now use All signals. Regression tests verify all 21,000 combinations and all five bands are available in the initial state. No input data or scoring rules changed.

## Version 2.2 validation

Current portfolio: 83 Very Strong, 2,665 Strong, 5,627 Moderate, 6,238 Emerging and 6,387 Not Prioritized. Analytics checks cover unchanged baseline, source demographics and footprints, deterministic generation, all bands and effective pipeline reconciliation. Client checks cover updated counts, filters, CSVs and the initially hidden explorer. Historical statements below refer to earlier versions.

26 Python tests and the JavaScript client checks passed. Browser verification confirmed: Overview initially hides the shortlist; the Explore these accounts action opens Account Explorer and retains All signals + Database (3,000 combinations); returning to Overview retains the same filters and hides the shortlist. Database has 16 Very Strong, 411 Strong, 801 Moderate, 887 Emerging and 885 Not Prioritized. The unfiltered All signals chart reconciles to 21,000. New Overview action and chart layout inspected at the current browser width; no JavaScript console errors observed. Version 2.1 backup ZIP and standalone HTML retained for rollback.

## Historical version 2.1 update

Added tests for enriched-input reconciliation, scenario coverage, all five bands, the Database upper-band examples, original baseline preservation, unchanged scores for unmodified accounts, KPI order and revised heading. Re-run automated tests against the current build. The detailed browser counts and 21,000-score original comparison below describe the previously validated 2.0 baseline, not the enriched 2.1 distribution. The original CSV hashes remain unchanged.


## Automated

- 21 Python unit tests: score bands and boundaries, scoring weights, rounding, deployment aggregation, modernization, classification precedence, normalization, analytical grain, rankings, pipeline reconciliation, AI & ML taxonomy, snapshot metrics and standalone assembly.
- JavaScript assertions: source decoding, scope, compound filters, multiple-band selection, account ID search, empty states, ordering, unique keys, pipeline totals, CSV limits, quoting and spreadsheet-formula escaping.
- Six source CSV SHA-256 hashes match the corresponding uploaded source files exactly.
- All 21,000 rebuilt scores compared with the uploaded analytical output. The 5,948 No Footprint rows increase by 7 points (10 whitespace points minus the incorrectly assigned 3 Cloud modernization points). All other scores are unchanged.
- Portfolio open pipeline reconciles to $9,081,615,878 across source Open opportunities.
- The original 534-row strategic output summed account-level pipeline to $2,547,807,108; the same rows contain $1,116,274,730 at the correct product grain. The corrected 624-row scope is different, so compare like-for-like before attributing total changes.

## Browser verification

- Desktop 1440×960 and mobile 390×844 layout inspection; no document-wide horizontal overflow on the mobile view. Wide detail tables scroll within their own container.
- Security + APAC + Whitespace returns 7 pursuits / 7 accounts.
- Nonmatching account search shows an empty state and disables export.
- All signals + Strong and Emerging bands returns 5,870 pursuits / 2,389 accounts.
- Product-chart click changes the product selector and filtered count; Security returns 127 strategic pursuits.
- Selecting a table row updates the detail panel; expanding evidence exposes account activity, product engagement and pipeline explanations.
- Export action reports 50 filtered, priority-ranked pursuits; CSV generation is separately verified by the client tests.
- Reset, Overview / Explorer / Methodology navigation and the source-audit panel verified. No JavaScript errors observed.

Direct file:// navigation was blocked by the browser automation policy. Interactive checks therefore used the same finished index.html through a local HTTP preview. Structural tests confirm the file embeds data, CSS and JavaScript and does not require external scripts or stylesheets. It is designed to open directly in a normal browser; no EXE, server or Python is required by its runtime.

These checks establish implementation behavior for the synthetic snapshot, not predictive accuracy or commercial impact.
