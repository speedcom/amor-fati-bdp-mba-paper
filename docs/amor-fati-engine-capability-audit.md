# Amor Fati engine capability audit for P1

Scope:

> This audit decides which P1 needs are genuine `amor-fati` engine capabilities, and which belong in `amor-fati-bdp-mba-paper` or a separate research repo. It deliberately excludes BDP-specific work from `amor-fati`, because BDP is a counterfactual scenario, not part of the Poland baseline represented by the engine.

Audited engine checkout:

- repo: `../amor-fati`
- commit: `2d8b46e5`

## Boundary rule

Create an `amor-fati` issue only when the artifact is reusable engine infrastructure:

- generic runtime/export support;
- generic Monte Carlo schema or terminal summary support;
- generic firm microdata or decision trace support;
- generic scenario/robustness support that does not encode BDP semantics;
- tests for those generic surfaces.

Do not create `amor-fati` issues for:

- BDP-specific SFC reconciliation;
- `BDP=0 == baseline`;
- BDP parameters, BDP sweeps, phase grids, or BDP interpretation;
- P1 literature, one-pager, abstract, figures, paper claims, or outreach;
- evidence indexing of already existing engine docs.

## Capability checklist

| Capability needed by P1 | Current `amor-fati` status | Evidence | Issue in `amor-fati`? | Decision |
| --- | --- | --- | --- | --- |
| Engine model documentation | Exists | `docs/odd-model-documentation.md`, `docs/behavioral-equations-and-decision-rules.md`, `docs/operations.md` | No | Use as pinned evidence from the paper repo. |
| SFC matrix evidence | Exists | `docs/sfc-matrix-evidence.md`, `docs/sfc-matrix-artifacts/*`, `SfcMatrixExport` | No | BDP-specific reconciliation belongs outside `amor-fati`. |
| Empirical validation infrastructure | Exists | `docs/empirical-validation-report.md`, `EmpiricalValidationExport`, baseline snapshot CSV | No | P1-specific validation tables belong outside `amor-fati`. |
| Calibration provenance | Exists | `docs/calibration-register.md`, `CalibrationRegisterExport` | No | P1 must classify calibration vs out-of-sample externally. |
| Scenario runner | Exists for named scenarios | `docs/scenario-registry.md`, `ScenarioRunExport`, `ScenarioRegistry` | Maybe | Only create an issue if we need a reusable parameter-grid/config-overlay runner. |
| Robustness runner | Exists for fixed scenario sets | `docs/sensitivity-robustness-workflow.md`, `SensitivityRobustnessExport` | Maybe | Good enough for engine-level local robustness; P1-specific MC design belongs outside. |
| Aggregate adoption metrics | Partially exists | `McTimeseriesSchema`: `TotalAdoption`, `AutoRatio`, `HybridRatio`, sector `*_Auto` | Yes | Add generic adoption/technology-finance diagnostics if needed by downstream work. |
| Aggregate financing metrics | Partially exists | `BankFirmLoansToGdp`, `CorpBondYield`, `CorpBondSpread`, `PrivateGrossInvestmentToGdp`, `CorpBondIssuance` | Maybe | Existing metrics cover much of the phase-screening surface; tech-specific loan/capex metrics are missing from CSV. |
| Terminal firm-size distribution | Exists, aggregate only | `_firms.csv`: `FirmSize_Micro`, `FirmSize_*Share` | No for aggregate; Yes for micro | Aggregate validation is present; CCDF/Gibrat requires micro snapshots. |
| Firm micro snapshot over time | Missing | Terminal `_firms.csv` is one aggregate row per seed; no per-firm rows. | Yes | Needed for firm-size CCDF, Gibrat-lite, adoption distribution. |
| Firm decision/adoption trace | Missing as export | `Firm.Decision` exists internally; `MonthTrace` is month-level, not per-firm decision trace. | Yes | Needed to avoid cherry-picked mechanism stories. |
| Upgrade failure diagnostics | Partially internal | `Decision.UpgradeFailed`, `BankruptReason.AiDebtTrap`, `Result.capexSpent/newLoan` exist internally. | Yes | Need generic counters/export, not BDP-specific interpretation. |
| Adoption by size/cash/debt quartile | Missing | No `Adoption_MicroShare`, `Adoption_CashQ*`, `Adoption_DebtQ*` in schema. | Yes | Could be derived from micro snapshots, but aggregate convenience metrics are useful. |
| Manifest/checksum packet | Mostly outside engine | Scenario/validation exports write metadata, but P1 needs experiment-level hashes. | No for now | Keep in paper/research repo unless generic engine output manifest becomes reusable need. |

## Proposed `amor-fati` issues

These are the only issue candidates that look justified in `amor-fati` after the audit.

### AF-1: Add generic firm micro snapshot export

Type: engine export capability.

Why it belongs in `amor-fati`:

> It exposes generic firm state, independent of BDP. It supports validation, Gibrat-lite, firm-size CCDF, adoption heterogeneity, and other future papers.

Output artifact:

- one CSV per Monte Carlo run, or one file per seed, with per-firm rows at selected months;
- configurable snapshot cadence: terminal-only, every N months, or explicit months.

Minimum columns:

- run id;
- seed;
- month;
- firm id;
- sector;
- region;
- size class;
- workers;
- tech state;
- bankruptcy reason if bankrupt;
- digital readiness;
- cash;
- firm loan;
- equity;
- bank id;
- risk profile;
- initial size;
- capital stock;
- inventory;
- green capital;
- foreign-owned flag;
- state-owned flag.

Done criteria:

- MC runner can emit firm snapshot CSV without changing baseline behavior when disabled;
- default local run remains cheap;
- tests cover header stability, row count, selected-month filtering, and alignment with terminal firm-size counts;
- docs mention the export in `docs/operations.md` or Monte Carlo docs only if the feature is added.

Non-goals:

- no BDP fields;
- no paper-specific pass/fail logic;
- no interpretation of adoption regimes.

### AF-2: Add generic firm decision/adoption trace export

Type: engine trace capability.

Why it belongs in `amor-fati`:

> Firm decisions already happen inside the engine, but the explanatory surface is not exported. A generic trace would make adoption, failure, downsizing, insolvency, and financing decisions auditable across scenarios.

Output artifact:

- sampled or filtered per-firm decision trace CSV/JSONL;
- supports deterministic selection by seed, firm id, stratum, or explicit sampling rule.

Minimum trace fields:

- run id;
- seed;
- month;
- firm id;
- opening tech state;
- closing tech state;
- decision type: survive, upsize, downsize, digi-invest, full-AI upgrade, hybrid upgrade, upgrade failed, bankrupt;
- bankruptcy reason if any;
- cash before/after;
- firm loan before/after;
- digital readiness before/after;
- workers before/after;
- capex;
- new loan;
- down payment if available;
- bank id;
- lending rate;
- bank approval flag where available;
- full-AI/hybrid feasibility flags if available;
- full-AI/hybrid adoption probabilities if available;
- random roll if recorded.

Done criteria:

- trace is disabled by default;
- enabling trace does not change decisions or random stream semantics;
- tests cover deterministic trace for a tiny run or controlled firm fixture;
- trace selection rule is explicit enough to prevent illustrative cherry-picking.

Non-goals:

- no BDP-specific trace labels;
- no paper-specific strata;
- no ex-post selection of firms inside the engine.

### AF-3: Add generic technology-adoption and financing diagnostics to Monte Carlo outputs

Type: schema/diagnostics capability.

Why it belongs in `amor-fati`:

> The engine already computes technology capex, technology imports, new firm loans, adoption ratios, and upgrade failures internally. Some of these are not exposed in the Monte Carlo CSV under stable diagnostic names.

Candidate monthly metrics:

- `Automation_TechCapex`;
- `Automation_TechImports`;
- `Automation_TechLoans`;
- `Automation_UpgradeFailures`;
- `Automation_AiDebtTrap`;
- `Automation_NewFullAi`;
- `Automation_NewHybrid`;
- `Adoption_MicroShare`;
- `Adoption_SmallShare`;
- `Adoption_MediumShare`;
- `Adoption_LargeShare`;
- `Adoption_CashQ1` / `Q2` / `Q3` / `Q4`;
- `Adoption_DebtQ1` / `Q2` / `Q3` / `Q4`.

Implementation note:

- `Automation_TechCapex` can likely reuse the current firm capex aggregate (`Firm.Result.capexSpent` -> `FirmEconomics` aggregate -> `MonthlyCalculus.firmCapex`), but the value is not currently a named MC column.
- `Automation_TechLoans` should be defined carefully because firm financing is split into equity, bonds, and bank loans.
- adoption-by-quartile metrics may be easier and less fragile if derived from AF-1 firm micro snapshots rather than emitted as core monthly columns.

Done criteria:

- schema columns are stable and tested in `McTimeseriesSchemaSpec`;
- output docs/validation manifests are updated only for generic engine metrics;
- metrics are defined without BDP semantics.

Non-goals:

- no phase-boundary classifier;
- no UBI/BDP wording;
- no paper-specific thresholds.

### AF-4: Optional generic parameter-grid or config-overlay runner

Type: optional diagnostics capability.

Current state:

- `ScenarioRunExport` supports named scenarios from `ScenarioRegistry`;
- `SensitivityRobustnessExport` supports fixed robustness scenario sets.

Open question:

> Is this enough for downstream research, or do we need a reusable runner that accepts a parameter grid without editing `ScenarioRegistry`?

Only create this issue if the paper/research repo cannot run the needed grids externally.

Allowed scope in `amor-fati`:

- generic parameter names;
- generic scenario provenance;
- no BDP-specific parameters;
- no paper-specific grid presets.

Done criteria:

- runs baseline plus parameter combinations with fixed seed bands;
- writes per-scenario metadata and deltas;
- rejects unknown or unsafe parameter paths clearly;
- tests cover parsing, provenance, and output layout.

## No-issue list

Do not create `amor-fati` issues for these items:

- "update ODD docs" unless AF-1/AF-2/AF-3 actually changes engine behavior;
- "create evidence index" because it belongs in this paper/research repo;
- "BDP-specific SFC reconciliation";
- "`BDP=0 == baseline`";
- "P1 Monte Carlo design note";
- "pre-registration table";
- "calibration vs out-of-sample manifest for P1";
- "phase diagram";
- "regime classifier";
- "literature map";
- "one-pager or abstract";
- "contact Prof. Safarzynska".

## Recommended next step

Create only three initial `amor-fati` issues:

1. AF-1 firm micro snapshot export.
2. AF-2 firm decision/adoption trace export.
3. AF-3 generic technology-adoption and financing diagnostics.

Keep AF-4 as a parking-lot issue or discussion until the paper repo proves that existing `ScenarioRunExport` and external scripts are insufficient.
