# TheoBox · Today section (Carousel to TheoBox)

Interactive prototype of the **TheoBox** promotional section for the Theo app's **Today** screen: it introduces the TheoBox speaker and its 9 Theolings, and sends parents to the web to buy.

- **Live prototype:** https://theo-home-theobox.vercel.app
- **Developer mode (inspect + download assets):** https://theo-home-theobox.vercel.app/theobox.html?dev
- Light: `theobox.html` · Dark: `theobox-oscuro.html`

> This is a **design prototype in HTML**, not production code. Use it as the visual and behavioural spec; build it natively with Theo's design system.

---

## Developer mode

Open the prototype on a computer. The panel on the right is the handoff tool:

| Action | How |
| --- | --- |
| Inspect a layer | Click **`</>`** in the panel (or press **⇧D**), then click anything in the TheoBox section |
| See distances | With a layer selected, hover another one — distances appear in red |
| Clear selection | `Esc` |
| Tap the app while inspecting | **Use app** |
| Light / dark | Sun / moon buttons in the panel header |
| Share a link that opens in dev mode | Link button (copies `…/theobox.html?dev`) |

For each layer the panel shows **size and position (pt)**, padding, gap, corner radius, **typography** (font, size, weight, line height, letter spacing, color), colors in hex, borders, shadows, **the analytics event** of that card, and — for images — a **thumbnail with @2x/@3x downloads**. **Copy CSS** copies the main properties.

**Download section (.zip)** gives you every asset at @2x and @3x plus `specs.json` (measures of every layer) and a short README.

Units: **1 pt = 1 CSS px** on the 390 × 844 pt phone.

---

## What the section does

Placed **right after Daily Missions** on Today (the Advent card and everything below moved down; nothing else in the home changed).

1. **Header** – “✦ New ✦” label, **Meet TheoBox**, “Place one of 9 Theolings on top and its Bible story begins.” and a **Shop now** button. On the right, the TheoBox speaker with a Theoling standing on its center ring and a soft yellow glow.
2. **Carousel** (horizontal, native scroll-snap, ~3 cards visible):
   1. **How it works** (double width) – child placing a figure on the speaker
   2. – 10. one square card per Theoling: Jesus, Theodore, David, Noah, Good Shepherd, Mary, Joseph, Baby Jesus, St. Michael
   11. **Bring TheoBox home** (double width) – speaker + figures and **Choose yours →**
3. **Interaction** – when the row is scrolled, the first visible Theoling jumps onto the speaker in the header and the ring lights up. On first appearance the cards enter with a short stagger (disabled with *Reduce Motion*).
4. **Tap any card or Shop now** → in-app browser to the web (simulated here; production URLs and `destination_id` values are still to be defined).
5. Soft wave background behind the section (two gentle curves, vertical fade into the page).

### Analytics (per Product ticket, 2026-11-10)

| Event | When |
| --- | --- |
| `eng_theobox_carousel_<card_id>_click` | Once per deliberate tap on a card, **before** opening the web. Scrolling never counts. |
| `eng_theobox_carousel_card_view` | Card ≥ 50 % visible for 1 continuous second, foreground, once per card per screen visit |
| `eng_theobox_section_shop_now_click` | *Shop now* button — **not in the ticket, confirm with Product** |

Properties: `placement`, `carousel_id=theobox_shop`, `card_id`, `card_position`, `creative_id`, `creative_version`, `destination_id`, `app_language`.
`card_id` values: `lifestyle`, `jesus`, `theodore`, `david`, `noah`, `good_shepherd`, `mary`, `joseph`, `baby_jesus`, `archangel_michael`, `complete_box`.
In the prototype the events are printed to the browser console.

### Design tokens used

- Fonts: **Neue Montreal** (titles, labels, buttons) and **Mulish** (body).
- Title `#00516D`, text `#2F5B6B`, accent teal `#1E8DA5`, honey button `#F5DB78` / `#06325A`, card `#FFFFFF` with curve `#BBD6EB`-family blue; dark theme equivalents in `theobox-oscuro.html`.

---

## Repository

```
theobox.html / theobox-oscuro.html   the Today screen with the section (light / dark) — generated
theobox-dev.js / theobox-dev.css     developer mode (inspector, distances, downloads, panel)
assets/theobox/                      images used by the section (WebP)
assets/theobox/dev/                  handoff assets: transparent PNGs @2x/@3x
source/home-light.html, home-dark.html   the current Theo home this is inserted into
tools/build.py                       rebuilds both pages from source/ (python3 tools/build.py)
expo-viewer/                         Expo Go app that opens the live prototype full screen
vercel.json                          "/" → theobox.html
```

### Run locally

```bash
python3 tools/build.py          # only if you changed tools/build.py
python3 -m http.server 5208     # then open http://localhost:5208/theobox.html
```

### Try it on an iPhone (Expo Go)

```bash
cd expo-viewer && npm install && npx expo start --lan
```
Scan the QR with the iPhone camera (same Wi-Fi). It loads the live Vercel prototype.

### Fonts

**Neue Montreal is a licensed font and is not included in this public repo.** Locally the page falls back to Mulish; the live prototype has the right font. Ask the team for the `.otf` files and put them in `assets/` (names are referenced in `fonts.css`).

---

## Open items

- Production purchase URLs and `destination_id` per card.
- App → web sign-in handoff (open question in the ticket).
- Copy: “Choose yours” is shorter than the ticket's “Choose your TheoBox” to fit the card.
- Character lines/short names to be reviewed by Content.

Contact: César (Design) — questions in the Engineering Slack channel.
