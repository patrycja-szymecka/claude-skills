# Punktacja — wzory i mapowanie ankiety

Wyniki liczy `scripts/scoring.py` (źródło prawdy) i wypisuje je `build_dashboard.py`.
Ten plik służy do tego, żeby poprawnie przeliczyć odpowiedzi z ankiety na `risk` i rozumieć,
skąd biorą się liczby. Zmieniając wzór, zmień go w `scoring.py`, tutaj oraz w zapasowej
funkcji `computeScores` w `assets/dashboard_template.html` (używanej tylko bez Pythona).

## 1. Ankieta → `risk` (0–1)

| Pytanie | Odpowiedź → risk |
|---|---|
| Cel zakupu | Wymiana zepsutej 0.1 · Nowa konkretna potrzeba 0.3 · Prezent 0.4 · Ulepszenie 0.6 · Po prostu mi się spodobało 0.9 |
| Skąd oferta | Sam szukałem 0.1 · Polecenie znajomych 0.3 · Przypadkiem 0.7 · Reklama/newsletter/powiadomienie 0.8 · Influencer/social media 0.9 |
| Presja czasu | Mogę poczekać 0.1 · Trochę 0.5 · Mocno 0.9 |
| Budżet | W planie 0.1 · Na granicy 0.5 · Ponad budżet 0.8 · Raty/zapłać później 0.9 |
| Podobna rzecz | Tak, zepsuta 0.1 · Nie 0.3 · Tak, działa 0.8 |
| Jak długo rozważasz | Tygodnie+ 0.1 · Kilka dni 0.4 · Dziś 0.9 |
| Nastrój | Spokój 0.1 · Nuda 0.6 · Nagroda/świętowanie 0.7 · Stres/zmęczenie 0.8 · Smutek 0.8 |
| Porównywanie | Dokładnie 0.1 · Pobieżnie 0.5 · Nie 0.9 |

Odpowiedź spoza listy (z pola "inne" lub wolnego tekstu) oceń analogicznie i dopisz `note`.
Wolna wypowiedź "dlaczego" nie ma własnego `risk`, ale może zmienić `amplifier` efektów
(np. "wszyscy w pracy już mają" → społeczny dowód słuszności ×1.3).

## 2. Efekty

Dla każdego efektu *i*:
- `w` — waga bazowa z katalogu (0.7–1.3),
- `intensity` — 0–3,
- `amplifier` — 0.8–1.5 (1.0 = ankieta nic nie zmienia).

**Siła efektu** `raw_i = w × intensity × amplifier`
**Udział %** `share_i = raw_i / Σ raw × 100` — to są procenty na wykresie udziałów.

## 3. Trzy składowe wskaźnika (każda 0–100)

**A. Taktyki sprzedażowe** — tylko efekty z `source` = `offer` lub `both`:
`T = 100 × (1 − e^(−Σ(w × intensity) / 12))`
(krzywa nasycenia: suma 6 → ~39, 12 → ~63, 24 → ~86; kilka mocnych taktyk szybko podnosi wynik,
ale nie przekracza 100).

**B. Rzetelność ceny (ryzyko)** — średnia z dostępnych podskładników:
- fałszywy rabat: `clamp((rabat_deklarowany − rabat_realny) × 2.5)`
  gdzie `rabat_realny = (cena_ref − cena_obecna) / cena_ref × 100`,
  `cena_ref` = najniższa cena z 30 dni, a gdy jej brak — cena typowa;
- wieczna promocja: `clamp(promocji_rocznie × 6)`;
- drożej niż konkurencja (ten sam produkt): `clamp(% powyżej najtańszej alternatywy × 4)`;
- drożej niż minimum historyczne: `clamp(% powyżej minimum historycznego × 3)`.
`clamp` = przytnij do 0–100. Brak wszystkich danych → składowa B = brak (i nie liczy się do wyniku).

**C. Twoja podatność** `P = średnia(risk z ankiety) × 100`.

## 4. Wskaźnik ryzyka manipulacji

`Wskaźnik = 0.45 × T + 0.30 × B + 0.25 × P`
Jeśli B jest brakiem, wagi T i P skaluje się do sumy 1 (0.643 / 0.357).

| Zakres | Strefa |
|---|---|
| 0–24 | Niski |
| 25–49 | Umiarkowany |
| 50–74 | Wysoki |
| 75–100 | Bardzo wysoki |
