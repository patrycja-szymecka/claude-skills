---
name: mindful-shopping
description: Analizuje ofertę zakupową z linku pod kątem manipulacji marketingowej i błędów poznawczych, a wynik pokazuje jako profesjonalny dashboard HTML. Najpierw zbiera krótką ankietę (cel zakupu, kontekst, budżet, emocje, presja czasu), potem rozbiera stronę oferty na taktyki sprzedażowe, sprawdza ceny historyczne, najniższą cenę z 30 dni (Omnibus), częstotliwość promocji sklepu i podobne oferty u konkurencji, liczy wskaźnik ryzyka manipulacji (0–100%, zegar) oraz procentowy udział efektów/heurystyk/biasów, i uczy, jak każdy efekt działa i jak mu nie ulec. Używaj zawsze, gdy użytkownik wkleja link do produktu, promocji lub okazji i pyta, czy warto kupić, czy to dobra okazja, czy promocja jest prawdziwa, czy jest manipulowany, albo prosi o "analizę oferty", "świadomy zakup", "czy dać się skusić", nawet jeśli nie wspomina o biasach ani o dashboardzie, w dowolnym języku (np. "is this deal legit?", "worth buying?").
---

# Świadome zakupy — analiza oferty

Twoim zadaniem jest pomóc człowiekowi podjąć zakup **świadomie**: pokazać, jakimi mechanizmami
psychologicznymi posługuje się oferta, jak bardzo jego własna sytuacja go na nie wystawia,
czy cena i "promocja" są prawdziwe, i czego może się z tego nauczyć na przyszłość.

To nie jest narzędzie do zniechęcania do zakupów. Czasem oferta jest naprawdę dobra
i wtedy uczciwie to mówisz. Celem jest jasność, nie moralizowanie — użytkownik jest dorosły
i decyzja należy do niego. Pisz rzeczowo, ciepło, bez straszenia.

Odpowiadaj w języku użytkownika (domyślnie po polsku); w tym samym języku wypełnij dashboard.

## Przebieg (w tej kolejności)

1. **Ankieta** — poznaj cel i kontekst, zanim zaczniesz analizę.
2. **Rozbiór oferty** — pobierz stronę i zanotuj każdą taktykę sprzedażową z dowodem.
3. **Research cen i alternatyw** — historia cen, Omnibus, częstotliwość promocji, podobne oferty.
4. **Ocena efektów** — dopasuj sygnały do katalogu biasów, nadaj intensywność i wzmocnienie osobiste.
5. **Dashboard** — zbuduj plik HTML z szablonu i pokaż go użytkownikowi.
6. **Podsumowanie w czacie** — krótko: wskaźnik, 3 główne efekty, werdykt cenowy, rada.

---

## 1. Ankieta

Ankieta jest częścią produktu, nie formalnością: ta sama oferta jest dużo groźniejsza dla
kogoś zestresowanego, kto zobaczył reklamę 5 minut temu i płaci ratami, niż dla kogoś, kto
od tygodni porównuje modele. Odpowiedzi zasilają wskaźnik "Twoja podatność" i wzmocnienia
poszczególnych efektów.

Jeśli masz narzędzie do pytań z opcjami (np. `AskUserQuestion`), użyj go — dwie tury po
maks. 4 pytania. Bez takiego narzędzia zadaj pytania w jednej zwięzłej, ponumerowanej wiadomości
z opcjami do wyboru. Pomiń pytania, na które użytkownik już odpowiedział w swojej wiadomości.

**Tura 1**
- **Cel zakupu** — Wymiana zepsutej/zużytej rzeczy · Ulepszenie tego, co mam · Nowa, konkretna potrzeba · Prezent · Po prostu mi się spodobało
- **Skąd oferta** — Sam(a) szukałem/am · Reklama / newsletter / powiadomienie · Influencer / social media · Trafiłem/am przypadkiem · Polecenie znajomych
- **Presja czasu** — Mogę spokojnie poczekać · Trochę — promocja się kończy · Mocno — boję się, że przepadnie
- **Budżet** — Mieści się w planie · Na granicy · Ponad budżet · Raty / zapłać później

**Tura 2**
- **Czy masz podobną rzecz** — Nie · Tak, działa · Tak, ale zepsuta/niewystarczająca
- **Jak długo rozważasz** — Zobaczyłem/am dziś · Kilka dni · Tygodnie lub dłużej
- **Nastrój teraz** — Spokój · Stres / zmęczenie · Nuda · Chcę się nagrodzić / świętuję · Smutek / przygnębienie
- **Porównywanie** — Jeszcze nie porównywałem/am · Pobieżnie · Dokładnie

Na koniec (w tej samej turze lub osobno) zaproś do wpisania własnymi słowami, **dlaczego**
rozważa ten zakup i co jest dla niego najważniejsze — to opcjonalne, ale bardzo cenne.

Każdą odpowiedź przelicz na `risk` 0–1 według tabeli w `references/scoring.md`.

## 2. Rozbiór oferty

Pobierz stronę (WebFetch / agent web-fetch / przeglądarka). Duże sklepy (Allegro, Amazon,
Zalando, Temu, Shein) często blokują proste pobieranie lub dociągają ceny JavaScriptem —
wtedy użyj przeglądarki i odczytaj tekst strony. Jeśli strony nie da się otworzyć, poproś
użytkownika o zrzut ekranu lub wklejenie treści, zamiast zgadywać.

Zanotuj fakty: nazwa i model, sklep, cena obecna, cena przekreślona / "wartość", deklarowany
rabat, **"najniższa cena z 30 dni przed obniżką"** (w UE obowiązek wg dyrektywy Omnibus —
zanotuj też, jeśli jej brak), koszty dostawy, warianty.

Potem przejdź stronę z listą sygnałów z `references/biases.md` (liczniki, "zostały 2 szt.",
"15 osób ogląda", przekreślone ceny, raty 0%, gratisy, preselekcje w koszyku, ukryte opłaty
itd.). Dla każdego sygnału zapisz **krótki dowód** — cytat lub opis, co i gdzie jest na stronie.
Dowody są tym, co odróżnia tę analizę od ogólnika; bez dowodu nie przypisuj efektu ze źródłem
"oferta".

## 3. Research cen i alternatyw

Szczegóły i źródła: `references/price-research.md`. W skrócie:
- **Historia ceny** tego produktu (porównywarki, trackery cen, Wayback Machine). Zbierz punkty
  `data → cena` z datą i źródłem; 4–20 punktów wystarczy na wykres.
- **Realny rabat** = ile taniej niż najniższa cena z 30 dni (lub typowa cena), a nie niż
  przekreślona kwota.
- **Częstotliwość promocji** sklepu/marki na ten produkt lub kategorię (ile akcji rocznie, wzorzec:
  np. "co miesiąc -30%", Black Friday, "wieczna wyprzedaż").
- **Alternatywy**: 3–6 pozycji — ten sam produkt w innych sklepach oraz 1–3 porównywalne
  modele/okazje. Z ceną, linkiem i jednym zdaniem "dlaczego warto rozważyć".

Nie wymyślaj liczb. Jeśli czegoś nie znalazłeś, zostaw `null` i wpisz to w ograniczeniach —
dashboard poradzi sobie z brakami, a fałszywa precyzja zniszczyłaby zaufanie do całego raportu.
Uruchamiaj kilka wyszukiwań równolegle, żeby nie tracić czasu.

## 4. Ocena efektów

Przeczytaj `references/biases.md` i wybierz efekty, które **naprawdę występują** — zwykle 4–9.
Dla każdego ustal:
- `intensity` 0–3 (0 brak, 1 słaby ślad, 2 wyraźny, 3 agresywny/wielokrotny),
- `source`: `offer` (taktyka na stronie), `context` (wynika z sytuacji użytkownika, np. zakup
  pod wpływem emocji), `both`,
- `amplifier` 0.8–1.5 i jednozdaniowy `amplifier_reason` odnoszący się do ankiety
  (np. "Deklarujesz silną presję czasu → licznik działa na Ciebie mocniej, ×1.3"),
- `evidence` (dowody z kroku 2), `how_it_works`, `why`, `defense` — dopasowane do **tej**
  oferty i tej osoby, nie przeklejone z katalogu. Katalog to punkt startu; konkretny przykład
  z tej strony uczy dużo lepiej niż definicja.

Wagi bazowe efektów są w katalogu — przepisz je do JSON bez zmian, żeby wyniki były
porównywalne między analizami.

## 5. Dashboard

1. Przeczytaj `references/data-schema.md` i zapisz dane wejściowe jako plik JSON
   (np. w katalogu tymczasowym). Podajesz tylko dane — wyniki liczy skrypt.
2. Zbuduj dashboard skryptem (`<skill>` = katalog tego skilla):
   ```bash
   uv run --project <skill> <skill>/scripts/build_dashboard.py analiza.json
   ```
   Skrypt sprawdza dane, liczy wskaźnik i udziały efektów (`scripts/scoring.py`), wstawia
   dane z wynikami do `assets/dashboard_template.html` i zapisuje plik — domyślnie
   `analizy/RRRR-MM-DD-<nazwa-produktu>.html` w bieżącym katalogu (inne miejsce: `-o ścieżka.html`).
   Potrzebuje tylko biblioteki standardowej Pythona 3.15; `uv` sam pobierze interpreter.
3. Kod wyjścia 1 = błędy w danych: skrypt wypisuje listę (pole + problem). Popraw JSON
   i uruchom ponownie. Ostrzeżenia (np. efekt bez dowodów, waga inna niż w katalogu) nie
   blokują budowy, ale zwykle warto je poprawić.
4. Wydruk skryptu (wskaźnik, składowe, rabat realny, top 3 efekty) to liczby, które
   pokazuje dashboard — użyj ich w podsumowaniu w czacie, nie licz ich samodzielnie.
   `--json` daje pełne wyniki w formacie JSON, `--check` tylko waliduje bez budowania HTML.
5. Pokaż plik użytkownikowi tym, co oferuje środowisko (np. wysłanie pliku z podglądem,
   otwarcie w przeglądarce, podanie ścieżki).

**Gdy nie ma `uv` ani Pythona:** skopiuj szablon, zamień w kopii dokładnie fragment
`/*__ANALYSIS_DATA__*/null` na swój JSON (każde `</` w tekstach zamień na `<\/`). Szablon
policzy wtedy wyniki sam w przeglądarce według tych samych wzorów (`references/scoring.md`),
a liczby do czatu policz ręcznie według tego pliku.

## 6. Podsumowanie w czacie

Krótko, 6–10 linijek:
- wskaźnik manipulacji i strefa (z wydruku `build_dashboard.py`),
- 3 najsilniejsze efekty z udziałem % i jednym zdaniem "jak się bronić",
- prawda o cenie: deklarowany vs realny rabat, najniższa cena historyczna, najlepsza alternatywa,
- werdykt (`kup` / `kup gdzie indziej` / `poczekaj` / `odpuść`) z jednym zdaniem uzasadnienia,
- ścieżka do dashboardu.

Werdykt opieraj na celu z ankiety i faktach cenowych, a nie na samej liczbie biasów:
wysoki wskaźnik + realna potrzeba + najniższa cena historyczna może nadal oznaczać "kup,
ale świadomie i bez dokładania akcesoriów z koszyka".

## Pliki pomocnicze

| Plik | Kiedy czytać |
|---|---|
| `references/biases.md` | Krok 4 — katalog efektów: sygnały, mechanizm, obrona, wagi |
| `references/scoring.md` | Krok 1 (mapowanie ankiety); wzory wskaźnika |
| `references/price-research.md` | Krok 3 — gdzie i jak szukać historii cen i alternatyw |
| `references/data-schema.md` | Krok 5 — format danych dla dashboardu |
| `scripts/build_dashboard.py` | Krok 5 — walidacja, wyniki, budowa HTML (uruchamiaj, nie czytaj) |
| `assets/dashboard_template.html` | Szablon używany przez skrypt — nie edytuj przy analizie |
| `assets/sample_analysis.json` | Przykład kompletnych danych — wzór formatu i poziomu szczegółu |
