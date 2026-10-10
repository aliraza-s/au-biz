# Preview site builder
Add one JSON file per business in `sites/` (copy an existing one, change content, images and theme),
then run `python3 _builder/build.py` from the repo root. Each business gets its own folder with
Home, Services, About, Contact and Thanks pages. Netlify serves every folder at /<slug>/.
