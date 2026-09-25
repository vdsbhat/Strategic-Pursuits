# Project 2 — review and improvements

## Version 2.2 update

At the user’s request, broader synthetic buying stages replace the 18 hand-selected examples. Scores still follow the original formula. See `scenario-design.md` for assumptions and limitations. Overview is now charts and summary only; Account Explorer holds the shortlist and evidence. Filters persist between views. Version 2.1 was saved separately for rollback.

## Historical version 2.1 update

At the user’s request, 18 curated synthetic scenarios populate the stronger bands while keeping all weights, thresholds, footprint states and account attributes unchanged. Four On-Premise examples target Very Strong; fourteen examples across all seven products target Strong. Account-wide activity uses an existing high-intent source profile; product engagement, competition and open pipeline are adjusted explicitly. This can also raise scores for other products belonging to those 18 accounts. These are demo scenarios, not independent evidence of model quality. Original source files remain unchanged. `data/effective/` and `data/demo-scenarios.json` provide the exact inputs and changes.

The earlier score-reconciliation statements below describe version 2.0 before enrichment.

## Retained

The uploaded project name, business question, seven product families, product/deployment separation, source data, seven fixed weights, score thresholds, modernization rules and broad pursuit categories remain. Project 1 has not been changed.

## Corrected

1. **Footprint aggregation:** The original fallback returned Cloud for explicit No Footprint records. All 5,948 source whitespace rows are now preserved. Mixed Cloud and On-Premise states resolve to Hybrid. For these No Footprint rows, the whitespace contribution increases by 10 and the mistaken Cloud modernization contribution decreases by 3: net +7 score points. Other source rows retain their original scoring calculation.
2. **Pipeline aggregation:** The original dashboard summed account-level open pipeline across account–product rows. The revised view sums open pipeline at the account–product grain, exactly once per visible combination. An account with multiple open product opportunities may still appear more than once; its different product amounts are not duplicates.
3. **Ranking consistency:** Original rank generation and display ordering differed. The build now ranks on score descending, product pipeline descending, account ID, then product name. Filters preserve global rank; pagination reports positions in the current view.
4. **Reproducibility and validation:** Source keys, ranges, account references, required account–product coverage and pipeline totals are checked before publishing. Original source CSVs are unchanged, with SHA-256 hashes recorded in the audit. Build logic has no third-party Python dependencies.

## Redesigned

Navy navigation rail, violet accents, separate overview/explorer/methodology views, interactive product and score charts, multiple signal-band selection, dependent account suggestions, detail-level evidence, empty states, mobile layout, keyboard focus styles and filtered CSV export. One self-contained HTML file replaces the EXE/Streamlit delivery path for this edition.

## Limitations deliberately not hidden

- Product engagement is supplied as a synthetic index. Raw product events do not exist in the upload, so we cannot honestly name the behaviors underlying that particular index.
- Account-level engagement includes channel and relative age but no unique event ID, person ID, absolute date or product family. We preserve all source records rather than inventing a deduplication rule.
- Product pipeline and account intent are normalized against portfolio extremes. These values can change when the portfolio changes; filtering does not recalculate them.
- Whitespace and modernization are partly mutually exclusive. A score of 100 is not achievable for every pursuit type. This, low normalized pipeline contributions and modest intent scores help explain the sparse upper bands.
- Competition may indicate displacement potential or risk. It is not evidence of positive intent by itself.
- Existing open pipeline is a reason to coordinate with the sales owner, not an incremental revenue estimate. Unlike Project 1's cross-sell eligibility, Project 2 deliberately includes existing pipeline and owned products.
- Source generation used correlated synthetic scenarios. Statistical model performance, sales outcomes and business uplift have not been validated.
- AI assisted the implementation and documentation. Users should describe their actual review and decision-making contribution honestly.

## Simple interview walkthrough

1. Explain the business question: which account and product should we investigate next, and why?
2. Show the current strategic-pursuit and unique-account counts, drawn from a 21,000-combination universe.
3. Click Whitespace and inspect the first result. Explain why the same account can have multiple pursuits.
4. Open the evidence panel, distinguish account-level intent from the synthetic product-engagement index, and explain weighted contributions.
5. Export a filtered top-50 list and emphasize human review and sales-owner coordination.
6. Open Methodology and explain the footprint/pipeline corrections. These analytical fixes are as important as the redesign.

## How this differs from Project 1

Project 1 is a cross-sell campaign shortlist with eligibility exclusions for already-owned products and open opportunities. Project 2 is a broader strategic-investigation view across whitespace, modernization, competitive activity and expansion, including existing product footprints and open pipeline. They should not be described as identical scoring models or directly comparable scores.
