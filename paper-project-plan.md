# MBA paper project plan

**Projekt:** BDP jako warunkowy katalizator automatyzacji: od rownowagi DSGE do wykonywalnego modelu SFC-ABM gospodarki polskiej
**Termin oddania:** koniec maja 2026
**Stan na 2026-05-12:** draft LaTeX istnieje, scenariusz BDP jest zaimplementowany, glowny wynik opiera sie na 10 seedach dla wariantu centralnego `lambda = 0.5`, analiza odpornosci lambda jest wykonana, wykresy i aneks SFC sa w PDF. Plan zostal ustawiony pod recenzenta klasyczno-makroekonomicznego: finanse publiczne, inwestycje firm, koszt kapitalu i most do MFW.
**Cel:** oddac prace, ktora wyglada jak maly replikowalny paper badawczy, nie jak standardowy referat MBA.

## North star

Praca ma pokazac trzy rzeczy:

1. **Hipoteza:** BDP moze byc katalizatorem automatyzacji, ale tylko warunkowo.
2. **Eksperyment:** hipoteza zostala zaimplementowana w wykonywalnym modelu `amor-fati`, a nie tylko opisana.
3. **Falsyfikacja:** wynik nie potwierdza mocnej wersji monotonicznej; wymusza wersje nieliniowa z progiem absorpcji fiskalno-finansowej.

Docelowa teza:

> BDP nie jest liniowym katalizatorem automatyzacji. Dziala katalitycznie tylko w przedziale, w ktorym kanal popytowo-kosztowy nie niszczy zdolnosci finansowania inwestycji prywatnych. Po przekroczeniu progu fiskalno-finansowego BDP przestaje przyspieszac automatyzacje i zaczyna ja ograniczac.

## Lens recenzenta: prof. Jacek Tomkiewicz

Recenzent jest mocno osadzony w makroekonomii, finansach publicznych, polityce fiskalnej i praktyce instytucjonalnej. Praca ma byc ambitna technicznie, ale argument musi byc prowadzony klasycznym jezykiem ekonomicznym.

Priorytety narracyjne:

1. **Finanse publiczne przed technika.** BDP nalezy opisywac przez deficyt, dlug/PKB, koszt obslugi dlugu, rentownosci obligacji i przestrzen fiskalna.
2. **Inwestycje firm jako centralny mechanizm.** Automatyzacja nie jest magiczna reakcja na drozsza prace, tylko decyzja CapEx wymagajaca gotowki, kredytu i akceptowalnego kosztu kapitalu.
3. **MFW jako punkt odniesienia, nie przeciwnik.** MFW odpowiada na pytanie o redystrybucje i dobrobyt w rownowadze; `amor-fati` odpowiada na pytanie o sciezke przejscia i bilansowe ograniczenia po drodze.
4. **Ostrozna teza.** Nie piszemy "BDP przyspiesza AI", tylko "BDP moze przyspieszac AI warunkowo, dopoki nie niszczy zdolnosci finansowania inwestycji".
5. **Technologia przetlumaczona na ekonomie.** SFC = kazdy wydatek ma druga strone. Ledger = pieniadz nie znika. ABM = heterogeniczne firmy/gospodarstwa. Seed = odpornosc wyniku na losowosc.
6. **Status wyniku.** To kontrfaktyczny eksperyment obliczeniowy, nie punktowa prognoza makroekonomiczna.

## Definition of done

- PDF sklada sie bez bledow LaTeX i bez kompromitujacych overfulli w czesci glownej.
- Spis tresci, abstract, slowa kluczowe, JEL codes, Code & Data sa kompletne.
- `amor-fati`, `amor-fati-ledger` i BoomBustGroup sa linkami.
- Wyniki glowne sa oparte na 10-seedowym wariancie centralnym `lambda = 0.5`.
- Wykresy pokazuja srednie i niepewnosc miedzy seedami.
- Praca zawiera most do MFW: Polska, kwota 2 111 PLN/os./rok, porownanie z naszymi poziomami BDP.
- Praca zawiera mape kanalow transmisji BDP w jezyku ekonomicznym, nie tylko opis kolumn outputu.
- Praca zawiera panel kontrolny gospodarstw domowych: Gini, ubostwo, oszczednosci/konsumpcja i bankructwa HH sa monitorowane, ale nie sa nadinterpretowane jako glowny mechanizm.
- Praca jednoznacznie pokazuje, ze glowna nieliniowosc w tym eksperymencie idzie przez firmy, inwestycje prywatne, koszt kapitalu i kanal fiskalno-finansowy.
- Praca jasno wskazuje, ze baseline `amor-fati` jest produkcyjnie skalibrowany do Polski na 2026-04-30.
- Aneks replikacyjny pozwala odtworzyc wynik: branch, commit, komendy, parametry, lokalizacja CSV, generator wykresow.
- Wnioski jasno mowia, co wynik wspiera, czego nie wspiera i jakie sa ograniczenia.
- Zakonczenie zawiera menedzerski "executive conclusion": zarzad pyta nie tylko o presje automatyzacyjna, ale o bilans, plynnosc i dostep do finansowania technologicznej odpowiedzi.

## Workstream 1: Eksperyment glowny

**Cel:** oprzec prace na 10-seedowym wariancie centralnym `lambda = 0.5`.

Run:

```sh
sbt assembly
java -jar target/scala-3.8.2/amor-fati.jar 10 robust-bdp-0000 --duration 60 --run-id robust-bdp-0000-60m-10s --bdp 0
java -jar target/scala-3.8.2/amor-fati.jar 10 robust-l050-bdp-0500 --duration 60 --run-id robust-l050-bdp-0500-60m-10s --bdp 500 --bdp-lambda 0.5
java -jar target/scala-3.8.2/amor-fati.jar 10 robust-l050-bdp-1000 --duration 60 --run-id robust-l050-bdp-1000-60m-10s --bdp 1000 --bdp-lambda 0.5
java -jar target/scala-3.8.2/amor-fati.jar 10 robust-l050-bdp-1500 --duration 60 --run-id robust-l050-bdp-1500-60m-10s --bdp 1500 --bdp-lambda 0.5
java -jar target/scala-3.8.2/amor-fati.jar 10 robust-l050-bdp-2000 --duration 60 --run-id robust-l050-bdp-2000-60m-10s --bdp 2000 --bdp-lambda 0.5
java -jar target/scala-3.8.2/amor-fati.jar 10 robust-l050-bdp-2500 --duration 60 --run-id robust-l050-bdp-2500-60m-10s --bdp 2500 --bdp-lambda 0.5
java -jar target/scala-3.8.2/amor-fati.jar 10 robust-l050-bdp-3000 --duration 60 --run-id robust-l050-bdp-3000-60m-10s --bdp 3000 --bdp-lambda 0.5
```

Do zrobienia:

- [x] Uruchomic 10-seedowy wariant centralny.
- [x] Zmienic generator wykresow tak, aby uzywal `robust-l050`.
- [x] Przeliczyc tabele terminalne.
- [x] Zmienic tekst na "eksperyment glowny" i usunac narracje o przebiegach wstepnych.
- [x] Raportowac srednie + odchylenia standardowe miedzy seedami.

## Workstream 2: Most do MFW

**Cel:** pokazac, ze praca nie ignoruje rekomendacji profesora/MFW, tylko precyzyjnie odpowiada na inne pytanie.

Kluczowe rozroznienie:

- MFW dla USA: DSGE, pytanie o dobrobyt/redystrybucje w nowej rownowadze.
- MFW dla Polski: partial static equilibrium na danych LIS 2013.
- Nasz model: SFC-ABM, pytanie o sciezke przejscia, bilanse, koszt kapitalu, inwestycje i automatyzacje.

Do zrobienia:

- [x] Dodac mala tabele "MFW vs amor-fati".
- [x] Wprost pokazac: `2 111 PLN/os./rok` = ok. `176 PLN/os./mies.` nominalnie w cenach 2013 i ok. `273 PLN/os./mies.` po indeksacji CPI do cen 2025.
- [x] Pokazac, gdzie ta kwota lezy wzgledem naszego sweepa.
- [x] Dopisac, ze wyzsze poziomy BDP sa mocniejszymi impulsami fiskalnymi niz polski wariant ilustracyjny MFW.

## Workstream 3: Jedna analiza odpornosci

**Cel:** sprawdzic, czy wynik nieliniowy zalezy wylacznie od zalozenia `lambda = 0.5`.

Proponowany minimalny robustness:

- `lambda = 0.00`
- `lambda = 0.25`
- `lambda = 0.50`
- `lambda = 0.75`
- `lambda = 1.00`

Zakres:

- 10 seedow;
- te same poziomy BDP;
- 60 miesiecy.

Decyzja techniczna:

- `Main` przyjmuje `--bdp`;
- domyslnie `--bdp > 0` uzywa centralnego `lambda = 0.5`;
- robustness uzywa parametru CLI `--bdp-lambda <0..1>`.

Do zrobienia:

- [x] Zdecydowac, czy robustness jest konieczny do finalnej pracy.
- [x] Jesli tak: dodac parametr `--bdp-lambda` albo inny prosty mechanizm.
- [x] Uruchomic sweep odpornosci 10 seedow.
- [x] Dodac jeden wykres: adopcja AI/hybrid vs BDP dla pieciu wartosci lambda.
- [x] Wnioski: czy ksztalt nieliniowy zostaje, przesuwa sie, czy znika.

Wynik: ksztalt nieliniowy utrzymuje sie w wariancie centralnym `lambda = 0.5`.
Dla `lambda = 0` adopcja pozostaje blisko baseline, czyli sam transfer popytowo-fiskalny
nie wystarcza do mocnej tezy o automatyzacji. Dla `lambda = 0.75` i `lambda = 1.0`
prog przesuwa sie w lewo: za silny kanal placy rezerwowej obniza inwestycje prywatne
i tlumi zdolnosc firm do automatyzacji. To wzmacnia wersje warunkowa hipotezy.

## Workstream 4: Udokumentowanie baseline dla Polski

**Cel:** uprzedzic pytanie: "z jakiego punktu startuje eksperyment BDP?"

Decyzja metodologiczna:

- Nie robimy w pracy osobnej tabeli, ktora porownuje dzisiejsze dane z wartosciami terminalnymi po 60 miesiacach.
- Piszemy krotko, ze `amor-fati` ma produkcyjny baseline skalibrowany do snapshotu Polski na 2026-04-30.
- Wyniki BDP interpretujemy jako kontrfaktyczne odchylenia od tego baseline.
- Dokumentacja szczegolowa zostaje w repo: `docs/calibration-register.md`, `docs/scenario-registry.md`, `docs/empirical-validation-report.md`.

Do zrobienia:

- [x] Dodac krotki akapit do sekcji o `amor-fati`.
- [x] Nie wprowadzac tabeli, ktora mieszalaby kalibracje startu z wynikiem po horyzoncie eksperymentu.
- [x] W aneksie replikacyjnym wskazac dokumenty repozytorium, ktore potwierdzaja date i zakres baseline.

## Workstream 5: Wykresy i analiza wynikow

Obecne wykresy:

- BDP vs adopcja AI/hybrid i inwestycje prywatne.
- Kanal fiskalno-dluzny.
- Kanal kosztu kapitalu.
- Kanal zewnetrzny.
- Panel firmowy sciezki przejscia.

Do zrobienia:

- [x] Przebudowac wykresy na 10-seedowy wariant centralny.
- [ ] Rozwazyc dodanie wykresu sektorowej adopcji AI/hybrid, jesli wnosi cos merytorycznie.
- [x] Dodac panel firmowy sciezki przejscia: `FirmDeaths`, `FirmBirths`, `LivingFirmCount`, inwestycje oraz adopcja AI/hybrid.
- [x] Dodac syntetyczna mape kanalow transmisji: BDP -> dochod HH/popyt; BDP -> placa rezerwowa/koszt pracy; BDP -> deficyt/dlug/rentownosci/koszt kapitalu; BDP -> kurs/import/inflacja; koszt pracy + koszt kapitalu -> CapEx/AI.
- [x] Dodac panel kontrolny HH: `Gini_Individual`, `Gini_Wealth`, `PovertyRate_50pct`, `PovertyRate_30pct`, `MeanSavings`, `MedianSavings`, `ConsumptionP50`, `BankruptcyRate`.
- [x] W panelu HH wprost napisac, ze w obecnym 60-miesiecznym eksperymencie metryki dystrybucyjne sa stabilne i nie tlumacza nieliniowosci adopcji AI/hybrid.
- [x] Nie dodawac wykresow tylko dlatego, ze dane sa dostepne. Kazdy wykres musi wspierac teze albo falsyfikowac alternatywne wyjasnienie.

## Workstream 6: Tekst i struktura LaTeX

Zasada: praca ma byc paperem, nie dokumentacja techniczna.

Do zrobienia:

- [ ] Skrocic sekcje, ktore brzmia jak opis repozytorium.
- [ ] Wzmocnic sekcje 2: MFW odpowiada na inne pytanie, nie "DSGE jest zle".
- [x] Wzmocnic sekcje 4: hipoteza warunkowa zamiast monotonicznej.
- [ ] W sekcji wynikow pisac jezykiem mechanizmow, nie nazw kolumn.
- [x] W ograniczeniach wprost napisac, czego model nie mowi.
- [x] We wnioskach pokazac dojrzzalosc: wynik poprawil hipoteze autora.
- [ ] Przejsc caly tekst pod katem recenzenta: czy kazde twierdzenie techniczne ma ekonomiczna translacje?
- [ ] Ograniczyc jezyk "complexity economics" do roli metodologicznej; glowny argument prowadzic przez deficyt, dlug, inwestycje, koszt kapitalu i decyzje firm.
- [ ] Usunac ton "pitch amor-fati"; `amor-fati` ma byc instrumentem badawczym, a nie produktem.
- [x] Upewnic sie, ze status modelu jest jasny: kontrfaktyczny eksperyment, nie prognoza.

## Workstream 7: Replikacja i OSS

**Cel:** pokazac cos, czego standardowy referat MBA nie ma: replikowalnosc.

Do zrobienia:

- [ ] Wpisac commit repozytorium po finalnym sweepie.
- [ ] Wpisac branch.
- [ ] Wpisac pelne komendy uruchomienia.
- [ ] Wpisac komendy generowania wykresow: `make figures`, `make paper`.
- [ ] Wpisac sciezki do CSV.
- [ ] Linki: `amor-fati`, `amor-fati-ledger`, BoomBustGroup.
- [ ] Zaznaczyc, ze repo jest OSS, ale narzedzie jest autorskie i rozwijane w ramach BoomBustGroup.

## Harmonogram do konca maja

### Dni 1-3

- [x] Eksperyment glowny 10 seedow.
- [x] Backup wynikow w `mc/`.
- [x] Wstepna kontrola ksztaltu wyniku.

### Dni 4-6

- [x] Nowe wykresy i tabele.
- [x] Aktualizacja sekcji wynikow.
- [x] Aktualizacja abstraktu.

### Dni 7-9

- [x] Decyzja o robustness lambda.
- [x] Jesli tak: implementacja/uruchomienie malego sweepa.
- [x] Jesli nie: uzasadnic w ograniczeniach, ze robustness jest dalsza praca.

### Dni 10-12

- [x] Most do MFW.
- [ ] Sprawdzenie, czy akapit o baseline 2026-04-30 jest spojny z aneksem replikacyjnym.
- [ ] Uporzadkowanie bibliografii.

### Dni 13-16

- [x] Dodanie mapy kanalow transmisji.
- [x] Dodanie panelu kontrolnego HH i interpretacji: stabilne Gini/ubostwo nie sa glownym mechanizmem wyniku.
- [x] Przepisanie wprowadzenia, hipotezy i wnioskow pod finalne wyniki oraz lens recenzenta.
- [ ] Usuniecie fragmentow zbyt technicznych z glownego tekstu.
- [ ] Przeniesienie nadmiaru do aneksu albo wyciecie.
- [x] Wzmocnienie executive conclusion dla zarzadu/CFO.

### Dni 17-19

- [ ] Korekta jezykowa.
- [ ] Sprawdzenie PDF strona po stronie.
- [ ] Sprawdzenie linkow, spisu tresci, numeracji tabel/rysunkow.
- [ ] Finalne `make paper`.

### Dzien 20

- [ ] Tylko czytanie jak recenzent.
- [ ] Bez duzych zmian strukturalnych.
- [ ] Eksport finalnego PDF.

## Najwieksze ryzyka

- **Za duzo techniki w glownym tekscie.** Rozwiazanie: technikalia do aneksu, w tekscie mechanizmy ekonomiczne.
- **Wynik moze byc nadinterpretowany jako prognoza.** Rozwiazanie: konsekwentnie piszemy o kontrfaktycznej sciezce modelu i mechanizmach transmisji.
- **Panel HH moze rozrosnac sie w osobny paper-06.** Rozwiazanie: uzywamy go jako kontroli alternatywnego wyjasnienia, nie jako rdzenia pracy.
- **MFW zostanie ustawione jako przeciwnik.** Rozwiazanie: MFW jest punktem odniesienia i narzedziem komplementarnym.
- **Praca bedzie wygladala jak pitch amor-fati.** Rozwiazanie: `amor-fati` jako instrument badawczy, nie produkt.
- **Recenzent zapyta o finanse publiczne i reguly fiskalne.** Rozwiazanie: eksponujemy dlug/PKB, deficyt/PKB, rentownosci, koszt kapitalu i efekt na inwestycje prywatne.
- **Teza "BDP katalizuje AI" zabrzmi zbyt mocno.** Rozwiazanie: konsekwentnie piszemy o katalizie warunkowej i progu fiskalno-finansowym.

## Ostatnia wersja przekazu

Najmocniejsza wersja narracji:

> Zaczalem od kontrarianskiej intuicji, ze BDP moze przyspieszac automatyzacje. Po implementacji w modelu SFC-ABM wynik okazal sie bardziej interesujacy: BDP przyspiesza automatyzacje tylko do pewnego progu. Powyzej tego progu kanal fiskalno-finansowy ogranicza zdolnosc firm do inwestowania. To nie jest porazka hipotezy, tylko jej doprecyzowanie. Wlasnie po to buduje sie wykonywalne modele.
