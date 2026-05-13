# BDP jako warunkowy katalizator automatyzacji

**Od równowagi DSGE do wykonywalnego modelu SFC-ABM gospodarki polskiej**

Dedykowane repozytorium pracy MBA z Ekonomii Menedżerskiej.

Repo zawiera warstwę paperową i replikacyjną eksperymentu BDP. Nie zawiera pełnej kopii silnika `amor-fati`.

## Relacja do `amor-fati`

Silnik modelu znajduje sie w:

https://github.com/boombustgroup/amor-fati

Eksperyment BDP opiera sie na upstreamowym `amor-fati` z galezi `main` na commicie:

```text
base commit: 2d8b46e5064abef9d7a054317028843837b6e1c4
```

Kontrfaktyczny mechanizm BDP nie jest czescia bazowego modelu Polski. W tym repo jest zapisany jako patch:

```text
patches/amor-fati-bdp-scenario.patch
```

## Struktura

```text
.
├── docs/
│   └── mba-basic-income-sweep-plan.md
├── mc/
│   └── artefakty Monte Carlo uzyte przez skrypty wykresow
├── paper/
│   ├── Makefile
│   ├── analysis/
│   └── latex/
├── patches/
│   └── amor-fati-bdp-scenario.patch
├── scripts/
│   ├── run-central-sweep.sh
│   └── run-lambda-sweep.sh
└── README.md
```

## Budowa PDF

Z katalogu repo:

```bash
cd paper
make paper
```

`make paper` regeneruje wykresy z `../mc/`, a nastepnie buduje PDF przez `xelatex + bibtex`.

Wynik:

```text
paper/latex/esej_mba.pdf
```

## Replikacja eksperymentu modelowego

Minimalna sciezka:

```bash
git clone https://github.com/boombustgroup/amor-fati.git
cd amor-fati
git checkout 2d8b46e5
git apply ../amor-fati-bdp-mba-paper/patches/amor-fati-bdp-scenario.patch
sbt assembly
```

Nastepnie mozna uruchomic sweep centralny:

```bash
../amor-fati-bdp-mba-paper/scripts/run-central-sweep.sh
```

albo sweep odpornosci parametru `lambda`:

```bash
../amor-fati-bdp-mba-paper/scripts/run-lambda-sweep.sh
```

Skrypty zakladaja prace z katalogu glownego, spatchowanego repo `amor-fati` i uzywaja JAR-a:

```text
target/scala-3.8.2/amor-fati.jar
```

## Status danych

Katalog `mc/` zawiera artefakty Monte Carlo wykorzystane do obecnego draftu pracy:

- wariant centralny: 60 miesiecy, 10 seedow, `lambda=0.5`;
- sweep BDP: `0, 500, 1000, 1500, 2000, 2500, 3000` PLN na agenta HH;
- analiza odpornosci: `lambda = 0, 0.25, 0.5, 0.75, 1.0`.
