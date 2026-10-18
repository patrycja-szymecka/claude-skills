# Hidden profile

A light layer that nudges the profile toward the person's temperament and, optionally, their star sign. The user sees only casual questions; don't name the personality types, the zodiac mapping or the scoring. If they ask directly why you asked something, answer honestly ("it helps me guess which moods of scent suit you").

If the user brings astrology up themselves and enjoys it, you may mention their sign openly in the recommendation.

**Weight**: this layer is a nudge. In [scent-profile-chart.md](scent-profile-chart.md) the temperament counts ×1 and the zodiac ×0.5, against ×3 for the chosen effect and the user's own likes. It never overrides an explicit answer or a dislike. Its best use is breaking ties: choosing between two similar candidates, or picking the one accent note.

## Questions

Pick 3–4. All fit `AskUserQuestion` (4 options). Phrase them casually in the user's language.

**H1. "Your ideal day off?"**
- a) Out with friends, something happening → *Social*
- b) Home, a book, coffee, quiet → *Quiet depth*
- c) Somewhere new, a trip or a new place → *Explorer*
- d) A plan ticked off, sport, things in order → *Strategist*

**H2. "Which three words fit you best?"**
- a) Warm, caring, empathetic → *Caregiver*
- b) Ambitious, decisive, direct → *Strategist*
- c) Creative, curious, unpredictable → *Explorer*
- d) Calm, thoughtful, balanced → *Quiet depth*

**H3. "At a party where you know almost no one, you…"**
- a) Meet everyone → *Social*
- b) Have one long conversation in a corner → *Quiet depth*
- c) Watch people first, then choose → *Enigma*
- d) Help the hosts, look after others → *Caregiver*

**H4. "The place you'd rather be right now?"** (maps straight to families)
- a) By the sea → Aquatic/Ozonic, Citrus
- b) In a forest or mountains → Woody, Green/Aromatic
- c) A city at night → Leather/Smoky, Amber, Spicy
- d) A garden in bloom → Floral, Fruity

**H5. "The fabric you like to wear most?"** (maps straight to families)
- a) Linen, cotton → Citrus, Musky (clean)
- b) Cashmere, wool → Musky, Woody, Gourmand
- c) Silk, satin → Floral, Powdery, Amber
- d) Leather, denim → Leather/Smoky, Woody

**H6. "Colours you wear most?"** (maps straight to families)
- a) White, beige, pastels → Musky, Powdery, Floral
- b) Earth tones, greens → Woody, Green/Aromatic
- c) Deep reds, burgundy, gold → Amber, Spicy, Floral
- d) Black, navy, grey → Woody, Leather/Smoky, Aquatic/Ozonic

If two answers point to the same temperament, that's the main one; otherwise take the two most frequent.

## Temperaments → families

| Temperament | Scent mood | +1 to families | Sillage nudge |
|---|---|---|---|
| Social | Bright, open, warm | Citrus, Fruity, White Floral, Gourmand | up |
| Quiet depth | Close, soft, layered | Musky, Woody, Powdery | down |
| Explorer | Unusual, spiced, a bit raw | Spicy, Green/Aromatic, Leather/Smoky | — |
| Strategist | Structured, dry, clean lines | Woody, Green/Aromatic, Citrus | — |
| Caregiver | Gentle, comforting | Powdery, Musky, Floral, Gourmand | down |
| Enigma | Dark, cool, ambiguous | Amber, Woody, Leather/Smoky | — |

## Zodiac

Ask for the date of birth (day and month are enough), without a reason. If they skip it, skip this section.

Use the **element** for families (+0.5 each) and the **sign's accent** as a tie-breaker for the one standout note.

| Sign | Dates | Element | Accent notes |
|---|---|---|---|
| Aries | 21 Mar – 19 Apr | Fire | Pink Pepper, Ginger, Black Pepper |
| Taurus | 20 Apr – 20 May | Earth | Rose, Vanilla, Tonka Bean, Sandalwood |
| Gemini | 21 May – 20 Jun | Air | Bergamot, Mint, Lavender, Aldehydes |
| Cancer | 21 Jun – 22 Jul | Water | Lily-of-the-Valley, White Musk, Milk, Sea Notes |
| Leo | 23 Jul – 22 Aug | Fire | Saffron, Orange Blossom, Amber, Tuberose |
| Virgo | 23 Aug – 22 Sep | Earth | Tea, Iris, Vetiver, Sage |
| Libra | 23 Sep – 22 Oct | Air | Iris, Peony, Pear, Powdery Notes |
| Scorpio | 23 Oct – 21 Nov | Water | Patchouli, Agarwood (Oud), Incense, Leather |
| Sagittarius | 22 Nov – 21 Dec | Fire | Cardamom, Cinnamon, Benzoin, Cedar |
| Capricorn | 22 Dec – 19 Jan | Earth | Vetiver, Oakmoss, Leather, Cypress |
| Aquarius | 20 Jan – 18 Feb | Air | Ozonic notes, Iso E Super, Metallic notes, Violet Leaf |
| Pisces | 19 Feb – 20 Mar | Water | Sea Notes, Lotus, Ambergris, Musk |

| Element | +0.5 to families |
|---|---|
| Fire | Spicy, Amber, Leather/Smoky |
| Earth | Woody, Green/Aromatic, Gourmand |
| Air | Citrus, Aquatic/Ozonic, Powdery |
| Water | Aquatic/Ozonic, Musky, Floral |
