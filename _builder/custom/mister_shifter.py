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

LOGO_SVG = '''<svg viewBox="0 0 300 64" width="190" height="40" aria-label="Mister Shifter Removals" role="img"><rect width="300" height="64" rx="6" fill="#0a0a0a"/><path d="M12 48c4-16 14-30 32-30 10 0 16 6 18 14-6-4-12-6-18-4-8 3-12 10-14 20z" fill="none" stroke="#35E51B" stroke-width="3" stroke-linejoin="round"/><text x="74" y="27" font-family="Barlow Condensed,Impact,sans-serif" font-weight="800" font-size="24" fill="#35E51B" letter-spacing="1">MISTER SHIFTER</text><text x="74" y="52" font-family="Barlow Condensed,Impact,sans-serif" font-weight="800" font-size="22" fill="#ffffff" letter-spacing="3">REMOVALS</text></svg>'''
FAVICON = "data:image/svg+xml," + urllib.parse.quote('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#0a0a0a"/><text x="16" y="24" text-anchor="middle" font-family="Impact,sans-serif" font-size="22" font-weight="800" fill="#35E51B">MS</text></svg>')

# ---------------------------------------------------------------- CSS
CSS = r"""
:root{--black:#0a0a0a;--ink:#111;--panel:#151515;--panel2:#1d1d1d;--green:#35E51B;--green2:#27b914;--white:#fff;--paper:#f4f5f1;--paper2:#e9ebe4;--muted:#5d6257;--mutedD:#a9ada3;--line:#dcdfd6;--lineD:rgba(255,255,255,.12);--r:14px;--hf:"Barlow Condensed",Impact,sans-serif;--bf:Barlow,system-ui,sans-serif}
*{box-sizing:border-box;margin:0}
html{scroll-behavior:smooth}
body{font-family:var(--bf);color:var(--ink);background:var(--paper);line-height:1.6;font-size:17px;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{max-width:100%;display:block}
a{color:inherit}
:focus-visible{outline:3px solid var(--green);outline-offset:3px}
h1,h2,h3,h4,.hf{font-family:var(--hf);font-weight:800;line-height:1;letter-spacing:.01em;text-transform:uppercase}
.wrap{max-width:1200px;margin:0 auto;padding:0 22px}
.eyebrow{display:inline-flex;align-items:center;gap:10px;font-size:13px;letter-spacing:.18em;text-transform:uppercase;font-weight:700;color:var(--green2);margin-bottom:14px}
.eyebrow:before{content:"";width:28px;height:3px;background:currentColor}
.dark .eyebrow,.hero .eyebrow{color:var(--green)}
.btn{display:inline-flex;align-items:center;gap:10px;padding:15px 26px;border-radius:8px;font-weight:700;text-decoration:none;border:2px solid transparent;font-size:16px;transition:transform .18s,background .18s,box-shadow .18s;line-height:1.1;font-family:var(--hf);text-transform:uppercase;letter-spacing:.06em;font-size:18px}
.btn:hover{transform:translateY(-2px)}
.btn svg{width:20px;height:20px;flex:0 0 20px}
.btn-green{background:var(--green);color:#0a0a0a;box-shadow:0 10px 30px rgba(53,229,27,.25)}
.btn-green:hover{background:#4dff33}
.btn-dark{background:var(--black);color:#fff}
.btn-ghost{border-color:currentColor}
.btn-ghostW{border-color:rgba(255,255,255,.5);color:#fff}
.btn-ghostW:hover{border-color:#fff}
/* reveal */
.js .rv{opacity:0;transform:translateY(22px);transition:opacity .7s ease,transform .7s ease}
.js .rv.in{opacity:1;transform:none}
/* header */
.topbar{background:var(--black);color:#cfd3c9;font-size:14px}
.topbar .wrap{display:flex;justify-content:space-between;gap:16px;padding:8px 22px;flex-wrap:wrap}
.topbar a{text-decoration:none;color:#fff;font-weight:600}
.topbar b{color:var(--green)}
header.site{position:sticky;top:0;z-index:30;background:rgba(10,10,10,.92);backdrop-filter:blur(10px);color:#fff;border-bottom:1px solid var(--lineD)}
.nav{display:flex;align-items:center;justify-content:space-between;height:78px;gap:18px}
.brand{display:flex;align-items:center;text-decoration:none}
.brand svg{height:40px;width:auto}
.menu{display:flex;gap:4px;align-items:center;list-style:none;padding:0}
.menu a{text-decoration:none;font-weight:600;font-size:15.5px;padding:9px 13px;border-radius:6px;color:#e8eae3}
.menu a:hover{background:rgba(255,255,255,.08)}
.menu a[aria-current]{color:var(--green)}
.menu .btn{padding:11px 18px;font-size:16px;margin-left:8px}
.burger{display:none;background:none;border:0;color:#fff;padding:8px;cursor:pointer}
.burger svg{width:28px;height:28px}
/* hero */
.hero{position:relative;color:#fff;min-height:min(92vh,820px);display:flex;align-items:flex-end;overflow:hidden;background:var(--black)}
.hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 40%}
.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,.25) 0%,rgba(10,10,10,.55) 45%,rgba(10,10,10,.92) 100%)}
.hero .wrap{position:relative;z-index:2;padding-top:140px;padding-bottom:70px;width:100%;display:grid;grid-template-columns:1.2fr .8fr;gap:40px;align-items:end}
.hero h1{font-size:clamp(46px,7.6vw,104px);max-width:12ch}
.hero h1 em{font-style:normal;color:var(--green)}
.hero .lede{font-size:clamp(18px,1.7vw,22px);max-width:50ch;margin:22px 0 32px;color:#e4e6df}
.hero .cta{display:flex;gap:14px;flex-wrap:wrap}
.hero-card{background:rgba(20,20,20,.75);border:1px solid var(--lineD);border-radius:var(--r);padding:26px;backdrop-filter:blur(8px)}
.hero-card h3{font-size:22px;color:var(--green);margin-bottom:12px}
.hero-card ul{list-style:none;padding:0;display:grid;gap:10px}
.hero-card li{display:flex;gap:10px;align-items:flex-start;font-weight:500}
.hero-card li svg{width:20px;height:20px;color:var(--green);flex:0 0 20px;margin-top:3px}
.hero-card .ph{display:block;font-family:var(--hf);font-size:34px;color:#fff;text-decoration:none;margin-top:16px;letter-spacing:.02em}
.hero-card .ph small{display:block;font-family:var(--bf);font-size:13px;color:var(--mutedD);letter-spacing:0;text-transform:none;font-weight:500}
/* strip */
.strip{background:var(--green);color:#0a0a0a;overflow:hidden;white-space:nowrap;padding:13px 0;font-family:var(--hf);font-weight:800;font-size:19px;letter-spacing:.08em;text-transform:uppercase}
.strip div{display:inline-block;animation:tick 38s linear infinite}
.strip span{padding:0 28px}
@keyframes tick{to{transform:translateX(-50%)}}
/* sections */
section{padding:96px 0}
.head{max-width:720px;margin-bottom:46px}
.head.c{text-align:center;margin-left:auto;margin-right:auto}
.head.row{max-width:none;display:flex;justify-content:space-between;align-items:flex-end;gap:28px;flex-wrap:wrap}
.head.row p{max-width:54ch}
.head h2{font-size:clamp(36px,5vw,64px)}
.head p{color:var(--muted);font-size:18.5px;margin-top:14px}
.dark{background:var(--black);color:#fff}
.dark .head p{color:var(--mutedD)}
.tone{background:var(--paper2)}
/* services */
.svcs{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.svc{background:#fff;border-radius:var(--r);overflow:hidden;text-decoration:none;display:flex;flex-direction:column;border:1px solid var(--line);transition:transform .25s,box-shadow .25s}
.svc:hover{transform:translateY(-6px);box-shadow:0 26px 50px rgba(0,0,0,.14)}
.svc .pic{aspect-ratio:4/3;overflow:hidden;background:#222}
.svc img{width:100%;height:100%;object-fit:cover;transition:transform .6s}
.svc:hover img{transform:scale(1.06)}
.svc .in{padding:22px 22px 24px;display:flex;flex-direction:column;gap:8px;flex:1}
.svc .ic{width:46px;height:46px;border-radius:10px;background:var(--black);color:var(--green);display:grid;place-items:center;margin-top:-45px;position:relative;border:3px solid #fff}
.svc .ic svg{width:24px;height:24px}
.svc h3{font-size:26px}
.svc p{color:var(--muted);font-size:15.5px}
.svc .more{margin-top:auto;padding-top:12px;font-weight:700;color:var(--green2);display:inline-flex;gap:6px;align-items:center}
.svc .more svg{width:18px;height:18px}
/* steps */
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;counter-reset:s}
.step{background:var(--panel);border:1px solid var(--lineD);border-radius:var(--r);padding:30px 28px;position:relative}
.step:before{counter-increment:s;content:"0" counter(s);font-family:var(--hf);font-size:64px;font-weight:800;color:var(--green);line-height:1;display:block;margin-bottom:14px}
.step h3{font-size:26px;margin-bottom:8px}
.step p{color:var(--mutedD)}
/* split */
.split{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center}
.split img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:var(--r)}
.split h2{font-size:clamp(34px,4.4vw,56px);margin-bottom:16px}
.split p+p{margin-top:12px}
.ticks{list-style:none;padding:0;margin-top:22px;display:grid;gap:12px}
.ticks li{display:flex;gap:12px;align-items:flex-start;font-weight:500}
.ticks li svg{width:22px;height:22px;flex:0 0 22px;color:#0a0a0a;background:var(--green);border-radius:50%;padding:4px;margin-top:2px}
.dark .ticks li svg{color:#0a0a0a}
.pic-stack{position:relative;padding:0 40px 40px 0}
.pic-stack img{aspect-ratio:1;border-radius:var(--r)}
.pic-stack img+img{position:absolute;width:52%;right:0;bottom:0;border:8px solid var(--paper);box-shadow:0 20px 40px rgba(0,0,0,.25)}
.dark .pic-stack img+img{border-color:var(--black)}
/* gallery */
.gal{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.gal a{display:block;border-radius:var(--r);overflow:hidden;background:#222;aspect-ratio:1}
.gal img{width:100%;height:100%;object-fit:cover;transition:transform .5s}
.gal a:hover img{transform:scale(1.04)}
.gal a:first-child{grid-column:span 2;grid-row:span 2;aspect-ratio:auto}
/* areas */
.areas{display:flex;flex-wrap:wrap;gap:10px}
.areas span{background:#fff;border:1px solid var(--line);border-radius:40px;padding:10px 18px;font-weight:600}
.dark .areas span{background:var(--panel);border-color:var(--lineD)}
/* social proof */
.proof{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.proof a{display:flex;gap:18px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:26px;text-decoration:none;transition:transform .2s,box-shadow .2s}
.proof a:hover{transform:translateY(-4px);box-shadow:0 18px 36px rgba(0,0,0,.1)}
.proof .ic{width:56px;height:56px;border-radius:14px;background:var(--black);color:var(--green);display:grid;place-items:center;flex:0 0 56px}
.proof .ic svg{width:26px;height:26px}
.proof b{display:block;font-family:var(--hf);font-size:24px;text-transform:uppercase}
.proof small{color:var(--muted)}
/* faq */
.faq details{border-bottom:1px solid var(--line);padding:18px 0}
.dark .faq details{border-color:var(--lineD)}
.faq summary{font-weight:700;cursor:pointer;font-size:18px;list-style:none;display:flex;justify-content:space-between;gap:16px}
.faq summary::-webkit-details-marker{display:none}
.faq summary:after{content:"+";font-size:26px;line-height:1;color:var(--green2);font-family:var(--hf)}
.faq details[open] summary:after{content:"–"}
.faq p{margin-top:10px;color:var(--muted)}
.dark .faq p{color:var(--mutedD)}
.faq-grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:56px;align-items:start}
/* cta */
.ctab{background:var(--green);color:#0a0a0a;padding:72px 0}
.ctab .wrap{display:flex;justify-content:space-between;align-items:center;gap:28px;flex-wrap:wrap}
.ctab h2{font-size:clamp(34px,4.6vw,60px);max-width:16ch}
.ctab .big{font-family:var(--hf);font-size:clamp(34px,4.6vw,60px);text-decoration:none;display:block;line-height:1}
.ctab p{font-weight:600;margin-top:6px}
/* pagehead */
.ph{position:relative;color:#fff;padding:120px 0 72px;overflow:hidden;background:var(--black)}
.ph>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.45}
.ph:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,.3),rgba(10,10,10,.92))}
.ph .wrap{position:relative;z-index:2}
.ph h1{font-size:clamp(42px,6.4vw,84px);max-width:16ch}
.ph p{font-size:19px;color:#dfe2d9;max-width:56ch;margin-top:14px}
.crumbs{font-size:14px;color:#b9bdb3;margin-bottom:16px}
.crumbs a{text-decoration:none}
/* service page */
.svc-hero{display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:center}
.svc-hero img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:var(--r)}
.svc-hero h2{font-size:clamp(32px,4vw,50px);margin-bottom:14px}
.svc-nav{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:40px}
.svc-nav a{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px 18px;text-decoration:none;font-weight:700;display:flex;gap:10px;align-items:center}
.svc-nav a svg{width:20px;height:20px;color:var(--green2)}
.svc-nav a[aria-current]{background:var(--black);color:#fff;border-color:var(--black)}
.svc-nav a[aria-current] svg{color:var(--green)}
.svc-row{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center;padding:48px 0;border-bottom:1px solid var(--line)}
.svc-row:nth-child(even) .svc-pic{order:2}
.svc-row img{width:100%;aspect-ratio:16/11;object-fit:cover;border-radius:var(--r)}
.svc-row h2{font-size:clamp(30px,3.6vw,46px);margin-bottom:12px}
/* contact */
.contact-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:52px;align-items:start}
form.q{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:34px;display:grid;gap:16px}
form.q h2{font-size:32px}
form.q label{font-weight:600;font-size:14.5px;display:grid;gap:6px}
form.q input,form.q select,form.q textarea{font:inherit;padding:13px 14px;border:1px solid var(--line);border-radius:8px;background:var(--paper);color:var(--ink);width:100%}
form.q input:focus,form.q select:focus,form.q textarea:focus{border-color:var(--green2);outline:0;box-shadow:0 0 0 3px rgba(53,229,27,.25)}
form.q .two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
form.q button{font-family:var(--hf);text-transform:uppercase;letter-spacing:.06em;font-weight:800;background:var(--black);color:var(--green);border:0;padding:17px;border-radius:8px;cursor:pointer;font-size:20px}
form.q button:hover{background:#000}
form.q .note{font-size:14px;color:var(--muted)}
.hide{position:absolute;left:-9999px}
.ccard{display:grid;gap:16px}
.ccard a.line,.ccard .line{display:flex;gap:16px;align-items:center;text-decoration:none;padding:20px;border:1px solid var(--line);border-radius:var(--r);background:#fff}
.ccard .ic{width:48px;height:48px;border-radius:12px;display:grid;place-items:center;background:var(--black);color:var(--green);flex:0 0 48px}
.ccard .ic svg{width:22px;height:22px}
.ccard b{display:block;font-size:17px}
.ccard small{color:var(--muted)}
.map{width:100%;height:400px;border:0;border-radius:var(--r);filter:grayscale(.3) saturate(.8)}
/* blog */
.posts{display:grid;grid-template-columns:repeat(2,1fr);gap:26px}
.post{background:#fff;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;text-decoration:none;display:flex;flex-direction:column;transition:transform .25s,box-shadow .25s}
.post:hover{transform:translateY(-6px);box-shadow:0 26px 50px rgba(0,0,0,.12)}
.post img{aspect-ratio:16/9;object-fit:cover;width:100%}
.post .in{padding:24px}
.post small{color:var(--green2);font-weight:700;letter-spacing:.1em;text-transform:uppercase;font-size:12px}
.post h3{font-size:26px;margin:8px 0 10px;text-transform:none;letter-spacing:0}
.post p{color:var(--muted)}
.article{max-width:760px;margin:0 auto}
.article h1{text-transform:none;letter-spacing:0;font-size:clamp(34px,5vw,56px);line-height:1.05}
.article .meta{color:var(--muted);margin:14px 0 30px;font-weight:600}
.article>img{border-radius:var(--r);aspect-ratio:16/9;object-fit:cover;width:100%;margin-bottom:34px}
.article h2{font-size:30px;margin:34px 0 10px;text-transform:none;letter-spacing:0}
.article p{font-size:18px}
.article .intro{font-size:21px;color:var(--muted)}
.article .box{background:var(--black);color:#fff;border-radius:var(--r);padding:30px;margin-top:44px;display:flex;justify-content:space-between;gap:20px;align-items:center;flex-wrap:wrap}
.article .box h3{font-size:26px;color:var(--green)}
/* footer */
footer.foot{background:var(--black);color:#c9cdc3;padding:70px 0 28px;font-size:15.5px}
.fgrid{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:36px}
.foot h4{font-family:var(--hf);font-size:19px;margin-bottom:14px;color:var(--green);letter-spacing:.08em}
.foot ul{list-style:none;padding:0;display:grid;gap:9px}
.foot a{text-decoration:none}
.foot a:hover{color:#fff;text-decoration:underline}
.soc{display:flex;gap:10px;margin-top:18px}
.soc a{width:42px;height:42px;border-radius:50%;display:grid;place-items:center;border:1px solid var(--lineD);color:#fff}
.soc svg{width:19px;height:19px}
.legal{border-top:1px solid var(--lineD);margin-top:44px;padding-top:22px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:14px}
.legal .heart{color:#ff5a6e}
.mbar{display:none}
@media (max-width:960px){
 .menu{display:none;position:absolute;left:0;right:0;top:78px;background:var(--black);flex-direction:column;align-items:stretch;padding:12px 22px 22px;gap:2px;border-bottom:1px solid var(--lineD)}
 .menu.open{display:flex}
 .menu a{padding:13px 10px}
 .menu .btn{margin:10px 0 0;justify-content:center}
 .burger{display:block}
 .hero .wrap{grid-template-columns:1fr;padding-top:90px}
 .svcs{grid-template-columns:1fr 1fr}
 .steps,.svc-nav{grid-template-columns:1fr}
 .split,.svc-hero,.svc-row,.contact-grid,.faq-grid,.proof,.posts{grid-template-columns:1fr;gap:34px}
 .svc-row:nth-child(even) .svc-pic{order:0}
 .fgrid{grid-template-columns:1fr 1fr}
 .gal{grid-template-columns:1fr 1fr}
 .gal a:first-child{grid-column:span 2;grid-row:auto;aspect-ratio:16/9}
}
@media (max-width:640px){
 body{font-size:16.5px}
 section{padding:66px 0}
 .topbar .hide-m{display:none}
 .svcs,.fgrid{grid-template-columns:1fr}
 .hero{min-height:0}
 .hero .wrap{padding-top:70px;padding-bottom:40px}
 .hero-card{padding:20px}
 form.q .two{grid-template-columns:1fr}
 form.q{padding:24px 18px}
 .pic-stack{padding:0 24px 24px 0}
 .mbar{display:grid;grid-template-columns:1fr 1fr;position:fixed;left:0;right:0;bottom:0;z-index:30;box-shadow:0 -6px 20px rgba(0,0,0,.25)}
 .mbar a{padding:16px;text-align:center;font-weight:800;text-decoration:none;font-family:var(--hf);text-transform:uppercase;letter-spacing:.06em;font-size:18px}
 .mbar a:first-child{background:var(--black);color:#fff}
 .mbar a:last-child{background:var(--green);color:#0a0a0a}
 footer.foot{padding-bottom:90px}
}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important;animation:none!important}.js .rv{opacity:1;transform:none}}
"""

JS = """<script>(function(){if(!('IntersectionObserver' in window))return;var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');o.unobserve(e.target)}})},{rootMargin:'0px 0px -8%'});document.querySelectorAll('.rv').forEach(function(el){o.observe(el)})})();</script>"""

NAV = [("index.html","Home"),("services.html","Services"),("about.html","About"),("gallery.html","Gallery"),("areas.html","Areas"),("blog.html","Blog"),("contact.html","Contact")]

def schema():
    return {"@context":"https://schema.org","@type":"MovingCompany","name":BIZ["name"],"telephone":BIZ["phoneIntl"],"email":BIZ["email"],
            "url":BIZ["site"],"sameAs":[BIZ["fb"]],"address":{"@type":"PostalAddress","addressLocality":BIZ["town"],"addressRegion":BIZ["state"],"postalCode":BIZ["postcode"],"addressCountry":"AU"},
            "areaServed":"Lismore and the Northern Rivers, NSW","image":BIZ["site"]+"img/truck.jpg"}

def shell(title, desc, cur, body, og="img/truck.jpg"):
    li = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{n}</a></li>' for h,n in NAV)
    abn = f'<li>ABN {E(BIZ["abn"])}</li>' if BIZ["abn"] else ""
    return f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:image" content="{BIZ['site']}{og}">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Barlow:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<script>document.documentElement.classList.add('js')</script>
<script type="application/ld+json">{json.dumps(schema())}</script>
</head>
<body>
<div class="topbar"><div class="wrap"><span class="hide-m"><b>Local &amp; interstate moves</b> · Pickups &amp; deliveries · Domestic &amp; green waste · Lismore NSW</span><span><a href="tel:{BIZ['phoneIntl']}">Call Will on {BIZ['phone']}</a></span></div></div>
<header class="site"><div class="wrap nav">
 <a class="brand" href="index.html" aria-label="{E(BIZ['name'])} home">{LOGO_SVG}</a>
 <button class="burger" aria-label="Open menu" aria-expanded="false" onclick="var m=document.getElementById('menu');m.classList.toggle('open');this.setAttribute('aria-expanded',m.classList.contains('open'))">{ICO['menu']}</button>
 <ul class="menu" id="menu">{li}<li><a class="btn btn-green" href="contact.html">Get a quote</a></li></ul>
</div></header>
<main>{body}</main>
<footer class="foot"><div class="wrap">
 <div class="fgrid">
  <div>{LOGO_SVG}<p style="margin-top:18px;max-width:36ch">Truck removals for homes and businesses across Lismore and the Northern Rivers. Local and interstate moves, pickups and deliveries, domestic and green waste removal.</p>
   <div class="soc"><a href="{BIZ['fb']}" aria-label="Facebook" rel="noopener">{ICO['fb']}</a></div></div>
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
    return f'<div class="ph"><img src="{img}" alt=""><div class="wrap"><div class="crumbs"><a href="index.html">Home</a> / {E(crumb)}</div><h1>{title}</h1><p>{E(sub)}</p></div></div>'

def ctab():
    return f'<div class="ctab"><div class="wrap"><div><h2>Got a move coming up?</h2><p>Call or text Will for a straight quote.</p></div><div><a class="big" href="tel:{BIZ["phoneIntl"]}">{BIZ["phone"]}</a><p><a href="contact.html" style="font-weight:800">or send a quote request →</a></p></div></div></div>'

def faq_html(items):
    return '<div class="faq">' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q,a in items) + "</div>"

GENERAL_FAQ = [
 ["Do you still do man-and-ute moves?","No. Mister Shifter runs pantech trucks with a crew for moves of all sizes, plus pickups, deliveries and waste runs."],
 ["What areas do you cover?","Lismore and the Northern Rivers for local work, and interstate moves out of the region. See the service areas page or call to check your suburb."],
 ["How do I get a quote?","Call or text Will on "+BIZ["phone"]+", message the Facebook page, or send the form on the contact page. Tell us where from, where to, how big and when."],
 ["Do I need to be there on the day?","Someone needs to let the crew in, point out what's going and lock up after. It doesn't have to be you, but it helps."],
 ["Can you move a single item?","Yes. Pickups and deliveries of furniture, whitegoods and marketplace buys are a big part of what we do."],
 ["Do you take rubbish as well?","Yes. Domestic and green waste removal, on its own or combined with a move."],
]

def svc_cards():
    out = ""
    for s in SERVICES:
        out += f'<a class="svc rv" href="{s["id"]}.html"><div class="pic"><img src="{s["img"]}" alt="{E(s["title"])}" loading="lazy"></div><div class="in"><span class="ic">{ICO[s["icon"]]}</span><h3>{E(s["title"])}</h3><p>{E(s["short"])}</p><span class="more">Learn more {ICO["arrow"]}</span></div></a>'
    return out

def page_index():
    strip = "".join(f"<span>{E(x)}</span><span aria-hidden='true'>✦</span>" for x in ["Local moves","Interstate moves","Pickups & deliveries","Domestic & green waste removal","Lismore & Northern Rivers","Call "+BIZ["phone"]])
    body = f"""
<div class="hero"><img src="img/fleet.jpg" alt="Mister Shifter Removals truck in Lismore" fetchpriority="high"><div class="wrap">
 <div><div class="eyebrow">Lismore · Northern Rivers · Interstate</div><h1>Trucks, crew, <em>done.</em></h1>
 <p class="lede">Mister Shifter Removals moves homes and businesses across Lismore and the Northern Rivers, and interstate when you're going further. Pickups, deliveries and waste runs too.</p>
 <div class="cta"><a class="btn btn-green" href="contact.html">Get a quote</a><a class="btn btn-ghostW" href="tel:{BIZ['phoneIntl']}">{ICO['phone']}{BIZ['phone']}</a></div></div>
 <aside class="hero-card rv"><h3>What we do</h3><ul>
  <li>{ICO['check']}Local &amp; interstate moves by truck</li><li>{ICO['check']}Pickups &amp; deliveries, single items welcome</li><li>{ICO['check']}Domestic &amp; green waste removal</li><li>{ICO['check']}Based in Lismore, deal direct with Will</li></ul>
  <a class="ph" href="tel:{BIZ['phoneIntl']}">{BIZ['phone']}<small>Call or text for a quote</small></a></aside>
</div></div>
<div class="strip" aria-label="Services"><div>{strip}{strip}</div></div>
<section><div class="wrap"><div class="head row"><div><div class="eyebrow">Services</div><h2>One truck. Every kind of job.</h2></div><p>From a full house move to a single lounge off Marketplace, the truck and crew turn up and get it done.</p></div><div class="svcs">{svc_cards()}</div></div></section>
<section class="dark"><div class="wrap"><div class="head"><div class="eyebrow">How it works</div><h2>Three steps to moved.</h2></div><div class="steps">
 <div class="step rv"><h3>Call or message Will</h3><p>Where from, where to, how big, and when. Phone, text, Facebook or the quote form. You'll get a straight price.</p></div>
 <div class="step rv"><h3>We turn up with the truck</h3><p>Pantech truck, blankets, straps and trolleys, plus a crew that does this for a living.</p></div>
 <div class="step rv"><h3>Loaded, driven, unloaded</h3><p>Everything wrapped, stacked and strapped, then unloaded into the right rooms at the other end.</p></div>
</div></div></section>
<section><div class="wrap split"><div class="pic-stack rv"><img src="img/team.jpg" alt="The Mister Shifter crew with the truck" loading="lazy"><img src="img/house.jpg" alt="Mister Shifter truck at a house" loading="lazy"></div>
 <div class="rv"><div class="eyebrow">About</div><h2>Will and the crew.</h2><p>Mister Shifter Removals is a Lismore business run by Will. It started small and has grown into a proper truck-based removalist for the Northern Rivers, with the same approach it had on day one: turn up on time, look after people's stuff, and be straight about the price.</p>
 <ul class="ticks"><li>{ICO['check']}Pantech trucks, not a ute</li><li>{ICO['check']}Based in Lismore, working across the Northern Rivers</li><li>{ICO['check']}Local and interstate</li><li>{ICO['check']}You deal with Will from quote to delivery</li></ul>
 <p style="margin-top:26px"><a class="btn btn-dark" href="about.html">More about us {ICO['arrow']}</a></p></div></div></section>
<section class="tone"><div class="wrap"><div class="head row"><div><div class="eyebrow">Gallery</div><h2>On the job.</h2></div><a class="btn btn-ghost" href="gallery.html">See all photos</a></div>
 <div class="gal">{gallery_html(6)}</div></div></section>
<section><div class="wrap"><div class="head"><div class="eyebrow">Reviews</div><h2>Don't take our word for it.</h2><p>Read what customers have said about Mister Shifter on Google and Facebook.</p></div>
 <div class="proof"><a href="https://www.google.com/search?q=Mister+Shifter+Removals+Lismore" rel="noopener"><span class="ic"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6.9 7.1.6-5.4 4.7 1.7 7.3L12 17.8 5.7 21.5l1.7-7.3L2 9.5l7.1-.6z"/></svg></span><span><b>Google reviews</b><small>Search "Mister Shifter Removals Lismore" to read them</small></span></a>
 <a href="{BIZ['fb']}" rel="noopener"><span class="ic">{ICO['fb']}</span><span><b>Facebook page</b><small>Photos, updates and recommendations</small></span></a></div></div></section>
<section class="dark"><div class="wrap"><div class="head"><div class="eyebrow">Service areas</div><h2>Lismore &amp; the Northern Rivers.</h2><p>Local moves, pickups and waste runs across the region. Interstate from here to wherever you're headed.</p></div>
 <div class="areas">{"".join(f"<span>{E(t)}</span>" for t in TOWNS)}<span>+ surrounding areas</span></div>
 <p style="margin-top:26px"><a class="btn btn-green" href="areas.html">Service areas</a></p></div></section>
<section><div class="wrap faq-grid"><div class="rv"><div class="eyebrow">FAQ</div><h2 style="font-size:clamp(34px,4.4vw,56px)">Common questions.</h2><p style="color:var(--muted);margin-top:12px">Something else? Call Will on {BIZ['phone']}.</p><p style="margin-top:22px"><a class="btn btn-ghost" href="faq.html">All FAQs</a></p></div><div class="rv">{faq_html(GENERAL_FAQ[:4])}</div></div></section>
{ctab()}"""
    return shell(f"{BIZ['name']} | Removalists in Lismore & the Northern Rivers", "Mister Shifter Removals: truck removals for homes and businesses across Lismore and the Northern Rivers. Local and interstate moves, pickups and deliveries, domestic and green waste removal. Call Will on 0475 074 906.", "index.html", body, "img/fleet.jpg")

PHOTOS = [("img/fleet.jpg","Mister Shifter truck and the crew's vehicles"),("img/truck.jpg","Mister Shifter pantech truck"),("img/team.jpg","Will and the crew in front of the truck"),("img/house.jpg","Truck backed into a driveway on moving day"),("img/heart.jpg","Mister Shifter truck in town"),("img/family.jpg","The Mister Shifter family at Christmas")]

def gallery_html(n=6):
    return "".join(f'<a href="{p}" target="_blank" rel="noopener"><img src="{p}" alt="{E(a)}" loading="lazy"></a>' for p,a in PHOTOS[:n])

def page_services():
    rows = ""
    for s in SERVICES:
        pts = "".join(f"<li>{ICO['check']}{E(p)}</li>" for p in s["points"])
        rows += f'<div class="svc-row" id="{s["id"]}"><div class="svc-pic rv"><img src="{s["img"]}" alt="{E(s["title"])}" loading="lazy"></div><div class="rv"><div class="eyebrow">{E(s["tag"])}</div><h2>{E(s["title"])}</h2><p>{E(s["lede"])}</p><ul class="ticks">{pts}</ul><p style="margin-top:24px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-dark" href="{s["id"]}.html">Details</a><a class="btn btn-green" href="contact.html">Get a quote</a></p></div></div>'
    body = pagehead("Removal services", "Local and interstate moves, pickups and deliveries, and waste removal, all by truck out of Lismore.", "Services", "img/truck.jpg") + f'<section style="padding-top:30px"><div class="wrap">{rows}</div></section>' + ctab()
    return shell(f"Services | {BIZ['name']}", "Local moves, interstate moves, pickups and deliveries, and domestic and green waste removal across Lismore and the Northern Rivers.", "services.html", body)

def page_service(s):
    others = "".join(f'<a href="{o["id"]}.html"{" aria-current=\"page\"" if o is s else ""}>{ICO[o["icon"]]}{E(o["title"])}</a>' for o in SERVICES)
    pts = "".join(f"<li>{ICO['check']}{E(p)}</li>" for p in s["points"])
    paras = "".join(f"<p>{E(p)}</p>" for p in s["body"])
    body = pagehead(E(s["title"]), s["lede"], s["title"], s["img"] if s["img"].startswith("img/") else "img/truck.jpg") + f"""
<section><div class="wrap"><div class="svc-hero"><div class="rv"><div class="eyebrow">{E(s["tag"])}</div><h2>{E(s["title"])} with Mister Shifter</h2>{paras}<ul class="ticks">{pts}</ul>
 <p style="margin-top:26px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-green" href="contact.html">Get a quote</a><a class="btn btn-ghost" href="tel:{BIZ['phoneIntl']}">{ICO['phone']}{BIZ['phone']}</a></p></div><img class="rv" src="{s["img"]}" alt="{E(s["title"])}" loading="lazy"></div>
 <div class="svc-nav">{others}</div></div></section>
<section class="tone"><div class="wrap faq-grid"><div><div class="eyebrow">FAQ</div><h2 style="font-size:clamp(30px,4vw,48px)">{E(s["title"])} questions.</h2></div>{faq_html(s["faq"] + GENERAL_FAQ[2:4])}</div></section>
{ctab()}"""
    return shell(f"{s['title']} | {BIZ['name']} Lismore", s["short"], "services.html", body)

def page_about():
    body = pagehead("About Will &amp; the crew", "A Lismore removalist that grew from one bloke and a ute into trucks and a crew.", "About", "img/team.jpg") + f"""
<section><div class="wrap split"><div class="rv"><div class="eyebrow">Our story</div><h2>Built in Lismore, one move at a time.</h2>
 <p>Mister Shifter Removals is run by Will out of Lismore. The business started small and has grown with the Northern Rivers: these days it runs pantech trucks and a crew, handling full house and business moves, interstate runs, pickups and deliveries, and domestic and green waste removal.</p>
 <p>What hasn't changed is how the job is done. Will quotes it straight, the crew turns up when they said they would, and your stuff gets wrapped, strapped and treated like it's their own.</p>
 <ul class="ticks"><li>{ICO['check']}Owner-operated, you deal with Will directly</li><li>{ICO['check']}Pantech trucks with blankets, straps and trolleys</li><li>{ICO['check']}Local, regional and interstate</li><li>{ICO['check']}Follow the crew on Facebook</li></ul></div>
 <div class="pic-stack rv"><img src="img/team.jpg" alt="Will and the crew" loading="lazy"><img src="img/family.jpg" alt="The Mister Shifter family" loading="lazy"></div></div></section>
<section class="dark"><div class="wrap"><div class="head"><div class="eyebrow">How we work</div><h2>Simple rules.</h2></div><div class="steps">
 <div class="step rv"><h3>Straight quotes</h3><p>You get a price before the truck moves. No surprises on the invoice.</p></div>
 <div class="step rv"><h3>Look after the gear</h3><p>Wrapped, stacked and strapped. Furniture and whitegoods get the blanket treatment.</p></div>
 <div class="step rv"><h3>Turn up and get it done</h3><p>On time, with the right truck and enough hands for the job.</p></div></div></div></section>
<section><div class="wrap"><div class="head row"><div><div class="eyebrow">Gallery</div><h2>The trucks and the team.</h2></div><a class="btn btn-ghost" href="gallery.html">All photos</a></div><div class="gal">{gallery_html(3)}</div></div></section>
{ctab()}"""
    return shell(f"About | {BIZ['name']}", "Mister Shifter Removals is a Lismore removalist run by Will, with pantech trucks and a crew working across the Northern Rivers and interstate.", "about.html", body, "img/team.jpg")

def page_gallery():
    body = pagehead("Gallery", "The trucks, the crew and a few jobs around the Northern Rivers.", "Gallery", "img/heart.jpg") + f'<section><div class="wrap"><div class="gal">{gallery_html(6)}</div><p style="margin-top:30px;color:var(--muted)">More photos on <a href="{BIZ["fb"]}" rel="noopener">Facebook</a>.</p></div></section>' + ctab()
    return shell(f"Gallery | {BIZ['name']}", "Photos of the Mister Shifter Removals trucks and crew.", "gallery.html", body, "img/heart.jpg")

def page_areas():
    chips = "".join(f"<span>{E(t)}</span>" for t in TOWNS)
    body = pagehead("Service areas", "Local work across Lismore and the Northern Rivers. Interstate moves from the region to wherever you're going.", "Service areas", "img/house.jpg") + f"""
<section><div class="wrap split"><div class="rv"><div class="eyebrow">Local &amp; regional</div><h2>Northern Rivers, covered.</h2><p>We're based in Lismore and work across the Northern Rivers: the city, the hinterland villages and the coast. If you're not sure whether we come to you, call and ask.</p><div class="areas" style="margin-top:24px">{chips}<span>+ surrounding areas</span></div></div>
 <div class="rv"><iframe class="map" title="Map of Lismore NSW" loading="lazy" src="https://maps.google.com/maps?q=Lismore+NSW+2480&z=10&output=embed"></iframe></div></div></section>
<section class="dark"><div class="wrap split"><img class="rv" src="{U('1716441592984-75d4c882e5cf',1100)}" alt="Highway through green hills" loading="lazy"><div class="rv"><div class="eyebrow">Interstate</div><h2>Going further? We'll take it.</h2><p>Interstate moves out of the Northern Rivers. One truck, loaded once and delivered to your new door.</p><p style="margin-top:26px"><a class="btn btn-green" href="interstate-moves.html">Interstate moves</a></p></div></div></section>
{ctab()}"""
    return shell(f"Service areas | {BIZ['name']}", "Mister Shifter Removals covers Lismore, Goonellabah, Ballina, Byron Bay, Casino and the rest of the Northern Rivers, plus interstate moves.", "areas.html", body, "img/house.jpg")

def page_faq():
    allq = GENERAL_FAQ + [q for s in SERVICES for q in s["faq"]]
    body = pagehead("FAQ", "Answers to the questions we get asked most. Anything else, call Will.", "FAQ") + f'<section><div class="wrap" style="max-width:860px">{faq_html(allq)}</div></section>' + ctab()
    return shell(f"FAQ | {BIZ['name']}", "Frequently asked questions about moving with Mister Shifter Removals in Lismore.", "faq.html", body)

def page_blog():
    cards = "".join(f'<a class="post rv" href="{p["slug"]}.html"><img src="{p["img"]}" alt="" loading="lazy"><div class="in"><small>{E(p["date"])}</small><h3>{E(p["title"])}</h3><p>{E(p["intro"])}</p></div></a>' for p in POSTS)
    body = pagehead("Moving tips", "Practical advice from people who move houses for a living.", "Blog", "img/truck.jpg") + f'<section><div class="wrap"><div class="posts">{cards}</div></div></section>' + ctab()
    return shell(f"Moving tips & blog | {BIZ['name']}", "Moving tips, checklists and advice from Mister Shifter Removals, Lismore.", "blog.html", body)

def page_post(p):
    secs = "".join(f"<h2>{E(h)}</h2><p>{E(t)}</p>" for h,t in p["sections"])
    body = f"""<section style="padding-top:60px"><div class="wrap"><article class="article"><div class="crumbs" style="color:var(--muted)"><a href="index.html">Home</a> / <a href="blog.html">Blog</a></div><h1>{E(p["title"])}</h1><div class="meta">{E(p["date"])} · Mister Shifter Removals</div><img src="{p["img"]}" alt=""><p class="intro">{E(p["intro"])}</p>{secs}
 <div class="box"><div><h3>Need a truck for it?</h3><p>Call Will on {BIZ['phone']} or send a quote request.</p></div><a class="btn btn-green" href="contact.html">Get a quote</a></div></article></div></section>"""
    return shell(f"{p['title']} | {BIZ['name']}", p["intro"], "blog.html", body)

def page_contact():
    opts = "".join(f"<option>{E(s['title'])}</option>" for s in SERVICES) + "<option>Not sure yet</option>"
    body = pagehead("Get a quote", "Tell us where from, where to, how big and when. Will will come back to you with a price.", "Contact", "img/fleet.jpg") + f"""
<section><div class="wrap contact-grid">
<form class="q" action="https://formsubmit.co/{BIZ['email']}" method="POST">
 <input type="hidden" name="_subject" value="New quote request from the Mister Shifter website">
 <input type="hidden" name="_template" value="table">
 <input type="hidden" name="_captcha" value="false">
 <input type="hidden" name="_next" value="{BIZ['site']}thanks.html">
 <input type="hidden" name="_autoresponse" value="Thanks for contacting Mister Shifter Removals. We've got your request and the team will be in touch soon. Need us faster? Call or text Will on {BIZ['phone']}.">
 <input type="text" name="_honey" class="hide" tabindex="-1" autocomplete="off">
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
    return shell(f"Get a quote | {BIZ['name']}", f"Contact Mister Shifter Removals, Lismore. Call {BIZ['phone']} or send a quote request online.", "contact.html", body)

def page_thanks():
    body = pagehead("Thanks, we've got it", "Your request is in Will's inbox and the team will contact you soon. Check your email for a confirmation.", "Thank you") + f'<section><div class="wrap"><p style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-dark" href="index.html">Back to home</a><a class="btn btn-green" href="tel:{BIZ["phoneIntl"]}">{ICO["phone"]}Need it sooner? Call {BIZ["phone"]}</a></p></div></section>'
    return shell(f"Thank you | {BIZ['name']}", "Request received.", "", body)

def build():
    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("*.html"): f.unlink()
    (OUT/"style.css").write_text(CSS)
    (OUT/"index.html").write_text(page_index())
    (OUT/"services.html").write_text(page_services())
    for s in SERVICES: (OUT/f"{s['id']}.html").write_text(page_service(s))
    (OUT/"about.html").write_text(page_about())
    (OUT/"gallery.html").write_text(page_gallery())
    (OUT/"areas.html").write_text(page_areas())
    (OUT/"faq.html").write_text(page_faq())
    (OUT/"blog.html").write_text(page_blog())
    for p in POSTS: (OUT/f"{p['slug']}.html").write_text(page_post(p))
    (OUT/"contact.html").write_text(page_contact())
    (OUT/"thanks.html").write_text(page_thanks())
    print("built", OUT.name, len(list(OUT.glob('*.html'))), "pages")

if __name__ == "__main__":
    build()
