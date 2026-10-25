# Search strategy

Four stages, from the strictest match to the loosest. Collect candidates into one list and tag each with the stage it came from; that tag appears in the recommendation as "Match". You need three good perfumes per price tier at the end ([price-tiers.md](price-tiers.md)), so aim for about 15 candidates across the stages, and keep an eye on which tiers are still short.

Before you start, have ready: the target pyramid with an anchor per level, the include and exclude lists, the gender filter and the sillage target ([scent-profile-chart.md](scent-profile-chart.md)).

## Stage 1: exact pyramid

Find perfumes whose notes sit on the same levels as the target pyramid.

1. In Fragrantica's ingredients search, include the **base and heart anchors** and set their pyramid positions (Filter by pyramid position). Base and heart notes define a perfume's character; top notes are fleeting, so add the top anchor only if results are still too many (over ~60).
2. Add the exclusions and the gender filter.
3. If there are no results, relax in this order: drop the top anchor → drop the pyramid positions but keep the notes → swap the weaker anchor for its closest neighbour ([profile-to-notes.md](profile-to-notes.md), "Similar notes").
4. Pick candidates from the results (prefer high review counts) and **open their pages to confirm the levels**: the summary paragraph lists top, middle and base notes. Keep a candidate if the anchors are on the right levels and it has none of the excluded notes.

With a reference perfume ("something like X"), the target pyramid is X's own pyramid; leave X itself out of the results.

## Stage 2: "People who like this also like"

On the pages of the best 2–3 stage-1 perfumes (and of the reference perfume, if there is one), read the **"People who like this also like"** list and, if present, **"This perfume reminds me of"**. These are real users' associations and often surface perfumes that a note search misses.

For each one that looks promising, open its page and check: no excluded notes, at least one anchor somewhere in the pyramid, and main accords that overlap the top families of the profile. Perfumes that appear on several of these lists are especially strong candidates.

## Stage 3: similar aroma

Now look for perfumes that *smell* related even if the notes sit on different levels or are different notes altogether.

- Search the anchors **without** pyramid positions.
- Swap anchors for their neighbours from "Similar notes", one at a time (e.g. Iris → Orris Root or Violet; Vetiver → Cedar).
- On candidate pages, compare **main accords** with the profile's top families. Accept a candidate if at least two of its top three accords match the top families and it has no excluded notes.

This stage is where to fill a short price tier: filter the results by the names of brands from that tier.

## Stage 4: other sources

Use other perfume sites and shops to confirm notes when Fragrantica can't be reached, to find candidates for a short tier, and to get prices.

| Source | Use for |
|---|---|
| Parfumo (parfumo.com) | Note pyramids, ratings, "similar perfumes"; good second opinion to Fragrantica |
| Basenotes (basenotes.com) | Notes and reviews, especially older and men's perfumes |
| Brand websites | Official notes and current formulation |
| Shops: Notino, Douglas, Sephora, and in Poland also Perfumeria Quality, Galilu, Lulua | Notes listed on product pages ("nuty zapachowe"), current prices, availability, sample/miniature sizes |
| Blogs, YouTube reviews | Only for impressions; never as the sole source of notes |

Trust order for notes: Fragrantica ≈ Parfumo ≈ brand site > shops > blogs. If sources disagree, go with Fragrantica and mention the difference only if it matters for the user (e.g. an excluded note).

Prices: take them from shops in the user's country and currency, for the 100 ml (or nearest) size, and write down the shop and today's date. If only another size is sold, give that price and the per-100 ml equivalent. Don't guess a price; if you couldn't check, write "price not checked", optionally with a foreign price you did find ("≈ 216 € / 100 ml in NL").

Getting prices is the slowest part, so be pragmatic:
- Run one web search per candidate, all in the same turn (`<Brand> <Perfume> 100 ml price`, in the user's currency).
- Big shops and price comparison sites (Notino, Douglas, idealo) often block `WebFetch` (403) or show a bot check in the browser. Don't try to get past a bot check; take what the search results show and move on.
- Smaller niche shops (e.g. niche-beauty.com) and brand sites are often readable.

---

## Using Fragrantica

Fragrantica returns HTTP 403 to `WebFetch` and `curl`, so try these in order and tell the user which one you used:

**A. Browser (preferred).** If Claude in Chrome or the built-in browser is available, load its skill first, then open `https://www.fragrantica.com/ingredients-search/` in a **background tab** (don't bring it to the front) and work from page text, not screenshots, so the user isn't watching the browsing. Open each perfume page in that same tab rather than a new one. In a real browser, Cloudflare normally lets the page through. If a CAPTCHA or bot check appears, don't try to bypass it; switch to option B. If the page looks different from what's described here, use `read_page` to see what's there and adapt.

- **Cookie banner.** A consent dialog (Sourcepoint, possibly in the user's language) may cover the page. Never ask the user to deal with it, and never remove or hide it with a script. Instead:
  1. Try clicking **"Reject all"** by its coordinates from a screenshot (rejecting is the privacy-preserving choice, so no need to ask).
  2. If the click doesn't reach the iframe, try the keyboard: `Tab` until the button is focused, then `Enter`.
  3. If it's still there, carry on anyway: the banner blocks clicks but not reading. The fast path below (reading pages with in-page `fetch`) works with the banner open. Only the ingredients-search UI needs clicks; if it's unusable, find candidates through the perfume pages' "People who like this also like" lists and web search instead.
  The choice is remembered in the browser profile, so this usually happens only once per machine.
- **Pop-ups.** A "Join our community" dialog may appear; close it with its ✕.
- **Adding notes.** Click **Include Note** or **Exclude Note**, type the note, and pick it from the autocomplete. The list shows duplicates and variants (e.g. "Vetiver" twice, "Haitian Vetiver", "Bourbon Vetiver"); pick the first plain match. Results refresh after each note; the URL doesn't change, so a search can't be shared as a link.
- **Pyramid filter.** Once a note is added, **Filter by pyramid position** lets you drag it into Top, Middle or Base. Stage 1 relies on this.
- **Other filters.** **Gender**: all / female / male / unisex. **My wardrobe** only works when logged in, so ignore it. **Toggle filters** hides and shows the filter panel.
- **Results.** Filter by name or brand; sort by Relevance (default), Year, Name or Brand. There is no popularity sort. `get_page_text` returns every card as name, brand, year (`0000` = unknown), gender and review count. Use the review count as a popularity and reliability signal.
- **Perfume pages** (`/perfume/<Brand>/<Name>-<id>.html`, links found with `find`). `get_page_text` gives the main accords, the rating ("X out of 5 with N votes"), season and day/night votes, a summary paragraph with launch year, perfumer and top/middle/base notes, and the "People who like this also like" list. Longevity and sillage are charts that don't come through as text; take a screenshot if you need them (useful for checking the sillage target). On popular perfumes `get_page_text` also dumps every review (50k+ characters), so prefer the fast path.
- **Fast path** (tested; reads ~40 perfumes in a minute without opening any of them):
  1. **Find a perfume's URL** by navigating the tab to `https://www.fragrantica.com/search/?query=<name brand>`, waiting ~2.5 s, and collecting `a[href*="/perfume/"]` hrefs with `javascript_tool`. Pick the one whose name matches exactly (flankers like "Intense" or "Le Parfum" are different perfumes).
  2. **Collect result cards** from the ingredients search the same way: each card link has an `aria-label` like "Link to <Brand> <Perfume> <gender> <year>". One script returns the whole list; filter out `male` if the user wants women's + unisex.
  3. **Read perfume pages without navigating**: from any fragrantica.com page, `javascript_tool` can `fetch('/perfume/…html')`, parse it with `DOMParser`, and pull out with regexes on the collapsed `textContent`:
     - main accords: text between `main accords` and `Search by accords`,
     - rating: `rating X out of 5 with N votes`,
     - pyramid: `Top notes are …; middle notes are …; base notes are ….` (some perfumes have a flat list instead: `notes are …`),
     - title and gender: `document.title`,
     - "People who like this also like": the names after that heading, separated by ` Compare `.
     - note icon ids for the report: `img[src*="sastojci"]` → `alt` (note name) and the number in `…/t.<id>.jpg`.
     Define the helper once on `window` and reuse it; check pyramid levels and excluded notes in the same script.
  4. **Throttle.** Fragrantica answers HTTP 429 (Too Many Requests) if you fetch too much at once. Fetch at most 3 pages in parallel, then wait ~2 s before the next 3. If you get a 429, wait ~30 s and continue more slowly.
  5. Batch UI steps with `browser_batch`: click Include Note, type the note, wait 2 s, `find` the exact autocomplete match, click it.
  6. To narrow a big result list, don't fight the drag-and-drop pyramid filter; read the candidates' pyramids with step 3 and filter by level there.
- **Don't call the site's background `/ajax` endpoints directly**, since robots.txt disallows them. Close the tabs you opened when you're done.

**B. Web search.** Without a browser, run several searches in one turn, e.g. `fragrantica <note> <note> <note>`, `parfumo <note> <note>`, and for each candidate `fragrantica <Brand> <Perfume> notes`. Fragrantica titles read "<Perfume> <Brand> for women and men", which confirms the gender. Confirm the pyramid on Parfumo or a shop page.

**C. Ask the user.** If neither works, give them the include/exclude lists, pyramid positions and gender filter to enter on the ingredients-search page themselves, and offer to rank whatever they paste back.
