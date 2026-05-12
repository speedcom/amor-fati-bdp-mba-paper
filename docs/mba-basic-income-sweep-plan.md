# MBA Basic Income Sweep Plan

This file is the local research checklist for the MBA basic-income counterfactual
branch. It records the agreed scope before implementation so the experiment does
not collapse into one arbitrary policy point.

## Research Framing

The experiment tests a response surface, not a single forecast. The model should
compare baseline runs against a sweep of monthly basic-income transfers and
identify nonlinear thresholds in fiscal pressure, inflation, policy rates,
labor costs, firm stress, credit conditions, and automation adoption.

The result should be described as a conditional computational experiment:
given the implemented behavioral rules and fixed seed bands, how does the
Polish SFC-ABM economy react as the transfer level changes?

## Implementation Tasks

- Add `fiscal.basicIncomeMonthly`, defaulting to `PLN.Zero`.
- Add `fiscal.basicIncomeReservationWagePassThrough`, defaulting to zero.
- Keep `SimParams.defaults` baseline behavior unchanged.
- Extend household social transfers so monthly transfer income equals existing
  child benefit plus basic income.
- Route the transfer through the existing `GovSocialTransfer` mechanism so the
  BDP channel remains visible in budget, ledger, TFM, deficit, debt, demand, and
  SFC validation.
- Extend reservation-wage computation:

```text
reservationWage = minWage + lambda * basicIncomeMonthly
```

- Extend the normal jar entrypoint with a BDP parameter.
- Keep the sweep outside the model runtime: each BDP level is a separate jar
  invocation, and report comparison is handled by downstream scripts.

## Sweep Design

Initial coarse sweep:

```text
0, 500, 1000, 1500, 2000, 2500, 3000 PLN/month/household
```

Use the same seed band and duration for every point. Start with a cheap smoke
run, then use 60 months for the MBA experiment.

Recommended workflow:

1. Run coarse sweep every 500 PLN over 60 months.
2. Inspect threshold regions in inflation, rates, bankruptcies, and adoption.
3. Add local refinement every 250 PLN only around detected threshold ranges.

Production workflow:

```bash
sbt assembly
java -jar target/scala-3.8.2/amor-fati.jar 10 bdp-0000 --duration 60 --run-id bdp-0000-60m-10s --bdp 0
java -jar target/scala-3.8.2/amor-fati.jar 10 bdp-0500 --duration 60 --run-id bdp-0500-60m-10s --bdp 500
java -jar target/scala-3.8.2/amor-fati.jar 10 bdp-1000 --duration 60 --run-id bdp-1000-60m-10s --bdp 1000
java -jar target/scala-3.8.2/amor-fati.jar 10 bdp-1500 --duration 60 --run-id bdp-1500-60m-10s --bdp 1500
java -jar target/scala-3.8.2/amor-fati.jar 10 bdp-2000 --duration 60 --run-id bdp-2000-60m-10s --bdp 2000
java -jar target/scala-3.8.2/amor-fati.jar 10 bdp-2500 --duration 60 --run-id bdp-2500-60m-10s --bdp 2500
java -jar target/scala-3.8.2/amor-fati.jar 10 bdp-3000 --duration 60 --run-id bdp-3000-60m-10s --bdp 3000
```

Reservation-wage pass-through:

```text
central lambda = 0.5
robustness lambda = 0.0, 0.25, 0.5, 0.75, 1.0
```

The production jar accepts the BDP transfer level and, for robustness checks,
the reservation-wage pass-through. When `--bdp` is greater than zero and no
lambda is provided, `Main` applies the central reservation-wage pass-through
assumption `lambda = 0.5`; baseline runs keep the default zero-transfer
configuration.

```bash
java -jar target/scala-3.8.2/amor-fati.jar 10 bdp-2000-lambda-075 \
  --duration 60 --run-id bdp-2000-lambda-075-60m-10s --bdp 2000 --bdp-lambda 0.75
```

## Core Metrics

- Fiscal and macro: `Inflation`, `RefRate`, `BondYield`, `DeficitToGdp`,
  `DebtToGdp`, `GovDeficit`, `SocialTransferSpend`, `MonthlyGdpProxy`.
- Labor and households: `MarketWage`, `Unemployment`, `EffectivePitRate`,
  poverty and Gini terminal summaries if available.
- Firms and automation: `TotalAdoption`, `AutoRatio`, `HybridRatio`,
  `GrossInvestment`, `FirmDeaths`, `FirmBirths`, `LivingFirmCount`.
- Banking and credit: `CreditToGdpGap`, `NPL`, `MinBankCAR`, `MinBankLCR`,
  `MaxBankNPL`.
- External channel: `CurrentAccount`, `ExRate`, `TotalImports_OE`.
- Accounting: runtime ledger status, 15 SFC identities, and SFC matrix evidence
  after representative runs.

## Documentation Tasks

- Update behavioral rules to show `socialTransfer_h = children * social800 +
  basicIncomeMonthly`.
- Update fiscal/reservation-wage rule documentation, including the `Main`
  default that BDP runs use `lambda = 0.5` unless `--bdp-lambda` is provided.
- Document the jar-level BDP parameter in operations notes.
- Update calibration/provenance docs so the BDP parameters are explicit policy
  scenario parameters, not empirical baseline calibration.
- In the MBA paper, frame IMF DSGE as answering the equilibrium
  efficiency/equity question, while Amor Fati answers the transition-path and
  heterogeneity question.

## Verification Tasks

- Add unit tests for zero-baseline behavior.
- Add unit tests for household social transfer with basic income.
- Add unit tests for reservation-wage pass-through.
- Add CLI parser tests for the BDP parameter.
- Run focused tests first, then `sbt test` if runtime is acceptable.
- Run a 60-month scenario comparison with fixed seed(s).
- Run each BDP level as a separate jar invocation and archive outputs under
  `mc/`.
