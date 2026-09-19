/* Ariel's Dapto — progressive enhancement. Site works fully without JS. */
document.documentElement.classList.add("js");

/* --- mobile nav --- */
const toggle = document.querySelector(".nav-toggle");
const links = document.querySelector(".nav-links");
toggle.addEventListener("click", () => {
  const open = links.classList.toggle("open");
  toggle.setAttribute("aria-expanded", String(open));
  toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
});
links.addEventListener("click", (e) => {
  if (e.target.tagName === "A") {
    links.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
  }
});

/* --- menu category filtering --- */
const chips = [...document.querySelectorAll(".chip")];
const cats = [...document.querySelectorAll(".menu-cat")];

function showCat(slug) {
  chips.forEach((c) => c.setAttribute("aria-pressed", String(c.dataset.cat === slug)));
  cats.forEach((c) => { c.hidden = c.dataset.cat !== slug; });
}
chips.forEach((c) => c.addEventListener("click", () => showCat(c.dataset.cat)));

/* deep links like #menu-coffee activate the right category */
function syncHash() {
  const m = location.hash.match(/^#menu-(\w+)$/);
  if (m && cats.some((c) => c.dataset.cat === m[1])) showCat(m[1]);
}
window.addEventListener("hashchange", syncHash);
if (cats.length) { showCat("coffee"); syncHash(); }

/* --- open-now status (Bopple trading hours: Mon–Fri 8–16, Sat–Sun 8–15) --- */
const HOURS = { 0: [8, 15], 1: [8, 16], 2: [8, 16], 3: [8, 16], 4: [8, 16], 5: [8, 16], 6: [8, 15] };
const el = document.getElementById("open-status");
const dot = document.querySelector(".status-dot");
if (el && dot) {
  const now = new Date();
  const [open, close] = HOURS[now.getDay()];
  const h = now.getHours() + now.getMinutes() / 60;
  const fmt = (v) => (v > 12 ? v - 12 : v) + (v >= 12 ? "pm" : "am");
  if (h >= open && h < close) {
    el.textContent = `Open now · until ${fmt(close)} today`;
    dot.classList.add("open");
  } else {
    el.textContent = h < open ? `Opens ${fmt(open)} today` : `Opens 8am tomorrow`;
    dot.classList.add("closed");
  }
}

/* --- gold frames draw in as they scroll into view --- */
const io = new IntersectionObserver((entries) => {
  entries.forEach((en) => {
    if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
  });
}, { threshold: 0.25 });
document.querySelectorAll(".frame").forEach((f) => io.observe(f));
