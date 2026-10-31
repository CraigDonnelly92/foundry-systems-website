#!/usr/bin/env python3
"""Builds the Foundry Systems static site into ./dist (or the folder given as argv[1])."""
import os, sys, shutil, json, html

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SRC, "..", "dist")
os.makedirs(OUT, exist_ok=True)

SITE = "https://foundrysystems.ca"
PHONE = "780-834-8078"; TEL = "+17808348078"; EMAIL = "craig.foundrysystems@gmail.com"
FORM_ACTION = "https://formsubmit.co/" + EMAIL
ROBOT = open(os.path.join(SRC, "robot.svg"), encoding="utf-8").read()
e = html.escape

ICON = {
 "glass":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 18 6 6h12l2 12z"/><path d="M9 9l-1 5M13 9l3 4"/></svg>',
 "auto":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/></svg>',
 "electrical":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg>',
 "plumbing":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/></svg>',
 "hvac":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1 19.1 4.9"/></svg>',
 "landscaping":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22V12"/><path d="M12 12C12 7 8 4 4 4c0 5 3 8 8 8zM12 12c0-4 3-7 8-7 0 4-3 7-8 7z"/></svg>',
 "phone":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="2" width="12" height="20" rx="2"/><path d="M11 18h2"/></svg>',
 "bolt":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg>',
 "call":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
 "form":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6l1 2h3v16H5V5h3z"/><path d="M9 12h6M9 16h4"/></svg>',
 "search":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>',
 "map":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
 "wrench":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/></svg>',
 "shield":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
 "person":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>',
 "clock":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "tag":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg>',
}

BRAND = ('<svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true"><rect x="2" y="2" width="36" height="36" rx="9" fill="#26262B" stroke="#FF6B1A" stroke-width="2"/>'
         '<path d="M13 11h15v5H18.5v3.5H26v5h-7.5V30H13z" fill="#FF6B1A"/></svg>')

NAV = [("index.html","Home"),("pricing.html","Pricing"),("work.html","Sample work"),("industries.html","Industries"),
       ("how-it-works.html","How it works"),("about.html","About"),("faq.html","FAQ")]

def schema():
    return json.dumps({
        "@context":"https://schema.org","@type":"ProfessionalService","name":"Foundry Systems",
        "description":"Fixed-price websites for trades and service businesses: glass shops, auto repair, electricians, plumbers, HVAC and landscapers.",
        "url":SITE,"telephone":"+1-"+PHONE,"email":EMAIL,"founder":{"@type":"Person","name":"Craig Donnelly"},
        "areaServed":[{"@type":"Place","name":"Peace Region, Alberta"},{"@type":"Country","name":"Canada"}],
        "priceRange":"$1,500–$1,997 CAD"})

CTA = '''<section class="section-tight"><div class="wrap"><div class="cta-band reveal">
<div><h2>Ready when you are.</h2><p>Fill out the project form in about 15 minutes, or just ask a question. I reply within one business day.</p></div>
<div class="btn-row"><a class="btn btn-primary" href="start.html">Start my project</a><a class="btn btn-ghost" href="contact.html">Ask a question</a></div>
</div></div></section>'''

def page(fname, title, desc, body, active=None, cta=True, bot_hello=None, extra_head="", body_attr=""):
    menu = "".join('<li><a href="%s"%s>%s</a></li>' % (h, ' aria-current="page"' if h == active else "", l) for h, l in NAV)
    hello = ' data-bot-hello="%s"' % e(bot_hello) if bot_hello else ""
    canon = SITE + "/" + ("" if fname == "index.html" else fname)
    doc = f'''<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta name="theme-color" content="#18181B">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
<script type="application/ld+json">{schema()}</script>
{extra_head}
</head>
<body{hello}{body_attr}>
<a class="skip" href="#main">Skip to content</a>
<div class="promo" role="region" aria-label="2026 special"><div class="wrap">
<span>🔥 2026 special: pay for your build by Dec 31 and lock in your care plan at <b>$99/mo for life</b>. Normally $147. <a href="pricing.html">See pricing</a></span>
<button type="button" aria-label="Close this banner">×</button></div></div>
<header class="site-header"><div class="wrap nav">
<a class="brand" href="index.html" aria-label="Foundry Systems home">{BRAND}<span>Foundry <b>Systems</b></span></a>
<button class="menu-toggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
<ul class="menu" id="menu">{menu}<li class="only-mobile"><a href="contact.html">Contact</a></li><li class="only-mobile"><a href="start.html">Start your project</a></li></ul>
<div class="nav-cta"><a class="btn btn-ghost" href="contact.html">Contact</a><a class="btn btn-primary" href="start.html">Start your project</a></div>
</div></header>
<main id="main">
{body}
{CTA if cta else ""}
</main>
<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div><a class="brand" href="index.html">{BRAND}<span>Foundry <b>Systems</b></span></a>
<p class="muted" style="margin-top:14px;max-width:34ch">Websites built to work as hard as you do. Based in the Peace region, building for businesses anywhere.</p>
<p><a href="tel:{TEL}">{PHONE}</a> (call or text)<br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<div><h4>Explore</h4><ul><li><a href="pricing.html">Pricing</a></li><li><a href="work.html">Sample work</a></li><li><a href="how-it-works.html">How it works</a></li><li><a href="about.html">About</a></li><li><a href="faq.html">FAQ</a></li></ul></div>
<div><h4>Industries</h4><ul>{"".join('<li><a href="%s">%s</a></li>' % (t["page"], t["label"]) for t in TRADES.values())}</ul></div>
<div><h4>Get started</h4><ul><li><a href="start.html">Start your project</a></li><li><a href="contact.html">Contact</a></li><li><a href="checkup.html">Free website checkup</a></li><li><a href="privacy.html">Privacy</a></li><li><a href="terms.html">Terms</a></li></ul></div>
</div>
<div class="legal"><span>© <span id="year">2026</span> Foundry Systems. Prices in Canadian dollars.</span><span>I reply to every call, text and form within one business day.</span></div>
</div></footer>
<nav class="mobile-bar" aria-label="Quick actions"><a class="btn btn-ghost" href="tel:{TEL}">Call or text</a><a class="btn btn-primary" href="start.html">Start my project</a></nav>
<template id="bot-svg">{ROBOT}</template>
<script src="app.js" defer></script>
</body>
</html>'''
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(doc)

def head(eyebrow, h1, lede):
    return f'<section class="page-head blueprint"><div class="wrap"><span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="lede">{lede}</p></div></section>'

# --------------------------------------------------------------------------
TRADES = {
 "glass":{"label":"Glass","page":"websites-for-glass-shops.html","who":"glass shops","seo":"Websites for Glass Shops",
   "intro":"Windshield chips don't wait. When someone cracks a windshield on the highway, they search on their phone and call the first shop that looks legit and makes it easy to get a quote.",
   "problems":["Quote requests come in missing the year, make and model, so you play phone tag","Customers can't tell if you do auto glass, home glass, or both","Nothing on the site explains insurance claims, so people call the dealer instead","Your mobile service is buried or missing entirely"],
   "features":[("Windshield quote form","Asks for year, make, model and a photo of the damage, so you can quote on the first reply."),("Auto, home and commercial sections","Each kind of customer lands on the right page fast."),("Insurance claim help","A plain explanation of how claims work with you, which builds trust right away."),("Mobile service area","A map and town list that show exactly where you'll come to."),("Click-to-call everywhere","One tap from any page on a phone."),("Reviews up front","Your best Google reviews where people actually see them.")]},
 "auto":{"label":"Auto Repair","page":"websites-for-auto-repair-shops.html","who":"auto repair shops","seo":"Websites for Auto Repair Shops",
   "intro":"People pick a mechanic on trust. Your website should make your shop look as honest and organized as it is, and make booking easy.",
   "problems":["Customers can't see what you service or roughly what it costs","Appointment requests only come by phone, during your busiest hours","Your certifications and warranty aren't shown anywhere","Fleet customers have no idea you want their business"],
   "features":[("Service menu","Oil, brakes, diagnostics, tires, with optional starting prices."),("Appointment requests","Customers pick a day and describe the problem; you confirm."),("Makes and models serviced","Answers the first question every new customer has."),("Certification badges","Red Seal, warranty details and more, shown with pride."),("Fleet accounts page","A direct pitch to local businesses with work trucks."),("Seasonal specials","Tire changeovers and winter checks, easy to update.")]},
 "electrical":{"label":"Electrical","page":"websites-for-electricians.html","who":"electricians","seo":"Websites for Electricians",
   "intro":"Nobody hires an electrician they don't trust. Your site needs to show you're licensed, insured and reliable before the phone rings.",
   "problems":["No proof of licensing or insurance on the site","Big-ticket jobs like panel upgrades and EV chargers get lost in a long list","Emergency callers can't find a number fast","Commercial and residential customers see the same generic page"],
   "features":[("Licensed and insured badges","Trust signals right at the top of every page."),("Panel upgrade and EV charger pages","Dedicated pages for the jobs you want more of."),("Generator installs","Show off standby generators for farms, homes and shops."),("Emergency call button","Pinned and impossible to miss when the power's out."),("Residential vs. commercial","Clear paths for each type of customer."),("Project gallery","Clean, finished work that speaks for itself.")]},
 "plumbing":{"label":"Plumbing","page":"websites-for-plumbers.html","who":"plumbers","seo":"Websites for Plumbers",
   "intro":"When a pipe bursts at 2 a.m., people don't browse. They search, tap and call. Your site should get that call before the next plumber's does.",
   "problems":["Emergency number hidden in the footer","No clear list of the towns you cover","Water heater and drain jobs don't show up on Google","The site is slow and hard to use on a phone"],
   "features":[("24/7 emergency banner","A tap-to-call bar across the top of every page."),("Water heater pages","Repair and replacement pages built to show up in searches."),("Drains and sewer","Clear explanations that turn worried visitors into calls."),("Service area map","Every town you cover, listed and mapped."),("Quote form with photo upload","Customers can show you the problem before you drive out."),("Well and septic","A section for rural work, if you do it.")]},
 "hvac":{"label":"HVAC","page":"websites-for-hvac-companies.html","who":"HVAC companies","seo":"Websites for HVAC Companies",
   "intro":"HVAC work runs on seasons and repeat customers. Your website should fill the slow months and keep people coming back every year.",
   "problems":["Seasonal promos never make it onto the website","Maintenance plans aren't explained or sold online","Financing and rebates are a mystery to customers","Brand dealer status isn't shown, so you look like everyone else"],
   "features":[("Seasonal tune-up promos","Spring AC checks and fall furnace tune-ups, front and center."),("Maintenance plans","A clear page that turns one-time jobs into yearly customers."),("Financing and rebates","Makes bigger installs an easier yes."),("Dealer badges","Show the brands you're certified to install."),("Heating and cooling pages","Furnaces, AC and heat pumps, each with its own page."),("Booking requests","Customers request a time without calling.")]},
 "landscaping":{"label":"Landscaping","page":"websites-for-landscapers.html","who":"landscapers","seo":"Websites for Landscapers",
   "intro":"Landscaping sells with pictures. Your site should show off your best work in big, beautiful photos, and keep the phone busy in winter too.",
   "problems":["Tiny photo galleries that don't do your work justice","No before-and-after shots, your strongest selling tool","Snow removal isn't mentioned, so winter goes quiet","Design, install and maintenance customers all get the same pitch"],
   "features":[("Big photo galleries","Full-width photos that load fast on a phone."),("Before/after sliders","Drag the slider and watch the yard transform."),("Seasonal services","Spring cleanups, fall cleanups and everything between."),("Snow removal contracts","Year-round work from the same website."),("Design vs. maintenance","Separate paths for big projects and regular upkeep."),("Estimate form","Property size, project type and photos, all up front.")]},
}

# ------------------------------- HOME --------------------------------------
INCLUDES = [("phone","Looks great on phones","Most of your customers find you on a phone. Every page is built for small screens first."),
 ("bolt","Loads fast","Fast pages keep people from hitting the back button, and Google likes them too."),
 ("call","Click-to-call","One tap and their phone is dialing you. No copying numbers."),
 ("form","Quote and contact forms","Requests land in your email with everything you need to reply."),
 ("search","Shows up on Google","Set up from day one so search engines know who you are and where you work."),
 ("map","Built-in Google Maps","Your location or service area, right on the page.")]

def plan_cards(compact=False):
    return f'''<div class="plans">
<div class="card plan tilt reveal"><span class="tag">5 pages</span><h3>Core Website</h3>
<div class="price">$1,500 <small>one-time build</small></div>
<p class="muted">Everything a service business needs to look professional and get calls.</p>
<ul class="checks"><li>Home, Services, About, Gallery or Reviews, Contact and Quote</li><li>Contact and quote forms</li><li>Mobile-friendly, click-to-call</li><li>Google setup and Google Map</li><li>Live in about 2 weeks</li><li>Care plan included (hosting, updates, fixes), first 30 days free</li></ul>
<a class="btn btn-ghost" href="start.html?plan=core">Start with Core</a></div>
<div class="card plan popular tilt reveal"><span class="ribbon">Most popular</span><span class="tag">8 pages</span><h3>Complete Website</h3>
<div class="price">$1,997 <small>one-time build</small></div>
<p class="muted">Room to give your top services their own pages and show up in more searches.</p>
<ul class="checks"><li>Everything in Core Website</li><li>Separate pages for your top services</li><li>Service Areas, FAQ or Specials pages</li><li>Google Business Profile setup</li><li>A page for each town you serve</li><li>Care plan included (hosting, updates, fixes), first 30 days free</li></ul>
<a class="btn btn-primary" href="start.html?plan=complete">Start with Complete</a></div>
</div>'''

CARE = '''<div class="card care reveal">
<div><span class="eyebrow">Care plan · included with every build</span><h2 style="font-size:clamp(1.8rem,3.6vw,2.6rem)">Your website, built and looked after.</h2>
<p class="muted">You run your business. I keep your site online, up to date and working. Just text or email me what you need changed.</p>
<p><b>Your first 30 days after launch are free.</b> Billing starts once your site has been live for 30 days.</p>
<ul class="pill-list"><li>Hosting</li><li>Text changes</li><li>Adding promotions</li><li>Updating hours</li><li>Swapping photos</li><li>Fixing anything that breaks</li></ul></div>
<div><div data-promo><span class="strike">$147/mo</span><span class="care-price">$99/mo</span>
<p style="margin-top:10px">Locked in for life when your build invoice is paid by <b>Dec 31, 2026</b>.</p>
<span class="countdown">⏳ <span data-countdown>days left</span></span></div>
<div data-nopromo><span class="care-price">$147/mo</span><p style="margin-top:10px">Hosting, updates and fixes, all handled.</p></div></div>
</div>'''

FAQ_TOP = [
 ("Do I own my website?","Yes. Once your build is paid, the finished site is yours, and so is your domain name, your logo, photos and text. If you ever leave, you can take it with you."),
 ("How long does it take?","About 2 weeks from the day your project form and payment come in. If I'm waiting on photos or info from you, the clock pauses until it arrives."),
 ("Is hosting included?","Yes. Hosting is part of the care plan that comes with every site, along with updates and fixes. You won't get a separate hosting bill."),
 ("What do I need to provide?","Your business info, your logo if you have one, and photos of your work. The project form walks you through it. Anything you're not sure about, we'll figure out together."),
]
FAQ_MORE = [
 ("What if I don't have a logo or photos?","No problem. I can use clean text-based branding to start, and fill gaps with good-quality stock photos that fit your trade. A simple logo can be added for an extra fee."),
 ("Can I change things later?","Yes. That's what the care plan is for. Text me a new price, new hours or a new promo and it gets done, usually within a few business days."),
 ("What are the payment terms?","The build is paid in full up front, before work starts. The care plan is billed monthly, and your first 30 days after launch are free, so the first charge comes 30 days after your site goes live. Prices are in Canadian dollars."),
 ("Why is the care plan included?","Because a website isn't a one-time thing. It needs hosting, updates and the odd fix. Including it means you never have to worry about any of that, and you always have someone to call."),
 ("Can I upgrade from 5 to 8 pages?","Yes. You can start with Core Website and move up to Complete Website later. You just pay the difference for the extra pages."),
 ("What counts as a page?","A page is one item in your site's menu, like Home, Services or Contact. Thank-you pages, the privacy policy and forms don't count."),
 ("What happens if I cancel the care plan?","Give 30 days' notice and your site stays live through your last paid month. After that, hosting ends. For a one-time $200 fee I'll hand over your site files and transfer your domain to you or your new provider. Any later work is quoted separately, $200 minimum."),
 ("How does the $99/mo promo work?","Pay your build invoice by December 31, 2026 and your care plan is $99 a month instead of $147, locked in for as long as you keep it. If you cancel and come back later, the regular rate applies."),
 ("Do you only work in the Peace region?","The Peace region is home, and I love working with local businesses. But everything can be done by phone, text and email, so I build for businesses anywhere in Canada."),
]
def faq_html(items):
    return "".join(f'<details class="reveal"><summary>{e(q)}</summary><div><p>{e(a)}</p></div></details>' for q, a in items)

def mock(href, title, sub, color, tag, real=False, ext=False):
    tgt = ' target="_blank" rel="noopener"' if ext else ""
    return f'''<a class="mock reveal" href="{href}"{tgt}><div class="mock-screen"><div class="mock-top" style="background:linear-gradient(135deg,{color},#111)">{e(title)}</div>
<div class="mock-body"><i style="width:80%"></i><i style="width:60%"></i><i style="width:70%"></i></div></div>
<div class="mock-meta"><span class="tag{' real' if real else ''}">{tag}</span><h3>{e(title)}</h3><p class="muted" style="margin:0">{e(sub)}</p></div></a>'''

home = f'''
<section class="hero blueprint"><div class="sparks" aria-hidden="true"></div><div class="hero-glow" aria-hidden="true"></div>
<div class="wrap hero-grid">
<div><span class="eyebrow">Websites for the trades</span>
<h1>Websites built to work <span class="accent">as hard as you do.</span></h1>
<p class="lede">Fast, good-looking websites for glass shops, auto repair, electricians, plumbers, HVAC and landscapers. Fixed prices. No tech headaches.</p>
<div class="btn-row"><a class="btn btn-primary" href="start.html">Start my project</a><a class="btn btn-ghost" href="work.html">See sample sites</a></div>
<div class="hero-stats"><div class="stat"><b data-count="2" data-pre="~" data-suf=" wks">~2 wks</b><span>from form to launch</span></div>
<div class="stat"><b data-count="1500" data-pre="$">$1,500</b><span>fixed-price builds from</span></div>
<div class="stat"><b data-count="1" data-suf=" person">1 person</b><span>who builds it and looks after it</span></div></div></div>
<div class="hero-art" aria-hidden="true"><div style="width:min(340px,80%);filter:drop-shadow(0 30px 40px rgba(255,107,26,.25))">{ROBOT.replace('class="bot"','class="bot" style="width:100%;height:auto"')}</div></div>
</div></section>

<section class="section" data-bot-say="Pick a trade and watch me build it!"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">See it for yourself</span><h2>What kind of business do you run?</h2>
<p class="lede">Tap your trade. The sample site below rebuilds itself for that business, right here on the page.</p></div>
<div class="picker reveal" id="picker" aria-label="Choose a trade"></div>
<div class="preview reveal" id="preview" aria-live="polite"></div>
<div class="picker-foot"><span class="muted">Sample concept for a made-up business.</span><span class="btn-row"><a class="btn btn-ghost" id="trade-link" href="industries.html">Websites for your trade</a><a class="btn btn-primary" id="preview-link" href="sample.html">Open the full sample</a></span></div>
</div></section>

<div class="rivets" aria-hidden="true"></div>

<section class="section"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">Every site includes</span><h2>The stuff that actually gets you calls.</h2></div>
<div class="grid g3">{"".join(f'<div class="card tilt reveal"><div class="icon">{ICON[i]}</div><h3>{t}</h3><p class="muted">{d}</p></div>' for i,t,d in INCLUDES)}</div>
</div></section>

<section class="section light"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">Real work and samples</span><h2>Built, not just talked about.</h2>
<p class="lede">Real client sites, plus working sample sites for each trade. Click any of them to look around.</p></div>
<div class="grid g3">
{mock("https://elitewindshields.ca","Elite Windshields","A glass shop site built to bring in windshield quotes.","#0f3b57","Client site",True,True)}
{mock("https://worsleybaptistchurch.ca","Worsley Baptist Church","A clean, welcoming site for a rural church.","#3a2a1a","Client site",True,True)}
{mock("sample.html?t=plumbing","Summit Plumbing & Drain","Emergency call banner and service area map.","#0c2d48","Sample concept")}
</div>
<p style="margin-top:28px"><a class="btn btn-primary" href="work.html">See all sample work</a></p>
</div></section>

<section class="section"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">How it works</span><h2>Four steps. About two weeks.</h2></div>
<div class="steps">
<div class="card step reveal"><h3>Fill out the project form</h3><p class="muted">About 15 minutes. It asks for everything I need, so there's no back-and-forth.</p></div>
<div class="card step reveal"><h3>Pay the build invoice</h3><p class="muted">One fixed price, paid up front. That starts the clock.</p></div>
<div class="card step reveal"><h3>I build it</h3><p class="muted">You get a private preview link to look over and send changes.</p></div>
<div class="card step reveal"><h3>You approve, we launch</h3><p class="muted">Your site goes live, and the care plan keeps it running.</p></div>
</div>
<p style="margin-top:26px"><a href="how-it-works.html">The full process, step by step →</a></p>
</div></section>

<section class="section blueprint" data-bot-say="Questions about the care plan? Click me."><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">Pricing</span><h2>Two fixed prices. No surprises.</h2>
<p class="lede">No "call for a quote" games. Pick 5 pages or 8, and every build comes with the care plan.</p></div>
{plan_cards()}
<div style="margin-top:22px">{CARE}</div>
<p style="margin-top:22px"><a class="btn btn-ghost" href="pricing.html">Full pricing details</a></p>
</div></section>

<section class="section"><div class="wrap split">
<div class="reveal"><span class="eyebrow">Why Foundry Systems</span><h2>One local person. Start to finish.</h2>
<p class="lede">No agency, no account managers, no call centre. I build your site myself and I'm the one who answers when you need a change.</p>
<ul class="checks"><li>Fixed prices, written down before we start</li><li>Live in about 2 weeks</li><li>Based in the Peace region</li><li>You own your site and your domain</li></ul>
<a class="btn btn-ghost" href="about.html">About Craig</a></div>
<div class="reveal"><blockquote class="quote">"Talk to the person who actually builds your site."</blockquote>
<p class="muted" style="margin-top:14px">Call or text <a href="tel:{TEL}">{PHONE}</a>. I reply to every call, text and form within one business day.</p></div>
</div></section>

<section class="section light"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">Common questions</span><h2>Straight answers.</h2></div>
{faq_html(FAQ_TOP)}
<p style="margin-top:20px"><a href="faq.html">All questions →</a></p>
</div></section>
'''
page("index.html", "Foundry Systems | Websites for Trades and Service Businesses",
     "Fixed-price websites for glass shops, auto repair, electricians, plumbers, HVAC and landscapers. Live in about 2 weeks. Based in the Peace region.",
     home, "index.html")

# ------------------------------- PRICING -----------------------------------
pricing = head("Pricing", "Fixed prices. Written down.", "Two website builds, one care plan that comes with both, and a 2026 special that's hard to beat. All prices in Canadian dollars.") + f'''
<section class="section"><div class="wrap">{plan_cards()}</div></section>
<section class="section-tight" data-bot-say="The $99/mo rate is locked in for life. Not bad!"><div class="wrap">{CARE}</div></section>
<section class="section"><div class="wrap">
<div class="card reveal"><span class="eyebrow">Price calculator</span><h3>What will it cost me?</h3>
<div class="calc" id="calc"><div class="seg" role="group" aria-label="Number of pages"><button type="button" data-plan="core" aria-pressed="false">5 pages</button><button type="button" data-plan="complete" aria-pressed="true">8 pages</button></div>
<div class="calc-out" id="calc-out" aria-live="polite">$1,997 today, then $99/mo for life</div>
<a class="btn btn-primary" id="calc-go" href="start.html?plan=complete">Start with this plan</a></div>
<p class="muted" style="margin:14px 0 0">Care plan billing starts 30 days after your site goes live.</p></div>
</div></section>
<section class="section light"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">Side by side</span><h2>Compare the plans</h2></div>
<div class="table-scroll reveal"><table class="compare" style="color:var(--ink)">
<thead><tr><th></th><th>Core Website</th><th>Complete Website <span class="tag">Most popular</span></th></tr></thead>
<tbody>
<tr><td><b>Build price</b></td><td>$1,500, paid up front</td><td>$1,997, paid up front</td></tr>
<tr><td><b>Pages</b></td><td>5</td><td>8</td></tr>
<tr><td><b>Typical pages</b></td><td>Home, Services, About, Gallery or Reviews, Contact and Quote</td><td>Everything in Core Website, plus separate pages for top services, Service Areas, FAQ or Specials</td></tr>
<tr><td><b>Care plan</b> (hosting, updates, fixes)</td><td>Included, first 30 days free: <span data-promo>$99/mo for life (2026 special), then </span>$147/mo</td><td>Same</td></tr>
<tr><td><b>Launch</b></td><td>About 2 weeks from project form</td><td>About 2 weeks from project form</td></tr>
<tr><td><b>Contact and quote forms, mobile-friendly, click-to-call</b></td><td>Yes</td><td>Yes</td></tr>
<tr><td><b>Extras</b></td><td>–</td><td>Google Business Profile setup, and a page for each town served</td></tr>
</tbody></table></div>
</div></section>
<section class="section"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">Add-ons</span><h2>Need a little more?</h2><p class="lede">Optional extras, quoted up front before any work starts.</p></div>
<div class="grid g3">
{"".join(f'<div class="card reveal"><h3>{t}</h3><p class="muted">{d}</p></div>' for t,d in [("Extra page","Need one more page than your plan includes? Easy."),("Logo design","A simple, clean logo if you don't have one yet."),("Google Business Profile setup","Get found on Google Maps and start collecting reviews."),("Business email setup","An email address at your own domain, like you@yourbusiness.ca."),("Copywriting","I write the words for your pages so you don't have to."),("French or Spanish version","Reach more customers in their own language.")])}
</div></div></section>
<section class="section light"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">Pricing questions</span><h2>The fine print, in plain English.</h2></div>
{faq_html([FAQ_MORE[2], FAQ_MORE[5], FAQ_MORE[3], FAQ_MORE[6], FAQ_MORE[4], FAQ_MORE[7]])}
</div></section>'''
page("pricing.html", "Pricing | Foundry Systems", "Core Website $1,500 (5 pages) or Complete Website $1,997 (8 pages). Care plan included: $99/mo for life when paid by Dec 31, 2026.", pricing, "pricing.html",
     bot_hello="Prices right here. No surprises.")

# ------------------------------- WORK --------------------------------------
work = head("Sample work", "Real sites. Working samples.", "Real client work comes first. Below that are working sample sites for each trade, so you can see what yours could look like.") + f'''
<section class="section"><div class="wrap">
<div class="split reveal">
<div><span class="tag real">Client site · Glass</span><h2>Elite Windshields</h2>
<p class="lede">A glass shop, just like the businesses I build for.</p>
<p><b>What they needed:</b> a professional site that makes it quick for drivers to request a windshield quote and call the shop.</p>
<p><b>What was built:</b> a fast, mobile-first site with clear service pages, click-to-call and a quote form that gets the details up front.</p>
<p class="muted"><i>Owner's quote coming soon.</i></p>
<a class="btn btn-primary" href="https://elitewindshields.ca" target="_blank" rel="noopener">Visit EliteWindshields.ca</a></div>
<div>{mock("https://elitewindshields.ca","Elite Windshields","Live client site","#0f3b57","Client site",True,True)}</div>
</div></div></section>
<div class="rivets"></div>
<section class="section"><div class="wrap split reveal">
<div>{mock("https://worsleybaptistchurch.ca","Worsley Baptist Church","Live client site","#3a2a1a","Client site",True,True)}</div>
<div><span class="tag real">Client site · Community</span><h2>Worsley Baptist Church</h2>
<p class="lede">Proof the same care works beyond the trades.</p>
<p>A warm, simple site with service times, events and a clear "New here?" path for visitors.</p>
<a class="btn btn-primary" href="https://worsleybaptistchurch.ca" target="_blank" rel="noopener">Visit WorsleyBaptistChurch.ca</a></div>
</div></section>
<section class="section light"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">Sample concepts</span><h2>A working sample for every trade.</h2>
<p class="lede">These are made-up businesses, built to show what's possible. Real client projects will replace them as they come in.</p></div>
<div class="grid g3">
{mock("sample.html?t=glass","Clearview Glass & Windshield","Shows off: windshield quote form with vehicle info","#0f3b57","Sample concept")}
{mock("sample.html?t=auto","Northline Auto Repair","Shows off: service menu and appointment requests","#1f2a1f","Sample concept")}
{mock("sample.html?t=electrical","Brightwire Electric","Shows off: licensed and insured badges, emergency calls","#1d1f3a","Sample concept")}
{mock("sample.html?t=plumbing","Summit Plumbing & Drain","Shows off: 24/7 emergency call banner","#0c2d48","Sample concept")}
{mock("sample.html?t=hvac","Aurora Heating & Air","Shows off: seasonal specials and maintenance plans","#2a1a12","Sample concept")}
{mock("sample.html?t=landscaping","Riverbend Landscaping","Shows off: before/after slider and big galleries","#1e3a24","Sample concept")}
</div></div></section>
<section class="section"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">Before and after</span><h2>Drag the slider.</h2><p class="lede">An outdated trade website on the left, a Foundry Systems redesign on the right.</p></div>
<div class="ba reveal"><div class="before old-site"><h4>Welcome to Bob's Plumbing!!!</h4><p class="blink-old">*** NOW SERVING THE AREA ***</p><p>We do plumbing. Call us. Click <u>here</u> for our services page (under construction).</p><p>Phone number on the contact page. Best viewed in Internet Explorer.</p><p>Visitors: 004231</p></div>
<div class="after new-site"><h4>Leaks fixed fast.</h4><p>Licensed plumbers, 24/7 emergency service, serving the whole region.</p><span class="b">Call now</span> <span class="b" style="background:transparent;border:2px solid #fff;color:#fff">Get a quote</span></div>
<input type="range" min="0" max="100" value="50" aria-label="Compare old and new website"><span class="handle"></span></div>
</div></section>'''
page("work.html", "Sample Work | Foundry Systems", "Real client websites and working sample sites for glass shops, auto repair, electricians, plumbers, HVAC and landscapers.", work, "work.html",
     bot_hello="These are real working demos. Click around!")

# ------------------------------- SAMPLE ------------------------------------
sample = '<section class="section-tight"><div class="wrap"><span class="eyebrow">Sample concept</span><h1 style="font-size:clamp(2rem,5vw,3.4rem)">Sample site</h1><div id="sample-root"></div></div></section>'
page("sample.html", "Sample Site | Foundry Systems", "A working sample website for a made-up trade business, built by Foundry Systems.", sample, "work.html",
     extra_head='<meta name="robots" content="noindex">')

# ------------------------------- INDUSTRIES --------------------------------
ind = head("Industries", "Built for the trades.", "Each trade has its own customers, its own questions and its own busy season. Your website should speak your language.") + f'''
<section class="section"><div class="wrap"><div class="grid g3">
{"".join(f'<a class="card tilt reveal" href="{t["page"]}" style="text-decoration:none;color:inherit"><div class="icon">{ICON[k]}</div><h3>{t["label"]}</h3><p class="muted">{e(t["intro"].split(".")[0])}.</p><span style="color:var(--orange);font-weight:700">Websites for {t["who"]} →</span></a>' for k,t in TRADES.items())}
</div>
<p class="muted" style="margin-top:28px">Run a different kind of service business? I build for those too. <a href="contact.html">Ask me about yours.</a></p>
</div></section>'''
page("industries.html", "Industries | Foundry Systems", "Websites for glass shops, auto repair shops, electricians, plumbers, HVAC companies and landscapers.", ind, "industries.html")

for k, t in TRADES.items():
    body = head(t["label"], t["seo"] + ".", t["intro"]) + f'''
<section class="section"><div class="wrap split">
<div class="reveal"><span class="eyebrow">Sound familiar?</span><h2>Common website problems for {t["who"]}</h2>
<ul class="checks">{"".join(f"<li>{e(p)}</li>" for p in t["problems"])}</ul></div>
<div class="card reveal"><span class="tag">Sample concept</span><h3>See a {t["label"].lower()} site in action</h3><p class="muted">A working sample site for a made-up {t["label"].lower()} business. Click around and picture your name on it.</p>
<a class="btn btn-primary" href="sample.html?t={k}">Open the sample site</a></div>
</div></section>
<section class="section light"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">Built in</span><h2>Features made for {t["who"]}</h2></div>
<div class="grid g3">{"".join(f'<div class="card reveal"><div class="icon">{ICON[k]}</div><h3>{e(a)}</h3><p class="muted">{e(b)}</p></div>' for a,b in t["features"])}</div>
</div></section>
<section class="section"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">Pricing</span><h2>Same fixed prices for every trade.</h2></div>
{plan_cards()}
<p style="margin-top:24px"><a class="btn btn-primary" href="start.html?trade={k}">Start my {t["label"].lower()} website</a></p>
</div></section>'''
    page(t["page"], f'{t["seo"]} | Foundry Systems', f'Fast, fixed-price websites for {t["who"]}. ' + t["intro"].split(".")[0] + ".", body, "industries.html",
         bot_hello=f"Want to see a {t['label'].lower()} site? Scroll down!")

# ------------------------------- HOW IT WORKS ------------------------------
hiw_steps = [
 ("Fill out the project form","About 15 to 20 minutes","The form asks one topic at a time: your business, services, hours, photos, the look you want. Anything you're not sure about, skip it and we'll talk it through. Your answers save as you go."),
 ("Pay the build invoice","Same day","After you send the form, you'll get your build invoice. The build is paid in full up front, and that's when the 2-week clock starts."),
 ("Quick kickoff call","Within 1 to 2 business days","A short call to go over your answers, fill any gaps and make sure we're on the same page."),
 ("I build your site","About 1 week","I design and build your pages, write or polish the text, and set up your forms, maps and Google info."),
 ("You review a preview","A few days","You get a private preview link. Look it over on your phone, send your changes, and I'll make them."),
 ("Launch day","Around the 2-week mark","Once you approve, your site goes live on your domain with a secure connection. Your phone starts ringing."),
 ("After launch: the care plan","Ongoing","First 30 days free, then billed monthly. Hosting, text changes, new promos, updated hours, new photos and fixes. Just text or email me."),
]
hiw = head("How it works", "Form to launch in about 2 weeks.", "A clear process with no surprises. Here's exactly what happens, how long it takes, and what you'll need.") + f'''
<section class="section"><div class="wrap"><div class="grid" style="max-width:860px">
{"".join(f'<div class="card reveal" style="display:grid;grid-template-columns:64px 1fr;gap:18px"><div style="font:800 2.6rem/1 var(--head);color:var(--orange)">{i+1:02d}</div><div><h3>{e(a)}</h3><p style="color:var(--ember);font-weight:700;font-size:.92rem;margin-bottom:.4em">{e(b)}</p><p class="muted" style="margin:0">{e(c)}</p></div></div>' for i,(a,b,c) in enumerate(hiw_steps))}
</div></div></section>
<section class="section light"><div class="wrap split">
<div class="reveal"><span class="eyebrow">Have these ready</span><h2>What you'll need</h2><p class="lede">Don't have all of it? That's fine. The form lets you skip anything and we'll sort it out together.</p></div>
<ul class="checks reveal"><li>Your logo, if you have one</li><li>Photos of your work, team, trucks or shop</li><li>Your list of services</li><li>Hours and the towns you serve</li><li>Any reviews you'd like to show</li><li>Your domain login, if you already own one</li></ul>
</div></section>'''
page("how-it-works.html", "How It Works | Foundry Systems", "From project form to launch in about 2 weeks. Here's every step, what it takes and what happens after launch.", hiw, "how-it-works.html")

# ------------------------------- ABOUT -------------------------------------
about = head("About", "Hi, I'm Craig.", "I build websites for the people who keep things running: the glass shops, mechanics, electricians, plumbers, HVAC techs and landscapers.") + f'''
<section class="section"><div class="wrap split">
<div class="photo-frame reveal"><div><div style="width:120px;margin:0 auto 12px">{ROBOT.replace('class="bot"','class="bot" style="width:100%;height:auto"')}</div><b>Photo of Craig goes here</b><br><span class="muted">Swap in a real photo before launch</span></div></div>
<div class="reveal">
<p class="lede">Foundry Systems is me, Craig Donnelly, based in Alberta's Peace region.</p>
<p>I started building websites for local businesses because I kept seeing the same thing: great tradespeople with websites that were slow, outdated or missing altogether. Meanwhile, customers were searching on their phones and calling whoever looked the most put-together.</p>
<p>So I keep it simple. Two fixed prices. A site that looks sharp and works on a phone. Live in about two weeks. And after launch, I'm still the one looking after it. No agency, no ticket system, no runaround.</p>
<p>I work with businesses across the Peace region, and anywhere else in Canada by phone, text and email.</p>
<ul class="checks"><li>Peace region based, builds for businesses anywhere</li><li>Fixed prices, paid once, no surprise bills</li><li>One person from start to finish</li></ul>
<h3 style="margin-top:24px">Talk to the person who actually builds your site.</h3>
<div class="btn-row"><a class="btn btn-primary" href="tel:{TEL}">Call or text {PHONE}</a><a class="btn btn-ghost" href="contact.html">Send a message</a></div>
</div></div></section>'''
page("about.html", "About Craig | Foundry Systems", "Foundry Systems is Craig Donnelly, a website builder based in Alberta's Peace region who builds and looks after websites for trades and service businesses.", about, "about.html")

# ------------------------------- FAQ ---------------------------------------
faq = head("FAQ", "Questions, answered.", "Can't find yours? Call or text " + PHONE + " or send a quick message.") + f'''
<section class="section"><div class="wrap" style="max-width:880px">{faq_html(FAQ_TOP + FAQ_MORE)}</div></section>'''
faq_schema = '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ_TOP+FAQ_MORE]}) + '</script>'
page("faq.html", "FAQ | Foundry Systems", "Answers about owning your website, hosting, timelines, payment terms, the care plan and the 2026 promo.", faq, "faq.html", extra_head=faq_schema)

# ------------------------------- CONTACT -----------------------------------
TRADE_OPTS = ["Glass","Auto repair","Electrical","Plumbing","HVAC","Landscaping","Other"]
hidden = lambda subj, nxt: (f'<input type="hidden" name="_subject" value="{e(subj)}"><input type="hidden" name="_template" value="table">'
        f'<input type="hidden" name="_captcha" value="false"><input type="hidden" name="_next" value="{nxt}">'
        '<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">')
contact = head("Contact", "Got a question? Ask away.", "Not ready for the full project form? No problem. This takes under a minute.") + f'''
<section class="section"><div class="wrap split" style="align-items:start">
<form class="form form-card reveal" id="contact-form" action="{FORM_ACTION}" method="POST">
{hidden("New question from the Foundry Systems website", "thanks.html?form=contact")}
<div class="row2"><div class="field"><label for="c-name">Your name *</label><input id="c-name" type="text" name="name" required autocomplete="name"></div>
<div class="field"><label for="c-biz">Business name</label><input id="c-biz" type="text" name="business" autocomplete="organization"></div></div>
<div class="field"><label for="c-type">Type of business</label><select id="c-type" name="type of business"><option value="">Choose one</option>{"".join(f"<option>{o}</option>" for o in TRADE_OPTS)}</select></div>
<div class="row2"><div class="field"><label for="c-phone">Phone</label><input id="c-phone" type="tel" name="phone" autocomplete="tel"></div>
<div class="field"><label for="c-email">Email</label><input id="c-email" type="email" name="email" autocomplete="email"></div></div>
<p class="hint muted" style="margin:-8px 0 0;font-size:.88rem">Phone or email is required, whichever you prefer.</p>
<fieldset class="field"><legend>Best way to reach you</legend><div class="choices">{"".join(f'<label class="choice"><input type="radio" name="best way to reach" value="{o}"><span>{o}</span></label>' for o in ["Call","Text","Email"])}</div></fieldset>
<div class="field"><label for="c-msg">What can I help with? *</label><textarea id="c-msg" name="message" required></textarea></div>
<div class="error" id="contact-err" role="alert"></div>
<button class="btn btn-primary" type="submit">Send my question</button>
</form>
<div class="reveal">
<div class="card"><h3>Call or text</h3><p><a href="tel:{TEL}" style="font:800 2rem/1 var(--head)">{PHONE}</a></p>
<h3>Email</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<h3>Where</h3><p class="muted">Serving the Peace region and beyond.</p>
<p class="notice">I reply to every call, text and form within one business day.</p></div>
<div class="card" style="margin-top:16px"><h3>Ready to go?</h3><p class="muted">The project form collects everything I need to build your site.</p><a class="btn btn-primary" href="start.html">Start my project</a></div>
</div></div></section>'''
page("contact.html", "Contact | Foundry Systems", "Call or text 780-834-8078, email craig.foundrysystems@gmail.com, or send a quick question. Replies within one business day.", contact, None, cta=False)

# ------------------------------- CHECKUP -----------------------------------
checkup = head("Free website checkup", "Send me your site. Get 3 fixes back.", "No pressure, no sales pitch. I'll look over your current website and send back three things that would bring in more calls.") + f'''
<section class="section"><div class="wrap" style="max-width:720px">
<form class="form form-card reveal" id="checkup-form" action="{FORM_ACTION}" method="POST">
{hidden("Free website checkup request", "thanks.html?form=checkup")}
<div class="field"><label for="k-url">Your current website *</label><input id="k-url" type="url" name="website" placeholder="https://" required></div>
<div class="row2"><div class="field"><label for="k-name">Your name *</label><input id="k-name" type="text" name="name" required autocomplete="name"></div>
<div class="field"><label for="k-email">Email *</label><input id="k-email" type="email" name="email" required autocomplete="email"></div></div>
<div class="field"><label for="k-type">Type of business</label><select id="k-type" name="type of business"><option value="">Choose one</option>{"".join(f"<option>{o}</option>" for o in TRADE_OPTS)}</select></div>
<button class="btn btn-primary" type="submit">Send me my checkup</button>
</form></div></section>'''
page("checkup.html", "Free Website Checkup | Foundry Systems", "Send your current website and get back three practical fixes to bring in more calls. Free.", checkup, None)

# ------------------------------- START (INTAKE) ----------------------------
def radios(name, opts, req=False):
    return '<div class="choices">' + "".join(f'<label class="choice"><input type="radio" name="{e(name)}" value="{e(o)}"{" required" if req and i==0 else ""}><span>{e(o)}</span></label>' for i,o in enumerate(opts)) + '</div>'
def checks(name, opts):
    return '<div class="choices">' + "".join(f'<label class="choice"><input type="checkbox" name="{e(name)}" value="{e(o)}"><span>{e(o)}</span></label>' for o in opts) + '</div>'
def fld(label, name, kind="text", req=False, hint="", ph="", fid=None):
    fid = fid or "f-" + "".join(c if c.isalnum() else "-" for c in name.lower())[:40]
    h = f'<span class="hint">{hint}</span>' if hint else ""
    r = " required" if req else ""
    if kind == "area":
        inp = f'<textarea id="{fid}" name="{e(name)}"{r} placeholder="{e(ph)}"></textarea>'
    else:
        inp = f'<input id="{fid}" type="{kind}" name="{e(name)}"{r} placeholder="{e(ph)}">'
    return f'<div class="field"><label for="{fid}">{e(label)}{" *" if req else ""}{h}</label>{inp}</div>'
NS = '<p class="notsure">Not sure? Leave it blank. We\'ll talk it through on the kickoff call.</p>'
days_ = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
TRADE_Q = {
 "Glass": checks("Glass: work you do", ["Auto glass","Home glass","Commercial glass"]) + checks("Glass: extras", ["Mobile service","Insurance claim help"]) + fld("Insurance companies you work with","Glass: insurance companies"),
 "Auto repair": fld("Makes and models you service","Auto: makes serviced", ph="All makes, or Ford/GM/Dodge, diesel, etc.") + checks("Auto: extras", ["Diagnostics","Fleet accounts","Loaner or shuttle"]),
 "Electrical": checks("Electrical: customers", ["Residential","Commercial","Farm / agricultural"]) + checks("Electrical: specialties", ["Panel upgrades","EV chargers","Generators","Emergency calls"]),
 "Plumbing": checks("Plumbing: services", ["24/7 emergency","Water heaters","Drains and sewer","Well and septic"]),
 "HVAC": fld("Brands you install","HVAC: brands", ph="Carrier, Lennox, Goodman…") + checks("HVAC: extras", ["Maintenance plans","Financing","Rebates help"]),
 "Landscaping": checks("Landscaping: work you do", ["Design and install","Ongoing upkeep","Hardscaping","Snow removal","Seasonal cleanups"]),
}
steps = []
steps.append(("You and your business", f'''
<div class="row2">{fld("Your name","Name",req=True)}{fld("Your role","Role",ph="Owner, manager…")}</div>
<div class="row2">{fld("Phone","Phone","tel",req=True)}{fld("Email","Email","email",req=True)}</div>
{fld("Best time to reach you","Best time to reach",ph="Mornings, after 5, anytime…")}
<div class="row2">{fld("Business name, as customers know it","Business name",req=True)}{fld("Legal name, if different","Legal business name")}</div>
<fieldset class="field"><legend>Type of business *</legend>{radios("Type of business", ["Glass","Auto repair","Electrical","Plumbing","HVAC","Landscaping","Other"], True)}</fieldset>
<div id="other-trade" hidden>{fld("What kind of business?","Other business type")}</div>
<div class="row2">{fld("Years in business","Years in business","number",hint="Used for \u201cServing the area since\u2026\u201d")}{fld("License numbers","License numbers",hint="Shown as trust badges")}</div>
<fieldset class="field"><legend>Insurance</legend>{checks("Insurance", ["Insured","Bonded"])}</fieldset>'''))
steps.append(("Plan and timing", f'''
<div class="field"><label for="f-plan">Which plan?</label><select id="f-plan" name="plan"><option value="Complete Website (8 pages, $1,997)">Complete Website: 8 pages, $1,997</option><option value="Core Website (5 pages, $1,500)">Core Website: 5 pages, $1,500</option><option value="Not sure yet">Not sure yet</option></select></div>
<div class="card" style="background:var(--charcoal)"><h3>Care plan included</h3><p class="muted">Hosting, updates and fixes come with every build.</p>
<p data-promo><b style="color:var(--orange)">$99/mo locked in for life</b> when your build invoice is paid by Dec 31, 2026 (normally $147/mo).</p>
<p data-nopromo><b>$147/mo</b>, starting 30 days after your site goes live.</p>
<p data-promo class="muted">Your first 30 days after launch are free.</p>
<label class="choice"><input type="checkbox" name="Care plan acknowledged" value="Yes" required><span>I understand the care plan is included and billed monthly, starting 30 days after my site goes live</span></label></div>
{fld("Ideal launch date","Ideal launch date","date")}
{fld("Why that date?","Launch date reason",ph="Before spring busy season, grand opening…")}'''))
steps.append(("Location, service area and hours", f'''
{fld("Business address","Business address")}
<fieldset class="field"><legend>Show the address on the website?</legend>{radios("Show address", ["Yes, show it","No, keep it private"])}</fieldset>
<fieldset class="field"><legend>Do customers come to you, or do you go to them?</legend>{radios("Customer location", ["They come to my shop","I go to them","Both"])}</fieldset>
{fld("Towns or areas you serve","Service area","area",ph="Fairview, Grande Prairie, Peace River… or a 100 km radius")}
<fieldset class="field"><legend>Hours</legend><div class="hours">{"".join(f'<label for="h-{d}">{d}</label><input id="h-{d}" type="text" name="Hours {d}" placeholder="8–5, closed, by appointment…">' for d in days_)}</div></fieldset>
{fld("Holiday hours","Holiday hours")}
<fieldset class="field"><legend>Emergency or after-hours service?</legend>{radios("After-hours service", ["Yes","No"])}</fieldset>
{fld("Emergency number, if different","Emergency number","tel")}{NS}'''))
steps.append(("Services", f'''
<div class="field"><label>Your services<span class="hint">Name, a sentence or two, and a starting price if you'd like to show one.</span></label>
<div id="svc-rows"><div class="svc-row"><input type="text" name="Service 1 name" placeholder="Service name" aria-label="Service name"><input type="text" name="Service 1 description" placeholder="A sentence or two" aria-label="Service description"><input type="text" name="Service 1 starting price" placeholder="From $" aria-label="Starting price (optional)"><span></span></div></div>
<button type="button" class="btn btn-ghost" id="add-svc" style="margin-top:6px">+ Add another service</button></div>
{fld("Top 3 services you want more of","Top 3 services","area",hint="These get the spotlight.")}
{fld("Jobs you don't take","Jobs not taken",hint="Keeps the wrong calls away.")}
{fld("Brands, certifications, dealer status","Certifications",ph="Red Seal, Carrier dealer…")}
{fld("Warranties or guarantees","Warranties")}
<fieldset class="field"><legend>Do you offer…</legend>{checks("Offers", ["Free estimates","Financing","Insurance claims"])}</fieldset>
{fld("Current specials or coupons","Specials")}
{"".join(f'<div data-trade="{k}" hidden><fieldset class="field"><legend>A few {k.lower()} questions</legend>{v}</fieldset></div>' for k,v in TRADE_Q.items())}{NS}'''))
steps.append(("Pages", '''
<p class="muted">Pick the pages you want. The list matches your trade, and it's limited to the number of pages in your plan.</p>
<div class="choices" id="page-list"></div>
<p id="page-limit" class="saved-note" aria-live="polite"></p>
''' + fld("Any custom page you want?","Custom page")))
steps.append(("Look and feel", f'''
<div class="field"><label for="f-logo">Logo upload<span class="hint">SVG or a large PNG is best.</span></label><input id="f-logo" type="file" name="attachment" accept="image/*,.svg,.pdf,.ai,.eps"></div>
<fieldset class="field"><legend>No logo?</legend>{checks("Logo", ["I need a logo (add-on)"])}</fieldset>
<fieldset class="field"><legend>Brand colours</legend>{radios("Colours", ["Match my logo","You choose","I'll pick them"])}</fieldset>
<div class="row2"><div class="field"><label for="f-c1">Main colour</label><input id="f-c1" type="color" name="Main colour" value="#0c2d48" style="height:52px;width:100%;padding:4px"></div><div class="field"><label for="f-c2">Accent colour</label><input id="f-c2" type="color" name="Accent colour" value="#ff6b1a" style="height:52px;width:100%;padding:4px"></div></div>
<div class="field"><label for="f-wrap">Photos of truck wraps, signs or uniforms<span class="hint">So the site matches what customers already see.</span></label><input id="f-wrap" type="file" name="attachment" accept="image/*" multiple></div>
{fld("Websites you like, and what you like about them","Sites liked","area",hint="Up to three links.")}
{fld("Websites you don't like","Sites disliked")}
<fieldset class="field"><legend>The feel you want</legend>{radios("Feel", ["Friendly and family-owned","No-nonsense and professional","Bold and modern"])}</fieldset>
{fld("Slogan or tagline, if you have one","Tagline")}{NS}'''))
steps.append(("Content and photos", f'''
{fld("Your story","Story","area",hint="How you got started, family-owned?, what makes you different.")}
{fld("Team members","Team","area",ph="Name, role… (photos optional)")}
<div class="field"><label for="f-photos">Photo uploads<span class="hint">Finished jobs, before/after, team, trucks, shop. You can also email or text photos later.</span></label><input id="f-photos" type="file" name="attachment" accept="image/*" multiple></div>
<fieldset class="field"><legend>Need stock photos to fill gaps?</legend>{radios("Stock photos", ["Yes","No"])}</fieldset>
{fld("Reviews and testimonials","Reviews","area",hint="Paste a few, or link your Google reviews.")}
{fld("Awards and memberships","Memberships",ph="BBB, chamber of commerce, trade associations…")}
<fieldset class="field"><legend>Who writes the text?</legend>{radios("Writer", ["You write it","I'll send it","A mix"])}</fieldset>'''))
steps.append(("Current online presence", f'''
{fld("Current website","Current website","url",ph="https://")}
{fld("What would you keep or change?","Keep or change")}
<fieldset class="field"><legend>Do you own a domain name?</legend>{radios("Owns domain", ["Yes","No","Not sure"])}</fieldset>
{fld("Which domain, where it's registered, and who has the login","Domain details")}
{fld("Google Business Profile link, and who manages it","Google Business Profile")}
{fld("Social and listing pages","Social links","area",ph="Facebook, Instagram, YouTube…")}
<fieldset class="field"><legend>Want an email at your own domain?</legend>{radios("Business email", ["Yes","No","Already have one"])}</fieldset>{NS}'''))
steps.append(("Forms and leads on your new site", f'''
{fld("Where should quote requests go?","Lead email",hint="Email address(es).")}
{fld("Text alert number","Lead text number","tel")}
{fld("What should your quote form ask customers?","Quote form questions","area",ph="Vehicle year/make/model, property size, problem type, urgency, photo upload…")}
<fieldset class="field"><legend>Booking or scheduling software you use</legend>{radios("Booking software", ["Housecall Pro","Jobber","ServiceTitan","Calendly","None","Other"])}</fieldset>
<fieldset class="field"><legend>Want a "Book now" button?</legend>{radios("Book now button", ["Yes","No"])}</fieldset>{NS}'''))
steps.append(("Extras and wrap-up", f'''
<fieldset class="field"><legend>Features you'd like</legend>{checks("Features", ["Before/after gallery","Coupons page","Financing info","Service area map","Emergency banner","French or Spanish version","Reviews feed"])}</fieldset>
{fld("Competitors","Competitors","area",hint="Links to 1 to 3 local competitors.")}
{fld("Anything else?","Anything else","area")}
{fld("How did you hear about Foundry Systems?","Heard about us")}
{fld("Times that work for a kickoff call","Kickoff times")}
<label class="choice"><input type="checkbox" name="Confirmation" value="Info is accurate and I have rights to the photos and logo I uploaded" required><span>My info is accurate, and I have the rights to the photos and logo I uploaded *</span></label>'''))

wsteps = "".join(f'<fieldset class="wstep" data-title="{e(t)}"><legend class="sr" style="position:absolute;left:-9999px">{e(t)}</legend><h2 style="font-size:clamp(1.7rem,4vw,2.4rem)">{e(t)}</h2>{b}</fieldset>' for t, b in steps)
start = head("Start your project", "Let's build your site.", "Ten short steps, about 15 to 20 minutes. Your answers save on this device as you go, so you can come back to finish.") + f'''
<section class="section-tight"><div class="wrap" style="max-width:860px">
<div class="wizard-top"><div class="step-meta"><b id="step-label">You and your business</b><span id="step-count">Step 1 of 10</span></div>
<div class="progress" aria-hidden="true"><div class="progress-fill"></div><div class="progress-bot">{ROBOT.replace('class="bot"','class="bot" style="width:100%;height:100%"')}</div></div></div>
<form class="form form-card" id="intake" action="{FORM_ACTION}" method="POST" enctype="multipart/form-data">
{hidden("New project form from the Foundry Systems website", "thanks.html?form=project")}
{wsteps}
<div class="wizard-nav"><button type="button" class="btn btn-ghost" id="w-prev">← Back</button>
<span class="saved-note" id="saved-note"></span>
<button type="button" class="btn btn-primary" id="w-next">Next →</button><button type="submit" class="btn btn-primary" id="w-send" hidden>Send my project form</button></div>
<p class="muted" style="font-size:.85rem;margin:14px 0 0">Uploaded files aren't saved between visits; add them right before you send. <button type="button" id="clear-saved" style="background:none;border:0;color:var(--ember);cursor:pointer;text-decoration:underline;font:inherit">Clear my answers</button></p>
</form></div></section>'''
page("start.html", "Start Your Project | Foundry Systems", "The guided project form: everything needed to build your website, in about 15 minutes.", start, None, cta=False,
     bot_hello="I'll ride along the progress bar. Let's go!")

# ------------------------------- THANKS ------------------------------------
thanks = f'''<section class="section blueprint"><div class="wrap" style="max-width:760px;text-align:center" id="thanks-root">
<div style="width:180px;margin:0 auto 10px">{ROBOT.replace('class="bot"','class="bot waving" style="width:100%;height:auto"')}</div>
<div data-form="other"><h1>Got it. 👍</h1><p class="lede" style="margin:0 auto 24px">Thanks for reaching out. I'll get back to you within one business day.</p>
<div class="btn-row" style="justify-content:center"><a class="btn btn-primary" href="start.html">Start my project</a><a class="btn btn-ghost" href="index.html">Back to home</a></div></div>
<div data-form="project" hidden><h1>Project form received!</h1><p class="lede" style="margin:0 auto 18px">Thanks! I'll look it over and get back to you within one business day to set up a quick kickoff call.</p>
<div id="pay-wrap" hidden><p><b>Ready to get started?</b> Pay your build invoice now and the 2-week clock starts.<span data-promo> Pay by Dec 31, 2026 to lock in the $99/mo care plan.</span></p><div class="btn-row" id="pay-links" style="justify-content:center"></div></div>
<p class="muted" style="margin-top:18px">Questions? Call or text <a href="tel:{TEL}">{PHONE}</a>.</p></div>
</div></section>'''
page("thanks.html", "Thank You | Foundry Systems", "Thanks for reaching out to Foundry Systems.", thanks, None, cta=False, extra_head='<meta name="robots" content="noindex">', body_attr=' data-no-bot')

# ------------------------------- LEGAL -------------------------------------
privacy = head("Privacy", "Privacy policy", "Short and plain: what I collect, why, and what I do with it.") + f'''
<section class="section"><div class="wrap prose">
<p class="muted">Last updated October 31, 2026</p>
<h2>What I collect</h2><p>When you fill out a form on this site, I receive what you type in and any files you upload: things like your name, business name, phone number, email, and details about your business and project.</p>
<h2>Why I collect it</h2><p>Only to reply to you, quote and build your website, and look after it afterwards. I don't sell, rent or trade your information to anyone.</p>
<h2>How it's handled</h2><ul><li>Form submissions are delivered to my email by a form delivery service.</li><li>Payments are handled by Stripe. I never see or store your card number.</li><li>This site may use simple, privacy-friendly analytics to count visits. It doesn't track you across other sites.</li><li>The project form can save your answers in your own browser so you can finish later. That data stays on your device until you send the form or clear it.</li></ul>
<h2>How long I keep it</h2><p>As long as needed to work with you and keep proper business records, then it's deleted.</p>
<h2>Your choices</h2><p>You can ask to see, correct or delete the information I have about you at any time. Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>Foundry Systems, Craig Donnelly · <a href="tel:{TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
</div></section>'''
page("privacy.html", "Privacy Policy | Foundry Systems", "How Foundry Systems collects and uses information from website forms.", privacy, None)

terms = head("Terms", "Terms, in plain English.", "A summary of how working together works. Every client signs a full agreement before the build invoice is paid.") + f'''
<section class="section"><div class="wrap prose">
<p class="muted">Last updated October 31, 2026</p>
<h2>Prices and payment</h2><ul><li>Core Website (5 pages) is $1,500. Complete Website (8 pages) is $1,997. Prices are in Canadian dollars.</li><li>The build is paid in full, up front, before work begins.</li><li>The care plan is included with every build and billed monthly by automatic payment. The first 30 days after launch are free; billing starts 30 days after your site goes live. The regular rate is $147/month.</li><li><b>2026 promotion:</b> if your build invoice is paid on or before December 31, 2026, your care plan is $99/month, locked in for as long as you keep it active. If you cancel and later return, the regular rate applies.</li><li>Extra work outside the build or care plan is quoted before it starts, with a $200 minimum.</li></ul>
<h2>Timeline</h2><p>Most sites launch about 2 weeks after payment and your completed project form. If I'm waiting on information from you, the timeline pauses.</p>
<h2>What a "page" is</h2><p>One distinct page in the site's menu, like Home, Services or Contact. Forms, the privacy policy and thank-you pages don't count toward your total.</p>
<h2>The care plan</h2><p>Covers hosting, a secure connection, text changes, promotions, hours and contact updates, photo swaps, and fixing anything that breaks. New pages, redesigns, new features and large batches of content are quoted separately.</p>
<h2>Ownership</h2><p>Your business name, logo, photos and text always belong to you. Once the build is paid, the finished site is yours. Your domain belongs to you, even if I register or manage it on your behalf.</p>
<h2>Cancelling the care plan</h2><p>Give 30 days' written notice (text or email is fine). Your site stays online through your last paid month, then hosting ends. For a one-time $200 transfer fee, I'll provide your website files and transfer your domain to you or a new provider. After cancelling, any work is quoted separately with a $200 minimum.</p>
<h2>Cancelling the build</h2><ul><li>Before work starts: 80% refund (a 20% fee covers planning, consultation and payment fees).</li><li>After work starts, before your first preview: 50% refund.</li><li>After your first preview: no refund.</li></ul>
<h2>Liability</h2><p>I build and look after your site with care, but I can't guarantee search rankings, a number of calls or sales, or that a site will never go down. Total responsibility is limited to the amount paid in the previous 12 months.</p>
<h2>Governing law</h2><p>These terms follow the laws of the Province of Alberta.</p>
</div></section>'''
page("terms.html", "Terms | Foundry Systems", "How pricing, payment, the care plan, ownership and cancellations work at Foundry Systems.", terms, None)

# ------------------------------- 404 ---------------------------------------
nf = f'''<section class="section blueprint"><div class="wrap" style="max-width:720px;text-align:center">
<div style="width:200px;margin:0 auto">{ROBOT.replace('class="bot"','class="bot" style="width:100%;height:auto;transform:rotate(-8deg)"')}</div>
<h1>Couldn't find that page.</h1><p class="lede" style="margin:0 auto 24px">I checked the map twice. It might have moved, or the link has a typo.</p>
<div class="btn-row" style="justify-content:center"><a class="btn btn-primary" href="/">Take me home</a><a class="btn btn-ghost" href="/contact.html">Ask a question</a></div>
</div></section>'''
page("404.html", "Page Not Found | Foundry Systems", "That page couldn't be found.", nf, None, cta=False, extra_head='<meta name="robots" content="noindex">', body_attr=' data-bot-hello="Hmm… I can\'t find that page either."')

# ------------------------------- STATIC ------------------------------------
for f in ("styles.css", "app.js"):
    shutil.copy(os.path.join(SRC, f), os.path.join(OUT, f))
with open(os.path.join(OUT, "favicon.svg"), "w") as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect x="2" y="2" width="36" height="36" rx="9" fill="#26262B" stroke="#FF6B1A" stroke-width="2"/><path d="M13 11h15v5H18.5v3.5H26v5h-7.5V30H13z" fill="#FF6B1A"/></svg>')
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
urls = ["", "pricing.html","work.html","industries.html","how-it-works.html","about.html","faq.html","contact.html","start.html","checkup.html","privacy.html","terms.html"] + [t["page"] for t in TRADES.values()]
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
with open(os.path.join(OUT, ".nojekyll"), "w") as f:
    f.write("")
print("Built", len([x for x in os.listdir(OUT) if x.endswith(".html")]), "pages into", OUT)
