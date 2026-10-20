# Preview site builder
Add one JSON file per business in `sites/` (copy an existing one, change content, images and theme),
then run `python3 _builder/build.py` from the repo root. Each business gets its own folder with
Home, Services, About, Contact and Thanks pages. Netlify serves every folder at /<slug>/.

## Real photos and logo
Put the business's own photos (from their Google Business Profile or Facebook page) into `<slug>/img/`:
`logo.png`, `hero.jpg`, `about.jpg`, `about2.jpg`, `gallery-1.jpg` … `gallery-6.jpg`, `svc-<service id>.jpg`
(.jpg/.png/.webp). Rebuild with `python3 _builder/build.py _builder/sites/<slug>.json` and they replace the stock images.

## Layout
`theme.layout` in each JSON picks the composition (nav, hero, services, why, gallery, reviews, hours, cta, footer,
pagehead, decor, buttons, section order). Options are listed at the top of `build.py`.
