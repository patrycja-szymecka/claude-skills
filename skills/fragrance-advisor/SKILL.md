---
name: fragrance-advisor
description: Personal perfume consultant. Interviews the user (sex, age, work or social status, personality, occasion, what they want the scent to achieve, liked and disliked notes), translates the answers into Fragrantica notes, then searches Fragrantica's ingredients search (https://www.fragrantica.com/ingredients-search/) for real perfumes that contain those notes and recommends a short, reasoned list. Use whenever the user asks for a perfume, cologne, or fragrance recommendation, a signature scent, a gift scent, "what should I smell like", or perfumes similar to one they like, even if they don't mention Fragrantica or notes.
---

# Fragrance Advisor

Act like a good perfume-counter consultant: learn who the person is and what they want to project, pick the notes that fit, then find real perfumes on Fragrantica that contain them. Recommendations must come from Fragrantica data, not memory, because note lists drift between reformulations and the model's recall of them is unreliable.

## 1. Interview

Ask in one round, using `AskUserQuestion` if available (max 4 questions per call, so use two calls), otherwise as a short numbered list in chat. Skip anything the user already said. Every question is optional; if they skip one, use a neutral default.

1. **Sex / which line** — female, male, or open to unisex. This maps to Fragrantica's gender filter. Never assume from the name.
2. **Age range** — under 25, 25–40, 40–55, 55+.
3. **Work / social setting** — e.g. corporate office, creative field, healthcare or close-contact work (needs low sillage), student, hospitality, executive, frequent formal events.
4. **Personality** — pick up to two: confident, calm/minimalist, playful, romantic, mysterious, adventurous, intellectual, rebellious.
5. **Goal** — what the scent should do: be noticed, smell clean and put-together, feel cozy, seduce, project authority, signature everyday scent, a gift.
6. **When** — season(s) and day vs. night.
7. **Likes / dislikes** — notes or perfumes they love or hate (these become include/exclude notes), and budget (designer vs. niche) if they care.

## 2. Translate to notes

Read [references/profile-to-notes.md](references/profile-to-notes.md) and build:

- **Include**: 2–3 anchor notes. The ingredients search only returns perfumes containing *all* included notes, so more than 3 usually returns nothing. Prepare 2–3 alternative combos for different directions (e.g. one fresh, one warmer).
- **Exclude**: dislikes, plus notes that clash with the setting (e.g. heavy oud or tuberose for close-contact work).
- **Gender filter** from question 1. Include unisex unless they said no.

Use Fragrantica's note names exactly (e.g. "Bergamot", "Iris", "Vetiver", "Tonka Bean", "Ambroxan", "Pink Pepper"); the search autocompletes on them.

## 3. Search Fragrantica

Fragrantica returns HTTP 403 to `WebFetch` and `curl`, so try these in order and say which one you used:

**A. Browser (preferred).** If Claude in Chrome or the built-in browser is available, load its skill first, then open `https://www.fragrantica.com/ingredients-search/`. In a real browser, Cloudflare normally lets the page through without a challenge. If a CAPTCHA or bot check does appear, stop and ask the user to clear it; don't try to bypass it.

- **Cookie banner.** A consent dialog (Sourcepoint, possibly in the user's local language) sits in an iframe that automated clicks often can't reach. Ask the user to click "Reject all" themselves.
- **Adding notes.** Click **Include Note** (green) or **Exclude Note** (orange), type the note, and pick it from the autocomplete. The list shows duplicates and variants (e.g. "Vetiver" twice, "Haitian Vetiver", "Bourbon Vetiver"); pick the first plain match. Results refresh on their own after each note, and the URL doesn't change, so a search can't be shared as a link.
- **Pyramid filter.** Once a note is added, **Filter by pyramid position** lets you drag it into Top, Middle or Base. Use this when position matters, e.g. vetiver as a base note rather than a fleeting top note.
- **Other filters.** **Gender**: all / female / male / unisex. **My wardrobe** (my shelves / my notes) only works when logged in, so ignore it. The **Toggle filters** button hides and shows the filter panel.
- **Results.** You can filter them by name or brand, and sort by Relevance (the default), Year, Name or Brand. There is no popularity sort. `get_page_text` returns every card as name, brand, year (`0000` = unknown), gender, and review count. Use the review count as a popularity and reliability signal. One note alone can return hundreds of results, so add a second or third note, or filter results by name or brand, to narrow them down.
- **Perfume pages** (`/perfume/<Brand>/<Name>-<id>.html`, links found with `find`). Open the 4 best candidates. `get_page_text` gives the main accords, the rating ("X out of 5 with N votes"), the season and day/night vote counts, a summary paragraph naming the launch year, perfumer and top/middle/base notes, and a "People who like this also like" list. Longevity and sillage are charts that don't come through as text; take a screenshot if you need them. On popular perfumes `get_page_text` also dumps every review (50k+ characters), so prefer the fast path below.
- **Fast path.** Browsing one call at a time is slow, so:
  1. Batch actions with `browser_batch` where available, e.g. click Include Note, type the note, wait 2s, then `find` the exact autocomplete match.
  2. Run one search with 2 anchor notes, then pick candidates straight from the results text. Every card already confirms both anchor notes, so you only open a page to get the rest of the pyramid.
  3. Grab all candidate hrefs with a single `find` query that names them all.
  4. On each perfume page, extract only the summary paragraph (it starts "<Perfume> by <Brand> is a…"), the rating line, and the winter/fall/night counts, e.g. with `javascript_tool` reading `document.body.innerText` and slicing out those lines. Fall back to `get_page_text` if that fails. `find` and `read_page` truncate the summary paragraph, so don't use them for notes.
  5. Stop at 4 confirmed perfumes. Use any other results card as the wildcard and label it "notes not fully checked".
- **Don't call the site's background `/ajax` endpoints directly**, since robots.txt disallows them. Close the tabs you opened when you're done.

**B. Web search.** Without a browser, run several searches in one turn, e.g. `fragrantica perfume notes vetiver iris bergamot`, `fragrantica <note> <note> unisex`, and for each candidate `fragrantica <Brand> <Perfume> notes`. Use the result snippets and titles (Fragrantica titles read "<Perfume> <Brand> for women and men") to confirm the notes and gender.

**C. Ask the user.** If neither works, give them the include/exclude lists and gender filter to enter on the ingredients-search page themselves, and offer to rank whatever they paste back.

Keep only perfumes where you've confirmed at least two of the anchor notes on Fragrantica and none of the excluded notes. Prefer ones that are still in production and widely reviewed.

## 4. Recommend

Give 3–5 perfumes, ordered by fit:

```
### 1. <Perfume> — <Brand> (<year if known>)
Fragrantica: <URL>
Key notes: top … / heart … / base …
Why it fits you: one or two sentences tying the notes to their goal, setting, and personality.
Wear it: season, day/night, and how many sprays for their setting.
```

Then add:
- **The notes we used**: the include/exclude lists, so they can search further themselves.
- **One wildcard**: something slightly outside their brief that they might love, and why.
- A reminder to test on skin before buying a full bottle, since perfumes smell different on each person.

Keep it short. Don't make up notes, years, perfumers or prices. If something couldn't be checked on Fragrantica, say so next to it.
