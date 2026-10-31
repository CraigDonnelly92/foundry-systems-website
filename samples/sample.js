/* Shared helpers for Foundry Systems sample sites */
(function(){
  // Sample banner
  var bar = document.createElement("div");
  bar.className = "fs-sample-bar";
  bar.innerHTML = '<span><b>Sample concept</b> built by Foundry Systems. This business is made up, and forms here don’t send anything.</span>' +
    '<a href="/work.html">Back to Foundry Systems</a>';
  document.body.insertBefore(bar, document.body.firstChild);
  var css = document.createElement("style");
  css.textContent = ".fs-sample-bar{position:relative;z-index:9999;display:flex;gap:14px;justify-content:center;align-items:center;flex-wrap:wrap;background:#18181B;color:#F4F1EC;font:500 13px/1.4 system-ui,-apple-system,'Segoe UI',sans-serif;padding:9px 16px;text-align:center}.fs-sample-bar b{color:#FF8F45}.fs-sample-bar a{color:#18181B;background:#FF6B1A;border-radius:6px;padding:5px 10px;font-weight:700;text-decoration:none;white-space:nowrap}.fs-note{margin-top:12px;font-size:.92rem;font-weight:600}";
  document.head.appendChild(css);

  // Forms: show a note instead of sending
  document.querySelectorAll("form").forEach(function(f){
    f.addEventListener("submit", function(e){
      e.preventDefault();
      var n = f.querySelector(".fs-note");
      if(!n){ n = document.createElement("p"); n.className = "fs-note"; n.setAttribute("role","status"); f.appendChild(n); }
      n.textContent = "This is a sample site, so nothing was sent. On a real Foundry Systems site, this request lands in the owner’s inbox right away.";
    });
  });

  // Mobile menu
  document.querySelectorAll("[data-menu-toggle]").forEach(function(btn){
    var menu = document.getElementById(btn.getAttribute("aria-controls"));
    btn.addEventListener("click", function(){
      var open = menu.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });

  // Before/after sliders
  document.querySelectorAll("[data-ba]").forEach(function(ba){
    var r = ba.querySelector("input"), top = ba.querySelector("[data-ba-top]"), h = ba.querySelector("[data-ba-handle]");
    function set(){ top.style.clipPath = "inset(0 " + (100 - r.value) + "% 0 0)"; h.style.left = r.value + "%"; }
    r.addEventListener("input", set); set();
  });
})();
