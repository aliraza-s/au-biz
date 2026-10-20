# Daily preview run (instructions for Claude)

Goal: build 5 new preview websites per day for leads in the Google Sheet
"AU Leads – Master Tracker" (Drive file id 1w7IjqXy6khEPR9OfoEJ9K0KNIl8HWfrwwzecnLM7nrI, tab "Leads"),
push them to this repo (aliraza-s/au-biz, branch main; GitHub Pages publishes to https://aliraza-s.github.io/au-biz/<slug>/),
and record them in the sheet.

1. Read the sheet (Drive read_file_content). Pick 5 rows where Status = "New" and Preview folder is empty.
   Work top to bottom (the sheet is already in priority order). Prefer "No site", "DOWN", "GONE", "UNFINISHED", "EMPTY" statuses.
   Skip migration agents unless no other rows are left.
2. For each business, research real details: Google Places search (name + town) for rating, review count,
   hours, address and 4-6 real review excerpts; web search for services, owner first name, socials.
   Never invent prices, awards, licences or staff names.
3. Write _builder/sites/<slug>.json by copying the structure of an existing JSON file.
   - Each site needs a DIFFERENT look: pick a new palette, font pair (Google Fonts) and a logo icon
     (see _builder/icons.py; add a new simple SVG icon there if none suits the trade).
   - Also set theme.layout (see the docstring at the top of build.py for every option):
     nav, hero, stats, services, why, gallery, reviews, hours, cta, footer, pagehead, decor, btn, order, eyebrow.
     Run `grep -h '"hero"\|"services"\|"nav"' _builder/sites/*.json | sort | uniq -c` and choose a combination
     (hero + services + why + nav) that no existing site in the same trade uses. If layout is missing, build.py
     derives one from the slug, but pick it deliberately so the 5 daily sites all look different from each other.
   - Real photos beat stock: if Ali has dropped photos/logo into <slug>/img/ (hero.jpg, about.jpg, about2.jpg,
     gallery-1..6.jpg, svc-<id>.jpg, logo.png) build.py uses them automatically. Otherwise use Unsplash as below.
   - Photos: Unsplash photo IDs that match the trade. Find them by WebFetch of
     https://unsplash.com/s/photos/<trade-keyword> and use only IDs that appear on that page
     (images.unsplash.com/photo-<id>), never plus.unsplash.com.
   - Footer credit is automatic ("Developed with ❤ by Mr. Developer" -> gemprogrammers.com).
4. Run `python3 _builder/build.py _builder/sites/<slug>.json` for each, screenshot index + contact at 390px and
   1366px with Playwright (executablePath /opt/pw-browsers/chromium; stub unsplash/fonts/maps requests)
   and fix any horizontal overflow or broken layout.
5. Commit ("Add previews: <names>") and push to main.
6. Update the sheet rows by HEADER NAME (column letters can change, read row 1 first):
   "Preview folder" = slug, "Site built on" = today's date (YYYY-MM-DD), "Status" = "Site built". Use the Google Sheets connector if available; otherwise use Claude in Chrome
   on the sheet (Name box -> cell -> type value). Do not touch the formula columns (Follow-up due, Preview link, Message to send, WhatsApp, Google Maps) or the Netlify address cell.
   If neither works, list the 5 slugs + links in the final message so Ali can paste them.
7. Final message (Roman Urdu, short): the 5 businesses with their live links.
