#!/usr/bin/env python3
"""Draw entry.png (v3, pictogram edition): the world news of Wednesday,
18 November 2026 in one image - the v2 fifteen-story front page, with a
small drawn pictogram in every panel's kicker bar so each story reads
at a glance: a bridge for Crimea, three summit circles for Shenzhen,
a virus for Ebola, a shield and cross for measles, a ballot box for
Israel's government vote, a falling chart for the markets, and a drone
over a burst for the lead story in the Gulf.

Stories (from the day's independent roundups): U.S. strikes Iran's
Qeshm Island and Iran fires drones at Bahrain and Kuwait; Ukraine
hits the Crimea Bridge again and a span falls; Xi hosts Putin in
Shenzhen as Trump tours Asia; Ebola in DR Congo doubles to 11,000
cases and 5,400 deaths; the U.S. loses measles-free status after 26
years; Israel's president taps Eisenkot to form a government; markets
slide (DAX -2.1%, gold $3,775); Peltola wins Alaska and Democrats
take 56 Senate seats; a Siberia plane crash kills 19, a magnitude 6.0
quake hits Papua New Guinea and Category 5 Cyclone Xavier hits the
Cook Islands; Gaza camps flood in the cold, France protests for a
fourth weekend, record migrant arrivals reach the Canaries, and the
World Court is to rule on the Myanmar genocide case.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
WHITE = (255, 255, 255)
RED = (178, 34, 30)
NAVY = (24, 46, 84)
TEAL = (16, 96, 92)
GOLD = (176, 124, 22)
PURPLE = (94, 54, 120)
GREEN = (38, 92, 48)
GREY = (92, 92, 88)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, max_w, leading=1.12):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def fit_line(draw, xy, text, fill, max_w, start=22):
    size = start
    while draw.textlength(text, font=font(SANS_B, size)) > max_w:
        size -= 1
    draw.text(xy, text, font=font(SANS_B, size), fill=fill)


# --- pictograms, drawn in white inside a 30x30 box at (x, y) ---

def icon_bridge(d, x, y, c):
    d.line([x, y + 22, x + 30, y + 22], fill=c, width=3)
    d.line([x + 5, y + 22, x + 5, y + 6], fill=c, width=3)
    d.line([x + 25, y + 22, x + 25, y + 6], fill=c, width=3)
    d.arc([x + 5, y - 2, x + 25, y + 22], start=180, end=360, fill=c, width=2)
    d.arc([x, y + 16, x + 14, y + 30], start=0, end=180, fill=c, width=2)
    d.arc([x + 16, y + 16, x + 30, y + 30], start=0, end=180, fill=c, width=2)


def icon_circles(d, x, y, c):
    d.ellipse([x + 1, y + 7, x + 17, y + 23], outline=c, width=3)
    d.ellipse([x + 13, y + 7, x + 29, y + 23], outline=c, width=3)
    d.ellipse([x + 7, y + 1, x + 23, y + 17], outline=c, width=3)


def icon_virus(d, x, y, c):
    d.ellipse([x + 9, y + 9, x + 21, y + 21], outline=c, width=3)
    for dx, dy in [(15, 2), (15, 24), (2, 15), (24, 15),
                   (6, 6), (24, 6), (6, 24), (24, 24)]:
        d.line([x + 15, y + 15, x + dx, y + dy], fill=c, width=2)
        d.ellipse([x + dx - 2, y + dy - 2, x + dx + 2, y + dy + 2], fill=c)


def icon_shield(d, x, y, c):
    d.polygon([(x + 15, y + 2), (x + 27, y + 6), (x + 27, y + 16),
               (x + 15, y + 28), (x + 3, y + 16), (x + 3, y + 6)],
              outline=c, width=3)
    d.line([x + 15, y + 9, x + 15, y + 21], fill=c, width=3)
    d.line([x + 9, y + 15, x + 21, y + 15], fill=c, width=3)


def icon_ballot(d, x, y, c):
    d.rectangle([x + 4, y + 14, x + 26, y + 27], outline=c, width=3)
    d.line([x + 10, y + 18, x + 20, y + 18], fill=c, width=3)
    d.rectangle([x + 11, y + 2, x + 19, y + 14], outline=c, width=2)


def icon_chart(d, x, y, c):
    pts = [(x + 3, y + 6), (x + 11, y + 12), (x + 18, y + 10),
           (x + 27, y + 22)]
    d.line(pts, fill=c, width=3)
    d.polygon([(x + 27, y + 22), (x + 20, y + 21), (x + 26, y + 15)],
              fill=c)


def icon_drone(d, x, y, c):
    d.rectangle([x + 11, y + 12, x + 19, y + 19], outline=c, width=2)
    for cx, cy in [(5, 6), (25, 6), (5, 25), (25, 25)]:
        d.ellipse([x + cx - 4, y + cy - 2, x + cx + 4, y + cy + 2],
                  outline=c, width=2)
    d.line([x + 11, y + 13, x + 6, y + 8], fill=c, width=2)
    d.line([x + 19, y + 13, x + 24, y + 8], fill=c, width=2)
    d.line([x + 11, y + 18, x + 6, y + 23], fill=c, width=2)
    d.line([x + 19, y + 18, x + 24, y + 23], fill=c, width=2)


ICONS = {
    "EUROPE - WAR": icon_bridge,
    "ASIA - SUMMIT": icon_circles,
    "AFRICA - HEALTH": icon_virus,
    "AMERICAS - HEALTH": icon_shield,
    "ISRAEL - POLITICS": icon_ballot,
    "WORLD - MARKETS": icon_chart,
}


def panel(draw, box, kicker, kicker_color, headline, detail):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=WHITE, outline=INK, width=3)
    draw.rectangle([x0, y0, x1, y0 + 36], fill=kicker_color)
    draw.text((x0 + 12, y0 + 7), kicker, font=font(SANS_B, 21), fill=WHITE)
    ICONS[kicker](draw, x1 - 40, y0 + 3, WHITE)
    y = text_block(draw, (x0 + 12, y0 + 48), headline,
                   font(SANS_B, 25), INK, x1 - x0 - 24)
    text_block(draw, (x0 + 12, y + 6), detail,
               font(SANS, 19), GREY, x1 - x0 - 24)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 104], fill=INK)
    d.text((W // 2, 12), "WEDNESDAY 18 NOVEMBER 2026",
           font=font(SANS_B, 44), fill=WHITE, anchor="ma")
    d.text((W // 2, 66), "THE WORLD IN ONE DAY - 15 TOP STORIES",
           font=font(SANS, 23), fill=(210, 205, 190), anchor="ma")

    # Lead story, with a drone pictogram beside the kicker.
    d.rectangle([16, 118, W - 16, 330], fill=NAVY)
    d.text((36, 130), "LEAD - MIDDLE EAST", font=font(SANS_B, 24),
           fill=(255, 196, 64))
    icon_drone(d, W - 76, 126, (255, 196, 64))
    text_block(d, (36, 162),
               "U.S. strikes Iran's Qeshm Island; Iran fires drones "
               "at Bahrain and Kuwait",
               font(SERIF_B, 39), WHITE, W - 72)
    d.text((36, 288),
           "Gulf fighting escalates days before a Trump-Xi-Putin summit.",
           font=font(SANS, 23), fill=(196, 214, 240))

    rows_y = [(344, 614), (626, 896)]
    cols_x = [(16, 341), (349, 674), (682, 1008)]
    stories = [
        ("EUROPE - WAR", RED,
         "Ukraine hits Crimea Bridge again; a span falls into the strait",
         "Second day of strikes on the Kerch Bridge to occupied Crimea."),
        ("ASIA - SUMMIT", TEAL,
         "Xi hosts Putin in Shenzhen as Trump tours Asia",
         "Beijing attacks protectionism; a three-leader summit is set "
         "for this week."),
        ("AFRICA - HEALTH", GOLD,
         "Ebola in DR Congo doubles: 11,000 cases, 5,400 dead",
         "The UN says children are hit hardest by the outbreak."),
        ("AMERICAS - HEALTH", NAVY,
         "U.S. loses measles-free status after 26 years",
         "Over 5,400 cases and 10 deaths, a first since the 1990s."),
        ("ISRAEL - POLITICS", PURPLE,
         "President taps Eisenkot to form Israel's government",
         "Netanyahu bypassed after October's deadlocked election."),
        ("WORLD - MARKETS", GREEN,
         "Markets slide worldwide on the day's shocks",
         "DAX -2.1%, S&P 500 -1.0%, FTSE -1.8%; gold falls to $3,775."),
    ]
    for i, (kicker, color, headline, detail) in enumerate(stories):
        y0, y1 = rows_y[i // 3]
        x0, x1 = cols_x[i % 3]
        panel(d, [x0, y0, x1, y1], kicker, color, headline, detail)

    d.rectangle([0, 908, W, H], fill=INK)
    fit_line(d, (16, 918),
             "U.S. VOTE: Peltola wins Alaska - Democrats take 56 Senate seats",
             WHITE, W - 32)
    fit_line(d, (16, 950),
             "DISASTERS: Siberia plane crash kills 19 - M6.0 quake Papua New "
             "Guinea - Cat-5 Cyclone Xavier, Cook Islands",
             (255, 196, 64), W - 32)
    fit_line(d, (16, 982),
             "ALSO: Gaza camps flood in the cold - France protests, week 4 - "
             "Record migrant arrivals in the Canaries - World Court: Myanmar case",
             WHITE, W - 32)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
