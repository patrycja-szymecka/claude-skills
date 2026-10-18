# Claude Skills

Skille dla [Claude Code](https://claude.com/claude-code).

## fragrance-advisor: Portret zapachowy

Osobisty doradca perfum. Zamiast pytań na czacie dostajesz elegancką ankietę. Po jej wysłaniu Claude:

- buduje Twój profil zapachowy na dzień, do pracy i na wieczór,
- szuka pasujących perfum na Fragrantice (piramidy nut, „People who like this also like”) i w sklepach,
- przygotowuje interaktywny **Portret zapachowy**: piramidy nut, wykres rodzin zapachowych i 18 perfum. W każdym trybie są po trzy perfumy w trzech półkach cenowych (budżetowe, designerskie, niszowe), w dwóch wariantach: dokładne i podobne dopasowanie.

Portret pojawia się w tym samym miejscu co ankieta, zwykle po 15–30 minutach.

### Wymagania

- **Claude Code w aplikacji desktopowej Claude**. Wbudowana przeglądarka jest potrzebna do Fragrantiki, która blokuje zwykłe zapytania. Zamiast niej może być Claude in Chrome.
- Zalogowanie kontem claude.ai: ankieta i portret są publikowane jako artefakty.
- **Windows**. Do obróbki zdjęć wystarczy PowerShell, który jest w systemie. Na macOS i Linuksie potrzebny jest Python z pakietami Pillow i numpy (`scripts/fragrantica_images.py`); ta ścieżka nie była jeszcze testowana.

### Instalacja

Skopiuj folder `skills/fragrance-advisor` do folderu skilli Claude Code:

- Windows: `C:\Users\<Ty>\.claude\skills\fragrance-advisor\`
- macOS / Linux: `~/.claude/skills/fragrance-advisor/`

Przykład z klonowaniem repozytorium:

```bash
git clone https://github.com/patrycja-szymecka/claude-skills.git
```

```bash
cp -r claude-skills/skills/fragrance-advisor ~/.claude/skills/
```

Na Windowsie możesz też pobrać repozytorium jako ZIP (Code → Download ZIP) i przenieść folder ręcznie. Potem otwórz **nową** sesję Claude Code.

### Użycie

Napisz np. **„Pomóż mi dobrać perfumy”**, „Szukam zapachu na prezent” albo „Coś podobnego do moich ulubionych perfum”.

1. Claude da Ci link do ankiety. Otworzy ją też w panelu obok.
2. Wypełnij ankietę i kliknij **Wyślij**.
3. Zostaw sesję otwartą i poczekaj na stronie ankiety. Pojawi się tam przycisk **„Otwórz portret”**.

Przy pierwszym użyciu Claude poprosi o zgodę na przeglądarkę, PowerShell i publikację artefaktów.

Ankietę możesz też udostępnić innym osobom: w menu Share daj im dostęp **Contributor**. Żeby ich portrety powstawały bez Twojego udziału, skill potrafi ustawić zadanie w tle. Opis jest w `skills/fragrance-advisor/references/remote-task.md`.

### Struktura

```
skills/fragrance-advisor/
├── SKILL.md                  # instrukcja główna
├── references/               # wywiad, drzewo efektów, profil, wyszukiwanie, półki cenowe
├── assets/
│   ├── questionnaire.html    # ankieta (artefakt z bazą odpowiedzi)
│   └── report-template.html  # szablon portretu
└── scripts/
    ├── build_report.ps1      # zdjęcia + ikony + składanie portretu (Windows)
    └── fragrantica_images.py # to samo w Pythonie (macOS / Linux)
```

Zdjęcia perfum i nut pochodzą z Fragrantiki i są osadzane w portrecie do prywatnego użytku osoby, dla której powstał.
