# TRL-gated AI/HPC governance — reproducibility package

**Manuscript:** JIAE-D-26-00545 — A TRL-Gated AI/HPC Governance Model for Entrepreneurial University Transformation: Longitudinal Evidence from Pakistan. Namal University, 2019–2025. **Version 1.1.0 (26 November 2026).**

## Scope and evidence
This release reproduces the reported historical aggregate counts and descriptive comparisons, and documents operational clarifications supplied by centre management during manuscript revision. It separates four kinds of material:

1. **Historical administrative aggregates (2019–2025):** 50 problem cases, 30 dataset-enabled cases, 12 laboratory-tested prototypes, five field-tested prototypes, 1,450 training participations and 185,377 completed jobs. Five relative to 50 equals 10%; the complementary 90% is a reported aggregate non-progression indicator under the nested-stage assumption, not a measured abandonment rate. Three named emerging venture pathways are reported separately; no field-to-venture conversion is calculated.
2. **Management-reported operational context (clarified 26 November 2026):** PIA/MoU gate process, partner acceptance, project-specific testing, delays, stakeholder feedback (approximately 200 interactions, approximately 100 recorded), workload-demand explanations and approximate 2025 operating-cost coverage (70% income-generating activities, 30% NEF support). These are attributed accounts, not independently coded interviews, verified ledger results or a new dataset of observed project milestones.
3. **Later portfolio context (2023–22 November 2026):** 50 PoC initiatives, 20 MVP candidates and six pre-CVPs, plus other provisional dashboard metrics. This window is not substituted for the 2019–2025 counts.
4. **Prospective methods and blank templates:** gate review, independent classification audit, stakeholder evidence inventory, monthly scheduler accounting and financial reconciliation. These are tools, not completed observations.

## Reproduce
Python 3.10+; standard library only. From repository root:

```bash
python3 scripts/verify.py
python3 scripts/reproduce.py
python3 -m unittest discover -s tests -v
python3 scripts/verify.py
```

Outputs: `results/summary.json`, `results/funnel.csv`, `results/funnel.svg`, `results/hpc_yearly_changes.csv`, `results/legacy_accounting_changes.csv`. The legacy mixed CPU/GPU series is isolated for traceability; no physical utilization, normalization, or workload intensity is inferred. Only recorded users, completed jobs and jobs per reported user are used for the main HPC comparisons. All generated files are deterministic.

## Repository map
- `data/annual_*.csv`: historical reported aggregates (unchanged from v1.0.0).
- `data/management_clarifications/`: attributed, aggregate-only operational and financing context, excluded from historical calculations.
- `data/context_2026/`: later dashboard context; `data/post_study_dataset_index.csv`: later dataset releases.
- `data/claim_evidence_matrix.csv`, `data/revision_issue_register.csv`: evidence scope and revision alignment.
- `docs/`: counting rules, operational governance, evidence provenance, independent-review protocol and release checks.
- `templates/`: unfilled forms, not study records.
- `scripts/`, `tests/`, `.github/workflows/`: deterministic calculations and CI; `MANIFEST.json` and `SHA256SUMS.txt`: release integrity.

## Publication and citation
The private source archive, reviewer correspondence, manuscript drafts, internal workbooks, recordings, agreements and financial ledgers must not be uploaded. Confirm institutional authorization and reuse terms before public release. Cite the repository's immutable version tag or commit alongside the manuscript; add the DOI when assigned. The GitHub destination is to be selected by the repository owner. See `LICENSE.md` and `docs/RELEASE_CHECKLIST.md`.

Related resources: https://github.com/ucerd and https://github.com/ucerd/peerj-hpc-reproducibility. These contextual resources do not independently validate the historical case-level outcomes.
