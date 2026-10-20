#!/usr/bin/env python3
"""Builds multi-page preview websites from sites/*.json into ../<slug>/.
Each site = Home, Services, About, Contact (+ thank-you page).

v2: every site gets its own LAYOUT (theme.layout) as well as its own colours/fonts, so no two
previews share the same composition. Layout keys (all optional, derived from the slug if missing):
  nav      bar | center | pill | split | stripe
  hero     split | overlay | center | stack | arch | card | diagonal | mosaic | editorial | frame
  stats    none | strip | pills | ticker
  services cards | tiles | list | bento | side | alt
  why      split | splitR | dark | stackimg | band
  gallery  bento | strip | grid | tilt
  reviews  cards | slider | featured | light
  hours    grid | cards | mapbg
  cta      band | dark | card
  footer   grid | simple | bold
  pagehead solid | image | light
  decor    none | dots | blob | grid | lines
  btn      flat | shadow | arrow
  order    A..F  (home page section order)
  eyebrow  true/false (small label above section headings)

Real photos: drop files into ../<slug>/img/ and they replace the stock photos automatically:
  logo.png|svg|jpg  hero.jpg  about.jpg  about2.jpg  gallery-1.jpg … gallery-6.jpg  svc-<service id>.jpg
(.jpg, .jpeg, .png, .webp all work.)
"""
import json, sys, html, pathlib, urllib.parse, hashlib
from icons import ICONS

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITES = pathlib.Path(__file__).resolve().parent / "sites"
YEAR = 2026
E = html.escape

OPTIONS = {
 "nav": ["bar","center","pill","split","stripe"],
 "hero": ["split","overlay","center","stack","arch","card","diagonal","mosaic","editorial","frame"],
 "stats": ["none","strip","pills","ticker"],
 "services": ["cards","tiles","list","bento","side","alt"],
 "why": ["split","splitR","dark","stackimg","band"],
 "gallery": ["bento","strip","grid","tilt"],
 "reviews": ["cards","slider","featured","light"],
 "hours": ["grid","cards","mapbg"],
 "cta": ["band","dark","card"],
 "footer": ["grid","simple","bold"],
 "pagehead": ["solid","image","light"],
 "decor": ["none","dots","blob","grid","lines"],
 "btn": ["flat","shadow","arrow"],
 "order": ["A","B","C","D","E","F"],
}
ORDERS = {
 "A": ["services","why","gallery","reviews","hours"],
 "B": ["why","services","reviews","gallery","faq","hours"],
 "C": ["services","reviews","why","gallery","faq","hours"],
 "D": ["services","gallery","why","reviews","hours","faq"],
 "E": ["why","services","gallery","reviews","faq","hours"],
 "F": ["services","why","reviews","faq","gallery","hours"],
}

def layout(s):
    """Layout for a site: theme.layout, with slug-derived defaults for anything missing."""
    t = s["theme"]
    h = hashlib.md5(s["slug"].encode()).digest()
    L = {}
    for n, (k, opts) in enumerate(OPTIONS.items()):
        L[k] = opts[h[n] % len(opts)]
    if t.get("hero") in OPTIONS["hero"]:
        L["hero"] = t["hero"]
    L["eyebrow"] = bool(h[15] % 2)
    L.update(t.get("layout", {}))
    return L

IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".svg")

def apply_local_photos(s):
    """If ../<slug>/img/ holds real photos, swap them in for the stock ones."""
    d = ROOT / s["slug"] / "img"
    if not d.is_dir(): return
    def find(stem):
        for ext in IMG_EXT:
            p = d / (stem + ext)
            if p.exists(): return "img/" + p.name
        return None
    i = s["images"]
    for k in ("hero", "about", "about2"):
        p = find(k)
        if p: i[k] = p
    for n in range(len(i["gallery"])):
        p = find(f"gallery-{n+1}")
        if p: i["gallery"][n] = p
    for sv in s["services"]:
        p = find("svc-" + sv["id"])
        if p: sv["img"] = p
    lg = find("logo")
    if lg: s["_logo"] = lg

def img(id_, w=1400):
    if "/" in id_ or id_.lower().endswith(IMG_EXT):
        return id_
    return f"https://images.unsplash.com/photo-{id_}?auto=format&fit=crop&w={w}&q=80"

def logo_svg(s, size=44):
    t = s["theme"]
    if s.get("_logo"):
        return f'<img class="logo-img" src="{E(s["_logo"])}" alt="{E(s["name"])} logo" style="height:{size+4}px">'
    return (f'<svg class="logo-mark" width="{size}" height="{size}" viewBox="0 0 32 32" aria-hidden="true" style="--logo-ink:{t["logoBg"]}">'
            f'<rect width="32" height="32" rx="{t.get("logoRadius",9)}" fill="{t["logoBg"]}"/>'
            f'<g style="color:{t["logoFg"]}" transform="translate(4 4) scale(.75)">{ICONS[t["icon"]]}</g></svg>')

def favicon(s):
    t = s["theme"]
    if s.get("_logo") and not s["_logo"].endswith(".svg"):
        return s["_logo"]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="{t.get("logoRadius",9)}" fill="{t["logoBg"]}"/>'
           f'<g style="color:{t["logoFg"]}" transform="translate(4 4) scale(.75)">{ICONS[t["icon"]].replace("currentColor", t["logoFg"]).replace("var(--logo-ink)", t["logoBg"])}</g></svg>')
    return "data:image/svg+xml," + urllib.parse.quote(svg)

def is_dark(hexcol):
    h = hexcol.lstrip("#")
    if len(h) != 6: return True
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return (0.299*r + 0.587*g + 0.114*b) < 150

def stars(r):
    full = int(round(r))
    return "★" * full + "☆" * (5 - full)

# ---------------------------------------------------------------- CSS
CSS = r"""
:root{--bg:$bg;--surface:$surface;--ink:$ink;--muted:$muted;--brand:$brand;--brand2:$brand2;--accent:$accent;--on-brand:$onBrand;--on-accent:$onAccent;--line:$line;--r:$radius;--rb:$btnRadius;--hf:$headFont;--bf:$bodyFont;--hw:$headWeight;--hbg:$headerBg;--hink:$headerInk}
*{box-sizing:border-box;margin:0}
html{scroll-behavior:smooth}
body{font-family:var(--bf);color:var(--ink);background:var(--bg);line-height:1.6;font-size:17px;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{max-width:100%;display:block}
a{color:inherit}
:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
h1,h2,h3,.hf{font-family:var(--hf);font-weight:var(--hw);line-height:1.08;letter-spacing:$headTrack;$headExtra}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px}
.eyebrow{display:inline-flex;align-items:center;gap:10px;font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:var(--accent);margin-bottom:14px}
.eyebrow:before{content:"";width:26px;height:3px;background:currentColor;border-radius:2px}
.dark .eyebrow,.hero .eyebrow{color:var(--accent)}
/* buttons */
.btn{display:inline-flex;align-items:center;gap:9px;padding:14px 24px;border-radius:var(--rb);font-weight:700;text-decoration:none;border:2px solid transparent;font-size:16px;transition:transform .18s,box-shadow .18s,background .18s;line-height:1.2}
.btn:hover{transform:translateY(-2px)}
.btn-main{background:var(--accent);color:var(--on-accent)}
.btn-ghost{border-color:currentColor}
.btn svg{width:18px;height:18px;flex:0 0 18px}
.btn-shadow .btn-main{box-shadow:5px 5px 0 var(--ink)}
.btn-shadow .btn-main:hover{box-shadow:7px 7px 0 var(--ink)}
.btn-shadow .dark .btn-main,.btn-shadow .hero .btn-main{box-shadow:5px 5px 0 rgba(0,0,0,.45)}
.btn-arrow .btn-main:after{content:"→";font-weight:900;transition:transform .18s}
.btn-arrow .btn-main:hover:after{transform:translateX(4px)}
/* reveal */
.js .rv-up{opacity:0;transform:translateY(22px);transition:opacity .7s ease,transform .7s ease}
.js .rv-up.in{opacity:1;transform:none}
/* top strip + header */
.top{background:var(--brand);color:var(--on-brand);font-size:14px}
.top .wrap{display:flex;justify-content:space-between;gap:12px;padding-top:8px;padding-bottom:8px;flex-wrap:wrap}
.top a{text-decoration:none;font-weight:600}
header.site{position:sticky;top:0;z-index:20;background:var(--hbg);color:var(--hink);border-bottom:1px solid var(--line)}
.nav{display:flex;align-items:center;justify-content:space-between;height:76px;gap:18px}
.brandmark{display:flex;align-items:center;gap:12px;text-decoration:none;min-width:0}
.brandmark b{font-family:var(--hf);font-weight:var(--hw);font-size:21px;line-height:1.05;display:block;$headExtra}
.brandmark small{display:block;font-size:12.5px;opacity:.75;margin-top:2px}
.logo-img{width:auto;max-width:180px;object-fit:contain}
.menu{display:flex;gap:26px;align-items:center;list-style:none;padding:0}
.menu a{text-decoration:none;font-weight:600;font-size:15.5px;padding:6px 0;border-bottom:2px solid transparent}
.menu a[aria-current]{border-color:var(--accent)}
.menu .btn{padding:11px 18px;border-bottom:0}
.burger{display:none;background:none;border:0;color:inherit;padding:8px;cursor:pointer}
.burger svg{width:28px;height:28px}
.nav-phone{display:flex;align-items:center;gap:10px;text-decoration:none;font-weight:800;font-size:19px;font-family:var(--hf)}
.nav-phone svg{width:22px;height:22px}
/* nav: center */
.nav-center header.site .nav{flex-direction:column;height:auto;padding:16px 0 0;gap:10px}
.nav-center .menu{border-top:1px solid var(--line);width:100%;justify-content:center;padding:10px 0 12px;gap:32px}
.nav-center .menu .btn{display:none}
.nav-center .burger{position:absolute;right:16px;top:18px}
/* nav: pill */
.nav-pill header.site{background:transparent;border:0;top:12px;padding:12px 0}
.nav-pill .nav{background:var(--hbg);border-radius:60px;padding:0 10px 0 22px;height:68px;box-shadow:0 12px 36px rgba(0,0,0,.14);border:1px solid var(--line)}
.nav-pill .menu .btn{border-radius:40px}
/* nav: split */
.nav-split .menu{gap:4px}
.nav-split .menu a{padding:9px 14px;border-radius:40px;border:0}
.nav-split .menu a[aria-current]{background:var(--surface)}
.nav-split .menu .btn{display:none}
/* nav: stripe */
.nav-stripe header.site{border-top:6px solid var(--accent);border-bottom:0;box-shadow:0 1px 0 var(--line)}
.nav-stripe .nav{height:92px}
.nav-stripe .brandmark b{font-size:25px}
.nav-stripe .menu a[aria-current]{color:var(--accent)}
/* ---------------- hero ---------------- */
.hero{position:relative;overflow:hidden}
.hero h1{font-size:clamp(40px,6.4vw,$h1max)}
.hero .lede{font-size:clamp(18px,1.6vw,21px);max-width:44ch;margin:20px 0 30px;opacity:.9}
.hero .cta{display:flex;gap:12px;flex-wrap:wrap}
.trust{display:flex;gap:22px;flex-wrap:wrap;margin-top:30px;font-weight:600;font-size:15px}
.trust span{display:flex;align-items:center;gap:8px}
.trust i{font-style:normal;color:var(--accent)}
.hero .wrap{position:relative;z-index:2}
.decor-dots:before,.decor-blob:before,.decor-grid:before,.decor-lines:before{content:"";position:absolute;inset:0;pointer-events:none;z-index:1}
.decor-dots:before{background-image:radial-gradient(currentColor 1.4px,transparent 1.6px);background-size:26px 26px;opacity:.12;mask-image:linear-gradient(100deg,transparent 45%,#000 100%);-webkit-mask-image:linear-gradient(100deg,transparent 45%,#000 100%)}
.decor-blob:before{background:radial-gradient(closest-side,var(--accent),transparent 70%);opacity:.28;inset:auto;width:60vw;height:60vw;top:-25vw;right:-20vw}
.decor-grid:before{background-image:linear-gradient(currentColor 1px,transparent 1px),linear-gradient(90deg,currentColor 1px,transparent 1px);background-size:64px 64px;opacity:.07}
.decor-lines:before{background:repeating-linear-gradient(-45deg,currentColor 0 1px,transparent 1px 18px);opacity:.07;mask-image:linear-gradient(90deg,transparent 55%,#000);-webkit-mask-image:linear-gradient(90deg,transparent 55%,#000)}
.hero-split{background:var(--brand);color:var(--on-brand)}
.hero-split .wrap{display:grid;grid-template-columns:1.05fr .95fr;gap:52px;align-items:center;padding-top:64px;padding-bottom:72px}
.hero-split .pic{position:relative}
.hero-split .pic img{width:100%;aspect-ratio:4/4.4;object-fit:cover;border-radius:var(--r)}
.badge{position:absolute;left:-22px;bottom:28px;background:var(--surface);color:var(--ink);padding:16px 20px;border-radius:var(--r);box-shadow:0 18px 40px rgba(0,0,0,.18)}
.badge b{font-family:var(--hf);font-size:34px;display:block;line-height:1}
.badge small{color:var(--muted)}
.hero-overlay{color:#fff;min-height:min(86vh,760px);display:flex;align-items:flex-end}
.hero-overlay>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.hero-overlay:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.05) 20%,$overlay 92%)}
.hero-overlay .wrap{padding-bottom:70px;padding-top:120px;width:100%}
.hero-center{background:var(--brand);color:var(--on-brand);text-align:center;padding:70px 0 0}
.hero-center .lede{margin-left:auto;margin-right:auto}
.hero-center .cta,.hero-center .trust{justify-content:center}
.collage{display:grid;grid-template-columns:1fr 1.25fr 1fr;gap:18px;margin-top:52px;align-items:end;transform:translateY(40px)}
.collage img{width:100%;object-fit:cover;border-radius:var(--r);aspect-ratio:3/3.6;border:6px solid var(--bg)}
.collage img:nth-child(2){aspect-ratio:3/3.9}
.hero-stack{background:var(--brand);color:var(--on-brand);padding-top:64px}
.hero-stack .row{display:grid;grid-template-columns:1fr auto;gap:40px;align-items:end;margin:26px 0 46px}
.hero-stack .band{height:min(48vw,520px);width:100%;object-fit:cover}
.hero-arch{background:var(--brand2)}
.hero-arch .wrap{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center;padding-top:60px;padding-bottom:70px}
.hero-arch .pic img{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:999px 999px var(--r) var(--r)}
.hero-card{overflow:visible;padding-bottom:28px}
.hero-card>img{width:100%;height:min(74vh,680px);object-fit:cover}
.hero-card .panel{background:var(--bg);color:var(--ink);max-width:620px;padding:44px 44px 40px;border-radius:var(--r);margin:-150px 0 0;box-shadow:0 30px 60px rgba(0,0,0,.18);position:relative;z-index:2}
.hero-card .panel .lede{opacity:1;color:var(--muted)}
.hero-card .wrap{padding-bottom:0}
.hero-diagonal{background:var(--brand);color:var(--on-brand);display:grid;grid-template-columns:1.05fr .95fr;min-height:min(78vh,700px)}
.hero-diagonal .txt{padding:80px 40px 80px max(22px,calc((100vw - 1180px)/2 + 22px));display:flex;flex-direction:column;justify-content:center;position:relative;z-index:2}
.hero-diagonal img{width:100%;height:100%;object-fit:cover;clip-path:polygon(14% 0,100% 0,100% 100%,0 100%)}
.hero-mosaic{background:var(--surface)}
.hero-mosaic .wrap{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center;padding-top:64px;padding-bottom:72px}
.mosaic{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.mosaic img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:var(--r)}
.mosaic img:nth-child(1){border-top-left-radius:120px}
.mosaic img:nth-child(2){transform:translateY(28px)}
.mosaic img:nth-child(3){transform:translateY(-10px)}
.mosaic img:nth-child(4){border-bottom-right-radius:120px;transform:translateY(18px)}
.hero-editorial{background:var(--bg);padding:56px 0 0}
.hero-editorial h1{font-size:clamp(44px,8vw,112px);max-width:18ch;border-top:3px solid var(--ink);padding-top:28px}
.hero-editorial .row{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:end;margin-top:36px}
.hero-editorial .row img{width:100%;aspect-ratio:5/4;object-fit:cover;border-radius:var(--r)}
.hero-editorial .lede{color:var(--muted);opacity:1}
.hero-editorial .cta{margin-bottom:8px}
.hero-editorial .pad{height:64px}
.hero-frame{background:var(--surface)}
.hero-frame .wrap{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center;padding-top:72px;padding-bottom:88px}
.hero-frame .pic{position:relative;padding:0 18px 18px 0}
.hero-frame .pic img{width:100%;aspect-ratio:4/4.6;object-fit:cover;border-radius:var(--r);box-shadow:18px 18px 0 var(--accent);transform:rotate(-1.5deg)}
.hero-frame .lede{color:var(--muted);opacity:1}
/* ---------------- stats ---------------- */
.stats-strip{background:var(--surface);border-bottom:1px solid var(--line)}
.stats-strip .wrap{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}
.stats-strip .st{padding:26px 22px;border-left:1px solid var(--line)}
.stats-strip .st:first-child{border-left:0;padding-left:0}
.stats-strip b{display:block;font-family:var(--hf);font-size:30px;line-height:1.1}
.stats-strip small{color:var(--muted);font-weight:600}
.stats-pills{position:relative;z-index:3;margin-top:-30px}
.stats-pills .wrap{display:flex;gap:12px;flex-wrap:wrap;justify-content:center}
.stats-pills .st{background:var(--bg);border:1px solid var(--line);box-shadow:0 14px 30px rgba(0,0,0,.12);padding:14px 22px;border-radius:60px;display:flex;align-items:center;gap:10px;font-weight:700}
.stats-pills .st b{font-family:var(--hf);font-size:22px;color:var(--brand)}
.ticker{background:var(--accent);color:var(--on-accent);overflow:hidden;white-space:nowrap;padding:14px 0;font-weight:800;font-family:var(--hf);font-size:18px;letter-spacing:.04em;text-transform:uppercase}
.ticker div{display:inline-block;animation:tick 40s linear infinite}
.ticker span{padding:0 26px}
@keyframes tick{to{transform:translateX(-50%)}}
/* ---------------- sections ---------------- */
section{padding:92px 0}
.head{max-width:680px;margin-bottom:44px}
.head.c{text-align:center;margin-left:auto;margin-right:auto}
.head h2{font-size:clamp(32px,4.2vw,52px)}
.head p{color:var(--muted);font-size:18px;margin-top:12px}
.head.row{max-width:none;display:flex;justify-content:space-between;align-items:flex-end;gap:28px;flex-wrap:wrap}
.head.row p{max-width:52ch}
.tone{background:var(--surface)}
.dark{background:var(--brand);color:var(--on-brand)}
.dark .head p{color:inherit;opacity:.85}
.darker{background:var(--brand2);color:var(--on-brand)}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.card{background:var(--bg);border-radius:var(--r);overflow:hidden;border:1px solid var(--line);display:flex;flex-direction:column;transition:transform .25s,box-shadow .25s}
.card:hover{transform:translateY(-6px);box-shadow:0 22px 44px rgba(0,0,0,.12)}
.card img{aspect-ratio:4/3;object-fit:cover;width:100%;transition:transform .6s}
.card:hover img{transform:scale(1.05)}
.card .in{padding:22px 22px 26px}
.card h3{font-size:24px;margin-bottom:8px}
.card p{color:var(--muted)}
.card .more{margin-top:14px;font-weight:700;text-decoration:none;color:var(--brand);display:inline-flex;gap:6px}
.pic-wrap{overflow:hidden}
/* services: tiles */
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.tile{background:var(--bg);border:1px solid var(--line);border-radius:var(--r);padding:30px 28px 28px;text-decoration:none;display:flex;flex-direction:column;gap:10px;transition:border-color .2s,transform .2s;position:relative}
.tile:hover{border-color:var(--accent);transform:translateY(-4px)}
.tile .n{font-family:var(--hf);font-size:15px;letter-spacing:.1em;color:var(--accent);font-weight:800}
.tile h3{font-size:25px}
.tile p{color:var(--muted)}
.tile .arrow{margin-top:auto;padding-top:16px;font-weight:800;color:var(--brand)}
.tone .tile{background:var(--bg)}
/* services: list */
.slist{border-top:1px solid var(--line)}
.srow{display:grid;grid-template-columns:100px 1fr auto;gap:28px;align-items:center;padding:30px 0;border-bottom:1px solid var(--line);text-decoration:none;transition:padding .2s}
.srow:hover{padding-left:12px}
.srow .n{font-family:var(--hf);font-size:52px;line-height:1;color:var(--accent)}
.srow h3{font-size:clamp(22px,2.6vw,32px);margin-bottom:6px}
.srow p{color:var(--muted)}
.srow .go{width:52px;height:52px;border-radius:50%;border:2px solid var(--line);display:grid;place-items:center;font-size:22px;transition:background .2s,color .2s}
.srow:hover .go{background:var(--brand);color:var(--on-brand);border-color:var(--brand)}
/* services: bento */
.bento{display:grid;grid-template-columns:1.3fr 1fr;grid-auto-rows:minmax(150px,auto);gap:18px}
.bento .big{grid-row:span 2;position:relative;border-radius:var(--r);overflow:hidden;min-height:420px;display:flex;align-items:flex-end;color:#fff;text-decoration:none}
.bento .big img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .7s}
.bento .big:hover img{transform:scale(1.05)}
.bento .big .in{position:relative;z-index:2;padding:30px;background:linear-gradient(transparent,rgba(0,0,0,.75));width:100%}
.bento .big h3{font-size:32px;margin-bottom:6px}
.bento .sm{display:flex;gap:18px;align-items:center;background:var(--bg);border:1px solid var(--line);border-radius:var(--r);padding:16px;text-decoration:none;transition:transform .2s,box-shadow .2s}
.bento .sm:hover{transform:translateX(6px);box-shadow:0 14px 30px rgba(0,0,0,.1)}
.bento .sm img{width:118px;height:118px;object-fit:cover;border-radius:calc(var(--r)/1.4);flex:0 0 118px}
.bento .sm h3{font-size:21px;margin-bottom:4px}
.bento .sm p{color:var(--muted);font-size:15.5px}
/* services: side */
.side{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.side .sm{display:flex;gap:20px;align-items:stretch;background:var(--bg);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;text-decoration:none;transition:transform .2s,box-shadow .2s}
.side .sm:hover{transform:translateY(-4px);box-shadow:0 18px 36px rgba(0,0,0,.1)}
.side .sm img{width:170px;object-fit:cover;flex:0 0 170px}
.side .sm div{padding:22px 22px 22px 0}
.side .sm h3{font-size:22px;margin-bottom:6px}
.side .sm p{color:var(--muted);font-size:15.5px}
/* services: alt rows */
.altrows{display:grid;gap:30px}
.altrow{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center;background:var(--bg);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;text-decoration:none}
.altrow:nth-child(even) .pic-wrap{order:2}
.altrow img{width:100%;height:100%;min-height:300px;object-fit:cover;transition:transform .6s}
.altrow:hover img{transform:scale(1.04)}
.altrow .in{padding:36px 40px 36px 0}
.altrow:nth-child(even) .in{padding:36px 0 36px 40px}
.altrow h3{font-size:30px;margin-bottom:8px}
.altrow p{color:var(--muted)}
/* why */
.split{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center}
.split img{width:100%;aspect-ratio:5/4;object-fit:cover;border-radius:var(--r)}
.split.rev img{order:2}
.split h2{font-size:clamp(32px,4vw,48px);margin-bottom:16px}
.split p+p{margin-top:12px}
.ticks{list-style:none;padding:0;margin-top:22px;display:grid;gap:12px}
.ticks li{display:flex;gap:12px;align-items:flex-start}
.ticks li:before{content:"";flex:0 0 22px;height:22px;margin-top:2px;border-radius:50%;background:var(--accent) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M6 12l4 4 8-8' fill='none' stroke='white' stroke-width='3' stroke-linecap='round'/%3E%3C/svg%3E") center/14px no-repeat}
.why-dark .grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
.numbox{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.numbox div{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);border-radius:var(--r);padding:22px}
.numbox b{display:block;font-family:var(--hf);font-size:30px;color:var(--accent);margin-bottom:6px}
.stackimg{position:relative;padding:0 40px 40px 0}
.stackimg img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:var(--r)}
.stackimg img+img{position:absolute;width:55%;right:0;bottom:0;border:8px solid var(--bg);box-shadow:0 20px 40px rgba(0,0,0,.18)}
.why-band{position:relative;color:#fff;overflow:hidden}
.why-band>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.why-band:before{content:"";position:absolute;inset:0;background:$overlay;opacity:.92}
.why-band .wrap{position:relative;z-index:2;text-align:center;max-width:900px}
.why-band h2{font-size:clamp(32px,4.4vw,54px);margin-bottom:14px}
.why-band .ticks{grid-template-columns:1fr 1fr;text-align:left;margin-top:34px;gap:16px 36px}
/* gallery */
.gallery{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:220px;gap:14px}
.gallery img{width:100%;height:100%;object-fit:cover;border-radius:var(--r);transition:transform .5s}
.gallery img:hover{transform:scale(1.03)}
.gallery img:nth-child(1){grid-row:span 2;grid-column:span 2}
.gstrip{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;padding:4px 0 18px;scrollbar-width:thin}
.gstrip img{flex:0 0 min(360px,78vw);aspect-ratio:4/5;object-fit:cover;border-radius:var(--r);scroll-snap-align:start}
.ggrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.ggrid img{aspect-ratio:1;width:100%;object-fit:cover;border-radius:var(--r);transition:transform .5s,filter .5s}
.ggrid img:hover{transform:scale(1.03)}
.gtilt{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;align-items:start}
.gtilt img{aspect-ratio:4/5;width:100%;object-fit:cover;border-radius:var(--r)}
.gtilt img:nth-child(3n+2){transform:translateY(36px)}
.gtilt{padding-bottom:36px}
/* reviews */
.reviews{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.rv{background:var(--bg);border-radius:var(--r);padding:28px;border:1px solid var(--line);display:flex;flex-direction:column;gap:14px}
.dark .rv{background:rgba(255,255,255,.07);border-color:rgba(255,255,255,.14)}
.rv .st{color:#F2B01E;letter-spacing:2px}
.rv p{font-size:17.5px}
.rv footer{margin-top:auto;font-size:14px;opacity:.75;display:flex;align-items:center;gap:8px}
.g{width:18px;height:18px}
.score{display:flex;align-items:center;gap:16px;margin-bottom:36px;flex-wrap:wrap}
.score b{font-family:var(--hf);font-size:58px;line-height:1}
.rslider{display:flex;gap:20px;overflow-x:auto;scroll-snap-type:x mandatory;padding:6px 0 20px;scrollbar-width:thin}
.rslider .rv{flex:0 0 min(420px,84vw);scroll-snap-align:start;position:relative;padding-top:54px}
.rslider .rv:before{content:"“";position:absolute;top:8px;left:24px;font-family:var(--hf);font-size:88px;line-height:1;color:var(--accent);opacity:.9}
.rfeat{display:grid;grid-template-columns:1.2fr .8fr;gap:48px;align-items:start}
.rfeat .bigq{font-family:var(--hf);font-size:clamp(26px,3.2vw,40px);line-height:1.25;position:relative;padding-top:36px}
.rfeat .bigq:before{content:"“";position:absolute;top:-24px;left:-6px;font-size:110px;line-height:1;color:var(--accent);opacity:.9}
.rfeat .who{margin-top:18px;opacity:.8;font-size:15px;display:flex;gap:8px;align-items:center}
.rfeat .list{display:grid;gap:14px}
.rfeat .list .rv{padding:18px 20px;gap:8px}
.rfeat .list .rv p{font-size:15.5px}
.rlight{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.rlight .rv{border-left:5px solid var(--accent);border-radius:0 var(--r) var(--r) 0;background:var(--bg)}
/* cta */
.ctaband{background:var(--accent);color:var(--on-accent);padding:64px 0}
.ctaband .wrap{display:flex;justify-content:space-between;align-items:center;gap:28px;flex-wrap:wrap}
.ctaband h2{font-size:clamp(28px,3.6vw,44px);max-width:20ch}
.ctaband .btn-main{background:var(--brand);color:var(--on-brand)}
.ctadark{background:var(--brand2);color:var(--on-brand);padding:90px 0;text-align:center}
.ctadark h2{font-size:clamp(28px,3.4vw,40px);opacity:.9}
.ctadark .big{font-family:var(--hf);font-size:clamp(40px,7vw,86px);display:block;text-decoration:none;margin:14px 0 26px;color:var(--accent);line-height:1}
.ctadark .cta{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.ctacard{padding:0 0 92px}
.ctacard .box{background:var(--brand);color:var(--on-brand);border-radius:calc(var(--r) * 1.4);padding:56px;display:grid;grid-template-columns:1.3fr .7fr;gap:36px;align-items:center;position:relative;overflow:hidden}
.ctacard .box:after{content:"";position:absolute;width:420px;height:420px;border-radius:50%;background:var(--accent);opacity:.18;right:-140px;top:-160px}
.ctacard h2{font-size:clamp(28px,3.6vw,46px);position:relative;z-index:2}
.ctacard .cta{display:flex;flex-direction:column;gap:12px;position:relative;z-index:2}
.ctacard .btn{justify-content:center}
/* hours */
.info{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start}
.hours{width:100%;border-collapse:collapse}
.hours td{padding:12px 0;border-bottom:1px solid var(--line)}
.hours td+td{text-align:right;font-weight:600}
.map{width:100%;height:380px;border:0;border-radius:var(--r);filter:saturate(.9)}
.icards{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:28px}
.icard{background:var(--bg);border:1px solid var(--line);border-radius:var(--r);padding:26px;display:flex;flex-direction:column;gap:8px}
.icard .ic{width:46px;height:46px;border-radius:50%;background:var(--brand);color:var(--on-brand);display:grid;place-items:center;margin-bottom:8px}
.icard .ic svg{width:20px;height:20px}
.icard h3{font-size:21px}
.icard .hours td{padding:7px 0;font-size:15px}
.mapbg{position:relative}
.mapbg .map{height:560px;border-radius:0}
.mapbg .float{position:absolute;top:50%;transform:translateY(-50%);left:max(22px,calc((100vw - 1180px)/2 + 22px));background:var(--bg);padding:34px;border-radius:var(--r);box-shadow:0 24px 50px rgba(0,0,0,.2);max-width:420px;width:calc(100% - 44px)}
.mapbg .float h2{font-size:30px;margin-bottom:10px}
/* faq */
.faq details{border-bottom:1px solid var(--line);padding:18px 0}
.faq summary{font-weight:700;cursor:pointer;font-size:18px;list-style:none;display:flex;justify-content:space-between;gap:16px}
.faq summary::-webkit-details-marker{display:none}
.faq summary:after{content:"+";font-size:24px;line-height:1;color:var(--accent)}
.faq details[open] summary:after{content:"–"}
.faq p{margin-top:10px;color:var(--muted)}
.faq-grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:56px;align-items:start}
/* page heads */
.pagehead{background:var(--brand);color:var(--on-brand);padding:76px 0 64px;position:relative;overflow:hidden}
.pagehead h1{font-size:clamp(38px,5.6vw,68px)}
.pagehead p{font-size:19px;opacity:.88;max-width:52ch;margin-top:14px}
.pagehead .wrap{position:relative;z-index:2}
.pagehead.image{color:#fff;padding:110px 0 80px}
.pagehead.image>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.pagehead.image:after{content:"";position:absolute;inset:0;background:$overlay;opacity:.88}
.pagehead.light{background:var(--surface);color:var(--ink);padding:70px 0 54px}
.pagehead.light h1:after{content:"";display:block;width:72px;height:5px;background:var(--accent);margin-top:20px;border-radius:3px}
.pagehead.light p{color:var(--muted);opacity:1}
.crumbs{font-size:14px;opacity:.75;margin-bottom:14px}
.crumbs a{text-decoration:none}
.svc-row{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center;padding:44px 0;border-bottom:1px solid var(--line)}
.svc-row:nth-child(even) .svc-pic{order:2}
.svc-row img{width:100%;aspect-ratio:16/11;object-fit:cover;border-radius:var(--r)}
.svc-row h2{font-size:clamp(28px,3.4vw,40px);margin-bottom:12px}
.contact-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:52px;align-items:start}
form.book{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:32px;display:grid;gap:16px}
form.book label{font-weight:600;font-size:14.5px;display:grid;gap:6px}
form.book input,form.book select,form.book textarea{font:inherit;padding:13px 14px;border:1px solid var(--line);border-radius:calc(var(--r)/2 + 2px);background:var(--bg);color:var(--ink);width:100%}
form.book .two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
form.book button{font:inherit;font-weight:700;background:var(--brand);color:var(--on-brand);border:0;padding:16px;border-radius:var(--rb);cursor:pointer;font-size:17px}
.hide{position:absolute;left:-9999px}
.contact-card{display:grid;gap:18px}
.contact-card a.line,.contact-card .line{display:flex;gap:14px;align-items:center;text-decoration:none;padding:18px;border:1px solid var(--line);border-radius:var(--r);background:var(--bg)}
.contact-card .ic{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;background:var(--brand);color:var(--on-brand);flex:0 0 44px}
.contact-card .ic svg{width:20px;height:20px}
.contact-card b{display:block}
.contact-card small{color:var(--muted)}
/* footer */
footer.foot{background:$footBg;color:$footInk;padding:64px 0 28px;font-size:15.5px}
.fgrid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:36px}
.foot h4{font-family:var(--hf);font-size:18px;margin-bottom:12px;color:$footHead}
.foot ul{list-style:none;padding:0;display:grid;gap:8px}
.foot a{text-decoration:none}
.foot a:hover{text-decoration:underline}
.soc{display:flex;gap:10px;margin-top:16px}
.soc a{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;border:1px solid currentColor;opacity:.85}
.soc svg{width:18px;height:18px}
.legal{border-top:1px solid rgba(255,255,255,.14);margin-top:44px;padding-top:22px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:14px;opacity:.85}
.legal .heart{color:#ff5a6e}
.foot.simple{text-align:center}
.foot.simple .brandmark{justify-content:center}
.foot.simple .fl{display:flex;gap:26px;justify-content:center;flex-wrap:wrap;margin:22px 0 6px;font-weight:600}
.foot.simple .soc{justify-content:center}
.foot.simple .legal{justify-content:center;text-align:center}
.foot.bold .bigname{font-family:var(--hf);font-size:clamp(40px,7vw,96px);line-height:.95;margin-bottom:34px;color:$footHead;$headExtra}
.foot.bold .fgrid{grid-template-columns:1fr 1fr 1fr;border-top:1px solid rgba(255,255,255,.14);padding-top:34px}
.mbar{display:none}
/* ---------------- responsive ---------------- */
@media (max-width:960px){
 .menu{display:none;position:absolute;left:0;right:0;top:76px;background:var(--hbg);flex-direction:column;align-items:stretch;padding:12px 22px 22px;gap:4px;border-bottom:1px solid var(--line)}
 .menu.open{display:flex}
 .menu a{padding:12px 0}
 .burger{display:block}
 .nav-phone{display:none}
 .nav-center header.site .nav{flex-direction:row;height:76px;padding:0}
 .nav-center .menu{border:0;padding:12px 22px 22px}
 .nav-center .burger{position:static}
 .nav-pill .menu{top:76px;left:0;right:0;border-radius:24px;box-shadow:0 12px 36px rgba(0,0,0,.14)}
 .nav-pill header.site{padding:0;top:8px}
 .nav-stripe .nav{height:80px}
 .nav-stripe .menu{top:80px}
 .nav-split .menu a[aria-current]{background:none;border-bottom:2px solid var(--accent);border-radius:0}
 .nav-split .menu .btn,.nav-center .menu .btn{display:inline-flex}
 .hero-split .wrap,.hero-arch .wrap,.hero-mosaic .wrap,.hero-frame .wrap,.hero-editorial .row,.split,.info,.contact-grid,.svc-row,.why-dark .grid,.rfeat,.faq-grid,.altrow,.bento,.side,.ctacard .box{grid-template-columns:1fr;gap:34px}
 .split.rev img{order:0}
 .svc-row:nth-child(even) .svc-pic{order:0}
 .altrow:nth-child(even) .pic-wrap{order:0}
 .altrow .in,.altrow:nth-child(even) .in{padding:0 28px 28px}
 .altrow img{min-height:240px}
 .bento .big{grid-row:auto;min-height:320px}
 .cards,.reviews,.tiles,.rlight{grid-template-columns:1fr 1fr}
 .fgrid,.foot.bold .fgrid{grid-template-columns:1fr 1fr}
 .hero-stack .row{grid-template-columns:1fr}
 .badge{left:12px}
 .hero-diagonal{grid-template-columns:1fr}
 .hero-diagonal img{clip-path:none;height:340px}
 .hero-diagonal .txt{padding:56px 22px}
 .icards{grid-template-columns:1fr}
 .stats-strip .st{padding:18px 16px}
 .ctacard .cta{flex-direction:row;flex-wrap:wrap}
 .mapbg .float{position:static;transform:none;max-width:none;width:auto;margin:-80px 22px 0;position:relative;z-index:2}
 .mapbg .map{height:380px}
}
@media (max-width:640px){
 body{font-size:16.5px}
 section{padding:64px 0}
 .top .hide-m{display:none}
 .cards,.reviews,.fgrid,.foot.bold .fgrid,.tiles,.rlight{grid-template-columns:1fr}
 .gallery{grid-template-columns:1fr 1fr;grid-auto-rows:150px}
 .ggrid,.gtilt{grid-template-columns:1fr 1fr}
 .gtilt img:nth-child(3n+2){transform:none}
 .gtilt img:nth-child(2n){transform:translateY(28px)}
 .collage{grid-template-columns:1fr 1fr;transform:translateY(30px)}
 .collage img:nth-child(3){display:none}
 .hero-split .wrap{padding-top:40px;padding-bottom:52px}
 .hero-overlay{min-height:640px}
 .hero-card{overflow:visible;padding-bottom:28px}
.hero-card>img{height:52vh}
 .hero-card .panel{padding:28px 22px;margin-top:-70px}
 .hero-editorial h1{font-size:clamp(40px,11vw,64px)}
 .mosaic img:nth-child(1){border-top-left-radius:60px}
 .mosaic img:nth-child(4){border-bottom-right-radius:60px}
 .srow{grid-template-columns:1fr;gap:8px}
 .srow .go{display:none}
 .srow .n{font-size:34px}
 .stats-strip .st{border-left:0;padding:14px 0;border-top:1px solid var(--line)}
 .stats-strip .st:first-child{border-top:0}
 .stats-strip .wrap{grid-template-columns:1fr 1fr}
 .stats-pills{margin-top:16px}
 .numbox{grid-template-columns:1fr}
 .why-band .ticks{grid-template-columns:1fr}
 .side .sm img{width:110px;flex-basis:110px}
 .side .sm div{padding:16px 16px 16px 0}
 .ctacard .box{padding:34px 26px}
 .ctacard .cta{flex-direction:column}
 .bento .sm img{width:84px;height:84px;flex-basis:84px}
 form.book .two{grid-template-columns:1fr}
 .mbar{display:grid;grid-template-columns:1fr 1fr;position:fixed;left:0;right:0;bottom:0;z-index:30;box-shadow:0 -6px 20px rgba(0,0,0,.12)}
 .mbar a{padding:15px;text-align:center;font-weight:700;text-decoration:none}
 .mbar a:first-child{background:var(--brand);color:var(--on-brand)}
 .mbar a:last-child{background:var(--accent);color:var(--on-accent)}
 footer.foot{padding-bottom:84px}
}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important;animation:none!important}.js .rv-up{opacity:1;transform:none}}
"""

def css(t):
    out = CSS
    for k in sorted(t, key=len, reverse=True):
        v = t[k]
        if isinstance(v, (str, int, float)):
            out = out.replace("$" + k, str(v))
    return out

SVG_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
SVG_PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s7-6.1 7-12a7 7 0 0 0-14 0c0 5.9 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>'
SVG_CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
SVG_CAL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>'
SVG_FB = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 8V6.3c0-.8.2-1.3 1.4-1.3H17V2h-2.6C11.3 2 10 3.6 10 6.1V8H8v3h2v11h4V11h2.7l.4-3H14z"/></svg>'
SVG_IG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>'
SVG_G = '<svg class="g" viewBox="0 0 48 48"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2A11.9 11.9 0 0 1 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3a12 12 0 0 1-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>'
SVG_BURGER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>'

REVEAL_JS = """<script>(function(){if(!('IntersectionObserver' in window))return;var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');o.unobserve(e.target)}})},{rootMargin:'0px 0px -8%'});document.querySelectorAll('.rv-up').forEach(function(el){o.observe(el)})})();</script>"""

def head(s, title, desc):
    t = s["theme"]; L = s["_L"]
    cls = f"nav-{L['nav']} btn-{L['btn']}"
    og = img(s['images']['hero'], 1200)
    return f"""<!doctype html>
<html lang="en-AU" class="{cls}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:image" content="{og}">
<link rel="icon" href="{favicon(s)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{t['fontsQuery']}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<script>document.documentElement.classList.add('js')</script>
<script type="application/ld+json">{json.dumps(schema(s))}</script>
</head>
<body>"""

def schema(s):
    d = {"@context":"https://schema.org","@type":s.get("schemaType","LocalBusiness"),"name":s["name"],"telephone":s["phoneIntl"],
         "address":{"@type":"PostalAddress","streetAddress":s.get("street",""),"addressLocality":s["suburb"],"addressRegion":s["state"],"postalCode":s.get("postcode",""),"addressCountry":"AU"},
         "areaServed":s["area"]}
    if s.get("rating"): d["aggregateRating"]={"@type":"AggregateRating","ratingValue":s["rating"],"reviewCount":s["reviewCount"]}
    return d

def eyebrow(s, text):
    return f'<div class="eyebrow">{E(text)}</div>' if s["_L"]["eyebrow"] else ""

def nav(s, cur):
    L = s["_L"]
    items = [("index.html","Home"),("services.html","Services"),("about.html","About"),("contact.html","Contact")]
    li = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{n}</a></li>' for h,n in items)
    top = f"""<div class="top"><div class="wrap"><span class="hide-m">{E(s['topline'])}</span><span><a href="tel:{s['phoneIntl']}">Call {E(s['phone'])}</a></span></div></div>"""
    if L["nav"] in ("pill", "stripe"): top = ""
    phone = f'<a class="nav-phone" href="tel:{s["phoneIntl"]}">{SVG_PHONE}{E(s["phone"])}</a>' if L["nav"] == "split" else ""
    burger = f"""<button class="burger" aria-label="Open menu" aria-expanded="false" onclick="var m=document.getElementById('menu');m.classList.toggle('open');this.setAttribute('aria-expanded',m.classList.contains('open'))">{SVG_BURGER}</button>"""
    return f"""{top}
<header class="site"><div class="wrap nav">
 <a class="brandmark" href="index.html">{logo_svg(s)}<span><b>{E(s['short'])}</b><small>{E(s['tag'])}</small></span></a>
 {burger}
 <ul class="menu" id="menu">{li}<li><a class="btn btn-main" href="contact.html">{E(s['ctaLabel'])}</a></li></ul>
 {phone}
</div></header>"""

def foot(s):
    L = s["_L"]
    soc = ""
    if s.get("facebook"): soc += f'<a href="{E(s["facebook"])}" aria-label="Facebook" rel="noopener">{SVG_FB}</a>'
    if s.get("instagram"): soc += f'<a href="{E(s["instagram"])}" aria-label="Instagram" rel="noopener">{SVG_IG}</a>'
    svc = "".join(f'<li><a href="services.html#{sv["id"]}">{E(sv["title"])}</a></li>' for sv in s["services"][:5])
    hrs = "".join(f"<li>{E(d)}: {E(h)}</li>" for d,h in s["hours"])
    legal = f"""<div class="legal"><span>© {YEAR} {E(s['name'])}. All rights reserved.</span><span>Developed with <span class="heart" aria-label="love">❤</span> by <a href="https://gemprogrammers.com" rel="noopener"><b>Mr. Developer</b></a></span></div>"""
    mbar = f"""<div class="mbar"><a href="tel:{s['phoneIntl']}">Call now</a><a href="contact.html">{E(s['ctaLabel'])}</a></div>"""
    if L["footer"] == "simple":
        body = f"""<a class="brandmark" href="index.html">{logo_svg(s,40)}<span><b>{E(s['short'])}</b><small>{E(s['tag'])}</small></span></a>
 <p style="margin:18px auto 0;opacity:.85;max-width:46ch">{E(s['footerBlurb'])}</p>
 <div class="fl"><a href="index.html">Home</a><a href="services.html">Services</a><a href="about.html">About</a><a href="contact.html">Contact</a><a href="tel:{s['phoneIntl']}">{E(s['phone'])}</a></div>
 <p style="opacity:.8">{E(s['addressLine'])}</p><div class="soc">{soc}</div>"""
    elif L["footer"] == "bold":
        body = f"""<div class="bigname">{E(s['name'])}</div><div class="fgrid">
  <div><p style="opacity:.85;max-width:34ch">{E(s['footerBlurb'])}</p><div class="soc">{soc}</div></div>
  <div><h4>Services</h4><ul>{svc}</ul></div>
  <div><h4>Contact</h4><ul><li><a href="tel:{s['phoneIntl']}">{E(s['phone'])}</a></li><li>{E(s['addressLine'])}</li><li><a href="contact.html">{E(s['ctaLabel'])}</a></li></ul></div>
 </div>"""
    else:
        body = f"""<div class="fgrid">
  <div><a class="brandmark" href="index.html">{logo_svg(s,40)}<span><b>{E(s['short'])}</b><small>{E(s['tag'])}</small></span></a><p style="margin-top:16px;opacity:.85;max-width:34ch">{E(s['footerBlurb'])}</p><div class="soc">{soc}</div></div>
  <div><h4>Services</h4><ul>{svc}</ul></div>
  <div><h4>Hours</h4><ul>{hrs}</ul></div>
  <div><h4>Contact</h4><ul><li><a href="tel:{s['phoneIntl']}">{E(s['phone'])}</a></li><li>{E(s['addressLine'])}</li><li><a href="contact.html">{E(s['ctaLabel'])}</a></li></ul></div>
 </div>"""
    return f"""<footer class="foot {L['footer']}"><div class="wrap">{body}{legal}</div></footer>{mbar}{REVEAL_JS}</body></html>"""

def review_cards(s, n=6):
    out = ""
    for r in s["reviews"][:n]:
        out += f'<article class="rv"><div class="st" aria-label="5 stars">★★★★★</div><p>“{E(r["text"])}”</p><footer>{SVG_G if r.get("src","Google")=="Google" else ""}<span>{E(r.get("who","Google review"))}</span></footer></article>'
    return out

def badge(s):
    if s.get("rating"):
        return f'<div class="badge"><b>{s["rating"]} <span style="color:#F2B01E;font-size:22px">★</span></b><small>{s["reviewCount"]} {E(s.get("ratingSource","Google"))} reviews</small></div>'
    if s.get("badge"):
        return f'<div class="badge"><b>{E(s["badge"][0])}</b><small>{E(s["badge"][1])}</small></div>'
    return ""

def cta_buttons(s):
    return f'<div class="cta"><a class="btn btn-main" href="contact.html">{SVG_CAL}{E(s["ctaLabel"])}</a><a class="btn btn-ghost" href="tel:{s["phoneIntl"]}">{SVG_PHONE}{E(s["phone"])}</a></div>'

def hero(s):
    L = s["_L"]; i = s["images"]; h = s["hero"]
    cta = cta_buttons(s)
    trust = '<div class="trust">' + "".join(f"<span><i>✔</i>{E(x)}</span>" for x in h["trust"]) + "</div>"
    title = h.get("titleHtml") or E(h["title"])
    eb = eyebrow(s, s["tag"])
    v = L["hero"]
    dec = f" decor-{L['decor']}" if L["decor"] != "none" and v not in ("overlay","card","diagonal") else ""
    if v == "split":
        return f"""<div class="hero hero-split{dec}"><div class="wrap"><div>{eb}<h1>{title}</h1><p class="lede">{E(h['lede'])}</p>{cta}{trust}</div>
<div class="pic"><img src="{img(i['hero'])}" alt="{E(i['heroAlt'])}" fetchpriority="high">{badge(s)}</div></div></div>"""
    if v == "overlay":
        return f"""<div class="hero hero-overlay"><img src="{img(i['hero'],2000)}" alt="{E(i['heroAlt'])}" fetchpriority="high"><div class="wrap">{eb}<h1 style="max-width:16ch">{title}</h1><p class="lede">{E(h['lede'])}</p>{cta}{trust}</div></div>"""
    if v == "center":
        g = i["gallery"]
        return f"""<div class="hero hero-center{dec}"><div class="wrap">{eb}<h1 style="max-width:15ch;margin:0 auto">{title}</h1><p class="lede">{E(h['lede'])}</p>{cta}{trust}
<div class="collage"><img src="{img(g[0],700)}" alt=""><img src="{img(i['hero'],900)}" alt="{E(i['heroAlt'])}"><img src="{img(g[1],700)}" alt=""></div></div></div>"""
    if v == "stack":
        return f"""<div class="hero hero-stack{dec}"><div class="wrap">{eb}<h1>{title}</h1><div class="row"><p class="lede" style="margin:0">{E(h['lede'])}</p>{cta}</div>{trust}<div style="height:34px"></div></div><img class="band" src="{img(i['hero'],2000)}" alt="{E(i['heroAlt'])}" fetchpriority="high"></div>"""
    if v == "arch":
        col = ' style="color:var(--on-brand)"' if is_dark(s["theme"]["brand2"]) else ""
        return f"""<div class="hero hero-arch{dec}"{col}><div class="wrap"><div>{eb}<h1>{title}</h1><p class="lede">{E(h['lede'])}</p>{cta}{trust}</div><div class="pic"><img src="{img(i['hero'])}" alt="{E(i['heroAlt'])}" fetchpriority="high"></div></div></div>"""
    if v == "card":
        return f"""<div class="hero hero-card"><img src="{img(i['hero'],2000)}" alt="{E(i['heroAlt'])}" fetchpriority="high"><div class="wrap"><div class="panel">{eb}<h1 style="font-size:clamp(34px,4.6vw,58px)">{title}</h1><p class="lede">{E(h['lede'])}</p>{cta}{trust}</div></div></div>"""
    if v == "diagonal":
        return f"""<div class="hero hero-diagonal{dec}"><div class="txt">{eb}<h1>{title}</h1><p class="lede">{E(h['lede'])}</p>{cta}{trust}</div><img src="{img(i['hero'],1600)}" alt="{E(i['heroAlt'])}" fetchpriority="high"></div>"""
    if v == "mosaic":
        g = i["gallery"]
        pics = "".join(f'<img src="{img(p,700)}" alt="">' for p in (i["hero"], g[0], g[1], g[2]))
        return f"""<div class="hero hero-mosaic{dec}"><div class="wrap"><div>{eb}<h1>{title}</h1><p class="lede" style="color:var(--muted);opacity:1">{E(h['lede'])}</p>{cta}{trust}</div><div class="mosaic">{pics}</div></div></div>"""
    if v == "editorial":
        return f"""<div class="hero hero-editorial{dec}"><div class="wrap">{eb or f'<div class="eyebrow">{E(s["tag"])}</div>'}<h1>{title}</h1><div class="row"><div><p class="lede">{E(h['lede'])}</p>{cta}{trust}</div><img src="{img(i['hero'],1100)}" alt="{E(i['heroAlt'])}" fetchpriority="high"></div><div class="pad"></div></div></div>"""
    if v == "frame":
        return f"""<div class="hero hero-frame{dec}"><div class="wrap"><div>{eb}<h1>{title}</h1><p class="lede">{E(h['lede'])}</p>{cta}{trust}</div><div class="pic"><img src="{img(i['hero'])}" alt="{E(i['heroAlt'])}" fetchpriority="high"></div></div></div>"""
    raise ValueError(v)

def stats_block(s):
    L = s["_L"]; v = L["stats"]
    if v == "none": return ""
    if v == "ticker":
        items = [sv["title"] for sv in s["services"]] + [f"Servicing {s['area']}"]
        inner = "".join(f"<span>{E(x)}</span><span aria-hidden='true'>✦</span>" for x in items)
        return f'<div class="ticker" aria-label="Services"><div>{inner}{inner}</div></div>'
    st = []
    if s.get("rating"):
        st.append((f"{s['rating']}★", f"{s['reviewCount']} {s.get('ratingSource','Google')} reviews"))
    elif s.get("badge"):
        st.append((s["badge"][0], s["badge"][1]))
    STOP = {"in","on","the","and","to","a","of","for","we","us","your","you","call","no"}
    def toks(x): return {w.strip("★.,&") for w in x.lower().split() if len(w) > 1} - STOP
    def dup(x):
        tx = toks(x)
        return any(tx & toks(a + " " + b) for a, b in st)
    for x in s["hero"]["trust"][:3]:
        if "★" in x and s.get("rating"): continue
        if dup(x): continue
        st.append((x, ""))
    st = st[:4]
    if v == "strip":
        cells = "".join(f'<div class="st"><b>{E(a)}</b>' + (f'<small>{E(b)}</small>' if b else '') + '</div>' for a,b in st)
        return f'<div class="stats-strip"><div class="wrap">{cells}</div></div>'
    cells = "".join(f'<div class="st">' + (f'<b>{E(a)}</b><span>{E(b)}</span>' if b else f'<span>✔ {E(a)}</span>') + '</div>' for a,b in st)
    return f'<div class="stats-pills"><div class="wrap">{cells}</div></div>'

def services_block(s, tone):
    L = s["_L"]; v = L["services"]
    svcs = s["services"]
    hd = f'<div class="head{" row" if v in ("list","tiles") else ""}"><div>{eyebrow(s,"What we do")}<h2>{E(s["servicesHead"])}</h2></div><p>{E(s["servicesSub"])}</p></div>' if v in ("list","tiles") else f'<div class="head{" c" if v=="cards" else ""}">{eyebrow(s,"What we do")}<h2>{E(s["servicesHead"])}</h2><p>{E(s["servicesSub"])}</p></div>'
    more = f'<p style="margin-top:34px"><a class="btn btn-ghost" href="services.html">See all services</a></p>'
    if v == "cards":
        body = '<div class="cards">' + "".join(f'<article class="card rv-up"><div class="pic-wrap"><img src="{img(sv["img"],800)}" alt="{E(sv["title"])}" loading="lazy"></div><div class="in"><h3>{E(sv["title"])}</h3><p>{E(sv["short"])}</p><a class="more" href="services.html#{sv["id"]}">Learn more →</a></div></article>' for sv in svcs[:3]) + '</div>'
        more = f'<p style="margin-top:34px;text-align:center"><a class="btn btn-ghost" href="services.html">See all services</a></p>'
    elif v == "tiles":
        body = '<div class="tiles">' + "".join(f'<a class="tile rv-up" href="services.html#{sv["id"]}"><span class="n">0{n+1}</span><h3>{E(sv["title"])}</h3><p>{E(sv["short"])}</p><span class="arrow">Learn more →</span></a>' for n,sv in enumerate(svcs[:6])) + '</div>'
        more = ""
    elif v == "list":
        body = '<div class="slist">' + "".join(f'<a class="srow rv-up" href="services.html#{sv["id"]}"><span class="n">0{n+1}</span><div><h3>{E(sv["title"])}</h3><p>{E(sv["short"])}</p></div><span class="go">→</span></a>' for n,sv in enumerate(svcs[:6])) + '</div>'
        more = ""
    elif v == "bento":
        first, rest = svcs[0], svcs[1:5]
        body = f'<div class="bento"><a class="big rv-up" href="services.html#{first["id"]}"><img src="{img(first["img"],1200)}" alt="" loading="lazy"><div class="in"><h3>{E(first["title"])}</h3><p>{E(first["short"])}</p></div></a>' + "".join(f'<a class="sm rv-up" href="services.html#{sv["id"]}"><img src="{img(sv["img"],400)}" alt="" loading="lazy"><div><h3>{E(sv["title"])}</h3><p>{E(sv["short"])}</p></div></a>' for sv in rest) + '</div>'
    elif v == "side":
        body = '<div class="side">' + "".join(f'<a class="sm rv-up" href="services.html#{sv["id"]}"><img src="{img(sv["img"],500)}" alt="" loading="lazy"><div><h3>{E(sv["title"])}</h3><p>{E(sv["short"])}</p></div></a>' for sv in svcs[:4]) + '</div>'
    else:  # alt
        body = '<div class="altrows">' + "".join(f'<a class="altrow rv-up" href="services.html#{sv["id"]}"><div class="pic-wrap"><img src="{img(sv["img"],1000)}" alt="" loading="lazy"></div><div class="in"><h3>{E(sv["title"])}</h3><p>{E(sv["long"])}</p><p style="margin-top:14px;font-weight:700;color:var(--brand)">Learn more →</p></div></a>' for sv in svcs[:3]) + '</div>'
    return f'<section class="{tone}"><div class="wrap">{hd}{body}{more}</div></section>'

def why_block(s, tone, v=None):
    L = s["_L"]; v = v or L["why"]; i = s["images"]
    ticks = "".join(f"<li>{E(x)}</li>" for x in s["why"])
    btn = f'<p style="margin-top:26px"><a class="btn btn-main" href="about.html">About {E(s["ownerOrUs"])}</a></p>'
    eb = eyebrow(s, "Why choose us" if s["ownerOrUs"]=="us" else f"Why {s['ownerOrUs']}")
    if v == "dark":
        boxes = "".join(f'<div><b>0{n+1}</b>{E(x)}</div>' for n,x in enumerate(s["why"][:4]))
        return f'<section class="dark why-dark"><div class="wrap grid"><div class="rv-up">{eb}<h2 style="font-size:clamp(32px,4vw,48px);margin-bottom:16px">{E(s["whyHead"])}</h2><p style="opacity:.9">{E(s["whyText"])}</p><p style="margin-top:26px"><a class="btn btn-main" href="about.html">About {E(s["ownerOrUs"])}</a></p></div><div class="numbox rv-up">{boxes}</div></div></section>'
    if v == "band":
        return f'<section class="why-band"><img src="{img(i["about"],2000)}" alt="" loading="lazy"><div class="wrap rv-up">{eb}<h2>{E(s["whyHead"])}</h2><p style="font-size:19px;opacity:.92">{E(s["whyText"])}</p><ul class="ticks">{ticks}</ul><p style="margin-top:34px"><a class="btn btn-main" href="about.html">About {E(s["ownerOrUs"])}</a></p></div></section>'
    if v == "stackimg":
        return f'<section class="{tone}"><div class="wrap split"><div class="rv-up">{eb}<h2>{E(s["whyHead"])}</h2><p>{E(s["whyText"])}</p><ul class="ticks">{ticks}</ul>{btn}</div><div class="stackimg rv-up"><img src="{img(i["about"],1000)}" alt="{E(i["aboutAlt"])}" loading="lazy"><img src="{img(i["about2"],700)}" alt="" loading="lazy"></div></div></section>'
    rev = " rev" if v == "splitR" else ""
    return f'<section class="{tone}"><div class="wrap split{rev}"><img class="rv-up" src="{img(i["about"],1100)}" alt="{E(i["aboutAlt"])}" loading="lazy"><div class="rv-up">{eb}<h2>{E(s["whyHead"])}</h2><p>{E(s["whyText"])}</p><ul class="ticks">{ticks}</ul>{btn}</div></div></section>'

def gallery_block(s, tone):
    L = s["_L"]; v = L["gallery"]; g = s["images"]["gallery"]
    hd = f'<div class="head{" c" if v=="grid" else ""}">{eyebrow(s,"Our work")}<h2>{E(s["galleryHead"])}</h2><p>{E(s["gallerySub"])}</p></div>'
    if v == "strip":
        body = '<div class="gstrip">' + "".join(f'<img src="{img(p,800)}" alt="" loading="lazy">' for p in g[:6]) + '</div>'
    elif v == "grid":
        body = '<div class="ggrid">' + "".join(f'<img class="rv-up" src="{img(p,800)}" alt="" loading="lazy">' for p in g[:6]) + '</div>'
    elif v == "tilt":
        body = '<div class="gtilt">' + "".join(f'<img class="rv-up" src="{img(p,800)}" alt="" loading="lazy">' for p in g[:6]) + '</div>'
    else:
        body = '<div class="gallery">' + "".join(f'<img src="{img(p,900)}" alt="" loading="lazy">' for p in g[:5]) + '</div>'
    return f'<section class="{tone}"><div class="wrap">{hd}{body}</div></section>'

def reviews_block(s, v=None):
    if not s.get("reviews"): return ""
    L = s["_L"]; v = v or L["reviews"]
    score = f"""<div class="score"><b>{s['rating']}</b><div><div style="color:#F2B01E;font-size:22px;letter-spacing:2px">{stars(s['rating'])}</div><div>{s['reviewCount']} reviews on {E(s.get('ratingSource','Google'))}</div></div></div>""" if s.get("rating") else ""
    sub = f'<p>{E(s["reviewsSub"])}</p>' if s.get("reviewsSub") else ""
    hd = f'<div class="head">{eyebrow(s,"Reviews")}<h2>{E(s["reviewsHead"])}</h2>{sub}</div>'
    if v == "slider":
        return f'<section class="tone"><div class="wrap">{score}{hd}<div class="rslider">{review_cards(s)}</div></div></section>'
    if v == "featured":
        r0 = s["reviews"][0]
        rest = "".join(f'<article class="rv"><div class="st">★★★★★</div><p>“{E(r["text"])}”</p><footer><span>{E(r.get("who","Google review"))}</span></footer></article>' for r in s["reviews"][1:4])
        return f'<section class="dark"><div class="wrap">{hd}<div class="rfeat"><div class="rv-up"><div class="bigq">{E(r0["text"])}</div><div class="who">{SVG_G if r0.get("src","Google")=="Google" else ""}{E(r0.get("who","Google review"))} · ★★★★★</div>{score.replace("margin-bottom:36px","margin-top:34px") if score else ""}</div><div class="list rv-up">{rest}</div></div></div></section>'
    if v == "light":
        return f'<section class="tone"><div class="wrap">{score}{hd}<div class="rlight">{review_cards(s,4)}</div></div></section>'
    return f'<section class="dark"><div class="wrap">{score}{hd}<div class="reviews">{review_cards(s)}</div></div></section>'

def faq_block(s, tone):
    faq = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q,a in s["faq"][:4])
    return f'<section class="{tone}"><div class="wrap faq-grid"><div class="rv-up">{eyebrow(s,"FAQ")}<h2 style="font-size:clamp(30px,3.8vw,46px)">Common questions</h2><p style="color:var(--muted);margin-top:12px">Can\'t find what you need? Call {E(s["phone"])}.</p><p style="margin-top:22px"><a class="btn btn-ghost" href="services.html">All services &amp; FAQs</a></p></div><div class="faq rv-up">{faq}</div></div></section>'

def hours_block(s, tone):
    L = s["_L"]; v = L["hours"]
    hrs = "".join(f"<tr><td>{E(d)}</td><td>{E(h)}</td></tr>" for d,h in s["hours"])
    mapq = urllib.parse.quote(s["mapQuery"])
    mp = f'<iframe class="map" title="Map showing {E(s["name"])}" loading="lazy" src="https://maps.google.com/maps?q={mapq}&z=13&output=embed"></iframe>'
    btns = f'<p style="margin-top:26px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-main" href="contact.html">{E(s["ctaLabel"])}</a><a class="btn btn-ghost" href="tel:{s["phoneIntl"]}">{E(s["phone"])}</a></p>'
    if v == "cards":
        cards = f"""<div class="icards"><div class="icard rv-up"><span class="ic">{SVG_PHONE}</span><h3>Call or text</h3><a href="tel:{s['phoneIntl']}" style="text-decoration:none;font-weight:700;font-size:20px">{E(s['phone'])}</a><small style="color:var(--muted)">{E(s['topline'])}</small></div>
<div class="icard rv-up"><span class="ic">{SVG_PIN}</span><h3>Where we work</h3><p>{E(s['addressLine'])}</p><small style="color:var(--muted)">{E(s['areaText'])}</small></div>
<div class="icard rv-up"><span class="ic">{SVG_CLOCK}</span><h3>Hours</h3><table class="hours">{hrs}</table></div></div>"""
        return f'<section class="{tone}"><div class="wrap"><div class="head">{eyebrow(s,"Find us")}<h2>Hours &amp; location</h2></div>{cards}{mp}</div></section>'
    if v == "mapbg":
        return f'<div class="mapbg">{mp.replace("loading=\"lazy\"","")}<div class="float rv-up">{eyebrow(s,"Find us")}<h2>Hours &amp; location</h2><p style="color:var(--muted)">{E(s["areaText"])}</p><table class="hours" style="margin-top:14px">{hrs}</table>{btns}</div></div>'
    return f'<section class="{tone}"><div class="wrap info"><div class="rv-up"><div class="head" style="margin-bottom:24px">{eyebrow(s,"Find us")}<h2>Hours &amp; location</h2><p>{E(s["areaText"])}</p></div><table class="hours">{hrs}</table>{btns}</div>{mp}</div></section>'

def cta_block(s):
    L = s["_L"]; v = L["cta"]
    if v == "dark":
        bgfix = ' style="background:var(--brand)"' if not is_dark(s["theme"]["brand2"]) else ""
        return f'<div class="ctadark"{bgfix}><div class="wrap"><h2>{E(s["bandText"])}</h2><a class="big" href="tel:{s["phoneIntl"]}">{E(s["phone"])}</a><div class="cta"><a class="btn btn-main" href="contact.html">{E(s["ctaLabel"])}</a><a class="btn btn-ghost" href="tel:{s["phoneIntl"]}">Call now</a></div></div></div>'
    if v == "card":
        return f'<section class="ctacard"><div class="wrap"><div class="box rv-up"><div><h2>{E(s["bandText"])}</h2><p style="opacity:.85;margin-top:10px;position:relative;z-index:2">{E(s["contactSub"])}</p></div><div class="cta"><a class="btn btn-main" href="contact.html">{SVG_CAL}{E(s["ctaLabel"])}</a><a class="btn btn-ghost" href="tel:{s["phoneIntl"]}">{SVG_PHONE}{E(s["phone"])}</a></div></div></div></section>'
    return f'<div class="ctaband"><div class="wrap"><h2>{E(s["bandText"])}</h2><a class="btn btn-main" href="contact.html">{E(s["ctaLabel"])}</a></div></div>'

def page_home(s):
    L = s["_L"]
    order = ORDERS[L["order"]]
    blocks = []
    tone_i = 0
    first_pad = "style='padding-top:130px'" if L["hero"] == "center" and L["stats"] == "none" else ""
    hero_dark = L["hero"] in ("split","overlay","center","stack","diagonal") or (L["hero"] == "arch" and is_dark(s["theme"]["brand2"]))
    prev_dark = hero_dark and L["stats"] in ("none","pills")
    for k in order:
        tone = "tone" if tone_i % 2 else ""
        if k == "services":
            b = services_block(s, tone); tone_i += 1; prev_dark = False
        elif k == "why":
            v = L["why"]
            if prev_dark and v in ("dark","band"): v = "stackimg" if v == "dark" else "splitR"
            b = why_block(s, tone, v); tone_i += 1; prev_dark = v in ("dark","band")
        elif k == "gallery":
            b = gallery_block(s, tone); tone_i += 1; prev_dark = False
        elif k == "reviews":
            v = L["reviews"]
            if prev_dark and v in ("cards","featured"): v = "light" if v == "cards" else "slider"
            b = reviews_block(s, v)
            prev_dark = v in ("cards","featured")
            tone_i = 0 if v in ("slider","light") else 1   # contrast with whatever reviews used
        elif k == "faq":
            b = faq_block(s, tone); tone_i += 1; prev_dark = False
        elif k == "hours":
            b = hours_block(s, tone); tone_i += 1; prev_dark = False
        if first_pad and b.startswith("<section"):
            b = b.replace("<section", f"<section {first_pad}", 1); first_pad = ""
        blocks.append(b)
    stats = stats_block(s)
    if L["hero"] == "center" and stats:
        stats = stats.replace('class="stats-strip"', 'class="stats-strip" style="padding-top:60px"').replace('class="stats-pills"','class="stats-pills" style="margin-top:60px"').replace('class="ticker"','class="ticker" style="margin-top:60px"')
    return (head(s, f'{s["name"]} | {s["seoTitle"]}', s["metaDesc"]) + nav(s,"index.html") + "<main>" + hero(s) + stats + "".join(blocks) + cta_block(s) + "</main>" + foot(s))

def pagehead(s, title, sub, crumb):
    L = s["_L"]; v = L["pagehead"]
    inner = f'<div class="wrap"><div class="crumbs"><a href="index.html">Home</a> / {E(crumb)}</div><h1>{E(title)}</h1><p>{E(sub)}</p></div>'
    if v == "image":
        return f'<div class="pagehead image"><img src="{img(s["images"]["hero"],2000)}" alt="">{inner}</div>'
    return f'<div class="pagehead {v}">{inner}</div>'

def page_services(s):
    rows = ""
    for sv in s["services"]:
        pts = "".join(f"<li>{E(p)}</li>" for p in sv.get("points",[]))
        rows += f'<div class="svc-row" id="{sv["id"]}"><div class="svc-pic rv-up"><img src="{img(sv["img"],1100)}" alt="{E(sv["title"])}" loading="lazy"></div><div class="rv-up"><h2>{E(sv["title"])}</h2><p>{E(sv["long"])}</p><ul class="ticks">{pts}</ul><p style="margin-top:24px"><a class="btn btn-main" href="contact.html">{E(s["ctaLabel"])}</a></p></div></div>'
    faq = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q,a in s["faq"])
    return (head(s, f'Services | {s["name"]}', f'{s["name"]} services: ' + ", ".join(x["title"] for x in s["services"]) + ".") + nav(s,"services.html") + "<main>" +
            pagehead(s, s["servicesHead"], s["servicesSub"], "Services") +
            f'<section style="padding-top:30px"><div class="wrap">{rows}</div></section><section class="tone"><div class="wrap" style="max-width:860px"><div class="head">{eyebrow(s,"FAQ")}<h2>Common questions</h2></div><div class="faq">{faq}</div></div></section>'
            + cta_block(s) + '</main>' + foot(s))

def page_about(s):
    i = s["images"]
    paras = "".join(f"<p>{E(p)}</p>" for p in s["aboutParas"])
    vals = "".join(f'<article class="tile rv-up" style="cursor:default"><span class="n">0{n+1}</span><h3>{E(a)}</h3><p>{E(b)}</p></article>' for n,(a,b) in enumerate(s["values"]))
    gal = "".join(f'<img src="{img(g,900)}" alt="" loading="lazy">' for g in i["gallery"][1:6])
    rv = ""
    if s.get("reviews"):
        rv = f'<section class="dark"><div class="wrap"><div class="head">{eyebrow(s,"Reviews")}<h2>{E(s["reviewsHead"])}</h2></div><div class="reviews">{review_cards(s,3)}</div></div></section>'
    return (head(s, f'About | {s["name"]}', s["metaDesc"]) + nav(s,"about.html") + "<main>" +
            pagehead(s, s["aboutHead"], s["aboutSub"], "About") +
            f'<section><div class="wrap split"><div class="rv-up">{paras}<p style="margin-top:26px"><a class="btn btn-main" href="contact.html">{E(s["ctaLabel"])}</a></p></div><img class="rv-up" src="{img(i["about2"],1100)}" alt="{E(i["aboutAlt"])}" loading="lazy"></div></section>'
            f'<section class="tone"><div class="wrap"><div class="head">{eyebrow(s,"Our approach")}<h2>{E(s["valuesHead"])}</h2></div><div class="tiles">{vals}</div></div></section>' + rv +
            f'<section><div class="wrap"><div class="gallery">{gal}</div></div></section>' + cta_block(s) + '</main>' + foot(s))

def page_contact(s):
    hrs = "".join(f"<tr><td>{E(d)}</td><td>{E(h)}</td></tr>" for d,h in s["hours"])
    opts = "".join(f"<option>{E(sv['title'])}</option>" for sv in s["services"]) + "<option>Not sure yet</option>"
    mapq = urllib.parse.quote(s["mapQuery"])
    fname = f"booking-{s['slug']}"
    extra = "".join(f'<label>{E(lbl)}<input name="{E(n)}"></label>' for lbl,n in s.get("formExtra",[]))
    book = f'<a class="line" href="{E(s["bookingUrl"])}" rel="noopener"><span class="ic">{SVG_CAL}</span><span><b>Book online</b><small>Pick a time that suits you</small></span></a>' if s.get("bookingUrl") else ""
    return (head(s, f'Contact | {s["name"]}', f'Contact {s["name"]}: call {s["phone"]} or send a booking request.') + nav(s,"contact.html") + "<main>" +
            pagehead(s, s["contactHead"], s["contactSub"], "Contact") +
            f"""<section><div class="wrap contact-grid">
<form class="book" name="{fname}" data-sms="{s['phoneIntl']}" data-mail="{E(s.get('formEmail',''))}" data-biz="{E(s['short'])}" onsubmit="return sendReq(this)">
 <h2 style="font-size:30px">{E(s['formHead'])}</h2>
 <div class="two"><label>Your name<input name="name" required autocomplete="name"></label><label>Phone<input name="phone" type="tel" required autocomplete="tel"></label></div>
 <div class="two"><label>Email<input name="email" type="email" autocomplete="email"></label><label>Suburb<input name="suburb" autocomplete="address-level2"></label></div>
 {extra}
 <label>What do you need?<select name="service">{opts}</select></label>
 <label>Anything we should know?<textarea name="message" rows="4"></textarea></label>
 <button type="submit">{E(s['formButton'])}</button>
 <p class="note-sms" style="font-size:14px;color:var(--muted)">Your {'email' if s.get('formEmail') else 'messages'} app will open with your request ready to send. Prefer to talk? Call {E(s['phone'])}.</p>
</form>
<script>
function sendReq(f){{var d=new FormData(f),t=[];
t.push("Hi "+f.dataset.biz+", booking request:");
d.forEach(function(v,k){{if(v)t.push(k.charAt(0).toUpperCase()+k.slice(1).replace(/_/g," ")+": "+v);}});
var body=encodeURIComponent(t.join(String.fromCharCode(10)));
if(f.dataset.mail){{window.location.href="mailto:"+f.dataset.mail+"?subject="+encodeURIComponent("Quote request")+"&body="+body;return false;}}
var sep=/iPhone|iPad|Mac/i.test(navigator.userAgent)?"&":"?";
window.location.href="sms:"+f.dataset.sms+sep+"body="+body;return false;}}
</script>
<div class="contact-card">
 <a class="line" href="tel:{s['phoneIntl']}"><span class="ic">{SVG_PHONE}</span><span><b>{E(s['phone'])}</b><small>Call or text any time during business hours</small></span></a>
 {book}
 <a class="line" href="https://www.google.com/maps/search/?api=1&query={mapq}" rel="noopener"><span class="ic">{SVG_PIN}</span><span><b>{E(s['addressLine'])}</b><small>{E(s['areaShort'])}</small></span></a>
 <div class="line" style="display:block"><div style="display:flex;gap:14px;align-items:center;margin-bottom:8px"><span class="ic">{SVG_CLOCK}</span><b>Opening hours</b></div><table class="hours">{hrs}</table></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><iframe class="map" title="Map showing {E(s['name'])}" loading="lazy" src="https://maps.google.com/maps?q={mapq}&z=13&output=embed"></iframe></div></section>
</main>""" + foot(s))

def page_thanks(s):
    return (head(s, f'Thank you | {s["name"]}', "Request received.") + nav(s,"") + "<main>" +
            pagehead(s, "Thanks, we've got your request", f"We'll call you back shortly. Need us sooner? Ring {s['phone']}.", "Thank you") +
            f'<section><div class="wrap"><a class="btn btn-main" href="index.html">Back to home</a></div></section></main>' + foot(s))

def build(path):
    s = json.load(open(path))
    t = s["theme"]
    t.setdefault("onAccent", "#FFFFFF")
    s["_L"] = layout(s)
    apply_local_photos(s)
    out = ROOT / s["slug"]; out.mkdir(exist_ok=True)
    for f in out.glob("*.html"): f.unlink()
    (out/"style.css").write_text(css(t))
    (out/"index.html").write_text(page_home(s))
    (out/"services.html").write_text(page_services(s))
    (out/"about.html").write_text(page_about(s))
    (out/"contact.html").write_text(page_contact(s))
    (out/"thanks.html").write_text(page_thanks(s))
    print("built", s["slug"], " ".join(f"{k}={v}" for k,v in s["_L"].items() if k in ("nav","hero","services","why","gallery","reviews","order")))

if __name__ == "__main__":
    files = sys.argv[1:] or sorted(str(p) for p in SITES.glob("*.json"))
    for f in files: build(f)
