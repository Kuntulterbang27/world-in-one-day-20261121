"""Draw an original, deterministic 1024-pixel newspaper with Pillow.

The renderer is an authoring tool, not the sandbox entrypoint. All copy comes
from a verified, frozen local editorial ledger. No network or system clock.
"""
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SCALE = 2
WIDTH = HEIGHT = 1024
PAPER = "#f4f0e5"
INK = "#17242a"
MUTED = "#59666a"
TEAL = "#146b73"
RUST = "#b4482e"
RULE = "#bbb9ad"
OCEAN = "#dce9e7"
STORIES = json.loads((ROOT / "stories.json").read_text(encoding="utf-8"))
IMAGE = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), PAPER)
DRAW = ImageDraw.Draw(IMAGE)


def font(size, bold=False):
    weight = "SemiBold" if bold else "Regular"
    return ImageFont.truetype(str(ROOT / "assets" / f"BarlowCondensed-{weight}.ttf"), round(size * SCALE))


def rect(box, fill, outline=None, width=1):
    DRAW.rectangle(tuple(round(v * SCALE) for v in box), fill=fill, outline=outline,
                   width=max(1, round(width * SCALE)))


def line(points, fill=RULE, width: float=1):
    DRAW.line([(round(x*SCALE), round(y*SCALE)) for x, y in points], fill=fill,
              width=max(1, round(width*SCALE)))


def polygon(points, fill, outline=None):
    DRAW.polygon([(round(x*SCALE), round(y*SCALE)) for x, y in points], fill=fill, outline=outline)


def ellipse(box, fill, outline=None, width: float=1):
    DRAW.ellipse(tuple(round(v*SCALE) for v in box), fill=fill, outline=outline,
                 width=max(1, round(width*SCALE)))


def text(x, y, value, size: float=16, bold=False, color=INK, anchor="lt"):
    DRAW.text((round(x*SCALE), round(y*SCALE)), value, font=font(size, bold),
              fill=color, anchor=anchor)


def text_width(value, size, bold=False):
    return DRAW.textlength(value, font=font(size, bold)) / SCALE


def fitted(x, y, value, width, size: float=16, minimum: float=12, bold=False, color=INK):
    while text_width(value, size, bold) > width and size > minimum:
        size -= .25
    if text_width(value, size, bold) > width:
        raise ValueError(f"Copy does not fit without becoming illegible: {value}")
    text(x, y, value, size, bold, color)
    return size


def wrapped(x, y, value, width, size=17, leading=20, bold=False, color=INK):
    words = value.split()
    rows = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and text_width(candidate, size, bold) > width:
            rows.append(current)
            current = word
        else:
            current = candidate
    if current:
        rows.append(current)
    for index, row in enumerate(rows):
        text(x, y + index*leading, row, size, bold, color)
    return y + len(rows)*leading


def masthead():
    rect((0, 0, 1024, 9), INK)
    text(25, 19, "THE WORLD IN ONE DAY", 57, True)
    text(998, 26, "SATURDAY EDITION", 15, True, TEAL, "rt")
    text(998, 48, "38 VERIFIED DEVELOPMENTS", 14, False, MUTED, "rt")
    line([(25, 82), (999, 82)], INK, 2)
    text(25, 91, "Saturday, 21 November 2026", 20, True)
    text(999, 95, "SIX CONTINENTS  /  ONE DAY  /  ORIGINAL ILLUSTRATIONS", 13, False, MUTED, "rt")


def tanker(x, y, scale: float=1):
    """Schematic illustration, not a photograph or reconstruction."""
    def p(points):
        return [(x+a*scale, y+b*scale) for a, b in points]
    polygon(p([(0, 47), (115, 47), (100, 68), (17, 68)]), INK)
    polygon(p([(15, 35), (95, 35), (95, 47), (15, 47)]), TEAL)
    polygon(p([(88, 11), (105, 11), (105, 47), (88, 47)]), "#e2ddd0")
    line(p([(95, 11), (95, 1)]), INK, 2)
    for offset in (0, 14, 28, 42):
        line(p([(24+offset, 36), (24+offset, 47)]), PAPER, 1)
    for wave in range(3):
        line(p([(-4, 75+wave*8), (31, 72+wave*8), (66, 76+wave*8), (113, 72+wave*8)]), TEAL, 1)
    polygon(p([(38, 35), (44, 13), (52, 26), (58, 5), (66, 35)]), RUST)
    ellipse((x+49*scale,y-6*scale,x+67*scale,y+12*scale), "#b8b8ad")


def hero():
    rect((25, 125, 654, 304), "#e9e4d7")
    rect((25, 125, 30, 304), RUST)
    text(42, 137, "THE LEAD  /  MIDDLE EAST  /  01", 14, True, RUST)
    text(42, 158, "THREE TANKERS", 44, True)
    text(42, 200, "ATTACKED NEAR HORMUZ", 40, True)
    wrapped(43, 249, "UK maritime officials report two projectile hits; Iran reports a mine strike near the strategic oil-shipping route on Saturday.",
            448, 17, 20)
    tanker(515, 196, .95)
    text(637, 287, "AP / UKMTO", 11, False, MUTED, "rb")


def world_map():
    rect((672, 125, 999, 304), OCEAN)
    text(685, 137, "WHERE THE NEWS HAPPENED", 15, True, TEAL)
    # Original schematic coastlines: deliberately simplified, never a border map.
    landmasses = [
        [(-168,70),(-130,72),(-108,60),(-81,48),(-56,48),(-63,27),(-83,10),(-103,23),(-126,49),(-157,58)],
        [(-82,12),(-62,10),(-36,-5),(-44,-24),(-68,-55),(-76,-27)],
        [(-52,82),(-19,73),(-42,59),(-62,66)],
        [(-11,36),(-6,58),(26,71),(51,56),(79,73),(122,68),(179,65),(159,42),(132,32),(116,7),(99,0),(79,23),(60,29),(35,36)],
        [(-17,35),(14,38),(37,27),(50,10),(36,-28),(18,-35),(1,-5),(-15,7)],
        [(112,-11),(137,-10),(154,-28),(145,-39),(116,-34)],
        [(166,-34),(178,-40),(171,-47)],
        [(46,-13),(50,-24),(45,-26),(43,-18)],
    ]
    def project(lon, lat):
        return 684+(lon+180)/360*300, 161+(84-lat)/144*113
    for latitude in (0, 45):
        line([project(-180, latitude), project(180, latitude)], "#c1d5d2", .5)
    for shape in landmasses:
        polygon([project(lon, lat) for lon, lat in shape], "#93b4ab")
    for story in STORIES:
        x, y = project(story["lon"], story["lat"])
        radius = 3.4 if story["hero"] else 1.9
        ellipse((x-radius,y-radius,x+radius,y+radius), RUST if story["hero"] else INK)
    hx, hy = project(56.2, 26.45)
    ellipse((hx-7,hy-7,hx+7,hy+7), None, RUST, 1.1)
    line([(hx+5,hy+5),(hx+24,hy+18),(hx+71,hy+18)], RUST, .8)
    text(hx+25, hy+20, "HORMUZ", 12, True, RUST)
    text(685, 283, "News locations / approximate; no borders implied", 11.5, False, MUTED)


def section(x, y, width, title):
    rect((x, y, x+width, y+23), INK)
    text(x+8, y+4, title.upper(), 16, True, PAPER)
    return y+29


def brief(x, y, width, story, row_height=40):
    text(x, y+1, f"{story['number']:02d}", 12, True, TEAL)
    fitted(x+23, y, story["image_headline"], width-23, 18, 14, True)
    fitted(x+23, y+20, story["image_context"], width-23, 14, 12.5, False, MUTED)
    line([(x+23,y+row_height-4),(x+width,y+row_height-4)], RULE, .5)
    return y+row_height


def news_columns():
    groups = [["Asia", "Africa"], ["Europe", "Americas"],
              ["Middle East", "Oceania", "Economy / Technology"]]
    for column, headings in enumerate(groups):
        x = 25 + column*332
        y = 320
        for heading in headings:
            y = section(x, y, 310, heading)
            for story in STORIES:
                if story["section"] == heading and not story["hero"]:
                    y = brief(x, y, 310, story, 40)
            y += 6
        assert y <= 995, (column, y)
    for x in (346, 678):
        line([(x, 320), (x, 982)], RULE, .75)


def footer():
    line([(25, 995), (999, 995)], INK, 1)
    text(25, 1002, "38 distinct events and new disclosures / Saturday follow-ups explicitly dated / Sources in repository", 12, False, MUTED)
    text(999, 1002, "EDITION 02", 12, True, TEAL, "rt")


def illustrated_spotlights():
    # Cross-references to existing stories, never additional counted events.
    rect((357, 804, 667, 884), "#dce8df")
    text(370, 815, "25 / PUBLIC HEALTH", 13, True, TEAL)
    text(370, 836, "ETHIOPIA'S POLIO DRIVE", 23, True)
    text(370, 864, "11.3 million children targeted", 15, False, MUTED)
    rect((626, 826, 647, 850), PAPER, TEAL)
    line([(630,838),(643,838)], TEAL, 3)
    line([(636.5,831),(636.5,845)], TEAL, 3)
    line([(636,850),(636,866)], TEAL, 2)
    rect((357, 896, 667, 980), "#e5e3d9")
    text(370, 907, "37 / TECHNOLOGY & WAR", 13, True, TEAL)
    text(370, 929, "AI-WEAPONS RULES WAIT", 23, True)
    text(370, 957, "Geneva agrees two more years of talks", 15, False, MUTED)
    rect((623, 922, 650, 943), PAPER, INK)
    ellipse((628,929,632,933), TEAL)
    ellipse((640,929,644,933), TEAL)
    line([(636,917),(636,922)], INK, 2)
    line([(628,947),(645,947)], INK, 2)


def main():
    assert len(STORIES) == 38
    assert sum(story["hero"] for story in STORIES) == 1
    masthead()
    hero()
    world_map()
    news_columns()
    illustrated_spotlights()
    footer()
    result = IMAGE.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    result.save(ROOT / "news.png", "PNG", optimize=True, compress_level=9)
    print("Rendered", ROOT / "news.png")


if __name__ == "__main__":
    main()
