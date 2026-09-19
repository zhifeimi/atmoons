#!/usr/bin/env python3
"""Regenerate the menu section of index.html from assets/data/menu.json.

Usage:  python3 build-menu.py
Fetches nothing — works from the local JSON snapshot (refresh that snapshot
with the Bopple API endpoints documented in research/menu.md). Injects
between the <!-- MENU:START --> / <!-- MENU:END --> markers in index.html.
"""
import json, re, html, pathlib

ROOT = pathlib.Path(__file__).parent
menu = json.load(open(ROOT / "assets/data/menu.json"))

# display grouping: JSON category -> (chip slug, display title, blurb)
GROUPS = {
    "Coffee & Tea": ("coffee", "Coffee & tea", "Campos beans, poured on the La Marzocco — every size from piccolo to a proper mug."),
    "Cake & Slices": ("cabinet", "The cabinet", "Baked fresh, stacked high, and it moves fast — croissants, slices, pies and rolls."),
    "Ice Drinks": ("iced", "Iced & shakes", "Espresso over ice, thick shakes, and the iced chai the regulars order by name."),
    "Smoothies": ("fresh", "Smoothies & juices", "Blended to order with coconut water, fruit and oats."),
    "Fresh Juices": ("fresh", None, None),
    "Cold Drinks": ("fresh", None, None),
    "Kids Corner": ("kids", "Kids corner", "Little appetites, sorted. Babycinos are two dollars."),
    "Catering": ("catering", "Catering", "Boxes and platters for meetings, birthdays and morning teas — order ahead on Bopple."),
}
ORDER = ["coffee", "cabinet", "iced", "fresh", "kids", "catering"]


def price(it):
    lo, hi = it["min"], it["max"]
    if lo is None:
        return ""
    if lo == 0:
        return "Free"
    fmt = lambda v: f"${v:.0f}" if float(v).is_integer() else f"${v:.2f}"
    return fmt(lo) if lo == hi else f"{fmt(lo)}–{fmt(hi)}"


merged = {}
for cat in menu:
    slug, title, blurb = GROUPS[cat["category"]]
    g = merged.setdefault(slug, {"title": title, "blurb": blurb, "items": []})
    g["items"].extend(cat["items"])

blocks = []
for slug in ORDER:
    g = merged[slug]
    rows = []
    for it in g["items"]:
        name = html.escape(it["name"])
        name = name[0].upper() + name[1:]  # Bopple data has a few lowercase names
        desc = f'<span class="mi-desc">{html.escape(it["desc"])}</span>' if it["desc"] else ""
        rows.append(
            f'        <li class="mi">\n'
            f'          <span class="mi-name">{name}{desc}</span>\n'
            f'          <span class="mi-dots" aria-hidden="true"></span>\n'
            f'          <span class="mi-price">{price(it)}</span>\n'
            f'        </li>')
    blurb = f'\n      <p class="menu-blurb">{g["blurb"]}</p>' if g["blurb"] else ""
    cols = " cols" if len(rows) > 12 else ""
    blocks.append(
        f'    <section class="menu-cat" data-cat="{slug}" id="menu-{slug}">\n'
        f'      <h3>{g["title"]}</h3>{blurb}\n'
        f'      <ul class="menu-items{cols}">\n' + "\n".join(rows) +
        f'\n      </ul>\n    </section>')

out = "<!-- MENU:START -->\n" + "\n".join(blocks) + "\n    <!-- MENU:END -->"
page = ROOT / "index.html"
src = page.read_text()
new = re.sub(r"<!-- MENU:START -->.*?<!-- MENU:END -->", out, src, flags=re.S)
assert new != src, "MENU markers not found in index.html"
page.write_text(new)
print(f"menu injected: {sum(len(m['items']) for m in merged.values())} items, {len(ORDER)} categories")
