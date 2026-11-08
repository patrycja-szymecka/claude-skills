# Research cen, promocji i alternatyw

Cel: odpowiedzieć na trzy pytania — (1) czy ta cena jest naprawdę niska, (2) jak często ten
sklep/marka robi "promocje", (3) czy można kupić to samo lub coś podobnego lepiej.
Uruchamiaj wyszukiwania równolegle. Każdą liczbę zapisuj z datą i źródłem.

## Źródła historii cen

| Rynek | Źródło | Co daje |
|---|---|---|
| PL | ceneo.pl (karta produktu → "historia cen") | ceny w wielu sklepach, wykres ok. 3–12 mies. |
| PL | skapiec.pl, porownywarka Allegro | ceny bieżące, czasem historia |
| PL | pepper.pl (wyszukaj model) | datowane okazje = świetne źródło częstotliwości promocji i rekordowo niskich cen |
| PL | promoklocki.pl (LEGO), x-kom/morele/RTV Euro AGD "hot shot" | kategorie specjalistyczne |
| DE/EU | idealo.de/.pl, geizhals.eu, mydealz.de | historia cen i okazji w UE |
| Skandynawia/UK | pricespy / prisjakt, hotukdeals | historia cen |
| Amazon | keepa.com, camelcamelcamel.com | pełna historia cen Amazon |
| Dowolny | Wayback Machine: `web.archive.org/web/*/<url oferty>` | archiwalne zrzuty strony = dawne ceny i "przekreślone" kwoty |
| Dowolny | Google Shopping | bieżące ceny u konkurencji |

Strony porównywarek często renderują wykres w JS — jeśli prosty fetch nie zwraca liczb,
użyj przeglądarki albo szukaj tekstowych wzmianek ("najniższa cena", pepper.pl, fora).

## Dyrektywa Omnibus (UE, w Polsce od 1.01.2023)

Przy każdej obniżce sklep musi podać **najniższą cenę z 30 dni przed obniżką**. To najważniejsza
liczba do wyliczenia realnego rabatu. Zwróć uwagę na:
- brak tej informacji przy deklarowanym rabacie (nieprawidłowość — odnotuj jako dowód kotwicy),
- "najniższa cena z 30 dni" równa lub niższa od obecnej → realny rabat ≈ 0 lub ujemny,
- przekreślona cena wyższa niż najniższa z 30 dni → kotwica nie odpowiada realnej cenie.

## Częstotliwość promocji

Szukaj: `"<model>" pepper`, `"<sklep>" promocja <kategoria> <rok>`, archiwalne newslettery,
historia cen z widocznymi dołkami. Policz akcje w ostatnich 12 mies. → `promos_per_year`.
Opisz wzorzec słowami (`promo_pattern`), np. "co 4–6 tygodni -25–35%; najgłębiej w Black Friday".
Jeśli produkt jest "w promocji" przez większość roku, napisz to wprost — to cena regularna
przebrana za okazję.

## Alternatywy

3–6 pozycji:
- `type: "ten sam produkt"` — ten sam model w innych sklepach (uwzględnij dostawę, jeśli istotna),
- `type: "podobny produkt"` — porównywalne modele (podobne parametry, poprzednia generacja,
  odnowiony/outlet, używany z gwarancją), zgodne z celem z ankiety.
Do każdej: cena, link, jedno zdanie, dlaczego warto rozważyć (lub na co uważać).
Jeśli cel z ankiety jest wąski (np. "słuchawki do biegania"), dobieraj alternatywy pod cel,
a nie tylko pod podobieństwo do oglądanego produktu.

## Uczciwość danych

- Nie interpoluj ani nie "wygładzaj" historii cen — wpisuj tylko znalezione punkty.
- Rozróżniaj cenę produktu u tego sprzedawcy od najniższej ceny rynkowej — zaznacz w `source`.
- Ustaw `meta.confidence` ("wysoka" / "średnia" / "niska") i wyjaśnij w `confidence_note`,
  na czym opiera się analiza i czego brakuje.
