(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var root = document.documentElement;

  /* ---------- Theme: light, dark or system ---------- */
  var themeButtons = document.querySelectorAll("button[data-theme-choice]");
  var colorQuery = window.matchMedia("(prefers-color-scheme: light)");
  var themeMeta = document.querySelector('meta[name="theme-color"]');

  function applyTheme(choice, save) {
    var resolved = choice === "system" ? (colorQuery.matches ? "light" : "dark") : choice;
    root.setAttribute("data-theme", resolved);
    root.setAttribute("data-theme-pref", choice);
    if (themeMeta) themeMeta.setAttribute("content", resolved === "light" ? "#ffffff" : "#000000");
    themeButtons.forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-theme-choice") === choice));
    });
    if (save) {
      try {
        localStorage.setItem("theme", choice);
      } catch (e) { /* storage unavailable, the choice still applies for this visit */ }
    }
  }

  applyTheme(root.getAttribute("data-theme-pref") || "dark", false);
  themeButtons.forEach(function (b) {
    b.addEventListener("click", function () { applyTheme(b.getAttribute("data-theme-choice"), true); });
  });
  colorQuery.addEventListener("change", function () {
    if (root.getAttribute("data-theme-pref") === "system") applyTheme("system", false);
  });

  /* ---------- Scroll to top: shown once the hero has left the viewport ---------- */
  var toTop = document.getElementById("to-top");
  var heroEl = document.getElementById("top");
  if (toTop && heroEl && "IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      toTop.classList.toggle("is-shown", !entries[0].isIntersecting);
    }, { threshold: 0 }).observe(heroEl);
    toTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
      var brand = document.querySelector(".brand");
      if (brand) brand.focus({ preventScroll: true });
    });
  }

  /* ---------- Mobile menu ---------- */
  var toggle = document.querySelector(".menu-toggle");
  var menu = document.getElementById("menu");

  function setMenu(open) {
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    menu.classList.toggle("is-open", open);
    root.classList.toggle("menu-open", open);
    if (open) {
      menu.removeAttribute("inert");
    } else {
      menu.setAttribute("inert", "");
    }
  }

  if (toggle && menu) {
    menu.setAttribute("inert", "");
    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) setMenu(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setMenu(false);
        toggle.focus();
      }
    });
    window.matchMedia("(min-width: 880px)").addEventListener("change", function (e) {
      if (e.matches) setMenu(false);
    });
  }

  /* ---------- Scroll reveals, once per element ---------- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { revealObserver.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* ---------- Tagline reveal: one word at a time as each crosses the trigger line ---------- */
  var words = document.querySelectorAll("#tagline .word");
  if (words.length) {
    if (reduced || !("IntersectionObserver" in window)) {
      words.forEach(function (w) { w.classList.add("is-on"); });
    } else {
      var wordObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          var w = entry.target;
          /* The trigger line is 40% up from the bottom of the viewport. */
          w.classList.toggle("is-on", entry.isIntersecting || entry.boundingClientRect.top < 0);
        });
      }, { rootMargin: "0px 0px -40% 0px", threshold: 0 });
      words.forEach(function (w) { wordObserver.observe(w); });
    }
  }

  /* ---------- Nav current section ---------- */
  var links = document.querySelectorAll(".nav-link, .menu-link");
  var sections = [];
  links.forEach(function (a) {
    var id = a.getAttribute("href").slice(1);
    var s = document.getElementById(id);
    if (s && sections.indexOf(s) === -1) sections.push(s);
  });
  if ("IntersectionObserver" in window && sections.length) {
    var navObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (a) {
          if (a.getAttribute("href") === "#" + entry.target.id) {
            a.setAttribute("aria-current", "true");
          } else {
            a.removeAttribute("aria-current");
          }
        });
      });
    }, { rootMargin: "-40% 0px -55% 0px", threshold: 0 });
    sections.forEach(function (s) { navObserver.observe(s); });
  }

  /* ---------- Credentials filter and search ---------- */
  var grid = document.getElementById("cred-grid");
  if (grid) {
    var cards = Array.prototype.slice.call(grid.children);
    var chips = document.querySelectorAll(".chip");
    var search = document.getElementById("cred-search");
    var count = document.getElementById("cred-count");
    var empty = document.getElementById("cred-empty");
    var reset = document.getElementById("cred-reset");
    var filter = "all";

    var apply = function () {
      var q = search.value.trim().toLowerCase().slice(0, 80);
      var shown = 0;
      cards.forEach(function (c) {
        var okCat = filter === "all" || c.getAttribute("data-cat") === filter;
        var okText = !q || c.textContent.toLowerCase().indexOf(q) !== -1;
        var ok = okCat && okText;
        c.hidden = !ok;
        if (ok) shown += 1;
      });
      count.textContent = "Showing " + shown + " of " + cards.length;
      empty.hidden = shown !== 0;
      grid.hidden = shown === 0;
    };

    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        filter = chip.getAttribute("data-filter");
        chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c === chip)); });
        apply();
      });
    });
    search.addEventListener("input", apply);
    reset.addEventListener("click", function () {
      filter = "all";
      search.value = "";
      chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c.getAttribute("data-filter") === "all")); });
      apply();
      search.focus();
    });
  }
})();
