# Format danych dashboardu

To format pliku wejściowego dla `scripts/build_dashboard.py`, który go sprawdza, dopisuje
pole `scores` z wynikami i wstawia całość do szablonu. Pełny przykład: `assets/sample_analysis.json`. Pola oznaczone `?` są opcjonalne — gdy brak
danych, wpisz `null` lub pomiń; dashboard ukryje element albo pokaże "brak danych".
Wszystkie kwoty jako liczby (bez "zł"), daty jako `RRRR-MM-DD`.

```jsonc
{
  "meta": {
    "generated_at": "2026-11-08",
    "currency": "PLN",                 // kod ISO waluty
    "locale": "pl-PL",                 // formatowanie liczb i dat
    "confidence": "średnia",           // wysoka | średnia | niska
    "confidence_note": "Na czym opiera się analiza, czego brakuje."
  },
  "offer": {
    "title": "Nazwa produktu",
    "store": "Sklep",
    "url": "https://…",
    "category?": "Słuchawki",
    "current_price": 1299,
    "claimed_old_price?": 1899,        // przekreślona / "regularna" cena
    "claimed_discount_pct?": 32,       // rabat deklarowany przez sklep
    "lowest_30d_price?": 1349,         // Omnibus — jak podano na stronie (lub ustalona)
    "omnibus_shown": true,             // czy sklep pokazał najniższą cenę z 30 dni
    "shipping?": "Darmowa od 199 zł",
    "key_specs?": ["ANC", "30 h baterii"],
    "captured_at": "2026-11-08"
  },
  "user_reason?": "Wolna wypowiedź użytkownika: dlaczego rozważa zakup.",
  "survey": [
    { "question": "Cel zakupu", "answer": "Ulepszenie tego, co mam", "risk": 0.6, "note?": "…" }
  ],
  "biases": [
    {
      "id": "anchoring",                // z katalogu biases.md
      "name": "Efekt zakotwiczenia",
      "name_en": "Anchoring",
      "weight": 1.3,                    // waga bazowa z katalogu
      "intensity": 3,                   // 0–3
      "amplifier": 1.2,                 // 0.8–1.5
      "amplifier_reason": "Nie porównywałaś jeszcze cen → kotwica działa mocniej.",
      "source": "offer",                // offer | context | both
      "evidence": ["Przekreślona cena 1899 zł przy najniższej z 30 dni 1349 zł"],
      "how_it_works": "2–3 zdania, na przykładzie tej oferty.",
      "why": "2–3 zdania o mechanizmie psychologicznym.",
      "defense": ["Konkretna rada 1", "Konkretna rada 2"]
    }
  ],
  "price": {
    "history": [                         // punkty znalezione w źródłach, rosnąco po dacie
      { "date": "2026-05-01", "price": 1599, "source": "ceneo.pl", "promo": false, "label?": "…" }
    ],
    "historical_low?": 1199,
    "historical_low_date?": "2025-11-28",
    "typical_price?": 1499,              // cena, po której produkt najczęściej się sprzedaje
    "promos_per_year?": 9,
    "promo_pattern?": "Opis wzorca promocji słowami.",
    "sources?": [{ "label": "ceneo.pl – historia cen", "url": "https://…" }]
  },
  "alternatives": [
    { "name": "…", "store": "…", "price": 1249, "url": "https://…",
      "type": "ten sam produkt",         // ten sam produkt | podobny produkt
      "note": "Dlaczego warto rozważyć / na co uważać." }
  ],
  "verdict": {
    "decision": "poczekaj",              // kup | kup gdzie indziej | poczekaj | odpuść
    "headline": "Jedno zdanie werdyktu.",
    "reasons": ["…", "…"],
    "target_price?": 1199,               // cena, przy której warto kupić
    "wait_for?": "Np. Black Friday — w zeszłym roku 1199 zł."
  },
  "checklist": ["Pytanie/krok do odhaczenia przed zakupem", "…"],
  "sources": [{ "label": "…", "url": "https://…" }],
  "limitations": ["Czego nie udało się sprawdzić", "…"]
}
```

Uwagi:
- Nie wpisuj wyników (wskaźnik, udziały %, pole `scores`) — skrypt liczy je z `weight`,
  `intensity`, `amplifier`, `risk` i danych cenowych.
- `realny rabat` liczony jest z `lowest_30d_price` (a gdy brak — z `price.typical_price`).
- Linki tylko `http(s)://` — inne są pomijane (skrypt ostrzega).
- Skrypt sam zabezpiecza `</` w tekstach; przy ręcznym wstawianiu (bez Pythona) zamień je na `<\/`.
