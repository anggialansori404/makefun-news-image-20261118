#!/usr/bin/env python3
"""Draw entry.png (v4, broadsheet edition): the world news of
Wednesday, 18 November 2026 set like a classic newspaper front page -
a serif masthead with the date as the biggest type, one lead story,
then fifteen more stories in three ruled text columns with short
article bodies, and a two-item ticker under the fold. Eighteen
stories in all, each cross-checked in the day's independent roundups:
the Gulf escalation, the Crimea Bridge, the Shenzhen summit, Ebola,
measles, Israel's government pick, Gaza's floods, Venezuela's oil
billions, the Siberia crash, Cyclone Xavier, the Papua New Guinea
quake, Alaska's Senate race, the market slide, France's protests,
record Canary Islands arrivals, the Myanmar genocide case, the
Thailand-U.S. trade deal and the European supermarket cyber-attack.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (250, 247, 238)
INK = (22, 22, 22)
GREY = (80, 78, 72)
RED = (178, 34, 30)
WHITE = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
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


def block(draw, xy, text, fnt, fill, max_w, leading=1.15):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def story(draw, x, y, max_w, kicker, headline, body):
    draw.text((x, y), kicker, font=font(SANS_B, 16), fill=RED)
    y = block(draw, (x, y + 21), headline, font(SERIF_B, 21), INK, max_w)
    y = block(draw, (x, y + 2), body, font(SERIF, 17), GREY, max_w,
              leading=1.18)
    return y + 8


def rule(draw, x0, x1, y):
    draw.line([x0, y, x1, y], fill=INK, width=1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.line([16, 14, W - 16, 14], fill=INK, width=4)
    d.line([16, 22, W - 16, 22], fill=INK, width=1)
    d.text((W // 2, 30), "WEDNESDAY, NOVEMBER 18, 2026",
           font=font(SERIF_B, 43), fill=INK, anchor="ma")
    d.text((W // 2, 84),
           "ONE DAY OF WORLD NEWS ON ONE PAGE - 18 STORIES",
           font=font(SANS, 20), fill=GREY, anchor="ma")
    d.line([16, 116, W - 16, 116], fill=INK, width=2)

    # Lead story.
    d.text((16, 126), "MIDDLE EAST - THE LEAD", font=font(SANS_B, 19),
           fill=RED)
    y = block(d, (16, 150),
              "U.S. strikes Iran's Qeshm Island; Iran answers with "
              "drones on Bahrain and Kuwait",
              font(SERIF_B, 37), INK, W - 32)
    block(d, (16, y + 4),
          "The Gulf fighting escalated sharply on Wednesday, days "
          "before Presidents Trump, Xi and Putin are due to meet - "
          "the day's dominant story on every continent.",
          font(SERIF, 20), GREY, W - 32)
    d.line([16, 318, W - 16, 318], fill=INK, width=2)

    # Three text columns.
    cols = [(16, 320), (352, 320), (688, 320)]
    col_w = 320
    col1 = [
        ("EUROPE - WAR", "Ukraine hits the Crimea Bridge again",
         "Kyiv's second day of strikes dropped part of the Kerch "
         "Bridge's road span into the strait, Moscow says."),
        ("ASIA - SUMMIT", "Xi hosts Putin in Shenzhen",
         "Beijing denounced protectionism as Trump tours Asia ahead "
         "of a three-leader summit this week."),
        ("ISRAEL", "Eisenkot tapped to form a government",
         "The president passed over Benjamin Netanyahu after "
         "October's deadlocked election."),
        ("GAZA", "Cold and floods batter the camps",
         "Australia, Canada, Italy and the UK urged Israel to open "
         "humanitarian access to Gaza."),
        ("VENEZUELA", "Oil cash funds Caracas spending",
         "A U.S. State Department report counts $12bn in oil and "
         "mineral revenue for the government."),
    ]
    col2 = [
        ("AFRICA - HEALTH", "Ebola outbreak doubles in DR Congo",
         "11,000 cases and 5,400 deaths in three months; the UN says "
         "children are hit hardest."),
        ("AMERICAS - HEALTH", "U.S. loses measles-free status",
         "5,400 cases and 10 deaths end the 26-year elimination "
         "status held since the 1990s."),
        ("RUSSIA", "Siberia warplane crash kills 19",
         "A Russian military plane came down near Kemerovo; no cause "
         "was given by officials."),
        ("PACIFIC", "Cyclone Xavier hits the Cook Islands",
         "The Category 5 storm struck the northern islands; damage "
         "reports were still coming in."),
        ("PAPUA NEW GUINEA", "Magnitude 6.0 earthquake strikes",
         "A strong quake shook Papua New Guinea on Wednesday, the "
         "day's second Pacific disaster."),
    ]
    col3 = [
        ("U.S. POLITICS", "Peltola wins Alaska Senate race",
         "Mary Peltola's victory gives the Democrats 56 seats in the "
         "U.S. Senate."),
        ("MARKETS", "Stocks slide around the world",
         "DAX -2.08%, S&P 500 -1.03%, FTSE 100 -1.76%; gold fell to "
         "$3,775, Brent crude to $91.55."),
        ("FRANCE", "Cost-of-living protests, week four",
         "Marchers filled French streets for a fourth straight "
         "weekend of protests."),
        ("SPAIN", "Record migrant arrivals in the Canaries",
         "2,331 people reached the Canary Islands over one weekend, "
         "a record for the route."),
        ("WORLD COURT", "Judges to rule on Myanmar case",
         "The World Court will decide the genocide case over "
         "Myanmar's treatment of the Rohingya."),
    ]
    for (x, _), items in zip(cols, [col1, col2, col3]):
        y = 332
        for kicker, headline, body in items:
            y = story(d, x, y, col_w, kicker, headline, body)
            rule(d, x, x + col_w, y)
            y += 8
    d.line([344, 330, 344, 918], fill=GREY, width=1)
    d.line([680, 330, 680, 918], fill=GREY, width=1)

    # Under the fold: two more stories in a dark band.
    d.rectangle([0, 928, W, H], fill=INK)
    d.text((16, 940),
           "TRADE: Thailand inks a preliminary U.S. deal - zero tariffs "
           "on certain goods",
           font=font(SANS_B, 20), fill=WHITE)
    d.text((16, 972),
           "CYBER: Hackers disable supermarket freezers across seven "
           "European countries",
           font=font(SANS_B, 20), fill=(255, 196, 64))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
