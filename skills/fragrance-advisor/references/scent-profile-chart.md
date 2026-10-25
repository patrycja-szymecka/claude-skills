# Scent profile and chart

Turn the interview into numbers: a share for each scent family and note in a **base profile**, then three variants of it (day, work, evening), each with its own family chart, target pyramid and three key notes. These feed the search and the interactive report.

The 13 families and their notes are in [profile-to-notes.md](profile-to-notes.md).

## 1. Score the families

Each source gives points to families. Multiply by the source's weight and add everything up.

| Source | Points | Weight |
|---|---|---|
| Reference perfume ("something like X") | its main accords on Fragrantica, mapped to families: 3 / 2 / 1 for the top three | ×4 |
| Effect leaf ([effects-tree.md](effects-tree.md)), leading direction | families listed in the leaf: 3 / 2 / 1 | ×3 |
| Effect leaf, second direction (if any) | same | ×1.5 |
| Liked notes | +1 per note to its family | ×3 |
| Liked perfumes (other than the reference) | their top three accords: 3 / 2 / 1 | ×2 |
| Notes shared by liked perfumes | a note in at least half of their liked perfumes (min. 2) counts as a liked note: +1 to its family | ×3 |
| Setting ("Lean on" column) | +1 per note to its family | ×2 |
| Season / time | +1 per listed family | ×2 |
| Temperament ([hidden-profiling.md](hidden-profiling.md)) | +1 per listed family | ×1 |
| Sensory answers (H4–H6) | +1 per listed family | ×1 |
| Zodiac element | +0.5 per listed family | ×1 |
| Age | +0.5 to one or two fitting families | ×1 |

Then apply the limits, in this order:
1. **Dislikes**: a family the user rejected outright ("nothing sweet" → Gourmand) goes to 0. A single disliked note only removes that note.
2. **Setting**: if the setting excludes most of a family's notes (e.g. Leather/Smoky in close-contact work), halve the family.
3. **Normalise** to 100% and round to whole numbers.
4. Merge families under 4% into **Other**. Show at most 8 slices.

Don't show the arithmetic to the user; it's your working.

## 2. Pick the notes

For each family slice, choose 1–3 notes and split the family's share between them. Take notes in this order:
1. notes the user named as liked,
2. the effect leaf's pyramid,
3. the reference perfume's pyramid,
4. the zodiac accent note (one at most, only if it fits),
5. the family's list in profile-to-notes.md.

Skip excluded notes. Show at most 10 notes; put the rest into **Other**.

## 3. Derive the three modes

The base profile is who they are; the modes are how it shifts across a day. Start each mode from the base family scores (before normalising) and apply its modifiers, then normalise, merge small slices and pick notes as in steps 1–2.

| Mode | Raise (×1.5) | Lower (×0.5) | Sillage cap |
|---|---|---|---|
| **Day** (`day`) | Citrus, Green/Aromatic, Aquatic/Ozonic, White Floral | Amber, Leather/Smoky, Gourmand | moderate |
| **Work** (`work`) | Musky, Woody, Powdery | Gourmand, Leather/Smoky, Amber; any note the setting excludes | skin (close-contact work) or moderate |
| **Evening** (`evening`) | Amber, Leather/Smoky, White Floral, Woody | Citrus, Aquatic/Ozonic, Green/Aromatic | strong (capped by setting) |

- If the user's arc answer ([effects-tree.md](effects-tree.md)) describes a change over time, the evening mode carries the full arc and the day mode keeps only its opening.
- Dislikes and exclusions apply to every mode.
- If the user said they'll never wear it to work (or have no work setting), still build the mode, framed as "everyday close to the skin".

## 4. Build each mode's pyramid and key notes

- **Pyramid**: head 2 notes, heart 3, base 4 (the report's layout expects exactly these counts). Place each chosen note on its usual level from the families table, highest share first. If a level is short, take the next note of a family that usually sits there.
- **Anchors** for search stage 1: the highest-share note on each level.
- **Key notes**: the three highest-share notes of the mode, preferably not all from the same level. They get the large medallions and the "learn more" sheets, so each needs a short "how it smells" and a personal "why it's in your portrait" (link it to their liked perfumes, an answer, or the arc).
- **Sillage target** from the mode's cap and the effect leaf, whichever is lower.

The three modes usually share the same signature note (here: orange blossom). That's good: it's the thread through the portrait. Let the key notes around it differ.

## 5. Into the report

Charts and pyramids go into the report's data block (`MODES` in [assets/report-template.html](../assets/report-template.html)), not into the chat:
- `fam`: `[familyKey, percent]` pairs, largest first, adding up to 100.
- `pyr`: three arrays of note keys (2, 3, 4).
- `keys`: three `[noteKey, one-line hook]` pairs.

Translate family names into the user's language (in `FAM`); note names stay in English in `name`, with the display name in the user's language in `label`. If you can't produce the report at all, fall back to a text table per mode in chat (one █ per 5%, rounded) plus the pyramid.

### Family colours

Warm, muted, and the same in every report:

| Family | Key | Colour |
|---|---|---|
| White Floral | `white` | #E6D1B6 |
| Citrus | `citrus` | #DFB25A |
| Floral | `floral` | #CF9597 |
| Green/Aromatic | `green` | #A7AB89 |
| Woody | `wood` | #8B6A59 |
| Amber | `amber` | #C2884E |
| Musky | `musk` | #B7AAA2 |
| Leather/Smoky | `leather` | #5C4148 |
| Powdery | `powder` | #C7B0C1 |
| Fruity | `fruity` | #D9997A |
| Gourmand | `gourmand` | #B98B6E |
| Aquatic/Ozonic | `aquatic` | #9DB4B8 |
| Spicy | `spicy` | #B5674F |
| Other | `other` | #DDD4C9 |