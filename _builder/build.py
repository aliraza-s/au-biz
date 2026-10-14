#!/usr/bin/env python3
"""Builds multi-page preview websites from sites/*.json into ../<slug>/.
Each site = Home, Services, About, Contact (+ thank-you page). Theme + hero variant come from the JSON."""
import json, sys, html, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITES = pathlib.Path(__file__).resolve().parent / "sites"
YEAR = 2026
E = html.escape

def img(id_, w=1400):
    return f"https://images.unsplash.com/photo-{id_}?auto=format&fit=crop&w={w}&q=80"

ICONS = {
 "mesh": '<g fill="none" stroke="currentColor"><rect x="4" y="4" width="24" height="24" rx="2" stroke-width="2.8"/><path d="M10 4v24M16 4v24M22 4v24M4 10h24M4 16h24M4 22h24" stroke-width="1.3"/></g>',
 "hammer": '<g fill="currentColor"><path d="M6 6h13l3 3v5h-6V11H6z"/><path d="M14 14h5v15a2.5 2.5 0 0 1-5 0z"/></g>',
 "leaf": '<path fill="currentColor" d="M27 4C13 4 5 11 5 21c0 2 .4 3.6 1 5l-2 2 1.5 1.5 2-2c1.6.9 3.5 1.5 5.5 1.5 11 0 14-11 14-25z"/><path d="M8 25c4-6 8-10 15-14" stroke="var(--logo-ink)" stroke-width="2" fill="none" stroke-linecap="round"/>',
 "sprout": '<g fill="currentColor"><path d="M15 29V17h2v12z"/><path d="M16 18C16 10 11 6 3 6c0 8 5 12 13 12z"/><path d="M16 15c0-6 4-10 13-10 0 7-4 10-13 10z"/><path d="M6 27h20v3H6z"/></g>',
 "mower": '<g fill="currentColor"><path d="M4 16h18l3 6v3H4z"/><path d="M14 16 25 3l2 1.5L17 16z"/><circle cx="8.5" cy="26" r="3.5"/><circle cx="21" cy="26" r="3.5"/></g><path d="M6 19h14" stroke="var(--logo-ink)" stroke-width="2"/>',
 "paw": '<g fill="currentColor"><ellipse cx="16" cy="21" rx="7" ry="6"/><circle cx="7.5" cy="13" r="3"/><circle cx="12.5" cy="8" r="3"/><circle cx="19.5" cy="8" r="3"/><circle cx="24.5" cy="13" r="3"/></g>',
 "drop": '<path fill="currentColor" d="M16 3c5 7 9 11.5 9 16.5A9 9 0 0 1 7 19.5C7 14.5 11 10 16 3z"/><path d="M12 20a4 4 0 0 0 4 4" stroke="var(--logo-ink)" stroke-width="2" fill="none" stroke-linecap="round"/>',
 "scissors": '<g fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><circle cx="9" cy="23" r="4"/><circle cx="23" cy="23" r="4"/><path d="M11.5 20 24 5M20.5 20 8 5"/></g>',
 "bubbles": '<g fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="12" cy="18" r="7"/><circle cx="23" cy="10" r="4.5"/><circle cx="24" cy="23" r="3"/></g>',
 "bolt": '<path fill="currentColor" d="M18.5 2 6 18h8l-2.5 12L26 13h-8.5z"/>',
 "sparkle": '<g fill="currentColor"><path d="M13 3c.9 6.2 3.8 9.1 10 10-6.2.9-9.1 3.8-10 10-.9-6.2-3.8-9.1-10-10 6.2-.9 9.1-3.8 10-10z"/><path d="M25 19c.4 2.6 1.4 3.6 4 4-2.6.4-3.6 1.4-4 4-.4-2.6-1.4-3.6-4-4 2.6-.4 3.6-1.4 4-4z"/></g>',
 "spray": '<g fill="currentColor"><path d="M10 12h9v16a2 2 0 0 1-2 2h-5a2 2 0 0 1-2-2z"/><path d="M11 6h8v4h-8z"/><path d="M19 7h4l2 3h-6z"/></g><g stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M27 5l2-1M28 9h2M27 13l2 1"/></g>',
 "trowel": '<g fill="currentColor"><path d="M4 22 18 8l6 6-14 14H4z"/><path d="M21 7l3-3a2.1 2.1 0 0 1 3 3l-3 3z"/></g>',
 "house": '<path fill="currentColor" d="M16 3 2 15h4v13h8v-8h4v8h8V15h4z"/>',
 "heart": '<path fill="currentColor" d="M16 27s-11-6.6-11-14a6 6 0 0 1 11-3.3A6 6 0 0 1 27 13c0 7.4-11 14-11 14z"/>',
 "mop": '<g fill="currentColor"><path d="M19.5 2.5a1.5 1.5 0 0 1 2.6 1.4L15.6 17h-2.9z"/><path d="M8 18h12l2.5 10h-17z"/></g>',
 "star": '<path fill="currentColor" d="M16 3l3.9 8 8.8 1.2-6.4 6.1 1.6 8.7L16 22.8 8.1 27l1.6-8.7-6.4-6.1 8.8-1.2z"/>',
 "layers": '<g fill="currentColor"><path d="M16 3 29 10 16 17 3 10z"/><path d="M5.6 14.4 16 20l10.4-5.6L29 16 16 23 3 16z" opacity=".78"/><path d="M5.6 20.4 16 26l10.4-5.6L29 22 16 29 3 22z" opacity=".55"/></g>',
 "grid": '<g fill="currentColor"><rect x="3" y="3" width="12" height="12" rx="2"/><rect x="17" y="3" width="12" height="12" rx="2"/><rect x="3" y="17" width="12" height="12" rx="2"/><rect x="17" y="17" width="12" height="12" rx="2"/></g>',
 "bone": '<path fill="currentColor" d="M9 10a3.5 3.5 0 1 1 4.5-3.3L20 13.2a3.5 3.5 0 1 1 3.3 4.5 3.5 3.5 0 1 1-4.5 3.3L12.3 14.5A3.5 3.5 0 1 1 9 10z"/>',
 "mixer": '<g fill="currentColor"><path d="M2 21V12h7l3 4v5z"/><path d="M13 9.5 26 6.5a3 3 0 0 1 3.6 2.4l.6 4.6a3 3 0 0 1-2.6 3.4L14 18z"/><rect x="12" y="19" width="18" height="3" rx="1"/><circle cx="7" cy="25" r="3"/><circle cx="18" cy="25" r="3"/><circle cx="26" cy="25" r="3"/></g>',
 "level": '<g fill="currentColor"><rect x="2" y="11" width="28" height="10" rx="2.5"/></g><rect x="12" y="13.5" width="8" height="5" rx="2.5" fill="var(--logo-ink)"/><circle cx="16" cy="16" r="1.4" fill="currentColor"/><path d="M6 13.5v5M26 13.5v5" stroke="var(--logo-ink)" stroke-width="1.6"/>',
 "blocks": '<g fill="currentColor"><rect x="2" y="5" width="13" height="6" rx="1"/><rect x="17" y="5" width="13" height="6" rx="1"/><rect x="2" y="13" width="6" height="6" rx="1"/><rect x="10" y="13" width="12" height="6" rx="1"/><rect x="24" y="13" width="6" height="6" rx="1"/><rect x="2" y="21" width="13" height="6" rx="1"/><rect x="17" y="21" width="13" height="6" rx="1"/></g>',
 "bear": '<g fill="currentColor"><circle cx="8" cy="9" r="4.2"/><circle cx="24" cy="9" r="4.2"/><ellipse cx="16" cy="18" rx="11.5" ry="10.5"/></g><g fill="var(--logo-ink)"><circle cx="11.5" cy="16" r="1.6"/><circle cx="20.5" cy="16" r="1.6"/><ellipse cx="16" cy="22" rx="3" ry="2.2"/></g>',
 "loader": '<g fill="currentColor"><path d="M9 6h9l3 8h3v9H6V12l3-1z"/><path d="M24 15l4 1 2 7h-4z"/><circle cx="10" cy="25.5" r="3.5"/><circle cx="21" cy="25.5" r="3.5"/></g><path d="M11 8.5h5.5l2 5.5H11z" fill="var(--logo-ink)"/>',
 "wrench": '<path fill="currentColor" d="M27.6 8.2a7 7 0 0 1-9.3 8.6L8 27.1a2.8 2.8 0 0 1-4-4l10.3-10.3a7 7 0 0 1 8.6-9.3l-4.4 4.4 1 3.6 3.6 1z"/>',
 "gear": '<path fill="currentColor" fill-rule="evenodd" d="M13.6 2h4.8l.7 3.6 2.6 1.1 3-2.1 3.4 3.4-2.1 3 1.1 2.6 3.6.7v4.8l-3.6.7-1.1 2.6 2.1 3-3.4 3.4-3-2.1-2.6 1.1-.7 3.6h-4.8l-.7-3.6-2.6-1.1-3 2.1-3.4-3.4 2.1-3-1.1-2.6L2 18.4v-4.8l3.6-.7 1.1-2.6-2.1-3 3.4-3.4 3 2.1 2.6-1.1zM16 11a5 5 0 1 0 0 10 5 5 0 0 0 0-10z"/>',
 "tyre": '<g fill="none" stroke="currentColor"><circle cx="16" cy="16" r="12" stroke-width="5"/><circle cx="16" cy="16" r="3.2" stroke-width="2.4"/><path d="M16 7.5v5M16 19.5v5M7.5 16h5M19.5 16h5" stroke-width="2.4"/></g>',
 "car": '<g fill="currentColor"><path d="M8 8h16l4 8h2v8h-4v-2H6v2H2v-8h2z"/><circle cx="9" cy="24" r="3.4"/><circle cx="23" cy="24" r="3.4"/></g><path d="M10 10.5h12l2.6 5.5H7.4z" fill="var(--logo-ink)"/>',
 "tow": '<g fill="currentColor"><path d="M2 12h11v12H2z"/><path d="M13 16h5l9-10 2 1.5-8 10.5v6H13z"/><circle cx="7" cy="25.5" r="3.4"/><circle cx="21" cy="25.5" r="3.4"/></g><path d="M4 14.5h7v4H4z" fill="var(--logo-ink)"/><path d="M28 7v6l-2 2" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/>',
 "picket": '<g fill="currentColor"><path d="M5 9l3-4 3 4v19H5zM13 9l3-4 3 4v19h-6zM21 9l3-4 3 4v19h-6z"/><path d="M2 12h28v3H2zM2 21h28v3H2z"/></g>',
 "farmgate": '<g fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 3v26"/><path d="M8 8h20v16H8z"/><path d="M8 13.3h20M8 18.6h20M8 24 28 8"/></g>',
 "wall": '<g fill="currentColor"><path d="M3 23h8v6H3zM12 23h8v6h-8zM21 23h8v6h-8zM7.5 16h8v6h-8zM16.5 16h8v6h-8zM12 9h8v6h-8z"/></g><path d="M3 9c3-3 5-3 8 0" stroke="currentColor" stroke-width="2.2" fill="none" stroke-linecap="round"/>',
 "palisade": '<g fill="currentColor"><path d="M6 3l2 5v20H4V8zM13 3l2 5v20h-4V8zM20 3l2 5v20h-4V8zM27 3l2 5v20h-4V8z"/><path d="M2 11h28v2.6H2zM2 21.5h28v2.6H2z"/></g>',
 "pane": '<g fill="none" stroke="currentColor" stroke-width="2.6"><rect x="4" y="4" width="24" height="24" rx="2"/><path d="M16 4v24M4 16h24"/></g><path d="M8 12.5l3.5-3.5M20 12.5l3.5-3.5M20 24.5l3.5-3.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>',
}

def logo_svg(s, size=44):
    t = s["theme"]
    return (f'<svg class="logo-mark" width="{size}" height="{size}" viewBox="0 0 32 32" aria-hidden="true" style="--logo-ink:{t["logoBg"]}">'
            f'<rect width="32" height="32" rx="{t.get("logoRadius",9)}" fill="{t["logoBg"]}"/>'
            f'<g style="color:{t["logoFg"]}" transform="translate(4 4) scale(.75)">{ICONS[t["icon"]]}</g></svg>')

def favicon(s):
    t = s["theme"]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="{t.get("logoRadius",9)}" fill="{t["logoBg"]}"/>'
           f'<g style="color:{t["logoFg"]}" transform="translate(4 4) scale(.75)">{ICONS[t["icon"]].replace("currentColor", t["logoFg"]).replace("var(--logo-ink)", t["logoBg"])}</g></svg>')
    return "data:image/svg+xml," + urllib.parse.quote(svg)

def stars(r):
    full = int(round(r))
    return "★" * full + "☆" * (5 - full)

CSS = """
:root{--bg:%(bg)s;--surface:%(surface)s;--ink:%(ink)s;--muted:%(muted)s;--brand:%(brand)s;--brand2:%(brand2)s;--accent:%(accent)s;--on-brand:%(onBrand)s;--line:%(line)s;--r:%(radius)s;--rb:%(btnRadius)s;--hf:%(headFont)s;--bf:%(bodyFont)s;--hw:%(headWeight)s}
*{box-sizing:border-box;margin:0}
html{scroll-behavior:smooth}
body{font-family:var(--bf);color:var(--ink);background:var(--bg);line-height:1.6;font-size:17px;-webkit-font-smoothing:antialiased}
img{max-width:100%%;display:block}
a{color:inherit}
:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
h1,h2,h3,.hf{font-family:var(--hf);font-weight:var(--hw);line-height:1.08;letter-spacing:%(headTrack)s;%(headExtra)s}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:14px 24px;border-radius:var(--rb);font-weight:700;text-decoration:none;border:2px solid transparent;font-size:16px;transition:transform .15s}
.btn:hover{transform:translateY(-1px)}
.btn-main{background:var(--accent);color:%(onAccent)s}
.btn-ghost{border-color:currentColor}
.btn svg{width:18px;height:18px}
/* header */
.top{background:var(--brand);color:var(--on-brand);font-size:14px}
.top .wrap{display:flex;justify-content:space-between;gap:12px;padding-top:8px;padding-bottom:8px;flex-wrap:wrap}
.top a{text-decoration:none;font-weight:600}
header.site{position:sticky;top:0;z-index:20;background:%(headerBg)s;color:%(headerInk)s;border-bottom:1px solid var(--line)}
.nav{display:flex;align-items:center;justify-content:space-between;height:76px;gap:18px}
.brandmark{display:flex;align-items:center;gap:12px;text-decoration:none}
.brandmark b{font-family:var(--hf);font-weight:var(--hw);font-size:21px;line-height:1.05;display:block;%(headExtra)s}
.brandmark small{display:block;font-size:12.5px;opacity:.75;margin-top:2px}
.menu{display:flex;gap:26px;align-items:center;list-style:none;padding:0}
.menu a{text-decoration:none;font-weight:600;font-size:15.5px;padding:6px 0;border-bottom:2px solid transparent}
.menu a[aria-current]{border-color:var(--accent)}
.menu .btn{padding:11px 18px;border-bottom:0}
.burger{display:none;background:none;border:0;color:inherit;padding:8px;cursor:pointer}
.burger svg{width:28px;height:28px}
/* hero variants */
.hero{position:relative;overflow:hidden}
.hero h1{font-size:clamp(40px,6.4vw,%(h1max)s)}
.hero .lede{font-size:clamp(18px,1.6vw,21px);max-width:44ch;margin:20px 0 30px;opacity:.9}
.hero .cta{display:flex;gap:12px;flex-wrap:wrap}
.trust{display:flex;gap:22px;flex-wrap:wrap;margin-top:30px;font-weight:600;font-size:15px}
.trust span{display:flex;align-items:center;gap:8px}
.trust i{font-style:normal;color:var(--accent)}
.hero-split{background:var(--brand);color:var(--on-brand)}
.hero-split .wrap{display:grid;grid-template-columns:1.05fr .95fr;gap:52px;align-items:center;padding-top:64px;padding-bottom:72px}
.hero-split .pic{position:relative}
.hero-split .pic img{width:100%%;aspect-ratio:4/4.4;object-fit:cover;border-radius:var(--r)}
.badge{position:absolute;left:-22px;bottom:28px;background:var(--surface);color:var(--ink);padding:16px 20px;border-radius:var(--r);box-shadow:0 18px 40px rgba(0,0,0,.18)}
.badge b{font-family:var(--hf);font-size:34px;display:block;line-height:1}
.badge small{color:var(--muted)}
.hero-overlay{color:#fff;min-height:min(86vh,760px);display:flex;align-items:flex-end}
.hero-overlay>img{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover}
.hero-overlay:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.05) 20%%,%(overlay)s 92%%)}
.hero-overlay .wrap{position:relative;z-index:2;padding-bottom:70px;padding-top:120px;width:100%%}
.hero-center{background:var(--brand);color:var(--on-brand);text-align:center;padding:70px 0 0}
.hero-center .lede{margin-left:auto;margin-right:auto}
.hero-center .cta,.hero-center .trust{justify-content:center}
.collage{display:grid;grid-template-columns:1fr 1.25fr 1fr;gap:18px;margin-top:52px;align-items:end;transform:translateY(40px)}
.collage img{width:100%%;object-fit:cover;border-radius:var(--r);aspect-ratio:3/3.6;border:6px solid var(--bg)}
.collage img:nth-child(2){aspect-ratio:3/3.9}
.hero-stack{background:var(--brand);color:var(--on-brand);padding-top:64px}
.hero-stack .row{display:grid;grid-template-columns:1fr auto;gap:40px;align-items:end;margin:26px 0 46px}
.hero-stack .band{height:min(48vw,520px);width:100%%;object-fit:cover}
.hero-arch{background:var(--brand2)}
.hero-arch .wrap{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center;padding-top:60px;padding-bottom:70px}
.hero-arch .pic img{width:100%%;aspect-ratio:4/5;object-fit:cover;border-radius:999px 999px var(--r) var(--r)}
/* sections */
section{padding:92px 0}
.head{max-width:680px;margin-bottom:44px}
.head.c{text-align:center;margin-left:auto;margin-right:auto}
.head h2{font-size:clamp(32px,4.2vw,52px)}
.head p{color:var(--muted);font-size:18px;margin-top:12px}
.tone{background:var(--surface)}
.dark{background:var(--brand);color:var(--on-brand)}
.dark .head p{color:inherit;opacity:.85}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.card{background:var(--bg);border-radius:var(--r);overflow:hidden;border:1px solid var(--line);display:flex;flex-direction:column}
.tone .card{background:var(--bg)}
.card img{aspect-ratio:4/3;object-fit:cover;width:100%%}
.card .in{padding:22px 22px 26px}
.card h3{font-size:24px;margin-bottom:8px}
.card p{color:var(--muted)}
.split{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center}
.split img{width:100%%;aspect-ratio:5/4;object-fit:cover;border-radius:var(--r)}
.split h2{font-size:clamp(32px,4vw,48px);margin-bottom:16px}
.split p+p{margin-top:12px}
.ticks{list-style:none;padding:0;margin-top:22px;display:grid;gap:12px}
.ticks li{display:flex;gap:12px;align-items:flex-start}
.ticks li:before{content:"";flex:0 0 22px;height:22px;margin-top:2px;border-radius:50%%;background:var(--accent) url("data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%%3E%%3Cpath d='M6 12l4 4 8-8' fill='none' stroke='white' stroke-width='3' stroke-linecap='round'/%%3E%%3C/svg%%3E") center/14px no-repeat}
.gallery{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:220px;gap:14px}
.gallery img{width:100%%;height:100%%;object-fit:cover;border-radius:var(--r)}
.gallery img:nth-child(1){grid-row:span 2;grid-column:span 2}
.reviews{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.rv{background:var(--bg);border-radius:var(--r);padding:28px;border:1px solid var(--line);display:flex;flex-direction:column;gap:14px}
.dark .rv{background:rgba(255,255,255,.07);border-color:rgba(255,255,255,.14)}
.rv .st{color:#F2B01E;letter-spacing:2px}
.rv p{font-size:17.5px}
.rv footer{margin-top:auto;font-size:14px;opacity:.75;display:flex;align-items:center;gap:8px}
.g{width:18px;height:18px}
.score{display:flex;align-items:center;gap:16px;margin-bottom:36px;flex-wrap:wrap}
.score b{font-family:var(--hf);font-size:58px;line-height:1}
.ctaband{background:var(--accent);color:%(onAccent)s;padding:64px 0}
.ctaband .wrap{display:flex;justify-content:space-between;align-items:center;gap:28px;flex-wrap:wrap}
.ctaband h2{font-size:clamp(28px,3.6vw,44px);max-width:20ch}
.ctaband .btn-main{background:var(--brand);color:var(--on-brand)}
.info{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start}
.hours{width:100%%;border-collapse:collapse}
.hours td{padding:12px 0;border-bottom:1px solid var(--line)}
.hours td+td{text-align:right;font-weight:600}
.map{width:100%%;height:380px;border:0;border-radius:var(--r);filter:saturate(.9)}
.faq details{border-bottom:1px solid var(--line);padding:18px 0}
.faq summary{font-weight:700;cursor:pointer;font-size:18px;list-style:none;display:flex;justify-content:space-between;gap:16px}
.faq summary:after{content:"+";font-size:24px;line-height:1;color:var(--accent)}
.faq details[open] summary:after{content:"–"}
.faq p{margin-top:10px;color:var(--muted)}
.pagehead{background:var(--brand);color:var(--on-brand);padding:76px 0 64px;position:relative;overflow:hidden}
.pagehead h1{font-size:clamp(38px,5.6vw,68px)}
.pagehead p{font-size:19px;opacity:.88;max-width:52ch;margin-top:14px}
.crumbs{font-size:14px;opacity:.75;margin-bottom:14px}
.crumbs a{text-decoration:none}
.svc-row{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center;padding:44px 0;border-bottom:1px solid var(--line)}
.svc-row:nth-child(even) .svc-pic{order:2}
.svc-row img{width:100%%;aspect-ratio:16/11;object-fit:cover;border-radius:var(--r)}
.svc-row h2{font-size:clamp(28px,3.4vw,40px);margin-bottom:12px}
.contact-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:52px;align-items:start}
form.book{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:32px;display:grid;gap:16px}
form.book label{font-weight:600;font-size:14.5px;display:grid;gap:6px}
form.book input,form.book select,form.book textarea{font:inherit;padding:13px 14px;border:1px solid var(--line);border-radius:calc(var(--r)/2 + 2px);background:var(--bg);color:var(--ink);width:100%%}
form.book .two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
form.book button{font:inherit;font-weight:700;background:var(--brand);color:var(--on-brand);border:0;padding:16px;border-radius:var(--rb);cursor:pointer;font-size:17px}
.hide{position:absolute;left:-9999px}
.contact-card{display:grid;gap:18px}
.contact-card a.line{display:flex;gap:14px;align-items:center;text-decoration:none;padding:18px;border:1px solid var(--line);border-radius:var(--r);background:var(--bg)}
.contact-card .ic{width:44px;height:44px;border-radius:50%%;display:grid;place-items:center;background:var(--brand);color:var(--on-brand);flex:0 0 44px}
.contact-card .ic svg{width:20px;height:20px}
.contact-card b{display:block}
.contact-card small{color:var(--muted)}
footer.foot{background:%(footBg)s;color:%(footInk)s;padding:64px 0 28px;font-size:15.5px}
.fgrid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:36px}
.foot h4{font-family:var(--hf);font-size:18px;margin-bottom:12px;color:%(footHead)s}
.foot ul{list-style:none;padding:0;display:grid;gap:8px}
.foot a{text-decoration:none}
.foot a:hover{text-decoration:underline}
.soc{display:flex;gap:10px;margin-top:16px}
.soc a{width:40px;height:40px;border-radius:50%%;display:grid;place-items:center;border:1px solid currentColor;opacity:.85}
.soc svg{width:18px;height:18px}
.legal{border-top:1px solid rgba(255,255,255,.14);margin-top:44px;padding-top:22px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:14px;opacity:.85}
.legal .heart{color:#ff5a6e}
.mbar{display:none}
@media (max-width:960px){
 .menu{display:none;position:absolute;left:0;right:0;top:76px;background:%(headerBg)s;flex-direction:column;align-items:stretch;padding:12px 22px 22px;gap:4px;border-bottom:1px solid var(--line)}
 .menu.open{display:flex}
 .menu a{padding:12px 0}
 .burger{display:block}
 .hero-split .wrap,.hero-arch .wrap,.split,.info,.contact-grid,.svc-row{grid-template-columns:1fr;gap:34px}
 .svc-row:nth-child(even) .svc-pic{order:0}
 .cards,.reviews{grid-template-columns:1fr 1fr}
 .fgrid{grid-template-columns:1fr 1fr}
 .hero-stack .row{grid-template-columns:1fr}
 .badge{left:12px}
}
@media (max-width:640px){
 body{font-size:16.5px}
 section{padding:64px 0}
 .top .hide-m{display:none}
 .cards,.reviews,.fgrid{grid-template-columns:1fr}
 .gallery{grid-template-columns:1fr 1fr;grid-auto-rows:150px}
 .collage{grid-template-columns:1fr 1fr;transform:translateY(30px)}
 .collage img:nth-child(3){display:none}
 .hero-split .wrap{padding-top:40px;padding-bottom:52px}
 .hero-overlay{min-height:640px}
 form.book .two{grid-template-columns:1fr}
 .mbar{display:grid;grid-template-columns:1fr 1fr;position:fixed;left:0;right:0;bottom:0;z-index:30;box-shadow:0 -6px 20px rgba(0,0,0,.12)}
 .mbar a{padding:15px;text-align:center;font-weight:700;text-decoration:none}
 .mbar a:first-child{background:var(--brand);color:var(--on-brand)}
 .mbar a:last-child{background:var(--accent);color:%(onAccent)s}
 footer.foot{padding-bottom:84px}
}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}
"""

SVG_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
SVG_PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s7-6.1 7-12a7 7 0 0 0-14 0c0 5.9 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>'
SVG_CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
SVG_CAL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>'
SVG_FB = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 8V6.3c0-.8.2-1.3 1.4-1.3H17V2h-2.6C11.3 2 10 3.6 10 6.1V8H8v3h2v11h4V11h2.7l.4-3H14z"/></svg>'
SVG_IG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>'
SVG_G = '<svg class="g" viewBox="0 0 48 48"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2A11.9 11.9 0 0 1 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3a12 12 0 0 1-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>'
SVG_BURGER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>'

def head(s, title, desc):
    t = s["theme"]
    return f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:image" content="{img(s['images']['hero'],1200)}">
<link rel="icon" href="{favicon(s)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{t['fontsQuery']}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<script type="application/ld+json">{json.dumps(schema(s))}</script>
</head>
<body>"""

def schema(s):
    d = {"@context":"https://schema.org","@type":s.get("schemaType","LocalBusiness"),"name":s["name"],"telephone":s["phoneIntl"],
         "address":{"@type":"PostalAddress","streetAddress":s.get("street",""),"addressLocality":s["suburb"],"addressRegion":s["state"],"postalCode":s.get("postcode",""),"addressCountry":"AU"},
         "areaServed":s["area"]}
    if s.get("rating"): d["aggregateRating"]={"@type":"AggregateRating","ratingValue":s["rating"],"reviewCount":s["reviewCount"]}
    return d

def nav(s, cur):
    items = [("index.html","Home"),("services.html","Services"),("about.html","About"),("contact.html","Contact")]
    li = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{n}</a></li>' for h,n in items)
    top = f"""<div class="top"><div class="wrap"><span class="hide-m">{E(s['topline'])}</span><span><a href="tel:{s['phoneIntl']}">Call {E(s['phone'])}</a></span></div></div>"""
    return f"""{top}
<header class="site"><div class="wrap nav">
 <a class="brandmark" href="index.html">{logo_svg(s)}<span><b>{E(s['short'])}</b><small>{E(s['tag'])}</small></span></a>
 <button class="burger" aria-label="Open menu" aria-expanded="false" onclick="var m=document.getElementById('menu');m.classList.toggle('open');this.setAttribute('aria-expanded',m.classList.contains('open'))">{SVG_BURGER}</button>
 <ul class="menu" id="menu">{li}<li><a class="btn btn-main" href="contact.html">{E(s['ctaLabel'])}</a></li></ul>
</div></header>"""

def foot(s):
    soc = ""
    if s.get("facebook"): soc += f'<a href="{E(s["facebook"])}" aria-label="Facebook" rel="noopener">{SVG_FB}</a>'
    if s.get("instagram"): soc += f'<a href="{E(s["instagram"])}" aria-label="Instagram" rel="noopener">{SVG_IG}</a>'
    svc = "".join(f'<li><a href="services.html#{sv["id"]}">{E(sv["title"])}</a></li>' for sv in s["services"][:5])
    hrs = "".join(f"<li>{E(d)}: {E(h)}</li>" for d,h in s["hours"])
    return f"""<footer class="foot"><div class="wrap">
 <div class="fgrid">
  <div><a class="brandmark" href="index.html">{logo_svg(s,40)}<span><b>{E(s['short'])}</b><small>{E(s['tag'])}</small></span></a><p style="margin-top:16px;opacity:.85;max-width:34ch">{E(s['footerBlurb'])}</p><div class="soc">{soc}</div></div>
  <div><h4>Services</h4><ul>{svc}</ul></div>
  <div><h4>Hours</h4><ul>{hrs}</ul></div>
  <div><h4>Contact</h4><ul><li><a href="tel:{s['phoneIntl']}">{E(s['phone'])}</a></li><li>{E(s['addressLine'])}</li><li><a href="contact.html">{E(s['ctaLabel'])}</a></li></ul></div>
 </div>
 <div class="legal"><span>© {YEAR} {E(s['name'])}. All rights reserved.</span><span>Developed with <span class="heart" aria-label="love">❤</span> by <a href="https://gemprogrammers.com" rel="noopener"><b>Mr. Developer</b></a></span></div>
</div></footer>
<div class="mbar"><a href="tel:{s['phoneIntl']}">Call now</a><a href="contact.html">{E(s['ctaLabel'])}</a></div>
</body></html>"""

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

def hero(s):
    t = s["theme"]; i = s["images"]; h = s["hero"]
    cta = f'<div class="cta"><a class="btn btn-main" href="contact.html">{SVG_CAL}{E(s["ctaLabel"])}</a><a class="btn btn-ghost" href="tel:{s["phoneIntl"]}">{SVG_PHONE}{E(s["phone"])}</a></div>'
    trust = '<div class="trust">' + "".join(f"<span><i>✔</i>{E(x)}</span>" for x in h["trust"]) + "</div>"
    v = t["hero"]
    if v == "split":
        return f"""<div class="hero hero-split"><div class="wrap"><div><h1>{E(h['title'])}</h1><p class="lede">{E(h['lede'])}</p>{cta}{trust}</div>
<div class="pic"><img src="{img(i['hero'])}" alt="{E(i['heroAlt'])}" fetchpriority="high">{badge(s)}</div></div></div>"""
    if v == "overlay":
        return f"""<div class="hero hero-overlay"><img src="{img(i['hero'],2000)}" alt="{E(i['heroAlt'])}" fetchpriority="high"><div class="wrap"><h1 style="max-width:16ch">{E(h['title'])}</h1><p class="lede">{E(h['lede'])}</p>{cta}{trust}</div></div>"""
    if v == "center":
        g = i["gallery"]
        return f"""<div class="hero hero-center"><div class="wrap"><h1 style="max-width:15ch;margin:0 auto">{E(h['title'])}</h1><p class="lede">{E(h['lede'])}</p>{cta}{trust}
<div class="collage"><img src="{img(g[0],700)}" alt=""><img src="{img(i['hero'],900)}" alt="{E(i['heroAlt'])}"><img src="{img(g[1],700)}" alt=""></div></div></div>"""
    if v == "stack":
        return f"""<div class="hero hero-stack"><div class="wrap"><h1>{h['titleHtml']}</h1><div class="row"><p class="lede" style="margin:0">{E(h['lede'])}</p>{cta}</div>{trust}<div style="height:34px"></div></div><img class="band" src="{img(i['hero'],2000)}" alt="{E(i['heroAlt'])}" fetchpriority="high"></div>"""
    if v == "arch":
        return f"""<div class="hero hero-arch"><div class="wrap"><div><h1>{h.get('titleHtml') or E(h['title'])}</h1><p class="lede">{E(h['lede'])}</p>{cta}{trust}</div><div class="pic"><img src="{img(i['hero'])}" alt="{E(i['heroAlt'])}" fetchpriority="high"></div></div></div>"""
    raise ValueError(v)

def reviews_block(s):
    if not s.get("reviews"):
        return ""
    score = f"""<div class="score"><b>{s['rating']}</b><div><div style="color:#F2B01E;font-size:22px;letter-spacing:2px">{stars(s['rating'])}</div><div>{s['reviewCount']} reviews on {E(s.get('ratingSource','Google'))}</div></div></div>""" if s.get("rating") else ""
    sub = f'<p>{E(s["reviewsSub"])}</p>' if s.get("reviewsSub") else ""
    return f"""<section class="dark"><div class="wrap">
 {score}
 <div class="head"><h2>{E(s['reviewsHead'])}</h2>{sub}</div>
 <div class="reviews">{review_cards(s)}</div>
</div></section>"""

def page_home(s):
    i = s["images"]
    cards = "".join(f'<article class="card"><img src="{img(sv["img"],800)}" alt="{E(sv["title"])}" loading="lazy"><div class="in"><h3>{E(sv["title"])}</h3><p>{E(sv["short"])}</p></div></article>' for sv in s["services"][:3])
    ticks = "".join(f"<li>{E(x)}</li>" for x in s["why"])
    gal = "".join(f'<img src="{img(g,900)}" alt="" loading="lazy">' for g in i["gallery"][:5])
    hrs = "".join(f"<tr><td>{E(d)}</td><td>{E(h)}</td></tr>" for d,h in s["hours"])
    mapq = urllib.parse.quote(s["mapQuery"])
    return (head(s, f'{s["name"]} | {s["seoTitle"]}', s["metaDesc"]) + nav(s,"index.html") + "<main>" + hero(s) + f"""
<section {"style='padding-top:130px'" if s['theme']['hero']=='center' else ''}><div class="wrap">
 <div class="head"><h2>{E(s['servicesHead'])}</h2><p>{E(s['servicesSub'])}</p></div>
 <div class="cards">{cards}</div>
 <p style="margin-top:30px"><a class="btn btn-ghost" href="services.html">See all services</a></p>
</div></section>
<section class="tone"><div class="wrap split">
 <img src="{img(i['about'],1100)}" alt="{E(i['aboutAlt'])}" loading="lazy">
 <div><h2>{E(s['whyHead'])}</h2><p>{E(s['whyText'])}</p><ul class="ticks">{ticks}</ul><p style="margin-top:26px"><a class="btn btn-main" href="about.html">About {E(s['ownerOrUs'])}</a></p></div>
</div></section>
<section><div class="wrap"><div class="head"><h2>{E(s['galleryHead'])}</h2><p>{E(s['gallerySub'])}</p></div><div class="gallery">{gal}</div></div></section>
{reviews_block(s)}
<section><div class="wrap info">
 <div><div class="head" style="margin-bottom:24px"><h2>Hours &amp; location</h2><p>{E(s['areaText'])}</p></div><table class="hours">{hrs}</table>
 <p style="margin-top:26px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-main" href="contact.html">{E(s['ctaLabel'])}</a><a class="btn btn-ghost" href="tel:{s['phoneIntl']}">{E(s['phone'])}</a></p></div>
 <iframe class="map" title="Map showing {E(s['name'])}" loading="lazy" src="https://maps.google.com/maps?q={mapq}&z=13&output=embed"></iframe>
</div></section>
<div class="ctaband"><div class="wrap"><h2>{E(s['bandText'])}</h2><a class="btn btn-main" href="contact.html">{E(s['ctaLabel'])}</a></div></div>
</main>""" + foot(s))

def pagehead(s, title, sub, crumb):
    return f'<div class="pagehead"><div class="wrap"><div class="crumbs"><a href="index.html">Home</a> / {E(crumb)}</div><h1>{E(title)}</h1><p>{E(sub)}</p></div></div>'

def page_services(s):
    rows = ""
    for sv in s["services"]:
        pts = "".join(f"<li>{E(p)}</li>" for p in sv.get("points",[]))
        rows += f'<div class="svc-row" id="{sv["id"]}"><div class="svc-pic"><img src="{img(sv["img"],1100)}" alt="{E(sv["title"])}" loading="lazy"></div><div><h2>{E(sv["title"])}</h2><p>{E(sv["long"])}</p><ul class="ticks">{pts}</ul><p style="margin-top:24px"><a class="btn btn-main" href="contact.html">{E(s["ctaLabel"])}</a></p></div></div>'
    faq = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q,a in s["faq"])
    return (head(s, f'Services | {s["name"]}', f'{s["name"]} services: ' + ", ".join(x["title"] for x in s["services"]) + ".") + nav(s,"services.html") + "<main>" +
            pagehead(s, s["servicesHead"], s["servicesSub"], "Services") +
            f'<section style="padding-top:30px"><div class="wrap">{rows}</div></section><section class="tone"><div class="wrap" style="max-width:860px"><div class="head"><h2>Common questions</h2></div><div class="faq">{faq}</div></div></section>'
            f'<div class="ctaband"><div class="wrap"><h2>{E(s["bandText"])}</h2><a class="btn btn-main" href="contact.html">{E(s["ctaLabel"])}</a></div></div></main>' + foot(s))

def page_about(s):
    i = s["images"]
    paras = "".join(f"<p>{E(p)}</p>" for p in s["aboutParas"])
    vals = "".join(f'<article class="card"><div class="in"><h3>{E(a)}</h3><p>{E(b)}</p></div></article>' for a,b in s["values"])
    gal = "".join(f'<img src="{img(g,900)}" alt="" loading="lazy">' for g in i["gallery"][1:6])
    return (head(s, f'About | {s["name"]}', s["metaDesc"]) + nav(s,"about.html") + "<main>" +
            pagehead(s, s["aboutHead"], s["aboutSub"], "About") +
            f'<section><div class="wrap split"><div>{paras}<p style="margin-top:26px"><a class="btn btn-main" href="contact.html">{E(s["ctaLabel"])}</a></p></div><img src="{img(i["about2"],1100)}" alt="{E(i["aboutAlt"])}" loading="lazy"></div></section>'
            f'<section class="tone"><div class="wrap"><div class="head"><h2>{E(s["valuesHead"])}</h2></div><div class="cards">{vals}</div></div></section>' +
            (f'<section class="dark"><div class="wrap"><div class="head"><h2>{E(s["reviewsHead"])}</h2></div><div class="reviews">{review_cards(s,3)}</div></div></section>' if s.get("reviews") else "") +
            f'<section><div class="wrap"><div class="gallery">{gal}</div></div></section></main>' + foot(s))

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
<form class="book" name="{fname}" data-sms="{s['phoneIntl']}" data-biz="{E(s['short'])}" onsubmit="return sendReq(this)">
 <h2 style="font-size:30px">{E(s['formHead'])}</h2>
 <div class="two"><label>Your name<input name="name" required autocomplete="name"></label><label>Phone<input name="phone" type="tel" required autocomplete="tel"></label></div>
 <div class="two"><label>Email<input name="email" type="email" autocomplete="email"></label><label>Suburb<input name="suburb" autocomplete="address-level2"></label></div>
 {extra}
 <label>What do you need?<select name="service">{opts}</select></label>
 <label>Anything we should know?<textarea name="message" rows="4"></textarea></label>
 <button type="submit">{E(s['formButton'])}</button>
 <p class="note-sms" style="font-size:14px;color:var(--muted)">Your messages app will open with your request ready to send. Prefer to talk? Call {E(s['phone'])}.</p>
</form>
<script>
function sendReq(f){{var d=new FormData(f),t=[];
t.push("Hi "+f.dataset.biz+", booking request:");
d.forEach(function(v,k){{if(v)t.push(k.charAt(0).toUpperCase()+k.slice(1).replace(/_/g," ")+": "+v);}});
var body=encodeURIComponent(t.join(String.fromCharCode(10)));var sep=/iPhone|iPad|Mac/i.test(navigator.userAgent)?"&":"?";
window.location.href="sms:"+f.dataset.sms+sep+"body="+body;return false;}}
</script>
<div class="contact-card">
 <a class="line" href="tel:{s['phoneIntl']}"><span class="ic">{SVG_PHONE}</span><span><b>{E(s['phone'])}</b><small>Call or text any time during business hours</small></span></a>
 {book}
 <a class="line" href="https://www.google.com/maps/search/?api=1&query={mapq}" rel="noopener"><span class="ic">{SVG_PIN}</span><span><b>{E(s['addressLine'])}</b><small>{E(s['areaShort'])}</small></span></a>
 <div class="line" style="display:block;padding:18px;border:1px solid var(--line);border-radius:var(--r)"><div style="display:flex;gap:14px;align-items:center;margin-bottom:8px"><span class="ic">{SVG_CLOCK}</span><b>Opening hours</b></div><table class="hours">{hrs}</table></div>
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
    out = ROOT / s["slug"]; out.mkdir(exist_ok=True)
    for f in out.glob("*.html"): f.unlink()
    (out/"style.css").write_text(CSS % t)
    (out/"index.html").write_text(page_home(s))
    (out/"services.html").write_text(page_services(s))
    (out/"about.html").write_text(page_about(s))
    (out/"contact.html").write_text(page_contact(s))
    (out/"thanks.html").write_text(page_thanks(s))
    print("built", s["slug"])

if __name__ == "__main__":
    files = sys.argv[1:] or sorted(str(p) for p in SITES.glob("*.json"))
    for f in files: build(f)
