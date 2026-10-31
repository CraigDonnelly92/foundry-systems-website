/* Foundry Systems site script */
(function(){
"use strict";
var CONFIG = {
  phone: "780-834-8078",
  phoneHref: "+17808348078",
  email: "craig.foundrysystems@gmail.com",
  promoEnd: new Date(2027, 0, 1, 0, 0, 0),   // promo switches off Jan 1, 2027 (visitor's local time)
  // Paste Stripe payment links here when ready; leave blank to hide the pay buttons.
  stripe: { core: "", complete: "" }
};
window.FS_CONFIG = CONFIG;

var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
var isPhone = function(){ return window.innerWidth <= 760; };
function $(s, r){ return (r||document).querySelector(s); }
function $$(s, r){ return Array.prototype.slice.call((r||document).querySelectorAll(s)); }
function store(k, v){ try{ if(v === undefined) return localStorage.getItem(k); if(v === null) localStorage.removeItem(k); else localStorage.setItem(k, v);}catch(e){ return null; } }
var now = new Date();
var promoOn = now < CONFIG.promoEnd;

/* ---------- Promo ---------- */
$$("[data-promo]").forEach(function(el){ if(!promoOn) el.hidden = true; });
$$("[data-nopromo]").forEach(function(el){ if(promoOn) el.hidden = true; });
var bar = $(".promo");
if(bar){
  if(!promoOn || store("fs-promo-closed") === "1") bar.hidden = true;
  var x = $(".promo button", bar);
  if(x) x.addEventListener("click", function(){ bar.hidden = true; store("fs-promo-closed","1"); });
}
var days = Math.max(0, Math.ceil((CONFIG.promoEnd - now) / 86400000));
$$("[data-countdown]").forEach(function(el){ el.textContent = days === 1 ? "1 day left" : days + " days left"; });

/* ---------- Nav ---------- */
var tog = $(".menu-toggle"), menu = $(".menu");
if(tog && menu){
  tog.addEventListener("click", function(){
    var open = menu.classList.toggle("open");
    tog.setAttribute("aria-expanded", open ? "true" : "false");
  });
}
var y = $("#year"); if(y) y.textContent = now.getFullYear();

/* ---------- Reveal + count-up ---------- */
function countUp(el){
  var end = parseFloat(el.getAttribute("data-count")), pre = el.getAttribute("data-pre")||"", suf = el.getAttribute("data-suf")||"";
  if(reduce){ el.textContent = pre + end.toLocaleString() + suf; return; }
  var t0 = null, dur = 1200;
  function f(t){ if(!t0) t0 = t; var p = Math.min(1,(t-t0)/dur), e = 1-Math.pow(1-p,3);
    el.textContent = pre + Math.round(end*e).toLocaleString() + suf; if(p<1) requestAnimationFrame(f); }
  requestAnimationFrame(f);
}
if("IntersectionObserver" in window){
  var io = new IntersectionObserver(function(ents){
    ents.forEach(function(en){ if(en.isIntersecting){ en.target.classList.add("in");
      if(en.target.hasAttribute("data-count")) countUp(en.target); io.unobserve(en.target);} });
  }, {threshold:.12});
  $$(".reveal,[data-count]").forEach(function(el){ io.observe(el); });
} else { $$(".reveal").forEach(function(el){ el.classList.add("in"); }); }

/* ---------- Tilt cards ---------- */
if(!reduce && window.matchMedia("(hover:hover)").matches){
  $$(".tilt").forEach(function(c){
    c.addEventListener("mousemove", function(e){ var r = c.getBoundingClientRect();
      var px = (e.clientX - r.left)/r.width - .5, py = (e.clientY - r.top)/r.height - .5;
      c.style.transform = "perspective(800px) rotateY("+(px*6)+"deg) rotateX("+(-py*6)+"deg) translateY(-3px)"; });
    c.addEventListener("mouseleave", function(){ c.style.transform = ""; });
  });
}

/* ---------- Sparks ---------- */
var sp = $(".sparks");
if(sp && !reduce){
  for(var i=0;i<18;i++){ var s = document.createElement("i"); s.className="spark";
    s.style.left = (Math.random()*100)+"%"; s.style.animationDuration = (4+Math.random()*5)+"s";
    s.style.animationDelay = (Math.random()*6)+"s"; sp.appendChild(s); }
}

/* ---------- Trades ---------- */
var TRADES = window.FS_TRADES = {
  glass:{label:"Glass", page:"websites-for-glass-shops.html", biz:"Clearview Glass & Windshield", url:"clearviewglass.ca", main:"#0f3b57", accent:"#1fa0d8",
    alert:"Mobile windshield service: we come to you", head:"Chipped windshield? We'll fix it today.",
    sub:"Auto, home and commercial glass. We handle the insurance paperwork.", btns:["Get a windshield quote","Call now"],
    feats:[["Windshield quote form","Year, make, model and a photo of the damage"],["Insurance claim help","We deal with the adjuster so you don't have to"],["Mobile service","At your home, shop or job site"]],
    services:["Windshield replacement","Rock chip repair","Home window glass","Storefront and commercial glass","Shower doors and mirrors","Mobile service"]},
  auto:{label:"Auto Repair", page:"websites-for-auto-repair-shops.html", biz:"Northline Auto Repair", url:"northlineauto.ca", main:"#1f2a1f", accent:"#d64545",
    alert:"Now booking winter tire changeovers", head:"Honest repairs. Straight answers.",
    sub:"All makes and models. Certified techs, fleet accounts welcome.", btns:["Book an appointment","Call the shop"],
    feats:[["Service menu","Oil, brakes, diagnostics, tires, with starting prices"],["Online booking requests","Pick a day, describe the problem"],["Fleet accounts","Priority service for work trucks"]],
    services:["Diagnostics","Brakes and suspension","Oil and maintenance","Tires and changeovers","Engine and transmission","Fleet service"]},
  electrical:{label:"Electrical", page:"websites-for-electricians.html", biz:"Brightwire Electric", url:"brightwire.ca", main:"#1d1f3a", accent:"#f2b705",
    alert:"24/7 emergency electrical: tap to call", head:"Power done right, the first time.",
    sub:"Licensed and insured. Homes, farms and commercial.", btns:["Request a quote","Emergency call"],
    feats:[["Licensed and insured badges","Trust before they even call"],["EV chargers and generators","Pages for the jobs you want more of"],["Emergency call button","One tap, day or night"]],
    services:["Panel upgrades","EV charger installs","Standby generators","Renovations and new builds","Lighting","Troubleshooting and repairs"]},
  plumbing:{label:"Plumbing", page:"websites-for-plumbers.html", biz:"Summit Plumbing & Drain", url:"summitplumbing.ca", main:"#0c2d48", accent:"#e8562a",
    alert:"Burst pipe? 24/7 emergency service: tap to call", head:"Leaks, clogs, no hot water? Fixed fast.",
    sub:"Licensed plumbers serving the whole region, day or night.", btns:["Get a free quote","Call 24/7"],
    feats:[["Emergency call banner","Pinned to the top of every page"],["Service area map","Shows every town you cover"],["Water heater pages","Built to rank on Google"]],
    services:["Emergency repairs","Water heaters","Drain cleaning","Sewer lines","Well and septic","Renovation plumbing"]},
  hvac:{label:"HVAC", page:"websites-for-hvac-companies.html", biz:"Aurora Heating & Air", url:"auroraheating.ca", main:"#2a1a12", accent:"#ff7a1a",
    alert:"Fall furnace tune-up: book before the first cold snap", head:"Warm winters. Cool summers. No surprises.",
    sub:"Furnaces, AC and heat pumps. Maintenance plans and financing available.", btns:["Book a tune-up","Call us"],
    feats:[["Seasonal specials","Tune-up promos that switch on and off by season"],["Maintenance plans","Recurring customers, every year"],["Financing info","Bigger jobs, easier yeses"]],
    services:["Furnace repair and install","Air conditioning","Heat pumps","Maintenance plans","Ductwork","Indoor air quality"]},
  landscaping:{label:"Landscaping", page:"websites-for-landscapers.html", biz:"Riverbend Landscaping", url:"riverbendlandscaping.ca", main:"#1e3a24", accent:"#8bc34a",
    alert:"Booking spring projects and winter snow contracts now", head:"Yards you'll actually want to spend time in.",
    sub:"Design, install, upkeep and snow removal. Residential and commercial.", btns:["Get an estimate","See our work"],
    feats:[["Big photo galleries","Your best work, front and center"],["Before/after sliders","The fastest way to sell a project"],["Snow removal contracts","Year-round work from one site"]],
    services:["Landscape design","Sod and planting","Patios and retaining walls","Lawn care","Fall cleanups","Snow removal"]}
};
var ICONS = {
  glass:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 18 6 6h12l2 12z"/><path d="M9 9l-1 5M13 9l3 4"/></svg>',
  auto:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/></svg>',
  electrical:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg>',
  plumbing:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/></svg>',
  hvac:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1 19.1 4.9"/></svg>',
  landscaping:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22V12"/><path d="M12 12C12 7 8 4 4 4c0 5 3 8 8 8zM12 12c0-4 3-7 8-7 0 4-3 7-8 7z"/></svg>'
};
window.FS_ICONS = ICONS;
function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); }

var picker = $("#picker");
if(picker){
  var preview = $("#preview"), link = $("#preview-link"), tradeLink = $("#trade-link");
  Object.keys(TRADES).forEach(function(k, i){
    var b = document.createElement("button"); b.type="button"; b.className="pick"; b.setAttribute("aria-pressed", i===0?"true":"false");
    b.dataset.trade = k; b.innerHTML = ICONS[k] + "<span>" + TRADES[k].label + "</span>";
    picker.appendChild(b);
  });
  function render(k){
    var t = TRADES[k];
    preview.style.setProperty("--pv-main", t.main); preview.style.setProperty("--pv-accent", t.accent);
    preview.innerHTML = '<div class="pv-chrome"><i></i><i></i><i></i><span class="url">'+esc(t.url)+'</span></div>'+
      '<div class="pv-alert">'+esc(t.alert)+'</div>'+
      '<div class="pv-nav"><span class="pv-logo">'+esc(t.biz)+'</span><span class="pv-call">Call now</span></div>'+
      '<div class="pv-hero"><h3>'+esc(t.head)+'</h3><p>'+esc(t.sub)+'</p><div class="pv-btns"><span>'+esc(t.btns[0])+'</span><span>'+esc(t.btns[1])+'</span></div></div>'+
      '<div class="pv-feats">'+t.feats.map(function(f){ return '<div><b>'+esc(f[0])+'</b>'+esc(f[1])+'</div>'; }).join("")+'</div>';
    link.href = "sample.html?t=" + k; link.textContent = "Open the full " + t.label.toLowerCase() + " sample";
    if(tradeLink){ tradeLink.href = t.page; tradeLink.textContent = "Websites for " + t.label.toLowerCase(); }
  }
  render("glass");
  picker.addEventListener("click", function(e){
    var b = e.target.closest(".pick"); if(!b) return;
    $$(".pick", picker).forEach(function(x){ x.setAttribute("aria-pressed", x===b?"true":"false"); });
    if(reduce){ render(b.dataset.trade); return; }
    preview.classList.add("building"); Bot.say("Building a " + TRADES[b.dataset.trade].label.toLowerCase() + " site…", 1600);
    setTimeout(function(){ render(b.dataset.trade); preview.classList.remove("building"); }, 320);
  });
}

/* ---------- Sample site page ---------- */
var sample = $("#sample-root");
if(sample){
  var q = new URLSearchParams(location.search).get("t"); if(!TRADES[q]) q = "plumbing";
  var t = TRADES[q];
  document.title = t.biz + " (sample concept) | Foundry Systems";
  sample.style.setProperty("--pv-main", t.main); sample.style.setProperty("--pv-accent", t.accent);
  var others = Object.keys(TRADES).map(function(k){ return '<a class="btn '+(k===q?'btn-primary':'btn-ghost')+'" href="sample.html?t='+k+'">'+TRADES[k].label+'</a>'; }).join("");
  sample.innerHTML =
   '<div class="notice" style="margin-bottom:22px"><b>Sample concept.</b> '+esc(t.biz)+' is a made-up business. This demo shows what a Foundry Systems '+esc(t.label.toLowerCase())+' site can look like. Buttons and forms here don\'t send anything.</div>'+
   '<div class="btn-row" style="margin-bottom:26px">'+others+'</div>'+
   '<div class="preview" style="--pv-main:'+t.main+';--pv-accent:'+t.accent+'">'+
   '<div class="pv-chrome"><i></i><i></i><i></i><span class="url">'+esc(t.url)+'</span></div>'+
   '<div class="pv-alert">'+esc(t.alert)+'</div>'+
   '<div class="pv-nav"><span class="pv-logo">'+esc(t.biz)+'</span><span style="display:flex;gap:14px;align-items:center;font-size:.9rem;font-weight:600"><span>Services</span><span>About</span><span>Reviews</span><span class="pv-call">Call now</span></span></div>'+
   '<div class="pv-hero" style="padding:64px 28px"><h3 style="font-size:clamp(2rem,5vw,3.4rem)">'+esc(t.head)+'</h3><p>'+esc(t.sub)+'</p><div class="pv-btns"><span>'+esc(t.btns[0])+'</span><span>'+esc(t.btns[1])+'</span></div></div>'+
   '<div style="padding:30px 28px"><h3 style="color:'+t.main+';text-transform:uppercase">Services</h3><div class="pv-feats" style="padding:0">'+
     t.services.map(function(s){ return '<div><b>'+esc(s)+'</b>Quick description of this service and what it includes.</div>'; }).join("")+'</div></div>'+
   '<div style="padding:0 28px 30px"><h3 style="color:'+t.main+';text-transform:uppercase">Why customers pick us</h3><div class="pv-feats" style="padding:0">'+
     t.feats.map(function(f){ return '<div><b>'+esc(f[0])+'</b>'+esc(f[1])+'</div>'; }).join("")+'</div></div>'+
   '<div style="padding:0 28px 30px;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px">'+
     '<div style="background:#f6f5f2;border-radius:12px;padding:20px"><b style="color:'+t.main+'">★★★★★</b><p style="margin:.5em 0 0">"Showed up when they said, fixed it fast, and the price was what they quoted." <br><small>Sample review</small></p></div>'+
     '<div style="background:#f6f5f2;border-radius:12px;padding:20px"><b style="color:'+t.main+'">★★★★★</b><p style="margin:.5em 0 0">"Easy to book online and they texted me when they were on the way." <br><small>Sample review</small></p></div>'+
   '</div>'+
   '<div style="padding:0 28px 34px"><h3 style="color:'+t.main+';text-transform:uppercase">Request a quote</h3>'+
     '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px">'+
     ['Your name','Phone','Town','What do you need?'].map(function(l){ return '<div style="border:1.5px solid #ddd;border-radius:8px;padding:14px;color:#888">'+l+'</div>'; }).join("")+
     '</div><div class="pv-btns"><span>Send my request</span></div></div>'+
   '<div style="background:'+t.main+';color:#fff;padding:22px 28px;font-size:.9rem;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px"><span>'+esc(t.biz)+' · Serving the Peace region</span><span>Mon–Fri 8–5 · Sat by appointment</span></div>'+
   '</div>'+
   '<div class="btn-row" style="margin-top:28px"><a class="btn btn-primary" href="start.html">Start my project</a><a class="btn btn-ghost" href="'+t.page+'">Websites for '+esc(t.label.toLowerCase())+'</a></div>';
}

/* ---------- Price calculator ---------- */
var calc = $("#calc");
if(calc){
  var out = $("#calc-out"), go = $("#calc-go"), plan = "complete";
  function upd(){
    var price = plan === "core" ? "$1,500" : "$1,997", care = promoOn ? "$99/mo for life" : "$147/mo";
    out.textContent = price + " today, then " + care;
    go.href = "start.html?plan=" + plan;
  }
  $$("button", calc).forEach(function(b){ b.addEventListener("click", function(){
    plan = b.dataset.plan; $$("button", calc).forEach(function(x){ x.setAttribute("aria-pressed", x===b?"true":"false"); }); upd(); }); });
  upd();
}

/* ---------- Before / after ---------- */
$$(".ba").forEach(function(ba){
  var r = $("input", ba), a = $(".after", ba), h = $(".handle", ba);
  function set(){ var v = r.value; a.style.clipPath = "inset(0 0 0 "+v+"%)"; h.style.left = v + "%"; }
  r.addEventListener("input", set); set();
});

/* ---------- Robot (Sprocket) ---------- */
var Bot = window.FS_BOT = { say:function(){}, };
var botTpl = $("#bot-svg");
if(botTpl && !document.body.hasAttribute("data-no-bot")){
  var dock = document.createElement("div"); dock.className = "bot-dock";
  dock.innerHTML = '<div class="bot-menu" id="bot-menu" role="menu"><p>Hi, I\'m Sprocket. What do you need?</p>'+
    '<a href="pricing.html" role="menuitem">See pricing</a><a href="work.html" role="menuitem">See sample sites</a>'+
    '<a href="start.html" role="menuitem">Start my project</a><a href="tel:'+CONFIG.phoneHref+'" role="menuitem">Call or text Craig</a>'+
    '<a href="contact.html" role="menuitem">Ask a question</a><button class="lnk min" type="button" id="bot-min">Shrink me down</button></div>'+
    '<div class="bot-bubble" aria-live="polite"></div>'+
    '<button class="bot-btn" type="button" aria-label="Open the help menu" aria-expanded="false" aria-controls="bot-menu">'+botTpl.innerHTML+'</button>';
  document.body.appendChild(dock);
  var btn = $(".bot-btn", dock), bmenu = $(".bot-menu", dock), bub = $(".bot-bubble", dock), svg = $(".bot", dock), eyes = $(".eyes", dock);
  var tmr;
  Bot.say = function(msg, ms){ if(!msg || dock.classList.contains("mini") || bmenu.classList.contains("open")) return;
    bub.textContent = msg; bub.classList.add("show"); clearTimeout(tmr); tmr = setTimeout(function(){ bub.classList.remove("show"); }, ms||3800); };
  Bot.wave = function(){ svg.classList.remove("waving"); void svg.getBBox; setTimeout(function(){ svg.classList.add("waving"); }, 20); };
  if(store("fs-bot-mini") === "1") dock.classList.add("mini");
  btn.addEventListener("click", function(){
    if(dock.classList.contains("mini")){ dock.classList.remove("mini"); store("fs-bot-mini", null); }
    var open = bmenu.classList.toggle("open"); btn.setAttribute("aria-expanded", open?"true":"false"); bub.classList.remove("show");
  });
  $("#bot-min", dock).addEventListener("click", function(){ dock.classList.add("mini"); bmenu.classList.remove("open"); btn.setAttribute("aria-expanded","false"); store("fs-bot-mini","1"); });
  document.addEventListener("keydown", function(e){ if(e.key === "Escape" && bmenu.classList.contains("open")){ bmenu.classList.remove("open"); btn.setAttribute("aria-expanded","false"); btn.focus(); } });
  document.addEventListener("click", function(e){ if(!dock.contains(e.target) && bmenu.classList.contains("open")){ bmenu.classList.remove("open"); btn.setAttribute("aria-expanded","false"); } });

  // Fly in (desktop, full motion, once per session)
  var seen = false; try{ seen = sessionStorage.getItem("fs-bot-in") === "1"; sessionStorage.setItem("fs-bot-in","1"); }catch(e){}
  if(!reduce && !isPhone() && !seen && !dock.classList.contains("mini")){
    dock.style.transform = "translate(-60vw,-70vh) rotate(-20deg)";
    setTimeout(function(){ dock.classList.add("flying"); dock.style.transform = "translate(0,0) rotate(0)"; }, 700);
    setTimeout(function(){ dock.classList.remove("flying"); Bot.wave(); Bot.say(document.body.getAttribute("data-bot-hello") || "Hey there! Click me if you need a hand."); }, 2200);
  } else if(!reduce && !isPhone()) { setTimeout(function(){ Bot.wave(); }, 600); }

  // Eyes follow cursor
  if(!reduce && eyes){
    window.addEventListener("mousemove", function(e){
      var r = btn.getBoundingClientRect(), cx = r.left + r.width/2, cy = r.top + r.height*.3;
      var dx = Math.max(-1, Math.min(1, (e.clientX - cx)/400)), dy = Math.max(-1, Math.min(1, (e.clientY - cy)/400));
      eyes.setAttribute("transform", "translate("+(dx*4)+" "+(dy*2.5)+")");
    }, {passive:true});
  }
  // Section hints (once each)
  if("IntersectionObserver" in window){
    var said = {};
    var hio = new IntersectionObserver(function(ents){ ents.forEach(function(en){
      var m = en.target.getAttribute("data-bot-say");
      if(en.isIntersecting && !said[m]){ said[m] = 1; Bot.say(m); }
    }); }, {threshold:.5});
    $$("[data-bot-say]").forEach(function(el){ hio.observe(el); });
  }
}

/* ---------- Simple forms (contact) ---------- */
function setNext(form, kind){
  var n = $('input[name="_next"]', form);
  if(n){ var base = location.href.replace(/[^\/]*([?#].*)?$/, ""); n.value = base + "thanks.html?form=" + kind; }
}
var cf = $("#contact-form");
if(cf){
  setNext(cf, "contact");
  cf.addEventListener("submit", function(e){
    var ph = cf.phone.value.trim(), em = cf.email.value.trim(), err = $("#contact-err");
    if(!ph && !em){ e.preventDefault(); err.textContent = "Please add a phone number or an email so I can get back to you."; cf.phone.focus(); }
  });
}
var ck = $("#checkup-form"); if(ck) setNext(ck, "checkup");

/* ---------- Intake wizard ---------- */
var wz = $("#intake");
if(wz){
  setNext(wz, "project");
  var steps = $$(".wstep", wz), cur = 0, fill = $(".progress-fill"), pbot = $(".progress-bot"), label = $("#step-label"), count = $("#step-count");
  var prev = $("#w-prev"), next = $("#w-next"), send = $("#w-send");
  var KEY = "fs-intake-v1";
  function show(i){
    cur = Math.max(0, Math.min(steps.length-1, i));
    steps.forEach(function(s, j){ s.classList.toggle("active", j===cur); });
    var pct = ((cur+1)/steps.length)*100;
    fill.style.width = pct + "%"; if(pbot) pbot.style.left = "calc(" + pct + "% - " + (pct>95?20:0) + "px)";
    label.textContent = steps[cur].getAttribute("data-title"); count.textContent = "Step " + (cur+1) + " of " + steps.length;
    prev.style.visibility = cur===0 ? "hidden" : "visible";
    next.hidden = cur === steps.length-1; send.hidden = cur !== steps.length-1;
    if(cur === steps.length-1) Bot.say("Last step! You're almost done.");
    var top = $(".wizard-top"); if(top) window.scrollTo({top: wz.getBoundingClientRect().top + window.scrollY - 140, behavior: reduce?"auto":"smooth"});
  }
  function valid(){
    var ok = true;
    $$("[required]", steps[cur]).forEach(function(f){ if(!f.checkValidity()){ if(ok){ f.reportValidity(); f.focus(); } ok = false; } });
    return ok;
  }
  next.addEventListener("click", function(){ if(valid()){ save(); show(cur+1); } });
  prev.addEventListener("click", function(){ show(cur-1); });
  wz.addEventListener("submit", function(e){
    if(!valid()){ e.preventDefault(); return; }
    // keep the chosen plan for the thank-you page, then clear saved answers
    store("fs-last-plan", (wz.plan && wz.plan.value) || ""); store(KEY, null);
  });

  // trade-specific questions
  function trade(){ var c = $('input[name="Type of business"]:checked', wz); return c ? c.value : ""; }
  function applyTrade(){
    var t = trade();
    $$("[data-trade]", wz).forEach(function(el){
      var on = el.getAttribute("data-trade") === t; el.hidden = !on;
      $$("input,select,textarea", el).forEach(function(f){ f.disabled = !on; });
    });
    var other = $("#other-trade"); if(other){ other.hidden = t !== "Other"; $("input", other).disabled = t !== "Other"; }
    buildPages();
  }
  // pages checklist
  var PAGES = {
    "Glass":["Home","Auto glass","Home and commercial glass","Insurance claims","About","Reviews","Gallery","Contact and quote","Service areas","FAQ"],
    "Auto repair":["Home","Services","Book an appointment","Fleet accounts","About","Reviews","Contact","Specials","FAQ"],
    "Electrical":["Home","Residential","Commercial","EV chargers and generators","About","Reviews","Gallery","Contact and quote","Service areas","FAQ"],
    "Plumbing":["Home","Services","Emergency service","Water heaters","Drains and sewer","About","Reviews","Contact and quote","Service areas","FAQ"],
    "HVAC":["Home","Heating","Cooling","Maintenance plans","Financing and rebates","About","Reviews","Contact and quote","Specials","FAQ"],
    "Landscaping":["Home","Services","Gallery","Snow removal","About","Reviews","Contact and estimate","Service areas","FAQ"],
    "":["Home","Services","About","Gallery","Reviews","Contact and quote","Service areas","FAQ","Specials"]
  };
  function limit(){ var p = wz.plan && wz.plan.value; return p && p.indexOf("Core") === 0 ? 5 : (p && p.indexOf("Complete") === 0 ? 8 : 8); }
  function buildPages(){
    var box = $("#page-list"); if(!box) return;
    var t = trade(), list = PAGES[t] || PAGES[""], kept = $$('input:checked', box).map(function(c){ return c.value; });
    box.innerHTML = list.map(function(p){ return '<label class="choice"><input type="checkbox" name="Pages wanted" value="'+esc(p)+'"'+(kept.indexOf(p)>-1?" checked":"")+'><span>'+esc(p)+'</span></label>'; }).join("");
    pageCount();
  }
  function pageCount(){
    var box = $("#page-list"), n = $$('input:checked', box).length, L = limit(), info = $("#page-limit");
    info.textContent = n + " of " + L + " pages picked" + (n > L ? ". That's over your plan; uncheck a few or pick the Complete Website." : "");
    info.style.color = n > L ? "#ff9c7a" : "";
    $$('input', box).forEach(function(c){ c.disabled = !c.checked && n >= L; });
  }
  wz.addEventListener("change", function(e){
    if(e.target.name === "Type of business") applyTrade();
    if(e.target.name === "Pages wanted") pageCount();
    if(e.target.name === "plan"){ pageCount(); }
    save();
  });
  // services rows
  var addSvc = $("#add-svc"), svcBox = $("#svc-rows"), svcN = 1;
  function svcRow(){
    svcN++;
    var d = document.createElement("div"); d.className = "svc-row";
    d.innerHTML = '<input type="text" name="Service '+svcN+' name" placeholder="Service name" aria-label="Service name">'+
      '<input type="text" name="Service '+svcN+' description" placeholder="A sentence or two" aria-label="Service description">'+
      '<input type="text" name="Service '+svcN+' starting price" placeholder="From $" aria-label="Starting price (optional)">'+
      '<button type="button" class="icon-btn" aria-label="Remove this service">×</button>';
    $("button", d).addEventListener("click", function(){ d.remove(); });
    svcBox.appendChild(d); return d;
  }
  if(addSvc) addSvc.addEventListener("click", function(){ $("input", svcRow()).focus(); });

  // autosave on this device
  function save(){
    var data = {};
    $$("input,select,textarea", wz).forEach(function(f){
      if(!f.name || f.type === "file" || f.type === "hidden" || f.name === "_honey") return;
      if(f.type === "checkbox" || f.type === "radio"){ if(f.checked){ (data[f.name] = data[f.name] || []).push(f.value); } }
      else if(f.value) data[f.name] = f.value;
    });
    data.__svc = svcN; data.__step = cur;
    store(KEY, JSON.stringify(data));
    var n = $("#saved-note"); if(n) n.textContent = "Answers saved on this device.";
  }
  wz.addEventListener("input", function(){ clearTimeout(wz._t); wz._t = setTimeout(save, 600); });
  function load(){
    var raw = store(KEY); if(!raw) return false;
    var data; try{ data = JSON.parse(raw); }catch(e){ return false; }
    while(svcN < (data.__svc||1)) svcRow();
    Object.keys(data).forEach(function(k){
      if(k.indexOf("__") === 0) return;
      $$('[name="'+k.replace(/"/g,'\\"')+'"]', wz).forEach(function(f){
        if(f.type === "checkbox" || f.type === "radio") f.checked = [].concat(data[k]).indexOf(f.value) > -1;
        else f.value = data[k];
      });
    });
    applyTrade();
    var pl = $("#page-list"); if(pl && data["Pages wanted"]) $$("input", pl).forEach(function(c){ c.checked = data["Pages wanted"].indexOf(c.value) > -1; });
    pageCount();
    return data.__step || 0;
  }
  var qp = new URLSearchParams(location.search).get("plan");
  var startAt = load();
  if(qp && wz.plan){ var m = qp === "core" ? "Core Website" : "Complete Website"; $$('[name="plan"] option', wz).forEach(function(o){ if(o.value.indexOf(m) === 0) wz.plan.value = o.value; }); }
  var qt = new URLSearchParams(location.search).get("trade");
  if(qt){ var map = {glass:"Glass",auto:"Auto repair",electrical:"Electrical",plumbing:"Plumbing",hvac:"HVAC",landscaping:"Landscaping"}; var r = $('input[name="Type of business"][value="'+map[qt]+'"]', wz); if(r) r.checked = true; }
  applyTrade();
  var clr = $("#clear-saved"); if(clr) clr.addEventListener("click", function(){ if(confirm("Clear your saved answers and start over?")){ store(KEY, null); location.href = "start.html"; } });
  show(typeof startAt === "number" ? startAt : 0);
}

/* ---------- Style switcher (owner preview: open any page with ?styles) ---------- */
(function(){
  var on = false; try{ on = localStorage.getItem("fs-style-picker") === "1"; }catch(e){}
  if(!on) return;
  var STYLES = [["original","Original"],["blueprint","Blueprint"],["print","Editorial"],["signage","Signage"],["forge","Forge (mix)"]];
  var root = document.documentElement, box = document.createElement("div");
  box.className = "style-switch"; box.setAttribute("role","group"); box.setAttribute("aria-label","Site style");
  box.innerHTML = '<b><span>Site style</span><button type="button" aria-label="Collapse">–</button></b><div class="opts">'+
    STYLES.map(function(s){ return '<button type="button" data-s="'+s[0]+'">'+s[1]+'</button>'; }).join("")+'</div>';
  document.body.appendChild(box);
  function mark(){ var cur = root.getAttribute("data-style"); $$(".opts button", box).forEach(function(b){ b.setAttribute("aria-pressed", b.dataset.s === cur ? "true" : "false"); }); }
  $(".opts", box).addEventListener("click", function(e){
    var b = e.target.closest("button"); if(!b) return;
    if(window.FS_loadFont) window.FS_loadFont(b.dataset.s);
    root.setAttribute("data-style", b.dataset.s); store("fs-style", b.dataset.s); mark();
  });
  $("b button", box).addEventListener("click", function(){ var c = box.classList.toggle("closed"); this.textContent = c ? "+" : "–"; this.setAttribute("aria-label", c ? "Expand" : "Collapse"); });
  mark();
})();

/* ---------- Thank-you page ---------- */
var ty = $("#thanks-root");
if(ty){
  var kind = new URLSearchParams(location.search).get("form");
  $$("[data-form]", ty).forEach(function(el){ el.hidden = el.getAttribute("data-form") !== (kind === "project" ? "project" : "other"); });
  var lp = store("fs-last-plan") || "", pay = $("#pay-links");
  if(pay){
    var links = [];
    if(CONFIG.stripe.core && lp.indexOf("Complete") !== 0) links.push('<a class="btn btn-primary" href="'+CONFIG.stripe.core+'">Pay for Core Website ($1,500)</a>');
    if(CONFIG.stripe.complete && lp.indexOf("Core") !== 0) links.push('<a class="btn btn-primary" href="'+CONFIG.stripe.complete+'">Pay for Complete Website ($1,997)</a>');
    if(links.length){ pay.innerHTML = links.join(""); $("#pay-wrap").hidden = false; }
  }
  setTimeout(function(){ var s = $(".bot", document); if(s) s.classList.add("waving"); Bot.say("Got it! Talk soon. 👍", 5000); }, 900);
}
})();
