# Claude Skills

Skills for [Claude Code](https://claude.com/claude-code).

## fragrance-advisor: Portret zapachowy (Scent Portrait)

A personal perfume advisor. Instead of answering questions in chat, you fill in a styled questionnaire. Once you send it, Claude:

- builds your scent profile for day, work and evening,
- searches Fragrantica (note pyramids, "People who like this also like") and shops for matching perfumes,
- prepares an interactive **Portret zapachowy**: note pyramids, a scent family chart and 18 perfumes. Each mode has three perfumes across three price tiers (budget, designer, niche), in two variants: exact and similar match.

The portrait appears in the same place as the questionnaire, usually after 15–30 minutes. The questionnaire and the portrait are in Polish.

### Requirements

- **Claude Code in the Claude desktop app**. The built-in browser is needed for Fragrantica, which blocks plain requests. Claude in Chrome works instead.
- Signed in with a claude.ai account: the questionnaire and the portrait are published as Artifacts.
- **Windows**. Image processing only needs PowerShell, which comes with the system. On macOS and Linux you need Python with Pillow and numpy (`scripts/fragrantica_images.py`); that path hasn't been tested yet.

### Installation

Copy the `skills/fragrance-advisor` folder into your Claude Code skills folder:

- Windows: `C:\Users\<You>\.claude\skills\fragrance-advisor\`
- macOS / Linux: `~/.claude/skills/fragrance-advisor/`

For example, by cloning the repository:

```bash
git clone https://github.com/patrycja-szymecka/claude-skills.git
```

```bash
cp -r claude-skills/skills/fragrance-advisor ~/.claude/skills/
```

On Windows you can also download the repository as a ZIP (Code → Download ZIP) and move the folder by hand. Then open a **new** Claude Code session.

### Usage

Write something like **"Help me pick a perfume"**, "I'm looking for a scent as a gift" or "Something similar to my favourite perfume".

1. Claude gives you a link to the questionnaire and also opens it in the side panel.
2. Fill it in and click **Wyślij** (Send).
3. Keep the session open and wait on the questionnaire page. An **Otwórz portret** (Open portrait) button will appear there.

On first use Claude will ask for permission to use the browser, PowerShell and publish Artifacts.

You can also share the questionnaire with other people: give them **Contributor** access in the Share menu. To have their portraits made without you starting each one, the skill can set up a background task. See `skills/fragrance-advisor/references/remote-task.md`.

### Structure

```
skills/fragrance-advisor/
├── SKILL.md                  # main instructions
├── references/               # interview, effects tree, profile, search, price tiers
├── assets/
│   ├── questionnaire.html    # questionnaire (Artifact with a response database)
│   └── report-template.html  # portrait template
└── scripts/
    ├── build_report.ps1      # bottles + note icons + portrait assembly (Windows)
    └── fragrantica_images.py # the same in Python (macOS / Linux)
```

Perfume and note images come from Fragrantica and are embedded in the portrait for the private use of the person it was made for.
