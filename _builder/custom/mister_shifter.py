#!/usr/bin/env python3
"""Custom multi-page site for Mister Shifter Removals (Lismore NSW) -> ../../mister-shifter-removals/
Built separately from build.py: real photos (img/), own design, blog, service pages, FormSubmit contact form.
Run: python3 _builder/custom/mister_shifter.py
Facts used come from the owner's own signage/photos and his message: local & interstate moves, pickups/deliveries,
domestic & green waste removal, trucks, Lismore base, phone, email, Facebook. Nothing else is claimed."""
import pathlib, html, json, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "mister-shifter-removals"
E = html.escape

BIZ = {
 "name": "Mister Shifter Removals", "short": "Mister Shifter",
 "phone": "0475 074 906", "phoneIntl": "+61475074906",
 "email": "willhayes666@gmail.com",
 "fb": "https://www.facebook.com/mistershifterremovals/",
 "town": "Lismore", "state": "NSW", "postcode": "2480",
 "owner": "Will",
 "site": "https://aliraza-s.github.io/au-biz/mister-shifter-removals/",
 "abn": "",   # add when Will supplies it
}
TOWNS = ["Lismore", "Goonellabah", "Ballina", "Byron Bay", "Casino", "Alstonville", "Bangalow", "Kyogle", "Nimbin", "Evans Head", "Lennox Head", "Tweed Heads"]

def U(id_, w=1200): return f"https://images.unsplash.com/photo-{id_}?auto=format&fit=crop&w={w}&q=80"

SERVICES = [
 {"id":"local-moves","title":"Local moves","tag":"Lismore & Northern Rivers","icon":"truck","img":"img/house.jpg",
  "short":"House and unit moves around Lismore and the Northern Rivers, done by truck with a proper crew.",
  "lede":"Moving across town or to the next one over? Our pantech trucks and crew handle the lot, from a one-bedroom unit to a full family home.",
  "body":["A local move with Mister Shifter starts with a quick call or message. Tell Will where you are, where you're going, how big the place is and when you'd like to move, and he'll give you a straight quote.",
          "On the day the crew arrives with the truck, blankets and straps, loads carefully, drives it over and unloads where you want it. No ute runs back and forth, it goes in one truck.",
          "We work across Lismore and the Northern Rivers, including the hinterland and coast."],
  "points":["Houses, units and granny flats","Pantech trucks, not a ute","Furniture wrapped and strapped","Straight quotes by phone"],
  "faq":[["How far ahead should I book?","As early as you can, especially for end-of-month and weekend moves. Call and we'll tell you what's open."],
         ["Do I need to pack everything?","Boxes packed and sealed before we arrive keeps the move quick. Furniture we'll wrap and handle on the day."]]},
 {"id":"interstate-moves","title":"Interstate moves","tag":"NSW · QLD · beyond","icon":"map",
  "img":U("1736333568932-7b28d3d5a3f3",1200),
  "short":"Heading over the border or further? We load it in Lismore and deliver it to your new door.",
  "lede":"Interstate moves from the Northern Rivers. One truck, one crew, your belongings loaded once and unloaded at the other end.",
  "body":["Moving interstate from Lismore means a long day on the road and a lot that can go wrong if the load isn't done right. We wrap, stack and strap everything so it arrives the way it left.",
          "Call with the destination, the size of your home and the dates you're working to. Will will work out the truck, the crew and the timing, and give you a quote for the whole job.",
          "Ask about your destination and Will will tell you if it's a run we do and what it will cost."],
  "points":["Door to door, one truck","Loaded and strapped for the highway","Clear quote before you commit","Flexible dates where possible"],
  "faq":[["Which states do you go to?","Call with your destination and Will will tell you if it's a run we do."],
         ["Is my stuff on the truck with other people's?","Ask when you book. Will can tell you how your move will be loaded."]]},
 {"id":"pickups-deliveries","title":"Pickups & deliveries","tag":"Furniture · marketplace · store buys","icon":"box","img":"img/truck.jpg",
  "short":"Bought a couch on Marketplace or a fridge in town? We'll collect it and deliver it to your door.",
  "lede":"Single-item pickups and deliveries around the Northern Rivers: furniture, whitegoods, marketplace buys and anything too big for the car.",
  "body":["Not every job is a full move. Sometimes it's a lounge from Ballina, a fridge from a store in Lismore, or a bed frame that needs to get to a rental.",
          "Send Will the pickup address, the drop-off address and what the item is, and he'll give you a price. The truck comes with trolleys, blankets and straps, so it arrives in one piece.",
          "Good for marketplace buys, store deliveries, moving items between family members, and getting things into or out of storage."],
  "points":["Furniture and whitegoods","Marketplace and store pickups","Storage runs","Priced per job"],
  "faq":[["Can you pick up from a store for me?","Yes. Give us the store, the order details and where it's going."],
         ["Do you take things upstairs?","Usually yes. Mention stairs or tight access when you book so we send the right crew."]]},
 {"id":"waste-removal","title":"Domestic & green waste removal","tag":"Clean-outs · garden waste · tip runs","icon":"leaf","img":U("1781517028333-85014c59c9a4",1200),
  "short":"Clean-outs, garden waste and tip runs. We load it, take it away and leave the place clear.",
  "lede":"Domestic and green waste removal for homes around Lismore and the Northern Rivers. Old furniture, clean-out piles, garden trimmings and storm debris.",
  "body":["Moving out, clearing a deceased estate, or just finally dealing with the pile behind the shed? We bring the truck, load what you point at and take it away.",
          "Green waste after a big garden tidy-up or a storm is the same deal. Branches, palm fronds, clippings and the lot.",
          "Tell Will roughly how much there is (a trailer load, half a truck, a full truck) and he'll quote it. End-of-lease clean-outs can be combined with your move."],
  "points":["Household junk and old furniture","Garden and green waste","End-of-lease clean-outs","Combine with your move"],
  "faq":[["What can't you take?","Call to check. Some materials have to go to specific facilities."],
         ["Can you do it on the same day as my move?","Often yes. Mention it when you book and we'll plan the truck around it."]]},
]

POSTS = [
 {"slug":"blog-moving-day-checklist","title":"Moving day in the Northern Rivers: a checklist that actually helps","date":"October 2026","img":U("1700165644892-3dd6b67b25bc",1200),
  "intro":"A move goes smoothly when the boring bits are done before the truck turns up. Here's the list we'd give our own family.",
  "sections":[
   ["Two weeks out","Book the truck and lock in the date. Start using up frozen food. Order boxes, tape and a couple of markers. Tell your landlord or agent your dates. Book a cleaner for the old place if you're renting."],
   ["One week out","Pack the rooms you use least first: spare room, garage, bookshelves. Label every box with the room it's going to, not just what's in it. Redirect your mail and update your address with the bank, Medicare, the electoral roll and your car rego."],
   ["The day before","Defrost the fridge and freezer. Pack a 'first night' box: kettle, mugs, chargers, toiletries, bed linen, a change of clothes and the kids' favourites. Take photos of how the TV and modem cables are plugged in."],
   ["Moving day","Clear a path from the front door to the driveway. Keep pets and kids somewhere safe. Walk the crew through the house so they know what's going and what's staying. Do a last check of cupboards, the garden shed and behind doors before you leave."],
   ["At the new place","Point the crew to the right rooms as the boxes come off. Beds and the fridge first, everything else can wait. Then put the kettle on."]]},
 {"slug":"blog-interstate-move-tips","title":"Moving interstate from Lismore: what to sort out first","date":"October 2026","img":U("1716441592984-75d4c882e5cf",1200),
  "intro":"An interstate move is a bigger job than a local one, but most of the extra work is admin. Get these sorted early and the move itself is the easy part.",
  "sections":[
   ["Get your dates straight","Interstate moves involve a long drive and sometimes an overnight stop, so the pickup day and the delivery day may not be the same. Book early, confirm both dates, and make sure the new place is ready to receive the truck."],
   ["Declutter before you pay to move it","Every item on the truck is weight and space you're paying for. Sell, donate or dump anything you haven't used in a year. A green and domestic waste run before the move is often cheaper than carting junk across the border."],
   ["Change over the paperwork","Driver's licence and car registration need transferring to the new state within a set period. Update your address with the ATO, Medicare, your super fund, your bank and your employer. Transfer or cancel utilities and internet."],
   ["Pack for the highway","Wrap fragile items more than you would for a local move. Fill boxes so nothing rattles. Label the boxes you'll need first and ask for them to go on last so they come off first."],
   ["Keep the essentials with you","Passports, medications, important documents, jewellery and anything you can't replace travel in your car, not the truck."]]},
 {"slug":"blog-green-waste","title":"Green waste and clean-outs: what to do with the pile out the back","date":"October 2026","img":U("1760009449712-09befce78964",1200),
  "intro":"After a storm, a big garden tidy-up or a shed clean-out, the pile grows faster than the car can shift it. Here's how to deal with it without spending every weekend at the tip.",
  "sections":[
   ["Sort it into three piles","Green waste (branches, fronds, clippings), general household junk (old furniture, broken appliances, boxes of nothing), and things that need special handling (paint, chemicals, gas bottles, batteries, tyres). The first two go on the truck. The third needs a specific drop-off point, and your council website lists them."],
   ["Break it down","Cut branches to manageable lengths and stack them the same way. Flatten boxes. Pull drawers out of dressers so they're lighter to carry. The quicker it loads, the less the job costs."],
   ["Combine it with a move","If you're moving out, a clean-out on the same day as the move saves a second truck and a second callout. Tell us when you book and we'll plan the load."],
   ["Give us an honest size","A trailer load, half a truck or a full truck. It helps us quote it right and bring the right crew. Photos help too."]]},
 {"slug":"blog-packing-tips","title":"Packing tips that make the truck load faster (and cost less)","date":"October 2026","img":U("1580674285054-bed31e145f59",1200),
  "intro":"The crew can only move as fast as the house is packed. A well-packed house loads in a fraction of the time, and that shows up on your bill.",
  "sections":[
   ["Use proper boxes","Uniform boxes stack. Random bags, laundry baskets and open containers don't, and they take up more truck space than they should. Book boxes for books and heavy things, tea chests for linen and light items."],
   ["Heavy on the bottom, light on top","Pack heavy items in small boxes so they're still liftable. Fill gaps with paper or towels so nothing moves. Tape the bottom twice."],
   ["Label the room, not the contents","'Kitchen' on two sides of the box is more useful than a list of what's inside. The crew puts it where it belongs without asking, and you unpack room by room."],
   ["Disassemble what you can","Bed frames, dining tables and flat-pack furniture travel better in pieces. Keep screws and bolts in a labelled zip bag taped to the piece they belong to."],
   ["Leave the fridge, washer and big furniture to us","We wrap and move them. Just have the fridge defrosted and the washing machine drained and disconnected the night before."]]},
]

# ---------------------------------------------------------------- icons
ICO = {
 "truck":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/></svg>',
 "map":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z"/><path d="M9 4v14M15 6v14"/></svg>',
 "box":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8l9-4 9 4-9 4z"/><path d="M3 8v8l9 4 9-4V8"/><path d="M12 12v8"/></svg>',
 "leaf":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 4c-9 0-15 5-15 12 0 1.6.4 3 1 4 7 0 14-5 14-16z"/><path d="M5 20c3-5 7-8 12-11"/></svg>',
 "phone":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
 "mail":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
 "pin":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s7-6.1 7-12a7 7 0 0 0-14 0c0 5.9 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>',
 "clock":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "check":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5 9-10"/></svg>',
 "fb":'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 8V6.3c0-.8.2-1.3 1.4-1.3H17V2h-2.6C11.3 2 10 3.6 10 6.1V8H8v3h2v11h4V11h2.7l.4-3H14z"/></svg>',
 "chat":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg>',
 "shield":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 5-3.5 8.5-8 9-4.5-.5-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/></svg>',
 "arrow":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "menu":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>',
}

_OLD_LOGO_SVG = '''<svg viewBox="0 0 300 64" width="190" height="40" aria-label="Mister Shifter Removals" role="img"><rect width="300" height="64" rx="6" fill="#0a0a0a"/><path d="M12 48c4-16 14-30 32-30 10 0 16 6 18 14-6-4-12-6-18-4-8 3-12 10-14 20z" fill="none" stroke="#35E51B" stroke-width="3" stroke-linejoin="round"/><text x="74" y="27" font-family="Barlow Condensed,Impact,sans-serif" font-weight="800" font-size="24" fill="#35E51B" letter-spacing="1">MISTER SHIFTER</text><text x="74" y="52" font-family="Barlow Condensed,Impact,sans-serif" font-weight="800" font-size="22" fill="#ffffff" letter-spacing="3">REMOVALS</text></svg>'''
FAVICON = "data:image/svg+xml," + urllib.parse.quote('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#0a0a0a"/><text x="16" y="24" text-anchor="middle" font-family="Impact,sans-serif" font-size="22" font-weight="800" fill="#35E51B">MS</text></svg>')

INDEXABLE = False   # flip to True once the site is on the client's own domain (also set BIZ["site"] to that domain)
IMG_SIZES = {"img/fleet.jpg":(1600,1592),"img/family.jpg":(636,634),"img/house.jpg":(720,719),"img/heart.jpg":(1000,1002),"img/team.jpg":(1002,1000),"img/truck.jpg":(1002,1000),"img/logo-t.png":(890,402)}

def IM(src, alt="", cls="", lazy=True, extra=""):
    """<img> with width/height for CLS, lazy by default."""
    wh = IMG_SIZES.get(src)
    dims = f' width="{wh[0]}" height="{wh[1]}"' if wh else ""
    return f'<img src="{src}" alt="{E(alt)}"{dims}{" loading=\"lazy\" decoding=\"async\"" if lazy else " fetchpriority=\"high\""}{" class=\""+cls+"\"" if cls else ""}{extra}>'

LOGO = IM("img/logo-t.png", "Mister Shifter Removals", "logo", lazy=False)

# ---------------------------------------------------------------- CSS
CSS = r"""
:root{--black:#060d14;--ink:#0f1720;--panel:#0d1823;--panel2:#13222f;--green:#2fe41b;--green2:#1fae12;--greenD:#1a8f10;--white:#fff;--paper:#f5f6f3;--paper2:#e8ebe4;--muted:#5b6670;--mutedD:#9fb0bd;--line:#dde2db;--lineD:rgba(255,255,255,.1);--r:18px;--hf:"Barlow Condensed",Impact,sans-serif;--bf:Barlow,system-ui,sans-serif;--glow:0 0 0 1px rgba(47,228,27,.25),0 20px 60px rgba(47,228,27,.18)}
*{box-sizing:border-box;margin:0}
html{scroll-behavior:smooth}
body{font-family:var(--bf);color:var(--ink);background:var(--paper);line-height:1.6;font-size:17px;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{max-width:100%;display:block;height:auto}
a{color:inherit}
:focus-visible{outline:3px solid var(--green);outline-offset:3px}
h1,h2,h3,h4,.hf{font-family:var(--hf);font-weight:800;line-height:.98;letter-spacing:.01em;text-transform:uppercase}
.wrap{max-width:1220px;margin:0 auto;padding:0 24px}
.eyebrow{display:inline-flex;align-items:center;gap:10px;font-size:12.5px;letter-spacing:.2em;text-transform:uppercase;font-weight:700;color:var(--greenD);margin-bottom:16px}
.eyebrow:before{content:"";width:10px;height:10px;border-radius:50%;background:var(--green);box-shadow:0 0 0 4px rgba(47,228,27,.2)}
.dark .eyebrow,.hero .eyebrow,.ph .eyebrow{color:var(--green)}
.btn{display:inline-flex;align-items:center;gap:10px;padding:16px 28px;border-radius:999px;font-weight:800;text-decoration:none;border:2px solid transparent;transition:transform .18s,background .18s,box-shadow .18s,border-color .18s;line-height:1;font-family:var(--hf);text-transform:uppercase;letter-spacing:.07em;font-size:18px}
.btn:hover{transform:translateY(-2px)}
.btn svg{width:20px;height:20px;flex:0 0 20px}
.btn-green{background:var(--green);color:#06130a;box-shadow:0 12px 32px rgba(47,228,27,.28)}
.btn-green:hover{background:#49ff35;box-shadow:0 16px 40px rgba(47,228,27,.38)}
.btn-dark{background:var(--black);color:#fff}
.btn-dark:hover{background:#0f1c29}
.btn-ghost{border-color:var(--ink)}
.btn-ghostW{border-color:rgba(255,255,255,.4);color:#fff;backdrop-filter:blur(6px)}
.btn-ghostW:hover{border-color:#fff}
.js .rv{opacity:0;transform:translateY(24px);transition:opacity .75s cubic-bezier(.2,.7,.2,1),transform .75s cubic-bezier(.2,.7,.2,1)}
.js .rv.in{opacity:1;transform:none}
.js .rv.d1{transition-delay:.1s}.js .rv.d2{transition-delay:.2s}.js .rv.d3{transition-delay:.3s}
/* header */
.topbar{background:#03080d;color:#aab6c0;font-size:14px}
.topbar .wrap{display:flex;justify-content:space-between;gap:16px;padding:8px 24px;flex-wrap:wrap}
.topbar a{text-decoration:none;color:#fff;font-weight:600}
.topbar b{color:var(--green)}
header.site{position:sticky;top:0;z-index:30;background:rgba(6,13,20,.86);backdrop-filter:blur(14px);color:#fff;border-bottom:1px solid var(--lineD)}
.nav{display:flex;align-items:center;justify-content:space-between;height:84px;gap:18px}
.brand{display:flex;align-items:center;text-decoration:none}
.brand .logo{height:62px;width:auto}
.menu{display:flex;gap:2px;align-items:center;list-style:none;padding:0}
.menu a{text-decoration:none;font-weight:600;font-size:15.5px;padding:10px 13px;border-radius:999px;color:#e4e9ee;position:relative}
.menu a:hover{background:rgba(255,255,255,.07)}
.menu a[aria-current]{color:var(--green)}
.menu .btn{padding:12px 20px;font-size:16px;margin-left:10px}
.burger{display:none;background:none;border:0;color:#fff;padding:8px;cursor:pointer}
.burger svg{width:28px;height:28px}
/* hero */
.hero{position:relative;color:#fff;overflow:hidden;background:var(--black)}
.hero .bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:60% 45%;opacity:.55}
.hero:before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(6,13,20,.96) 0%,rgba(6,13,20,.82) 42%,rgba(6,13,20,.35) 100%);z-index:1}
.hero:after{content:"";position:absolute;width:70vw;height:70vw;max-width:900px;max-height:900px;border-radius:50%;background:radial-gradient(closest-side,rgba(47,228,27,.28),transparent 70%);left:-20vw;top:-30vw;z-index:1;pointer-events:none}
.hero .wrap{position:relative;z-index:2;display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center;padding-top:88px;padding-bottom:96px;min-height:min(88vh,800px)}
.hero h1{font-size:clamp(50px,7.8vw,112px);max-width:11ch}
.hero h1 em{font-style:normal;color:var(--green);position:relative;display:inline-block}
.hero .lede{font-size:clamp(18px,1.7vw,22px);max-width:50ch;margin:24px 0 34px;color:#d6dde4}
.hero .cta{display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.chips{display:flex;gap:10px;flex-wrap:wrap;margin-top:34px}
.chips span{display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);border-radius:999px;padding:8px 14px;font-size:14px;font-weight:600;backdrop-filter:blur(6px)}
.chips svg{width:16px;height:16px;color:var(--green)}
.qq{background:rgba(13,24,35,.78);border:1px solid rgba(255,255,255,.14);border-radius:24px;padding:28px;backdrop-filter:blur(14px);box-shadow:0 30px 80px rgba(0,0,0,.45);display:grid;gap:12px}
.qq h3{font-size:30px;color:#fff}
.qq h3 em{font-style:normal;color:var(--green)}
.qq p{color:var(--mutedD);font-size:15px;margin-top:-6px}
.qq label{display:grid;gap:5px;font-size:13px;font-weight:600;color:#cfd8df}
.qq input,.qq select{font:inherit;padding:12px 14px;border:1px solid rgba(255,255,255,.14);border-radius:12px;background:rgba(255,255,255,.06);color:#fff;width:100%}
.qq select option{color:#000}
.qq input::placeholder{color:#7f8c97}
.qq input:focus,.qq select:focus{outline:0;border-color:var(--green);box-shadow:0 0 0 3px rgba(47,228,27,.25)}
.qq .two{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.qq button{font:inherit;font-family:var(--hf);text-transform:uppercase;letter-spacing:.07em;font-weight:800;font-size:19px;background:var(--green);color:#06130a;border:0;padding:16px;border-radius:999px;cursor:pointer;margin-top:4px;transition:transform .18s,background .18s}
.qq button:hover{background:#49ff35;transform:translateY(-2px)}
.qq small{color:var(--mutedD);font-size:12.5px;text-align:center}
/* trust bar */
.trustbar{background:#03080d;color:#fff;border-top:1px solid var(--lineD)}
.trustbar .wrap{display:grid;grid-template-columns:repeat(4,1fr)}
.trustbar div{display:flex;gap:14px;align-items:center;padding:22px 18px;border-left:1px solid var(--lineD)}
.trustbar div:first-child{border-left:0;padding-left:0}
.trustbar svg{width:30px;height:30px;color:var(--green);flex:0 0 30px}
.trustbar b{display:block;font-family:var(--hf);font-size:21px;text-transform:uppercase;letter-spacing:.03em}
.trustbar small{color:var(--mutedD)}
.strip{background:var(--green);color:#06130a;overflow:hidden;white-space:nowrap;padding:13px 0;font-family:var(--hf);font-weight:800;font-size:19px;letter-spacing:.08em;text-transform:uppercase}
.strip div{display:inline-block;animation:tick 38s linear infinite}
.strip span{padding:0 28px}
@keyframes tick{to{transform:translateX(-50%)}}
/* sections */
section{padding:100px 0}
.head{max-width:740px;margin-bottom:48px}
.head.c{text-align:center;margin-left:auto;margin-right:auto}
.head.row{max-width:none;display:flex;justify-content:space-between;align-items:flex-end;gap:28px;flex-wrap:wrap}
.head.row p{max-width:54ch}
.head h2{font-size:clamp(38px,5.2vw,68px)}
.head p{color:var(--muted);font-size:18.5px;margin-top:14px}
.dark{background:var(--black);color:#fff}
.dark .head p{color:var(--mutedD)}
.tone{background:var(--paper2)}
/* services bento */
.bento{display:grid;grid-template-columns:1.25fr 1fr;grid-auto-rows:minmax(160px,auto);gap:18px}
.bento .big{grid-row:span 3;position:relative;border-radius:var(--r);overflow:hidden;min-height:520px;display:flex;align-items:flex-end;color:#fff;text-decoration:none;background:#1b2a37}
.bento .big img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .8s}
.bento .big:hover img{transform:scale(1.05)}
.bento .big .in{position:relative;z-index:2;padding:34px;background:linear-gradient(transparent,rgba(6,13,20,.92) 60%);width:100%}
.bento .big h3{font-size:40px;margin:10px 0 8px}
.bento .big p{color:#d6dde4;max-width:44ch}
.bento .ic{width:48px;height:48px;border-radius:14px;background:var(--green);color:#06130a;display:grid;place-items:center}
.bento .ic svg{width:24px;height:24px}
.bento .sm{display:flex;gap:20px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:18px;text-decoration:none;transition:transform .25s,box-shadow .25s,border-color .25s}
.bento .sm:hover{transform:translateX(8px);box-shadow:0 20px 44px rgba(0,0,0,.1);border-color:var(--green)}
.bento .sm .pic{width:150px;height:130px;border-radius:12px;overflow:hidden;flex:0 0 150px;background:#1b2a37}
.bento .sm img{width:100%;height:100%;object-fit:cover}
.bento .sm h3{font-size:25px;margin-bottom:4px}
.bento .sm p{color:var(--muted);font-size:15.5px}
.bento .sm .go{margin-left:auto;width:44px;height:44px;border-radius:50%;border:2px solid var(--line);display:grid;place-items:center;flex:0 0 44px;transition:background .2s,border-color .2s,color .2s}
.bento .sm:hover .go{background:var(--green);border-color:var(--green)}
.bento .sm .go svg{width:18px;height:18px}
/* why */
.why{display:grid;grid-template-columns:.9fr 1.1fr;gap:56px;align-items:center}
.why .pic{position:relative}
.why .pic img{border-radius:var(--r) 120px var(--r) var(--r);aspect-ratio:1;object-fit:cover;width:100%}
.why .float{position:absolute;left:-18px;bottom:28px;background:var(--green);color:#06130a;border-radius:16px;padding:16px 20px;box-shadow:0 20px 40px rgba(0,0,0,.35)}
.why .float b{display:block;font-family:var(--hf);font-size:26px;text-transform:uppercase;line-height:1}
.why .float small{font-weight:600}
.feat{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:30px}
.feat.three{grid-template-columns:repeat(3,1fr)}
.feat div{background:var(--panel);border:1px solid var(--lineD);border-radius:16px;padding:22px}
.feat svg{width:28px;height:28px;color:var(--green);margin-bottom:10px}
.feat b{display:block;font-family:var(--hf);font-size:22px;text-transform:uppercase;margin-bottom:4px}
.feat p{color:var(--mutedD);font-size:15px}
/* timeline */
.tl{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;position:relative;counter-reset:s}
.tl:before{content:"";position:absolute;left:4%;right:4%;top:34px;height:2px;background:linear-gradient(90deg,var(--green),rgba(47,228,27,.15))}
.tl div{position:relative;padding-top:92px}
.tl div:before{counter-increment:s;content:"0" counter(s);position:absolute;top:0;left:0;width:68px;height:68px;border-radius:50%;background:var(--green);color:#06130a;font-family:var(--hf);font-size:28px;font-weight:800;display:grid;place-items:center;box-shadow:0 0 0 10px var(--paper)}
.tl h3{font-size:27px;margin-bottom:8px}
.tl p{color:var(--muted)}
/* gallery */
.gal{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.gal a{display:block;border-radius:var(--r);overflow:hidden;background:#1b2a37;aspect-ratio:1;position:relative}
.gal img{width:100%;height:100%;object-fit:cover;transition:transform .6s}
.gal a:hover img{transform:scale(1.05)}
.gal a:first-child{grid-column:span 2;grid-row:span 2;aspect-ratio:auto}
.gal span{position:absolute;left:14px;bottom:14px;background:rgba(6,13,20,.8);color:#fff;font-size:13px;font-weight:600;padding:6px 12px;border-radius:999px;backdrop-filter:blur(6px)}
/* blog cards */
.posts{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.posts.two{grid-template-columns:repeat(2,1fr)}
.post{background:#fff;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;text-decoration:none;display:flex;flex-direction:column;transition:transform .25s,box-shadow .25s}
.post:hover{transform:translateY(-6px);box-shadow:0 26px 50px rgba(0,0,0,.12)}
.post .pic{aspect-ratio:16/10;overflow:hidden;background:#1b2a37}
.post img{width:100%;height:100%;object-fit:cover;transition:transform .6s}
.post:hover img{transform:scale(1.05)}
.post .in{padding:22px 24px 26px}
.post small{color:var(--greenD);font-weight:700;letter-spacing:.12em;text-transform:uppercase;font-size:12px}
.post h3{font-size:24px;margin:8px 0 10px;text-transform:none;letter-spacing:0;line-height:1.15}
.post p{color:var(--muted);font-size:15.5px}
/* areas */
.areas{display:flex;flex-wrap:wrap;gap:10px}
.areas span{background:var(--panel);border:1px solid var(--lineD);border-radius:999px;padding:10px 18px;font-weight:600}
.light .areas span{background:#fff;border-color:var(--line)}
.map{width:100%;height:420px;border:0;border-radius:var(--r);filter:grayscale(.35) saturate(.8)}
/* proof */
.proof{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.proof a{display:flex;gap:18px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:26px;text-decoration:none;transition:transform .2s,box-shadow .2s}
.proof a:hover{transform:translateY(-4px);box-shadow:0 18px 36px rgba(0,0,0,.1)}
.proof .ic{width:58px;height:58px;border-radius:16px;background:var(--black);color:var(--green);display:grid;place-items:center;flex:0 0 58px}
.proof .ic svg{width:26px;height:26px}
.proof b{display:block;font-family:var(--hf);font-size:24px;text-transform:uppercase}
.proof small{color:var(--muted)}
/* faq */
.faq details{border:1px solid var(--line);border-radius:14px;padding:4px 20px;background:#fff;margin-bottom:10px}
.dark .faq details{border-color:var(--lineD);background:var(--panel)}
.faq summary{font-weight:700;cursor:pointer;font-size:17.5px;list-style:none;display:flex;justify-content:space-between;gap:16px;padding:14px 0}
.faq summary::-webkit-details-marker{display:none}
.faq summary:after{content:"+";font-size:26px;line-height:1;color:var(--greenD);font-family:var(--hf)}
.faq details[open] summary:after{content:"–"}
.faq p{padding:0 0 16px;color:var(--muted)}
.dark .faq p{color:var(--mutedD)}
.faq-grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:56px;align-items:start}
/* cta */
.ctab{background:var(--green);color:#06130a;padding:76px 0;position:relative;overflow:hidden}
.ctab:after{content:"";position:absolute;width:520px;height:520px;border-radius:50%;background:rgba(255,255,255,.18);right:-160px;top:-220px}
.ctab .wrap{display:flex;justify-content:space-between;align-items:center;gap:28px;flex-wrap:wrap;position:relative;z-index:2}
.ctab h2{font-size:clamp(36px,4.8vw,64px);max-width:16ch}
.ctab .big{font-family:var(--hf);font-size:clamp(36px,4.8vw,64px);text-decoration:none;display:block;line-height:1}
.ctab p{font-weight:600;margin-top:6px}
/* pagehead */
.ph{position:relative;color:#fff;padding:110px 0 76px;overflow:hidden;background:var(--black)}
.ph>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.4}
.ph:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(6,13,20,.95),rgba(6,13,20,.55))}
.ph .wrap{position:relative;z-index:2}
.ph h1{font-size:clamp(44px,6.6vw,88px);max-width:16ch}
.ph p{font-size:19px;color:#d6dde4;max-width:56ch;margin-top:14px}
.crumbs{font-size:14px;color:#9fb0bd;margin-bottom:16px}
.crumbs a{text-decoration:none}
/* service pages */
.svc-hero{display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:center}
.svc-hero img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:var(--r)}
.svc-hero h2{font-size:clamp(34px,4.2vw,54px);margin-bottom:14px}
.svc-hero p+p{margin-top:12px}
.ticks{list-style:none;padding:0;margin-top:22px;display:grid;gap:12px}
.ticks li{display:flex;gap:12px;align-items:flex-start;font-weight:500}
.ticks li svg{width:22px;height:22px;flex:0 0 22px;color:#06130a;background:var(--green);border-radius:50%;padding:4px;margin-top:2px}
.svc-nav{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:44px}
.svc-nav a{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 18px;text-decoration:none;font-weight:700;display:flex;gap:10px;align-items:center;transition:border-color .2s}
.svc-nav a:hover{border-color:var(--green)}
.svc-nav a svg{width:20px;height:20px;color:var(--greenD)}
.svc-nav a[aria-current]{background:var(--black);color:#fff;border-color:var(--black)}
.svc-nav a[aria-current] svg{color:var(--green)}
.svc-row{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center;padding:52px 0;border-bottom:1px solid var(--line)}
.svc-row:nth-child(even) .svc-pic{order:2}
.svc-row img{width:100%;aspect-ratio:16/11;object-fit:cover;border-radius:var(--r)}
.svc-row h2{font-size:clamp(32px,3.8vw,50px);margin-bottom:12px}
.incl{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.incl div{background:#fff;border:1px solid var(--line);border-radius:14px;padding:22px}
.incl svg{width:26px;height:26px;color:var(--greenD);margin-bottom:10px}
.incl b{display:block;font-family:var(--hf);font-size:21px;text-transform:uppercase}
.incl p{color:var(--muted);font-size:15px}
/* contact */
.contact-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:52px;align-items:start}
form.q{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:36px;display:grid;gap:16px;box-shadow:0 30px 60px rgba(0,0,0,.06)}
form.q h2{font-size:34px}
form.q label{font-weight:600;font-size:14.5px;display:grid;gap:6px}
form.q input,form.q select,form.q textarea{font:inherit;padding:13px 14px;border:1px solid var(--line);border-radius:10px;background:var(--paper);color:var(--ink);width:100%}
form.q input:focus,form.q select:focus,form.q textarea:focus{border-color:var(--green2);outline:0;box-shadow:0 0 0 3px rgba(47,228,27,.25)}
form.q .two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
form.q button{font-family:var(--hf);text-transform:uppercase;letter-spacing:.07em;font-weight:800;background:var(--green);color:#06130a;border:0;padding:18px;border-radius:999px;cursor:pointer;font-size:20px;transition:transform .18s,background .18s}
form.q button:hover{background:#49ff35;transform:translateY(-2px)}
form.q .note{font-size:14px;color:var(--muted)}
.hide{position:absolute;left:-9999px}
.ccard{display:grid;gap:14px}
.ccard a.line,.ccard .line{display:flex;gap:16px;align-items:center;text-decoration:none;padding:20px;border:1px solid var(--line);border-radius:var(--r);background:#fff;transition:border-color .2s}
.ccard a.line:hover{border-color:var(--green)}
.ccard .ic{width:50px;height:50px;border-radius:14px;display:grid;place-items:center;background:var(--black);color:var(--green);flex:0 0 50px}
.ccard .ic svg{width:22px;height:22px}
.ccard b{display:block;font-size:17px}
.ccard small{color:var(--muted)}
/* article */
.article{max-width:780px;margin:0 auto}
.article h1{text-transform:none;letter-spacing:0;font-size:clamp(36px,5vw,58px);line-height:1.04}
.article .meta{color:var(--muted);margin:16px 0 30px;font-weight:600}
.article>img{border-radius:var(--r);aspect-ratio:16/9;object-fit:cover;width:100%;margin-bottom:36px}
.article h2{font-size:30px;margin:36px 0 10px;text-transform:none;letter-spacing:0}
.article p{font-size:18px}
.article .intro{font-size:21px;color:var(--muted)}
.article .box{background:var(--black);color:#fff;border-radius:var(--r);padding:32px;margin-top:48px;display:flex;justify-content:space-between;gap:20px;align-items:center;flex-wrap:wrap}
.article .box h3{font-size:28px;color:var(--green)}
/* footer */
footer.foot{background:#03080d;color:#b8c4ce;padding:72px 0 28px;font-size:15.5px}
.fgrid{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;gap:36px}
.foot .logo{height:84px;width:auto}
.foot h4{font-family:var(--hf);font-size:19px;margin-bottom:14px;color:var(--green);letter-spacing:.08em}
.foot ul{list-style:none;padding:0;display:grid;gap:9px}
.foot a{text-decoration:none}
.foot a:hover{color:#fff;text-decoration:underline}
.soc{display:flex;gap:10px;margin-top:18px}
.soc a{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;border:1px solid var(--lineD);color:#fff;transition:background .2s,color .2s}
.soc a:hover{background:var(--green);color:#06130a}
.soc svg{width:19px;height:19px}
.legal{border-top:1px solid var(--lineD);margin-top:44px;padding-top:22px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:14px}
.legal .heart{color:#ff5a6e}
.mbar{display:none}
@media (max-width:960px){
 .menu{display:none;position:absolute;left:0;right:0;top:84px;background:var(--black);flex-direction:column;align-items:stretch;padding:12px 24px 22px;gap:2px;border-bottom:1px solid var(--lineD)}
 .menu.open{display:flex}
 .menu a{padding:13px 12px}
 .menu .btn{margin:10px 0 0;justify-content:center}
 .burger{display:block}
 .hero .wrap{grid-template-columns:1fr;padding-top:64px;padding-bottom:60px;min-height:0}
 .hero:before{background:linear-gradient(180deg,rgba(6,13,20,.9),rgba(6,13,20,.85))}
 .trustbar .wrap{grid-template-columns:1fr 1fr}
 .trustbar div{border-left:0;padding:18px 0;border-top:1px solid var(--lineD)}
 .bento{grid-template-columns:1fr}
 .bento .big{grid-row:auto;min-height:360px}
 .why,.svc-hero,.svc-row,.contact-grid,.faq-grid,.proof,.feat.three{grid-template-columns:1fr;gap:34px}
 .tl{grid-template-columns:1fr}
 .tl:before{display:none}
 .svc-row:nth-child(even) .svc-pic{order:0}
 .svc-nav,.incl,.posts{grid-template-columns:1fr 1fr}
 .fgrid{grid-template-columns:1fr 1fr}
 .gal{grid-template-columns:1fr 1fr}
 .gal a:first-child{grid-column:span 2;grid-row:auto;aspect-ratio:16/9}
 .why .float{left:12px}
}
@media (max-width:640px){
 body{font-size:16.5px}
 section{padding:68px 0}
 .topbar .hide-m{display:none}
 .brand .logo{height:44px}
 .fgrid,.svc-nav,.incl,.posts,.posts.two,.feat{grid-template-columns:1fr}
 .hero h1{font-size:clamp(46px,13vw,64px)}
 .qq{padding:20px}
 .qq .two{grid-template-columns:1fr}
 form.q .two{grid-template-columns:1fr}
 form.q{padding:24px 18px}
 .bento .sm .pic{width:96px;height:96px;flex-basis:96px}
 .bento .sm .go{display:none}
 .mbar{display:grid;grid-template-columns:1fr 1fr;position:fixed;left:0;right:0;bottom:0;z-index:30;box-shadow:0 -6px 20px rgba(0,0,0,.25)}
 .mbar a{padding:16px;text-align:center;font-weight:800;text-decoration:none;font-family:var(--hf);text-transform:uppercase;letter-spacing:.06em;font-size:18px}
 .mbar a:first-child{background:var(--black);color:#fff}
 .mbar a:last-child{background:var(--green);color:#06130a}
 footer.foot{padding-bottom:90px}
}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important;animation:none!important}.js .rv{opacity:1;transform:none}}
"""

JS = """<script>(function(){if(!('IntersectionObserver' in window))return;var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');o.unobserve(e.target)}})},{rootMargin:'0px 0px -8%'});document.querySelectorAll('.rv').forEach(function(el){o.observe(el)})})();</script>"""

NAV = [("index.html","Home"),("services.html","Services"),("about.html","About"),("gallery.html","Gallery"),("areas.html","Areas"),("blog.html","Blog"),("contact.html","Contact")]
FAVICON = "data:image/svg+xml," + urllib.parse.quote('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#060d14"/><text x="16" y="24" text-anchor="middle" font-family="Impact,sans-serif" font-size="21" font-weight="800" fill="#2fe41b">MS</text></svg>')

# ---------------------------------------------------------------- SEO helpers
def org_schema():
    return {"@type":"MovingCompany","@id":BIZ["site"]+"#business","name":BIZ["name"],"telephone":BIZ["phoneIntl"],"email":BIZ["email"],
            "url":BIZ["site"],"logo":BIZ["site"]+"img/logo-t.png","image":BIZ["site"]+"img/truck.jpg","sameAs":[BIZ["fb"]],
            "address":{"@type":"PostalAddress","addressLocality":BIZ["town"],"addressRegion":BIZ["state"],"postalCode":BIZ["postcode"],"addressCountry":"AU"},
            "areaServed":[{"@type":"City","name":t} for t in TOWNS],"priceRange":"$$",
            "founder":{"@type":"Person","name":BIZ["owner"]}}

def breadcrumbs(items):
    return {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":BIZ["site"]+h} for i,(n,h) in enumerate(items)]}

def shell(title, desc, cur, body, og="img/truck.jpg", extra_schema=None, crumbs=None, preload=None, page=None):
    page = page or cur or "index.html"
    canonical = BIZ["site"] + ("" if page == "index.html" else page)
    li = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{n}</a></li>' for h,n in NAV)
    abn = f'<li>ABN {E(BIZ["abn"])}</li>' if BIZ["abn"] else ""
    graph = [org_schema()]
    if crumbs: graph.append(breadcrumbs([("Home","index.html")] + crumbs))
    if extra_schema: graph += extra_schema if isinstance(extra_schema, list) else [extra_schema]
    ld = json.dumps({"@context":"https://schema.org","@graph":graph})
    robots = "index, follow" if INDEXABLE else "noindex, nofollow"
    pre = f'<link rel="preload" as="image" href="{preload}">' if preload else ""
    return f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{E(BIZ['name'])}"><meta property="og:locale" content="en_AU">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{BIZ['site']}{og}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{BIZ['site']}{og}">
<meta name="geo.region" content="AU-NSW"><meta name="geo.placename" content="Lismore"><meta name="theme-color" content="#060d14">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Barlow:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">{pre}
<script>document.documentElement.classList.add('js')</script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<div class="topbar"><div class="wrap"><span class="hide-m"><b>Local &amp; interstate moves</b> · Pickups &amp; deliveries · Domestic &amp; green waste · Lismore NSW</span><span><a href="tel:{BIZ['phoneIntl']}">Call Will on {BIZ['phone']}</a></span></div></div>
<header class="site"><div class="wrap nav">
 <a class="brand" href="index.html" aria-label="{E(BIZ['name'])} home">{LOGO}</a>
 <button class="burger" aria-label="Open menu" aria-expanded="false" onclick="var m=document.getElementById('menu');m.classList.toggle('open');this.setAttribute('aria-expanded',m.classList.contains('open'))">{ICO['menu']}</button>
 <nav aria-label="Main"><ul class="menu" id="menu">{li}<li><a class="btn btn-green" href="contact.html">Get a quote</a></li></ul></nav>
</div></header>
<main>{body}</main>
<footer class="foot"><div class="wrap">
 <div class="fgrid">
  <div>{LOGO}<p style="margin-top:18px;max-width:38ch">Truck removals for homes and businesses across Lismore and the Northern Rivers. Local and interstate moves, pickups and deliveries, domestic and green waste removal.</p>
   <div class="soc"><a href="{BIZ['fb']}" aria-label="Facebook" rel="noopener">{ICO['fb']}</a><a href="mailto:{BIZ['email']}" aria-label="Email">{ICO['mail']}</a><a href="tel:{BIZ['phoneIntl']}" aria-label="Phone">{ICO['phone']}</a></div></div>
  <div><h4>Services</h4><ul>{"".join(f'<li><a href="{s["id"]}.html">{E(s["title"])}</a></li>' for s in SERVICES)}<li><a href="areas.html">Service areas</a></li></ul></div>
  <div><h4>Company</h4><ul><li><a href="about.html">About Will &amp; the crew</a></li><li><a href="gallery.html">Gallery</a></li><li><a href="blog.html">Moving tips</a></li><li><a href="faq.html">FAQ</a></li><li><a href="contact.html">Contact</a></li></ul></div>
  <div><h4>Contact</h4><ul><li><a href="tel:{BIZ['phoneIntl']}">{BIZ['phone']}</a></li><li><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></li><li>Lismore NSW 2480</li>{abn}<li><a href="{BIZ['fb']}" rel="noopener">Facebook</a></li></ul></div>
 </div>
 <div class="legal"><span>© 2026 {E(BIZ['name'])}. All rights reserved.</span><span>Developed with <span class="heart" aria-label="love">❤</span> by <a href="https://gemprogrammers.com" rel="noopener"><b>Mr. Developer</b></a></span></div>
</div></footer>
<div class="mbar"><a href="tel:{BIZ['phoneIntl']}">Call now</a><a href="contact.html">Get a quote</a></div>
{JS}
</body></html>"""

def pagehead(title, sub, crumb, img="img/fleet.jpg"):
    return f'<div class="ph">{IM(img, "", lazy=False)}<div class="wrap"><div class="crumbs"><a href="index.html">Home</a> / {E(crumb)}</div><h1>{title}</h1><p>{E(sub)}</p></div></div>'

def ctab():
    return f'<div class="ctab"><div class="wrap"><div><h2>Got a move coming up?</h2><p>Call or text Will for a straight quote.</p></div><div><a class="big" href="tel:{BIZ["phoneIntl"]}">{BIZ["phone"]}</a><p><a href="contact.html" style="font-weight:800">or send a quote request →</a></p></div></div></div>'

def faq_html(items):
    return '<div class="faq">' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q,a in items) + "</div>"

def faq_schema(items):
    return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]}

GENERAL_FAQ = [
 ["Do you still do man-and-ute moves?","No. Mister Shifter runs pantech trucks with a crew for moves of all sizes, plus pickups, deliveries and waste runs."],
 ["What areas do you cover?","Lismore and the Northern Rivers for local work, and interstate moves out of the region. See the service areas page or call to check your suburb."],
 ["How do I get a quote?","Call or text Will on "+BIZ["phone"]+", message the Facebook page, or send the form on the contact page. Tell us where from, where to, how big and when."],
 ["Do I need to be there on the day?","Someone needs to let the crew in, point out what's going and lock up after. It doesn't have to be you, but it helps."],
 ["Can you move a single item?","Yes. Pickups and deliveries of furniture, whitegoods and marketplace buys are a big part of what we do."],
 ["Do you take rubbish as well?","Yes. Domestic and green waste removal, on its own or combined with a move."],
]

PHOTOS = [("img/fleet.jpg","Mister Shifter Removals truck and ute parked under palms near Lismore","The fleet"),("img/truck.jpg","Mister Shifter Removals Fuso pantech truck with green signage","Pantech truck"),("img/team.jpg","Will and the Mister Shifter crew standing in front of the truck","Will and the crew"),("img/house.jpg","Mister Shifter truck backed into a driveway on moving day","Moving day"),("img/heart.jpg","Mister Shifter truck driving through town","Out and about"),("img/family.jpg","The Mister Shifter family in front of the truck at Christmas","Family business")]

def gallery_html(n=6):
    return "".join(f'<a href="{p}" target="_blank" rel="noopener">{IM(p,a)}<span>{E(c)}</span></a>' for p,a,c in PHOTOS[:n])

def form_hidden(subject):
    return f"""<input type="hidden" name="_subject" value="{E(subject)}">
 <input type="hidden" name="_template" value="table">
 <input type="hidden" name="_captcha" value="false">
 <input type="hidden" name="_next" value="{BIZ['site']}thanks.html">
 <input type="hidden" name="_autoresponse" value="Thanks for contacting Mister Shifter Removals. We've got your request and the team will be in touch soon. Need us faster? Call or text Will on {BIZ['phone']}.">
 <input type="text" name="_honey" class="hide" tabindex="-1" autocomplete="off">"""

def post_cards(posts, cls=""):
    return f'<div class="posts {cls}">' + "".join(f'<a class="post rv" href="{p["slug"]}.html"><div class="pic"><img src="{p["img"]}" alt="" loading="lazy" decoding="async" width="1200" height="750"></div><div class="in"><small>{E(p["date"])}</small><h3>{E(p["title"])}</h3><p>{E(p["intro"])}</p></div></a>' for p in posts) + '</div>'

def page_index():
    strip = "".join(f"<span>{E(x)}</span><span aria-hidden='true'>✦</span>" for x in ["Local moves","Interstate moves","Pickups & deliveries","Domestic & green waste removal","Lismore & Northern Rivers","Call "+BIZ["phone"]])
    opts = "".join(f"<option>{E(s['title'])}</option>" for s in SERVICES) + "<option>Not sure yet</option>"
    first, rest = SERVICES[0], SERVICES[1:]
    def anyimg(src, alt):
        return IM(src, alt) if src.startswith("img/") else f'<img src="{src}" alt="{E(alt)}" loading="lazy" decoding="async">'
    bento = f'<a class="big rv" href="{first["id"]}.html">{IM(first["img"], first["title"])}<div class="in"><span class="ic">{ICO[first["icon"]]}</span><h3>{E(first["title"])}</h3><p>{E(first["short"])}</p></div></a>' + "".join(
        f'<a class="sm rv d{n+1}" href="{s["id"]}.html"><div class="pic">{anyimg(s["img"], s["title"])}</div><div><h3>{E(s["title"])}</h3><p>{E(s["short"])}</p></div><span class="go">{ICO["arrow"]}</span></a>' for n,s in enumerate(rest))
    body = f"""
<div class="hero">{IM("img/fleet.jpg","Mister Shifter Removals truck and ute in Lismore","bg",lazy=False)}<div class="wrap">
 <div><div class="eyebrow">Lismore · Northern Rivers · Interstate</div><h1>Trucks, crew, <em>done.</em></h1>
 <p class="lede">Mister Shifter Removals moves homes and businesses across Lismore and the Northern Rivers, and interstate when you're going further. Pickups, deliveries and waste runs too.</p>
 <div class="cta"><a class="btn btn-green" href="contact.html">Get a quote {ICO['arrow']}</a><a class="btn btn-ghostW" href="tel:{BIZ['phoneIntl']}">{ICO['phone']}{BIZ['phone']}</a></div>
 <div class="chips"><span>{ICO['truck']}Pantech trucks</span><span>{ICO['map']}Local &amp; interstate</span><span>{ICO['box']}Single items welcome</span><span>{ICO['leaf']}Waste removal</span></div></div>
 <form class="qq rv" action="https://formsubmit.co/{BIZ['email']}" method="POST">{form_hidden("Quick quote from the Mister Shifter website")}
  <h3>Quick <em>quote</em></h3><p>Takes 30 seconds. Will calls you back.</p>
  <div class="two"><label>Name<input name="Name" required autocomplete="name" placeholder="Your name"></label><label>Phone<input name="Phone" type="tel" required autocomplete="tel" placeholder="04…"></label></div>
  <label>Email<input name="Email" type="email" required autocomplete="email" placeholder="you@email.com"></label>
  <div class="two"><label>From<input name="Moving from" placeholder="Suburb"></label><label>To<input name="Moving to" placeholder="Suburb"></label></div>
  <label>What do you need?<select name="Service">{opts}</select></label>
  <button type="submit">Get my quote</button><small>No spam. Just a call back from Will.</small></form>
</div></div>
<div class="trustbar"><div class="wrap">
 <div>{ICO['truck']}<span><b>Pantech trucks</b><small>Not a ute. The whole house goes in one load.</small></span></div>
 <div>{ICO['map']}<span><b>Local &amp; interstate</b><small>Northern Rivers to anywhere you're headed.</small></span></div>
 <div>{ICO['chat']}<span><b>Deal with Will</b><small>Owner-operated. One person, start to finish.</small></span></div>
 <div>{ICO['shield']}<span><b>Wrapped &amp; strapped</b><small>Blankets, straps and trolleys on every job.</small></span></div>
</div></div>
<section><div class="wrap"><div class="head row"><div><div class="eyebrow">Services</div><h2>One truck. Every kind of job.</h2></div><p>From a full house move to a single lounge off Marketplace, the truck and crew turn up and get it done.</p></div><div class="bento">{bento}</div></div></section>
<div class="strip" aria-hidden="true"><div>{strip}{strip}</div></div>
<section class="dark"><div class="wrap why"><div class="pic rv">{IM("img/team.jpg","Will and the Mister Shifter crew in front of the truck")}<div class="float"><b>Will &amp; crew</b><small>Lismore, NSW</small></div></div>
 <div class="rv"><div class="eyebrow">Why Mister Shifter</div><h2 style="font-size:clamp(36px,4.8vw,62px)">Local blokes. Proper trucks. No mucking around.</h2><p style="color:var(--mutedD);margin-top:14px">Mister Shifter started small in Lismore and has grown into a truck-based removalist for the whole Northern Rivers. The approach hasn't changed: turn up on time, look after people's stuff, and be straight about the price.</p>
 <div class="feat"><div>{ICO['truck']}<b>Pantech trucks</b><p>Enclosed, dry and big enough for a full home.</p></div><div>{ICO['clock']}<b>On time</b><p>You get a window, and the truck turns up in it.</p></div><div>{ICO['shield']}<b>Careful loading</b><p>Furniture wrapped, boxes stacked, everything strapped.</p></div><div>{ICO['chat']}<b>Straight quotes</b><p>A price before we start. No surprises after.</p></div></div>
 <p style="margin-top:28px"><a class="btn btn-green" href="about.html">About Will &amp; the crew {ICO['arrow']}</a></p></div></div></section>
<section><div class="wrap"><div class="head c"><div class="eyebrow">How it works</div><h2>Three steps to moved.</h2></div><div class="tl">
 <div class="rv"><h3>Call or message Will</h3><p>Where from, where to, how big, and when. Phone, text, Facebook or the quote form. You'll get a straight price.</p></div>
 <div class="rv d1"><h3>We turn up with the truck</h3><p>Pantech truck, blankets, straps and trolleys, plus a crew that does this for a living.</p></div>
 <div class="rv d2"><h3>Loaded, driven, unloaded</h3><p>Everything wrapped, stacked and strapped, then unloaded into the right rooms at the other end.</p></div></div></div></section>
<section class="tone"><div class="wrap"><div class="head row"><div><div class="eyebrow">Gallery</div><h2>On the job.</h2></div><a class="btn btn-ghost" href="gallery.html">See all photos</a></div><div class="gal">{gallery_html(6)}</div></div></section>
<section><div class="wrap"><div class="head"><div class="eyebrow">Reviews</div><h2>Don't take our word for it.</h2><p>Read what customers have said about Mister Shifter on Google and Facebook.</p></div>
 <div class="proof"><a href="https://www.google.com/search?q=Mister+Shifter+Removals+Lismore+reviews" rel="noopener"><span class="ic"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6.9 7.1.6-5.4 4.7 1.7 7.3L12 17.8 5.7 21.5l1.7-7.3L2 9.5l7.1-.6z"/></svg></span><span><b>Google reviews</b><small>Search "Mister Shifter Removals Lismore" to read them</small></span></a>
 <a href="{BIZ['fb']}" rel="noopener"><span class="ic">{ICO['fb']}</span><span><b>Facebook page</b><small>Photos, updates and recommendations</small></span></a></div></div></section>
<section class="dark"><div class="wrap"><div class="head"><div class="eyebrow">Service areas</div><h2>Lismore &amp; the Northern Rivers.</h2><p>Local moves, pickups and waste runs across the region. Interstate from here to wherever you're headed.</p></div>
 <div class="areas">{"".join(f"<span>{E(t)}</span>" for t in TOWNS)}<span>+ surrounding areas</span></div>
 <p style="margin-top:28px"><a class="btn btn-green" href="areas.html">Service areas {ICO['arrow']}</a></p></div></section>
<section><div class="wrap"><div class="head row"><div><div class="eyebrow">Moving tips</div><h2>From the blog.</h2></div><a class="btn btn-ghost" href="blog.html">All posts</a></div>{post_cards(POSTS[:3])}</div></section>
<section class="tone"><div class="wrap faq-grid"><div class="rv"><div class="eyebrow">FAQ</div><h2 style="font-size:clamp(34px,4.4vw,56px)">Common questions.</h2><p style="color:var(--muted);margin-top:12px">Something else? Call Will on {BIZ['phone']}.</p><p style="margin-top:22px"><a class="btn btn-dark" href="faq.html">All FAQs</a></p></div><div class="rv">{faq_html(GENERAL_FAQ[:4])}</div></div></section>
{ctab()}"""
    return shell(f"Removalists Lismore & Northern Rivers | {BIZ['name']}", "Mister Shifter Removals: truck removals for homes and businesses across Lismore and the Northern Rivers. Local and interstate moves, pickups and deliveries, domestic and green waste removal. Call Will on 0475 074 906.", "index.html", body, "img/fleet.jpg", extra_schema=faq_schema(GENERAL_FAQ[:4]), preload="img/fleet.jpg")

def page_services():
    rows = ""
    for s in SERVICES:
        pts = "".join(f"<li>{ICO['check']}{E(p)}</li>" for p in s["points"])
        pic = IM(s["img"], s["title"]) if s["img"].startswith("img/") else f'<img src="{s["img"]}" alt="{E(s["title"])}" loading="lazy" decoding="async">'
        rows += f'<div class="svc-row" id="{s["id"]}"><div class="svc-pic rv">{pic}</div><div class="rv"><div class="eyebrow">{E(s["tag"])}</div><h2>{E(s["title"])}</h2><p>{E(s["lede"])}</p><ul class="ticks">{pts}</ul><p style="margin-top:24px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-dark" href="{s["id"]}.html">Details {ICO["arrow"]}</a><a class="btn btn-green" href="contact.html">Get a quote</a></p></div></div>'
    body = pagehead("Removal services", "Local and interstate moves, pickups and deliveries, and waste removal, all by truck out of Lismore.", "Services", "img/truck.jpg") + f'<section style="padding-top:30px"><div class="wrap">{rows}</div></section>' + ctab()
    sch = {"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":BIZ["site"]+s["id"]+".html","name":s["title"]} for i,s in enumerate(SERVICES)]}
    return shell(f"Removal services in Lismore | {BIZ['name']}", "Local moves, interstate moves, pickups and deliveries, and domestic and green waste removal across Lismore and the Northern Rivers.", "services.html", body, extra_schema=sch, crumbs=[("Services","services.html")])

INCL = {"local-moves":[("truck","Pantech truck","Enclosed truck sized for the job."),("shield","Blankets & straps","Furniture wrapped and secured."),("box","Trolleys","Heavy items moved safely."),("chat","Will on the phone","One contact, start to finish.")],
        "interstate-moves":[("map","Door to door","Loaded once, unloaded at your new place."),("shield","Highway-ready load","Packed and strapped for the long haul."),("clock","Agreed dates","Pickup and delivery days confirmed."),("chat","One quote","The whole job priced up front.")],
        "pickups-deliveries":[("box","Any big item","Furniture, whitegoods, marketplace buys."),("truck","Truck with gear","Trolleys and blankets on board."),("map","Store pickups","We collect, you stay home."),("chat","Priced per job","Tell us pickup, drop-off and item.")],
        "waste-removal":[("leaf","Green waste","Branches, fronds, clippings."),("box","Household junk","Old furniture and clean-out piles."),("truck","We load it","You point, we lift."),("clock","Same day as a move","Combine it and save a callout.")]}

def page_service(s):
    others = "".join(f'<a href="{o["id"]}.html"{" aria-current=\"page\"" if o is s else ""}>{ICO[o["icon"]]}{E(o["title"])}</a>' for o in SERVICES)
    pts = "".join(f"<li>{ICO['check']}{E(p)}</li>" for p in s["points"])
    paras = "".join(f"<p>{E(p)}</p>" for p in s["body"])
    pic = IM(s["img"], s["title"]) if s["img"].startswith("img/") else f'<img src="{s["img"]}" alt="{E(s["title"])}" loading="lazy" decoding="async">'
    incl = "".join(f'<div class="rv d{n%4}">{ICO[i]}<b>{E(t)}</b><p>{E(d)}</p></div>' for n,(i,t,d) in enumerate(INCL[s["id"]]))
    related = [p for p in POSTS if (s["id"]=="waste-removal" and "green" in p["slug"]) or (s["id"]=="interstate-moves" and "interstate" in p["slug"]) or (s["id"] in ("local-moves","pickups-deliveries") and p["slug"] in ("blog-moving-day-checklist","blog-packing-tips"))][:2]
    body = pagehead(E(s["title"]), s["lede"], s["title"], s["img"] if s["img"].startswith("img/") else "img/truck.jpg") + f"""
<section><div class="wrap"><div class="svc-hero"><div class="rv"><div class="eyebrow">{E(s["tag"])}</div><h2>{E(s["title"])} with Mister Shifter</h2>{paras}<ul class="ticks">{pts}</ul>
 <p style="margin-top:26px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-green" href="contact.html">Get a quote {ICO['arrow']}</a><a class="btn btn-ghost" href="tel:{BIZ['phoneIntl']}">{ICO['phone']}{BIZ['phone']}</a></p></div><div class="rv">{pic}</div></div>
 <div class="svc-nav">{others}</div></div></section>
<section class="tone"><div class="wrap"><div class="head"><div class="eyebrow">What's included</div><h2>What you get.</h2></div><div class="incl">{incl}</div></div></section>
<section><div class="wrap faq-grid"><div><div class="eyebrow">FAQ</div><h2 style="font-size:clamp(30px,4vw,48px)">{E(s["title"])} questions.</h2></div>{faq_html(s["faq"] + GENERAL_FAQ[2:4])}</div></section>
{('<section class="tone"><div class="wrap"><div class="head row"><div><div class="eyebrow">Tips</div><h2>Worth a read.</h2></div></div>' + post_cards(related, "two") + '</div></section>') if related else ''}
{ctab()}"""
    sch = [{"@type":"Service","name":s["title"],"serviceType":s["title"],"provider":{"@id":BIZ["site"]+"#business"},"areaServed":"Lismore and the Northern Rivers, NSW","description":s["short"],"url":BIZ["site"]+s["id"]+".html"}, faq_schema(s["faq"])]
    return shell(f"{s['title']} Lismore & Northern Rivers | {BIZ['name']}", s["short"], "services.html", body, extra_schema=sch, crumbs=[("Services","services.html"),(s["title"],s["id"]+".html")], page=s["id"]+".html")

def page_about():
    body = pagehead("About Will &amp; the crew", "A Lismore removalist that grew from one bloke and a ute into trucks and a crew.", "About", "img/team.jpg") + f"""
<section><div class="wrap why"><div class="pic rv">{IM("img/team.jpg","Will and the crew")}<div class="float"><b>Est. Lismore</b><small>Owner-operated</small></div></div>
 <div class="rv"><div class="eyebrow">Our story</div><h2 style="font-size:clamp(36px,4.8vw,62px)">Built in Lismore, one move at a time.</h2>
 <p style="margin-top:14px">Mister Shifter Removals is run by Will out of Lismore. The business started small and has grown with the Northern Rivers: these days it runs pantech trucks and a crew, handling full house and business moves, interstate runs, pickups and deliveries, and domestic and green waste removal.</p>
 <p style="margin-top:12px">What hasn't changed is how the job is done. Will quotes it straight, the crew turns up when they said they would, and your stuff gets wrapped, strapped and treated like it's their own.</p>
 <ul class="ticks"><li>{ICO['check']}Owner-operated, you deal with Will directly</li><li>{ICO['check']}Pantech trucks with blankets, straps and trolleys</li><li>{ICO['check']}Local, regional and interstate</li><li>{ICO['check']}Follow the crew on <a href="{BIZ['fb']}" rel="noopener">Facebook</a></li></ul></div></div></section>
<section class="dark"><div class="wrap"><div class="head"><div class="eyebrow">How we work</div><h2>Simple rules.</h2></div><div class="feat three">
 <div class="rv">{ICO['chat']}<b>Straight quotes</b><p>You get a price before the truck moves. No surprises on the invoice.</p></div>
 <div class="rv d1">{ICO['shield']}<b>Look after the gear</b><p>Wrapped, stacked and strapped. Furniture and whitegoods get the blanket treatment.</p></div>
 <div class="rv d2">{ICO['clock']}<b>Turn up and get it done</b><p>On time, with the right truck and enough hands for the job.</p></div></div></div></section>
<section><div class="wrap"><div class="head row"><div><div class="eyebrow">Gallery</div><h2>The trucks and the team.</h2></div><a class="btn btn-ghost" href="gallery.html">All photos</a></div><div class="gal">{gallery_html(3)}</div></div></section>
{ctab()}"""
    return shell(f"About Will & the crew | {BIZ['name']} Lismore", "Mister Shifter Removals is a Lismore removalist run by Will, with pantech trucks and a crew working across the Northern Rivers and interstate.", "about.html", body, "img/team.jpg", crumbs=[("About","about.html")])

def page_gallery():
    body = pagehead("Gallery", "The trucks, the crew and a few jobs around the Northern Rivers.", "Gallery", "img/heart.jpg") + f'<section><div class="wrap"><div class="gal">{gallery_html(6)}</div><p style="margin-top:30px;color:var(--muted)">More photos on <a href="{BIZ["fb"]}" rel="noopener">Facebook</a>.</p></div></section>' + ctab()
    sch = {"@type":"ImageGallery","name":"Mister Shifter Removals gallery","image":[BIZ["site"]+p for p,_,_ in PHOTOS]}
    return shell(f"Gallery | {BIZ['name']}", "Photos of the Mister Shifter Removals trucks and crew around Lismore and the Northern Rivers.", "gallery.html", body, "img/heart.jpg", extra_schema=sch, crumbs=[("Gallery","gallery.html")])

def page_areas():
    chips = "".join(f"<span>{E(t)}</span>" for t in TOWNS)
    body = pagehead("Service areas", "Local work across Lismore and the Northern Rivers. Interstate moves from the region to wherever you're going.", "Service areas", "img/house.jpg") + f"""
<section class="light"><div class="wrap svc-hero"><div class="rv"><div class="eyebrow">Local &amp; regional</div><h2>Northern Rivers, covered.</h2><p>We're based in Lismore and work across the Northern Rivers: the city, the hinterland villages and the coast. If you're not sure whether we come to you, call and ask.</p><div class="areas" style="margin-top:24px">{chips}<span>+ surrounding areas</span></div></div>
 <div class="rv"><iframe class="map" title="Map of Lismore NSW" loading="lazy" src="https://maps.google.com/maps?q=Lismore+NSW+2480&z=10&output=embed"></iframe></div></div></section>
<section class="dark"><div class="wrap svc-hero"><img class="rv" src="{U('1716441592984-75d4c882e5cf',1100)}" alt="Highway through green hills" loading="lazy" decoding="async" width="1100" height="825"><div class="rv"><div class="eyebrow">Interstate</div><h2>Going further? We'll take it.</h2><p style="color:var(--mutedD)">Interstate moves out of the Northern Rivers. One truck, loaded once and delivered to your new door.</p><p style="margin-top:26px"><a class="btn btn-green" href="interstate-moves.html">Interstate moves {ICO['arrow']}</a></p></div></div></section>
{ctab()}"""
    return shell(f"Service areas: Lismore, Ballina, Byron Bay & Northern Rivers | {BIZ['name']}", "Mister Shifter Removals covers Lismore, Goonellabah, Ballina, Byron Bay, Casino and the rest of the Northern Rivers, plus interstate moves.", "areas.html", body, "img/house.jpg", crumbs=[("Service areas","areas.html")])

def page_faq():
    allq = GENERAL_FAQ + [q for s in SERVICES for q in s["faq"]]
    body = pagehead("FAQ", "Answers to the questions we get asked most. Anything else, call Will.", "FAQ") + f'<section><div class="wrap" style="max-width:880px">{faq_html(allq)}</div></section>' + ctab()
    return shell(f"FAQ | {BIZ['name']} Lismore", "Frequently asked questions about moving with Mister Shifter Removals in Lismore and the Northern Rivers.", "faq.html", body, extra_schema=faq_schema(allq), crumbs=[("FAQ","faq.html")])

def page_blog():
    body = pagehead("Moving tips", "Practical advice from people who move houses for a living.", "Blog", "img/truck.jpg") + f'<section><div class="wrap">{post_cards(POSTS, "two")}</div></section>' + ctab()
    sch = {"@type":"Blog","name":"Mister Shifter Removals blog","blogPost":[{"@type":"BlogPosting","headline":p["title"],"url":BIZ["site"]+p["slug"]+".html"} for p in POSTS]}
    return shell(f"Moving tips & advice | {BIZ['name']} blog", "Moving tips, checklists and advice from Mister Shifter Removals, Lismore.", "blog.html", body, extra_schema=sch, crumbs=[("Blog","blog.html")])

def page_post(p):
    secs = "".join(f"<h2>{E(h)}</h2><p>{E(t)}</p>" for h,t in p["sections"])
    others = [o for o in POSTS if o is not p][:2]
    body = f"""<article class="article" style="padding-top:60px"><div class="wrap"><div class="crumbs" style="color:var(--muted)"><a href="index.html">Home</a> / <a href="blog.html">Blog</a></div><h1>{E(p["title"])}</h1><div class="meta">{E(p["date"])} · Mister Shifter Removals</div><img src="{p["img"]}" alt="" width="1200" height="675" fetchpriority="high"><p class="intro">{E(p["intro"])}</p>{secs}
 <div class="box"><div><h3>Need a truck for it?</h3><p>Call Will on {BIZ['phone']} or send a quote request.</p></div><a class="btn btn-green" href="contact.html">Get a quote</a></div></div></article>
<section class="tone"><div class="wrap"><div class="head row"><div><div class="eyebrow">More tips</div><h2>Keep reading.</h2></div></div>{post_cards(others, "two")}</div></section>"""
    sch = {"@type":"BlogPosting","headline":p["title"],"description":p["intro"],"image":p["img"],"datePublished":"2026-10-22","author":{"@type":"Organization","name":BIZ["name"]},"publisher":{"@id":BIZ["site"]+"#business"},"mainEntityOfPage":BIZ["site"]+p["slug"]+".html"}
    return shell(f"{p['title']} | {BIZ['name']}", p["intro"], "blog.html", body, extra_schema=sch, crumbs=[("Blog","blog.html"),(p["title"],p["slug"]+".html")], page=p["slug"]+".html")

def page_contact():
    opts = "".join(f"<option>{E(s['title'])}</option>" for s in SERVICES) + "<option>Not sure yet</option>"
    body = pagehead("Get a quote", "Tell us where from, where to, how big and when. Will will come back to you with a price.", "Contact", "img/fleet.jpg") + f"""
<section><div class="wrap contact-grid">
<form class="q" action="https://formsubmit.co/{BIZ['email']}" method="POST">{form_hidden("New quote request from the Mister Shifter website")}
 <h2>Quote request</h2>
 <div class="two"><label>Your name<input name="Name" required autocomplete="name"></label><label>Phone<input name="Phone" type="tel" required autocomplete="tel"></label></div>
 <label>Email<input name="Email" type="email" required autocomplete="email"></label>
 <label>What do you need?<select name="Service">{opts}</select></label>
 <div class="two"><label>Moving from<input name="Moving from" placeholder="Suburb or address"></label><label>Moving to<input name="Moving to" placeholder="Suburb or address"></label></div>
 <div class="two"><label>Preferred date<input name="Date" type="date"></label><label>Size of the job<select name="Size"><option>1 bedroom / small</option><option>2–3 bedrooms</option><option>4+ bedrooms</option><option>Single item</option><option>Trailer load of waste</option><option>Half a truck of waste</option><option>Full truck of waste</option><option>Not sure</option></select></label></div>
 <label>Anything we should know?<textarea name="Message" rows="4" placeholder="Stairs, heavy items, access, dates that won't work…"></textarea></label>
 <button type="submit">Send quote request</button>
 <p class="note">Goes straight to Will's inbox. You'll get an email confirmation and the team will contact you soon.</p>
</form>
<div class="ccard">
 <a class="line" href="tel:{BIZ['phoneIntl']}"><span class="ic">{ICO['phone']}</span><span><b>{BIZ['phone']}</b><small>Call or text Will</small></span></a>
 <a class="line" href="mailto:{BIZ['email']}"><span class="ic">{ICO['mail']}</span><span><b>{BIZ['email']}</b><small>Email us the details</small></span></a>
 <a class="line" href="{BIZ['fb']}" rel="noopener"><span class="ic">{ICO['fb']}</span><span><b>Facebook</b><small>Message the page</small></span></a>
 <div class="line"><span class="ic">{ICO['pin']}</span><span><b>Lismore NSW 2480</b><small>Servicing the Northern Rivers and interstate</small></span></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><iframe class="map" title="Map of Lismore NSW" loading="lazy" src="https://maps.google.com/maps?q=Lismore+NSW+2480&z=11&output=embed"></iframe></div></section>"""
    sch = {"@type":"ContactPage","name":"Contact Mister Shifter Removals","url":BIZ["site"]+"contact.html"}
    return shell(f"Get a removal quote in Lismore | {BIZ['name']}", f"Contact Mister Shifter Removals, Lismore. Call {BIZ['phone']} or send a quote request online for local, interstate, pickup or waste removal jobs.", "contact.html", body, extra_schema=sch, crumbs=[("Contact","contact.html")])

def page_thanks():
    body = pagehead("Thanks, we've got it", "Your request is in Will's inbox and the team will contact you soon. Check your email for a confirmation.", "Thank you") + f'<section><div class="wrap"><p style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-dark" href="index.html">Back to home</a><a class="btn btn-green" href="tel:{BIZ["phoneIntl"]}">{ICO["phone"]}Need it sooner? Call {BIZ["phone"]}</a></p></div></section>'
    return shell(f"Thank you | {BIZ['name']}", "Request received.", "", body, page="thanks.html")

def sitemap(pages):
    urls = "".join(f"<url><loc>{BIZ['site']}{'' if p=='index.html' else p}</loc><changefreq>monthly</changefreq><priority>{'1.0' if p=='index.html' else '0.7'}</priority></url>" for p in pages)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n'

def build():
    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("*.html"): f.unlink()
    (OUT/"style.css").write_text(CSS)
    pages = {"index.html":page_index(),"services.html":page_services(),"about.html":page_about(),"gallery.html":page_gallery(),"areas.html":page_areas(),"faq.html":page_faq(),"blog.html":page_blog(),"contact.html":page_contact()}
    for s in SERVICES: pages[f"{s['id']}.html"] = page_service(s)
    for p in POSTS: pages[f"{p['slug']}.html"] = page_post(p)
    for n,h in pages.items(): (OUT/n).write_text(h)
    (OUT/"thanks.html").write_text(page_thanks())
    (OUT/"sitemap.xml").write_text(sitemap(list(pages)))
    (OUT/"robots.txt").write_text(("User-agent: *\nAllow: /\n" if INDEXABLE else "User-agent: *\nDisallow: /\n") + f"Sitemap: {BIZ['site']}sitemap.xml\n")
    print("built", OUT.name, len(pages)+1, "pages")

if __name__ == "__main__":
    build()
