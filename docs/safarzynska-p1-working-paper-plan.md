# Plan P1: working-paper-grade package przed kontaktem z prof. Karolina Safarzynska

Decyzja: rezygnujemy z polsrodkow typu P0/P0+. Przed pierwszym kontaktem przygotowujemy pakiet, ktory moze byc zalazkiem working paperu, a nie tylko zaproszeniem do rozmowy o narzedziu.

Rdzen programu:

> BDP/UBI + automatyzacja + heterogeniczna adopcja technologii + ograniczenia bilansowe firm + phase diagram + pattern-oriented validation.

Nie robimy jako glownego tematu:

- zielonej transformacji;
- energy/CO2 accounting;
- climate tipping;
- generycznego RL;
- samego paperu o ledgerze.

## 1. Cel P1

Przygotowac pakiet, ktory odpowiada na pytanie:

> Czy w SFC-ABM-ie z heterogenicznymi firmami, bankami i ograniczeniami finansowania BDP/UBI ma niemonotoniczny wplyw na adopcje automatyzacji, oraz czy granica miedzy rezimem accelerating-automation i suppressed-automation jest widoczna jako phase boundary w przestrzeni polityka x finansowanie?

Pakiet ma zawierac:

- dzialajacy, replikowalny 2D phase diagram;
- mikro- lub semimikro-metryki adopcji firm;
- pattern-oriented validation suite;
- 1-stronicowa dokumentacje mechanizmu adopcji firm;
- mape literatury;
- one-pager;
- szkic abstractu i struktury paperu;
- README reprodukujace glowne figury.

## 2. Roboczy paper

Roboczy tytul:

> A non-monotonic effect of UBI on automation: phase diagram of finance-constrained adoption in a verified SFC-ABM

Alternatywy:

> Universal basic income and automation: emergent adoption regimes under firm balance-sheet constraints

> Policy-induced technological transition: when UBI accelerates or suppresses automation in a stock-flow consistent agent-based economy

Glowna teza:

> UBI nie dziala jako liniowy akcelerator automatyzacji. Przy umiarkowanym transferze kanal popytowo-kosztowy zwieksza presje substytucji pracy kapitalem, ale przy wysokim transferze kanal fiskalno-finansowy pogarsza koszt i dostepnosc finansowania CapEx, przez co adopcja automatyzacji slabnie.

Scientific claim:

> Model generuje odrebne rezimy adopcji technologii w przestrzeni UBI generosity x financing constraint. Przejscie miedzy rezimami jest nieliniowe i wynika z interakcji heterogenicznych bilansow firm, kosztu pracy, popytu i finansowania.

Engineering credibility:

> `amor-fati` jest wykonywalnym SFC-ABM z runtime SFC checks i formalnie weryfikowanymi wybranymi wlasnosciami ledgera. To jest fundament wiarygodnosci eksperymentu, ale nie headline naukowy.

### 2.1. Odpowiedz na pytanie: skad wiemy, ze tool dziala?

To pytanie trzeba potraktowac jako centralny gate metodologiczny, nie jako defensywna uwage techniczna.

Krotka odpowiedz dla prof. Safarzynskiej:

> Nie wiemy tego z samego faktu, ze model sie uruchamia. Budujemy lancuch dowodowy: testy implementacji, runtime SFC checks, artefakty macierzy SFC, deterministyczna replikacja, trace mechanizmu adopcji firm, pattern-oriented validation oraz sensitivity/ablation checks. To nie dowodzi, ze model jest prognoza Polski. Dowodzi, ze eksperyment z BDP (bezwarunkowym dochodem podstawowym) jest wykonywalny, ksiegowo spojny, replikowalny i falsyfikowalny w zakresie zadeklarowanych przed runami patternow i ablacji.

Centralnym artefaktem ma byc evidence map, ktora rozdziela gotowa wiarygodnosc silnika od dowodow specyficznych dla P1:

| Pytanie metodologiczne | Pokryte juz przez engine docs | Nowe dowody P1 |
| --- | --- | --- |
| Co to jest model i jakie ma encje/decyzje? | `../amor-fati/docs/odd-model-documentation.md`, `../amor-fati/docs/behavioral-equations-and-decision-rules.md` | 1-stronicowy opis tylko mechanizmu UBI/adoption/financing |
| Czy przeplywy zachowuja SFC? | `../amor-fati/docs/sfc-matrix-evidence.md`, `../amor-fati/docs/sfc-matrix-artifacts/*` | BDP-specific SFC reconciliation dla `BDP=0` i co najmniej jednego dodatniego BDP |
| Czy model ma jawna kalibracje? | `../amor-fati/docs/calibration-register.md` | manifest: ktore patterny byly uzyte do kalibracji, a ktore sa out-of-sample validation |
| Czy model ma empiryczne punkty odniesienia? | `../amor-fati/docs/empirical-validation-report.md`, manifesty i baseline snapshot | P1 pattern table dla firm, adopcji, finansowania i bankructw |
| Czy wyniki sa stabilne? | `../amor-fati/docs/sensitivity-robustness-workflow.md` | P1 Monte Carlo design, phase-grid seed envelopes, sign-stability metrics |
| Czy da sie to uruchomic ponownie? | `../amor-fati/docs/operations.md` | `manifest.json`, `checksums.txt`, README reprodukcji P1, pinowany JAR/commit |

Warstwy wiarygodnosci:

1. [engine + P1] Poprawnosc obliczeniowa:
   - projekt kompiluje sie z pinowanym commitem;
   - testy jednostkowe i regresyjne dla BDP, transferow, parsera CLI, kanalow kosztu pracy i finansowania przechodza;
   - `BDP=0` jest regression/consistency check: powinien odtwarzac baseline bit-identical albo miec jawnie udokumentowany, akceptowany diff;
   - seed daje deterministyczny wynik;
   - runtime kontrakty lapia nielegalne stany: ujemne przeplywy tam, gdzie sa niedozwolone, naruszenia indeksow, przelewy bez przeciwstrony, overflow/range errors.

2. [engine + P1] Poprawnosc ksiegowa SFC:
   - kazdy transfer BDP jest ksiegowany po obu stronach: wydatek rzadu, dochod gospodarstw, finansowanie deficytu/dlugu;
   - runtime ledger zatrzymuje symulacje przy naruszeniu bilansu;
   - dla wybranych seedow publikujemy SFC reconciliation: expected, actual, residual, status;
   - macierze SFC sa rekoncyliowane miedzy symbolicznym BSM/TFM a wykonanym runtime; znane diagnostic exceptions sa wymienione w `sfc-matrix-evidence.md`, a nie uzywane jako ukryte balancing rows;
   - P1 musi pokazac osobno reconciliation dla baseline oraz dodatniego scenariusza BDP.

3. [P1] Trace mechanizmu:
   - firmy do trace wybieramy wedlug z gory zadeklarowanej reguly, nie jako ilustracyjne przypadki po fakcie;
   - minimalna stratyfikacja: adopter, non-adopter, failed upgrade, early adopter, late adopter, high-debt firm, high-cash firm;
   - w kazdej warstwie firma jest losowana z ustalonego seed/run albo wybierana przez jawny percentyl metryki, np. debt/cash/readiness;
   - trace musi pokazywac cash, debt, digital readiness, koszt CapEx, bank approval, wage pressure, adoption probability, final state;
   - jesli firma adoptuje, w danych musi byc widac jednoczesnie zmiane tech state, cash/debt, tech CapEx, loan demand i labor demand;
   - jesli upgrade fails, w danych musi byc widac koszt porazki i ewentualne bankructwo.

4. [engine + P1] Replikowalnosc:
   - README zawiera dokladne komendy, commit modelu, commit repo paperu, wersje JDK/SBT/Scala, seedy i parametry;
   - `manifest.json` zawiera commit `amor-fati`, commit repo paperu, hash JAR-a, hash wejsc/CSV/figur, wersje dokumentow z `../amor-fati/docs`;
   - surowe CSV, figury i agregaty maja `checksums.txt`;
   - jedna komenda reprodukuje glowne figury z dostarczonych CSV;
   - druga sciezka, jesli runtime jest dostepny, odtwarza CSV z pinowanego JAR-a.

5. [P1] Pattern-oriented validation:
   - model nie jest oceniany tylko przez jeden headline result;
   - przed runami powstaje tabela pre-registration dla patternow: pattern, metryka, oczekiwany kierunek lub zakres, prog pass/fail, status `declared-before-run` albo `post-hoc`;
   - sprawdzamy firm-size distribution, Gibrat-lite, adoption distribution, default clustering i/lub volatility clustering;
   - `pass` oznacza przekroczenie zadeklarowanego progu; `fail` ogranicza claim paperu; `diagnostic` oznacza wynik mieszany wzgledem pre-registered progu i nie moze byc liczony jako wsparcie glownej tezy;
   - patterny uzyte do kalibracji sa oznaczane jako calibration checks, nie jako out-of-sample validation.

6. [P1] Sensitivity, Monte Carlo i ablation:
   - P1 ma osobna Monte Carlo design note: liczba seedow, horyzont, czy jest burn-in, headline statistic, obsluga outlierow i sposob raportowania envelopes;
   - roboczo: screening osi finansowania moze uzywac 3 seedow, full grid 10-20 seedow, a komorki graniczne lub headline robustness 30+ seedow, jesli koszt obliczeniowy pozwala;
   - burn-in domyslnie nie jest stosowany, bo eksperyment startuje ze skalibrowanego snapshotu Polski; pierwsze 12 miesiecy mozna raportowac osobno jako transition period;
   - headline effect raportujemy jako delta wzgledem baseline oraz stabilnosc znaku, np. udzial seedow z oczekiwanym znakiem; roboczy prog dla headline/boundary cells: znak stabilny w co najmniej 80% seedow;
   - wylaczenie albo oslabienie kanalu finansowego powinno oslabic finance-constrained/suppressed automation;
   - podniesienie kosztu CapEx lub spreadu powinno poruszyc adopcje w przewidywanym kierunku;
   - jesli ablation nie dziala zgodnie z pre-registered kierunkiem, nie ma paperu o tym mechanizmie, tylko debug mechanizmu.

Minimalny artefakt "tool-validity packet" przed kontaktem:

- evidence map: `already covered by engine docs` kontra `new evidence produced for this paper`;
- tabela pre-registration dla pattern-oriented validation i ablations;
- P1 Monte Carlo design note;
- calibration/validation separation manifest: patterny kalibracyjne, out-of-sample validation, diagnostic-only;
- log testow albo lista test suites i status;
- BDP-specific SFC reconciliation dla baseline i jednego dodatniego scenariusza BDP;
- trace adopcji, non-adoption i failed upgrade wedlug zadeklarowanej reguly doboru firm;
- `manifest.json` z commitami, hashami JAR/CSV/figur i wersjami dokumentow;
- README reprodukcji;
- `checksums.txt` surowych CSV i figur;
- tabela pattern-oriented validation: pass/fail/diagnostic z progami;
- tabela sensitivity/ablation: co zmieniono, czego oczekiwano, co wyszlo.

Granica repo dla ticketow:

> `amor-fati` reprezentuje baseline gospodarki polskiej na stan 2026-04-30 oraz generyczna infrastrukture SFC-ABM. BDP nie jest standardowym elementem Polski w baseline, tylko kontrfaktycznym scenariuszem tego repozytorium. Dlatego BDP-specific SFC reconciliation, `BDP=0 == baseline`, sweepy BDP, phase diagramy i interpretacja wynikow nie powinny byc ticketami produktowymi w `amor-fati`.

Do `amor-fati` moga isc tylko generyczne capabilities potrzebne wielu scenariuszom:

- mikroeksport firm bez odniesienia do BDP;
- generyczny trace decyzji/adopcji firm;
- generyczne metryki adopcji technologii i finansowania firm;
- generyczne mechanizmy scenario override / parameter sweep, jesli nie koduja BDP jako standardowej polityki;
- generyczne eksporty SFC reconciliation dla dowolnego scenariusza;
- dokumentacja silnika: ODD, behavioral rules, calibration register, operations, SFC evidence.

Do `amor-fati-bdp-mba-paper` albo nowego repo badawczego ida:

- BDP-specific SFC reconciliation;
- regression check `BDP=0 == baseline`;
- parametry BDP, seedy, sweepy i phase grid;
- pattern-oriented validation specyficzne dla paperu UBI/adoption;
- ablations kanalu finansowania w kontekscie BDP;
- figury, interpretacja, literature map, one-pager, abstract i kontakt z prof. Safarzynska.

Granica claimu:

> Ten pakiet nie dowodzi, ze swiat dziala tak jak model. Dowodzi, ze narzedzie nie jest arbitralnym generatorem wykresow: zachowuje ksiegowosc, ma jawny mechanizm, daje sie powtorzyc, przechodzi lub oblewa zewnetrzne patterny i reaguje na ablations zgodnie z deklarowanym kanalem przyczynowym.

## 3. Workstream A: metryki i mikroeksport

Cel:

> Wyjsc poza agregat `TotalAdoption` i pokazac, kto adoptuje technologie.

Minimalne metryki terminalne:

- `Adoption_MicroShare`
- `Adoption_SmallShare`
- `Adoption_MediumShare`
- `Adoption_LargeShare`
- `Adoption_BySector_*`
- `Adoption_CashQ1` / `Q2` / `Q3` / `Q4`
- `Adoption_DebtQ1` / `Q2` / `Q3` / `Q4`
- `Automation_TechCapex`
- `Automation_TechLoans`
- `Automation_UpgradeFailures`
- `Automation_AiDebtTrap`

Mikro snapshot firm, najlepiej co 12 miesiecy i w terminalu:

- run id;
- seed;
- month;
- firm id;
- sector;
- size class;
- workers;
- tech state: traditional, hybrid, automated, bankrupt;
- digital readiness;
- cash;
- firm loan;
- bank id;
- risk profile;
- flag: newly adopted this period;
- flag: failed upgrade;
- bankruptcy reason.

Decyzja techniczna:

> Paper 1 jest paperem o firmach, adopcji technologii i finansowaniu. HH snapshot nie wchodzi do scope paperu 1. Wraca dopiero w paperze dystrybucyjnym albo P2.

## 4. Workstream B: phase diagram

Cel:

> Zbudowac 2D phase diagram dla UBI/BDP x financing constraint.

Os X:

- BDP/UBI level: `0, 500, 1000, 1500, 2000, 2500, 3000`.

Os Y do przetestowania:

- `banking.baseSpread`;
- `corpBond.spread`;
- `firm.aiCapex` / `firm.hybridCapex`;
- wariant CAR / `bankCanLend`, jesli da sie kontrolowac bez posrednich artefaktow.

Najpierw robimy mini-screening osi Y:

- 7 poziomow BDP x 3 poziomy parametru x 3 seedy;
- horyzont 60 miesiecy;
- metryki: `TotalAdoption`, `PrivateGrossInvestmentToGdp`, `CorpBondYield`, `BankFirmLoansToGdp`, tech CapEx, tech loan demand.

Hard-gate wyboru osi Y:

> Os Y zostaje wybrana tylko wtedy, gdy miedzy minimum i maksimum parametru przy ustalonym BDP, np. `1500` albo `2000`, widac ekonomicznie istotna roznice w `TotalAdoption` po 60 miesiacach i kierunek efektu jest stabilny w co najmniej 2 z 3 seedow.

Roboczy prog:

- co najmniej 3-5 punktow procentowych roznicy w `TotalAdoption`, albo
- mniejsza roznica w adopcji, ale jednoznaczna roznica w tech CapEx / tech loan demand / inwestycjach prywatnych.

Jesli zadna os Y nie przejdzie tego gate'u:

> Nie idziemy do full grid. Wracamy do mechanizmu adopcji i sprawdzamy, czy finansowanie naprawde przechodzi przez decyzje firmy.

Potem finalny P1 phase grid:

- 7 poziomow BDP x 5-7 poziomow osi Y;
- 10-20 seedow;
- horyzont 60 miesiecy;
- opcjonalnie drugi horyzont 120 miesiecy dla stabilnosci rezimow.

Klasyfikator rezimow:

- `accelerating automation`: adopcja powyzej baseline i inwestycje prywatne bez silnego stresu;
- `finance-constrained automation`: presja adopcyjna widoczna, ale tech CapEx i inwestycje spadaja;
- `suppressed automation`: adopcja ponizej lokalnego maksimum mimo wysokiego BDP;
- `fiscal-financial stress`: wysoki koszt dlugu, wysoki deficyt/dlug, spadek inwestycji prywatnych.

Figury:

- heatmap `TotalAdoption`;
- heatmap tech CapEx;
- heatmap private investment / GDP;
- heatmap cost of capital;
- regime map z dyskretnymi kolorami;
- kontury wariancji miedzy seedami.

Tipping / early-warning signatures jako czesc post-processingu, nie opcja:

- wariancja wyniku miedzy seedami w okolicy granicy rezimu;
- lag-1 autocorrelation wybranej zmiennej, np. private investment / GDP albo `TotalAdoption`;
- skewness rozkladu wyniku miedzy seedami.

Uwaga:

> Nie claimujemy critical slowing-down bez danych. W paperze te metryki sa testem: jesli sygnatura jest widoczna, wzmacnia framing tipping; jesli nie, phase diagram pozostaje glownym wynikiem.

## 5. Workstream C: pattern-oriented validation

Cel:

> Pokazac, ze `amor-fati` nie jest tylko level-matching simulator, ale generuje lub falsyfikuje wybrane stylized facts.

Nie zakladamy, ze wszystkie patterny przejda. Wynik negatywny tez jest diagnostyczny.

### C1. Firm-size distribution

Test:

- CCDF rozmiaru firm;
- udzial micro/small/medium/large;
- opcjonalnie Hill estimator dla ogona.

Status dzis:

- terminalne klasy firm juz sa eksportowane;
- brakuje pelnego mikro rozkladu firm w CSV.

Wymagane:

- mikro snapshot firm;
- porownanie z GUS/REGON lub innym zrodlem struktury firm.
- jawny bridge definicji wielkosci firmy model <-> GUS, najlepiej przez liczbe pracownikow.

### C2. Gibrat-lite

Test:

> Czy wzrost firm jest niezalezny od rozmiaru poczatkowego?

Metoda:

- dla firm zyjacych w `t0` i `t1`: growth = log(size_t1 / size_t0);
- regresja growth na log(size_t0);
- test nachylenia bliskiego zera;
- oddzielnie dla traditional, hybrid, automated.

Wymagane:

- firm id zachowany w czasie;
- workers jako podstawowy proxy rozmiaru w kilku punktach czasowych;
- capital albo revenue tylko jesli sa juz latwo dostepne w eksporcie, bez rozszerzania scope paperu 1.

### C3. Adoption distribution

Test:

> Czy adopcja automatyzacji jest skoncentrowana w okreslonych klasach firm, sektorach lub kwartylach plynnosci?

Metoda:

- adopcja wg size class;
- adopcja wg sector;
- adopcja wg cash/debt quartile;
- Lorenz/Gini adopcji, jesli metryka ma sens.

To jest pattern najblizszy pierwszemu paperowi i powinien byc gotowy jako pierwszy.

### C4. Volatility clustering

Test:

> Czy model generuje klastrowanie zmiennosci wzrostu PKB/inwestycji/adopcji bez recznego szoku?

Metoda:

- dlugie baseline runs: 600-1200 miesiecy;
- wzrost miesieczny lub kwartalny `MonthlyGdpProxy`, inwestycji prywatnych, adopcji;
- autocorrelation squared returns / absolute returns;
- porownanie z prostym iid benchmarkiem.

Status:

- P1-late albo appendix. Nie jest blokujacym patternem paperu 1, bo wymaga dlugich przebiegow 600-1200 miesiecy.

### C5. Default clustering / heavy-tail cascades

Test:

> Czy bankructwa firm klastruja sie w czasie i czy miesieczne fale upadlosci maja gruby ogon?

Metoda:

- rozklad miesiecznych `FirmDeaths`;
- autocorrelation;
- tail index / CCDF;
- oddzielnie baseline i wysokie BDP.

To jest realistyczniejsze niz pelny wealth Pareto i blisko mechanizmu finansowania.

### C6. Wealth / liquidity inequality

Test:

- Gini wealth/liquidity;
- ewentualnie Pareto tail HH liquidity/wealth.

Status:

- P2. Nie wchodzi do paperu 1, zeby nie rozszerzac scope poza firmy, adopcje technologii i finansowanie.

## 6. Workstream D: literatura i positioning

Cel:

> Pokazac, gdzie `amor-fati` siedzi wzgledem znanych rodzin ABM/SFC-ABM i gdzie jest wklad.

Najpierw audyt prof. Safarzynskiej:

- sprawdzic 3 ostatnie prace z lat 2024-2026 albo najnowsze publiczne working papers;
- zanotowac, czy dotykaja UBI, adopcji technologii, nierownosci, tipping, ABM albo transformacji spoleczno-gospodarczych;
- wprost okreslic, czy proponowany paper rozszerza jej dorobek, czy idzie rownolegla sciezka;
- nie wysylac maila bez tego audytu.

Tabela literatury:

- Caiani et al. 2016, AB-SFC benchmark;
- K+S / Dosi-Roventini, w tym prace o automatyzacji;
- Eurace;
- JAMEL;
- Lengnick;
- Acemoglu-Restrepo;
- Korinek-Stiglitz;
- Berg-Buffie-Zanna;
- Hoynes-Rothstein;
- Banerjee-Niehaus-Suri;
- Safarzynska & van den Bergh;
- Safarzynska solo / z koautorami o ABM, heterogenicznej adopcji, tipping albo transformacjach.

Kolumny:

- metoda;
- ABM;
- SFC;
- firmy heterogeniczne;
- banki i finansowanie;
- automatyzacja/technologia;
- UBI/transfers;
- pattern-oriented validation;
- phase diagrams / regimes;
- formal verification / runtime accounting;
- gap.

Uwaga:

> Nie wpisywac claimow bez zrodla. Jesli jakis paper jest niepewny, idzie do sekcji "to verify", nie do mapy.

## 7. Workstream E: artefakty paperowe

Do przygotowania:

- one-pager po angielsku;
- paragraf "what is new";
- abstract 150-200 slow;
- 5-figurowy outline paperu;
- README reprodukcji;
- komendy uruchomieniowe;
- `checksums.txt` dla nowych artefaktow;
- wersja commitow `amor-fati` i `amor-fati-bdp-mba-paper`;
- lista znanych ograniczen.

Minimalny outline paperu:

1. Introduction: UBI and automation are not monotonic.
2. Literature: ABM/SFC-ABM, automation, UBI, complexity regimes.
3. Model: `amor-fati`, only the parts needed for this paper.
4. Mechanism: firm adoption, financing, BDP/UBI shock.
5. Pattern-oriented validation.
6. Phase diagram.
7. Heterogeneous adoption: who automates first.
8. Robustness.
9. Discussion and limits.

Paragraf "what is new" musi odpowiedziec na pytanie:

> Czego dokladnie nie ma w literaturze i co ten paper wnosi poza pokazaniem kolejnego modelu?

Robocza struktura:

> Prior work discusses UBI, automation, and heterogeneous-agent macro models, but the non-monotonic effect of cash transfers on technology adoption has not been derived from heterogeneous firm balance sheets inside a stock-flow consistent ABM with explicit financing constraints. This paper provides a phase-diagram account of when UBI accelerates automation and when fiscal-financial feedback suppresses it.

## 8. Workstream F: dokumentacja mechanizmu

Cel:

> Opisac decyzje adopcji per-firma tak, zeby recenzent rozumial mechanizm bez czytania kodu.

Artefakty:

- 1-stronicowa specyfikacja mechanizmu;
- pseudocode decyzji firmy w 5-10 liniach;
- diagram przeplywu: BDP -> popyt / placa rezerwowa / fiskus -> koszt pracy i kapitalu -> decyzja firmy;
- lista zrodel heterogenicznosci: sektor, wielkosc, digital readiness, cash, dlug, bank, risk profile;
- jasne rozdzielenie mechanizmu finansowego i behawioralnego.

Minimalny pseudocode:

```text
for each traditional firm:
  estimate full-AI and hybrid candidate costs
  check profitability, down payment, digital readiness, and bank approval
  compute adoption probability from risk profile, readiness, local adoption, global adoption pressure, losses, and ramp
  draw stochastic adoption outcome
  if adopted: update tech state, debt, cash, imports, and labor demand
  if failed: apply partial capex/loan/down-payment loss and possible bankruptcy
```

Deklaracja scope:

> Paper 1 jest balance-sheet-driven. Imitacja i local adoption pressure istnieja w mechanizmie, ale nie robimy z nich glownego behavioral-learning claimu. Rozszerzenie o silniejszy behavioral adoption mechanism, np. Bass/imitation/adaptive expectations, jest P2 albo paper 2.

## 9. Kolejnosc pracy

### Etap 0: audyt dorobku prof. Safarzynskiej

Cel:

- przeczytac lub przynajmniej technicznie przejrzec 3 najnowsze prace;
- znalezc overlap z UBI, automatyzacja, nierownosciami, adopcja, tipping albo ABM;
- upewnic sie, ze proponowany paper nie jest remake'em jej istniejacej pracy.

Output:

- notatka 1-2 strony;
- lista cytowan do mapy literatury;
- korekta "what is new" pod jej dorobek.

### Etap 1: audyt i projekt eksportow

Cel:

- potwierdzic, ktore metryki sa juz dostepne;
- zaprojektowac minimalny mikro snapshot firm;
- wybrac format CSV.

Output:

- lista kolumn;
- lista plikow w `amor-fati` do zmiany;
- maly test eksportu.

### Etap 2: implementacja mikroeksportu firm

Cel:

- wygenerowac CSV, ktory pozwala liczyc adoption distribution, Gibrat-lite i firm-size CCDF.

Output:

- snapshot firm co 12 miesiecy i terminal;
- test lub smoke run;
- dokumentacja kolumn.

### Etap 3: pattern-oriented pilot

Cel:

- policzyc minimum trzy patterny:
  - firm-size distribution;
  - Gibrat-lite;
  - adoption distribution.

Output:

- 3 wykresy;
- tabela pass/fail/diagnostic;
- notka interpretacyjna.

### Etap 4: screening osi finansowania

Cel:

- sprawdzic, czy `banking.baseSpread`, `corpBond.spread`, `firm.aiCapex/hybridCapex` albo CAR/bufor najlepiej porusza adopcje.

Output:

- mala tabela wynikow;
- decyzja o osi Y.
- decyzja gate: przechodzimy do full grid albo wracamy do mechanizmu.

### Etap 5: full phase grid

Cel:

- wykonac finalny 2D sweep.

Output:

- heatmapy;
- regime classifier;
- seed variance;
- lag-1 autocorrelation;
- skewness;
- CSV z wynikami.

### Etap 6: mechanism note

Cel:

- opisac mechanizm adopcji i finansowania w formie paper-ready.

Output:

- 1-stronicowa specyfikacja;
- pseudocode;
- diagram mechanizmu;
- notka scope: balance-sheet-driven paper 1, behavioral adoption jako P2.

### Etap 7: one-pager + literature map + abstract

Cel:

- przygotowac material gotowy do wyslania.

Output:

- one-pager;
- mapa literatury;
- what-is-new paragraph;
- abstract;
- draft maila.

## 10. Harmonogram

Realistycznie:

- Etap 0: 2 dni;
- Etapy 1-2: 2-3 tygodnie;
- Etap 3: 2-3 tygodnie;
- Etap 4: 1-2 tygodnie;
- Etap 5: 3-5 tygodni, zalezne od CPU;
- Etap 6: 3-5 dni;
- Etap 7: 2-3 tygodnie.

Lacznie:

> 3.5-4.5 miesiaca pelnego skupienia albo 5-6 miesiecy kalendarzowych, jesli praca idzie obok innych obowiazkow.

## 11. Publiczny slad w trakcie

Cel:

> Gdy prof. Safarzynska dostanie maila, w 2 minuty ma zobaczyc, ze projekt istnieje publicznie jako program badawczy, nie prywatny skrypt.

Opcje:

- opublikowac MBA-paper jako preprint / working paper snapshot;
- przygotowac krotka strone projektu albo README z phase-diagram roadmap;
- zglosic mini-talk na seminarium, workshop, WEHIA, EAEPE albo krajowe wydarzenie;
- po pierwszym phase diagramie przygotowac krotka notke techniczna.

Nie trzeba robic wszystkiego. Minimum:

- publiczny link do PDF / repo;
- czytelny README;
- jeden publiczny artefakt poza prywatnym repo.

## 12. Kryteria gotowosci do kontaktu

Nie piszemy do prof. Safarzynskiej, dopoki nie ma:

- dzialajacego mikroeksportu firm;
- minimum 3 pattern-oriented diagnostics;
- przynajmniej jednego 2D phase diagramu;
- tipping / early-warning metrics policzonych jako post-processing;
- engine-level evidence index z konkretnymi sciezkami do `../amor-fati/docs`: ODD, behavioral rules, SFC matrix evidence, empirical validation, calibration register, sensitivity workflow, operations;
- P1-specific tool-validity packet: pre-registration table, P1 Monte Carlo design note, calibration/validation separation manifest, BDP-specific SFC reconciliation, firm-adoption traces, manifest.json, checksums, pattern table i ablation table;
- 1-stronicowej dokumentacji mechanizmu;
- reprodukowalnego README;
- mapy literatury;
- audytu 3 najnowszych prac prof. Safarzynskiej;
- one-pagera po angielsku;
- paragrafu "what is new";
- jasnego "ask": wspolne doprecyzowanie working paperu, nie konsultacja narzedzia.

## 13. Ryzyka

### Patterny nie wyjda

To nie jest porazka, jesli bedzie dobrze opisane. Wtedy paper mówi:

> Model generuje phase boundary dla adopcji, ale nie reprodukuje jeszcze pelnego zestawu stylized facts; wskazuje to na brakujace mechanizmy wzrostu proporcjonalnego, wejscia/wyjscia firm lub sieci finansowania.

### Phase diagram nie pokaze czytelnego rezimu

Wtedy trzeba:

- sprawdzic os finansowania;
- wydluzyc horyzont;
- zwiekszyc seedy;
- sprawdzic, czy parametr naprawde przechodzi przez decyzje adopcji.

### Mikroeksport bedzie ciezki

Nie eksportowac wszystkiego co miesiac. Zaczac od:

- month 1;
- month 12;
- month 24;
- month 36;
- month 48;
- month 60;
- terminal.

### Mechanizm bedzie nieczytelny dla recenzenta

Wtedy heatmapy nie wystarcza. Trzeba najpierw uproscic opis mechanizmu:

- pseudocode;
- tabela warunkow adopcji;
- diagram transmisji BDP -> firma;
- jawna lista zmiennych heterogenicznych.

### Behavioral adoption bedzie uznane za za slabe

Paper 1 nie udaje pelnego behavioral-learning modelu. Framing:

> The headline mechanism is balance-sheet-driven. Local imitation and adoption pressure enter the current mechanism, while richer behavioral learning is a follow-up extension.

### Kalibracja bedzie uznana za reczna

Nie ukrywac tego. Framing:

> Calibration follows a documented hand-targeting protocol; SMM/ABC calibration is a next-stage pipeline.

### Network topology bedzie uznana za zbyt uboga

Nie robic z sieci claimu paperu 1. Framing:

> Network topology is used for local adoption pressure, but systemic network contagion is outside paper 1 and belongs to a follow-up paper.

### Kontakt opozni sie o kilka miesiecy

To akceptujemy. Decyzja strategiczna jest taka, ze wchodzimy z materialem klasy working-paper, nie z requestem o konsultacje.
