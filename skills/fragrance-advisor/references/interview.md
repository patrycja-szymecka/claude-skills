# Interview

Three rounds. Use `AskUserQuestion` when available; otherwise ask as a short numbered list in chat. `AskUserQuestion` allows at most 4 questions per call and 2–4 options per question (the user can always type "Other"), so the options below are already sized for it. Use `multiSelect` where marked.

Skip anything the user already told you. Every question is optional; if they skip one, use a neutral default and move on. Don't ask about budget: everyone gets three perfumes per price tier at the end.

If the scent is a **gift**, ask the same questions about the recipient ("what is she/he/they like?"), and drop the questions the user can't reasonably answer for someone else (the hidden profile questions can stay, rephrased as "how would you describe them?").

## Round 1: basics

1. **Who is it for?** — for me / a gift.
2. **Which line?** — women's / men's / unisex / doesn't matter. Maps to Fragrantica's gender filter. Never assume from the name.
3. **Age range** — under 25 / 25–40 / 40–55 / 55+.
4. **Where will you wear it most?** — office or formal work / creative or casual work / close-contact work (healthcare, teaching, hospitality, childcare) / evenings and events. Free text via "Other": student, outdoor work, working from home, etc.

Second call:

5. **Season(s)** (`multiSelect`) — spring / summer / autumn / winter.
6. **Time of day** — day / evening and night / both.
7. **Perfumes you love or have loved** — free text. If they name one, offer the "something like X" shortcut from SKILL.md.
8. **Notes or perfumes you can't stand** — free text, e.g. "too sweet", "oud", "smells like my grandmother". Translate vague dislikes into notes or families using [profile-to-notes.md](profile-to-notes.md); these become exclusions.

9. **Name** — "What name should go on your portrait?" (for a gift: the recipient's name). Optional; it appears on the cover and in the running head. If they skip it, the cover shows only "Portret zapachowy". Never take a name from an email address, account or anywhere else they didn't give it.

For 7, 8 and 9, free text works better in chat than in `AskUserQuestion`, so ask them together as one plain message.

## Round 2: the effect

Walk the tree in [effects-tree.md](effects-tree.md): first the main direction, then one or two refining questions, then the arc question. This is the heart of the interview, so take the extra question if the answer is ambiguous.

Level 1 uses `multiSelect`, which can't cap the number of picks. If the user picks one, go on. If they pick two or more, ask in one call "which matters most?" and "and second?", then follow the tree for the first and only level 2 for the second.

If the user answers a tree question with their own words instead of an option, that answer wins: build the pyramid from it directly rather than forcing it into the nearest leaf.

## Round 3: hidden profile

Ask 3–4 light questions from [hidden-profiling.md](hidden-profiling.md), phrased casually ("a few quick ones to get a feel for your style"). Don't explain what they map to. Also ask for their date of birth (day and month are enough), optional, without a reason attached; if they skip it, skip the zodiac layer.

## After the interview

Don't show a summary or ask for confirmation. Write the brief for yourself (setting, season, effect, arc, likes, dislikes, hidden profile) and go straight to scoring and search. Tell the user only one short line, e.g. "Thanks, I'm putting your report together; it'll take a few minutes."

If an answer was ambiguous enough that it would change the search, ask that one question before you go quiet, not a summary.
