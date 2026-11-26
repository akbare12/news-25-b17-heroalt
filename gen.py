#!/usr/bin/env python3
"""Render entry.png for news-image-20261125, variant HEROALT (b17).
Canvas 1024x640. 50 stories, 10 regions, all text English.
Heroalt: Shenzhou-led large drawn scene + 2 hero cards + 47-story grid.
Run: python3 gen.py  -> writes entry.png next to this file.
"""
import os, random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 640
FD = "/usr/share/fonts/truetype/dejavu"
def F(sz, bold=False):
    return ImageFont.truetype(os.path.join(FD, "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), sz)

NAVY = (11, 31, 58); GOLD = (201, 162, 39); PAPER = (247, 243, 234)
INK = (18, 24, 32); MUT = (90, 96, 108); RED = (178, 34, 34); GREEN = (27, 120, 70)
BLUE = (24, 90, 160); CARD = (255, 255, 255); LINE = (205, 198, 184)
SKY1 = (8, 18, 46); SKY2 = (24, 52, 96)

# (headline, region, certainty) -- C confirmed, R reported, CL claim. 47 grid stories.
STORIES = [
 ("Iran says mines hit tankers in Hormuz strait", "MIDDLE EAST", "CL"),
 ("Houthis say they struck Saudi Ras Tanura refinery", "MIDDLE EAST", "R"),
 ("Houthi strike on Riyadh tower injures 11", "MIDDLE EAST", "C"),
 ("Saudi-led coalition strikes Yemen's Hodeidah port", "MIDDLE EAST", "C"),
 ("Israel kills Hamas security chief in Gaza strike", "MIDDLE EAST", "R"),
 ("UN warns of fresh Israeli attacks in Gaza", "MIDDLE EAST", "R"),
 ("Trump: Iran war funding secured through January", "NORTH AMERICA", "C"),
 ("Iran claims it shot down two US drones", "MIDDLE EAST", "CL"),
 ("Israel claims Iran is building chemical weapons", "MIDDLE EAST", "CL"),
 ("Sudan drone strikes kill 19 civilians, medics say", "AFRICA", "R"),
 ("Ebola teams evacuated amid Congo fighting", "AFRICA", "R"),
 ("Cairo fuel tanker crash kills at least 30", "AFRICA", "C"),
 ("Bogor gold mine collapse: 9 dead, 17 trapped", "SOUTHEAST ASIA", "C"),
 ("Australia signs security treaty with Solomons", "OCEANIA", "C"),
 ("China, Cambodia begin Golden Dragon drills", "SOUTHEAST ASIA", "C"),
 ("India, Malaysia hold Harimau Shakti army drills", "SOUTH ASIA", "C"),
 ("Huawei convicted of trade-secret theft in US", "EAST ASIA", "C"),
 ("Nvidia reinstates Jensen Huang as chief executive", "NORTH AMERICA", "C"),
 ("Huang apologises to Nvidia staff after comeback", "NORTH AMERICA", "C"),
 ("CIA and ODNI hit by apparent cyberattack", "NORTH AMERICA", "R"),
 ("US charges 800 in global anti-scam crackdown", "NORTH AMERICA", "C"),
 ("US Army destroys 5 tons of lead azide in Iowa", "NORTH AMERICA", "C"),
 ("Six recovered from plane crash off Mississippi", "NORTH AMERICA", "C"),
 ("COP31 ends without deal as Pope voices concern", "GLOBAL", "C"),
 ("30 nations urge Russia to halt chemical weapons", "EUROPE", "C"),
 ("Ukraine strikes Russian energy infrastructure", "EUROPE", "R"),
 ("Russian strike on Odesa kills two, injures three", "EUROPE", "C"),
 ("Leaked data puts Russian war dead at 490,334", "EUROPE", "R"),
 ("Spain heads to snap general election on Sunday", "EUROPE", "C"),
 ("China urges Dutch to safeguard business ties", "EUROPE", "C"),
 ("China urges Britain to back free trade", "EUROPE", "C"),
 ("US: Beijing did not direct spy suspect Huang", "NORTH AMERICA", "R"),
 ("Spy suspect Huang linked to Chinese official", "EAST ASIA", "R"),
 ("India condemns Houthi attack on Riyadh tower", "SOUTH ASIA", "C"),
 ("Two Indians hurt in Riyadh tower strike", "SOUTH ASIA", "C"),
 ("Wall Street slides: S&P -2.2%, Nasdaq -3.2%", "NORTH AMERICA", "C"),
 ("Japan, Taiwan stocks slide in AI sell-off", "EAST ASIA", "C"),
 ("UN aid chief urges access for war-hit Yemen", "MIDDLE EAST", "C"),
 ("US scraps Brazil aircraft tariff exemption", "LATIN AMERICA", "C"),
 ("US raises duties on Brazilian sugar", "LATIN AMERICA", "C"),
 ("Suriname marks Independence Day", "LATIN AMERICA", "C"),
 ("Oil climbs after Houthi refinery attack claim", "GLOBAL", "R"),
 ("US disputes Iran's Hormuz mine claims", "MIDDLE EAST", "R"),
 ("Riyadh tower hit in second attack in a week", "MIDDLE EAST", "R"),
 ("Houthis threaten Red Sea ports", "MIDDLE EAST", "R"),
 ("Spain's Socialists trail ahead of snap vote", "EUROPE", "R"),
 ("Pope warns climate extremes grow more frequent", "GLOBAL", "C"),
]
assert len(STORIES) == 47, len(STORIES)
assert len({r for _, r, _ in STORIES}) == 10, {r for _, r, _ in STORIES}

def wrap(draw, text, font, maxw, maxlines=2):
    words = text.split(); lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines[:maxlines], len(lines) <= maxlines

def fit(draw, text, font, maxw):
    return draw.textlength(text, font=font) <= maxw

def draw_scene(d, x0, y0, x1, y1):
    # sky gradient
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        c = tuple(int(SKY1[i] + (SKY2[i] - SKY1[i]) * t) for i in range(3))
        d.line([(x0, y), (x1, y)], fill=c)
    rnd = random.Random(25)
    for _ in range(90):
        sx, sy = rnd.randint(x0 + 4, x1 - 4), rnd.randint(y0 + 4, y1 - 60)
        r = rnd.choice([1, 1, 2])
        d.ellipse([sx, sy, sx + r, sy + r], fill=(255, 255, 255) if rnd.random() > 0.3 else GOLD)
    # Earth arc at bottom
    d.ellipse([x0 - 160, y1 - 58, x1 + 160, y1 + 190], fill=(28, 78, 150))
    d.arc([x0 - 160, y1 - 58, x1 + 160, y1 + 190], 200, 340, fill=(120, 190, 235), width=3)
    d.ellipse([x0 + 60, y1 - 22, x0 + 210, y1 + 6], fill=(46, 130, 80))
    d.ellipse([x0 + 330, y1 - 30, x0 + 470, y1 + 2], fill=(46, 130, 80))
    # Tiangong station, upper right: core module + solar panels
    sx, sy = x0 + 330, y0 + 26
    d.rectangle([sx, sy, sx + 150, sy + 16], fill=(210, 216, 224), outline=(140, 150, 165))
    d.rectangle([sx + 58, sy - 8, sx + 92, sy + 24], fill=(190, 198, 210), outline=(140, 150, 165))
    d.rectangle([sx - 52, sy + 3, sx - 2, sy + 13], fill=(30, 80, 160), outline=(160, 200, 255))
    d.rectangle([sx + 152, sy + 3, sx + 202, sy + 13], fill=(30, 80, 160), outline=(160, 200, 255))
    d.line([(sx - 52, sy + 8), (sx, sy + 8)], fill=(200, 210, 225), width=2)
    d.line([(sx + 150, sy + 8), (sx + 152, sy + 8)], fill=(200, 210, 225), width=2)
    d.text((sx + 18, sy + 20), "TIANGONG", font=F(9, True), fill=(220, 228, 240))
    # Shenzhou rocket, left, ascending with flame
    rx, ry = x0 + 78, y0 + 52
    d.polygon([(rx, ry - 34), (rx + 12, ry - 16), (rx + 12, ry + 44), (rx, ry + 52), (rx - 12, ry + 44), (rx - 12, ry - 16)], fill=(235, 238, 242), outline=(150, 160, 175))
    d.polygon([(rx, ry - 34), (rx + 12, ry - 16), (rx - 12, ry - 16)], fill=(178, 34, 34))
    d.rectangle([rx - 12, ry + 18, rx + 12, ry + 28], fill=(178, 34, 34))
    d.polygon([(rx - 8, ry + 52), (rx + 8, ry + 52), (rx, ry + 78)], fill=(255, 176, 32))
    d.polygon([(rx - 4, ry + 52), (rx + 4, ry + 52), (rx, ry + 66)], fill=(255, 236, 160))
    d.text((rx - 34, ry + 84), "SHENZHOU-24", font=F(9, True), fill=(255, 255, 255))
    # astronaut floating between rocket and station, tether to station
    ax, ay = x0 + 250, y0 + 92
    d.line([(ax + 26, ay - 6), (sx + 40, sy + 8)], fill=(220, 228, 240), width=1)
    d.rounded_rectangle([ax - 14, ay - 12, ax + 14, ay + 26], 8, fill=(240, 242, 245), outline=(150, 160, 175))
    d.ellipse([ax - 10, ay - 26, ax + 10, ay - 6], fill=(240, 242, 245), outline=(150, 160, 175))
    d.ellipse([ax - 7, ay - 23, ax + 7, ay - 9], fill=(120, 190, 235))
    d.rectangle([ax - 4, ay + 2, ax + 4, ay + 12], fill=(20, 120, 60))
    d.text((ax - 44, ay + 32), "ALI: 1ST FOREIGNER ABOARD", font=F(9, True), fill=(255, 255, 255))
    # number badge: 3 crew
    d.rounded_rectangle([x1 - 92, y0 + 8, x1 - 10, y0 + 32], 6, fill=GOLD)
    d.text((x1 - 84, y0 + 13), "3 CREW", font=F(11, True), fill=(11, 31, 58))

def hero_card(d, x0, y0, x1, y1, kicker, title, numbers, why, also, badge, badge_fill):
    d.rounded_rectangle([x0, y0, x1, y1], 6, fill=CARD, outline=LINE)
    d.rectangle([x0 + 6, y0, x1 - 6, y0 + 4], fill=badge_fill)
    d.text((x0 + 10, y0 + 10), kicker, font=F(9, True), fill=MUT)
    d.text((x0 + 10, y0 + 24), title, font=F(15, True), fill=INK)
    # number badge top-right
    bw = d.textlength(badge, font=F(13, True)) + 14
    d.rounded_rectangle([x1 - bw - 8, y0 + 8, x1 - 8, y0 + 30], 5, fill=badge_fill)
    d.text((x1 - bw - 1, y0 + 11), badge, font=F(13, True), fill=(255, 255, 255))
    d.text((x0 + 10, y0 + 46), numbers, font=F(11, True), fill=BLUE)
    d.text((x0 + 10, y0 + 64), why, font=F(10), fill=INK)
    d.text((x0 + 10, y0 + 80), also, font=F(10), fill=MUT)
    d.text((x1 - 118, y1 - 16), "[C] CONFIRMED", font=F(8, True), fill=GREEN)

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # ---- header ----
    d.rectangle([0, 0, W, 52], fill=NAVY)
    d.rectangle([0, 52, W, 55], fill=GOLD)
    d.text((10, 9), "THE WORLD IN ONE DAY", font=F(26, True), fill=(255, 255, 255))
    d.text((10, 38), "50 STORIES  •  10 REGIONS  •  ALL THE NEWS THAT MATTERED", font=F(9, True), fill=(180, 195, 215))
    dt = "Wednesday 25 November 2026"
    d.text((W - 10 - d.textlength("DATE CHECK", font=F(9, True)), 9), "DATE CHECK", font=F(9, True), fill=GOLD)
    d.text((W - 10 - d.textlength(dt, font=F(16, True)), 24), dt, font=F(16, True), fill=(255, 255, 255))
    # ---- hero scene (Shenzhou-led) ----
    draw_scene(d, 8, 60, 600, 220)
    # caption strip under scene
    d.rectangle([8, 220, 600, 268], fill=NAVY)
    d.text((16, 225), "SHENZHOU-24 CARRIES PAKISTAN'S FIRST ASTRONAUT TO TIANGONG", font=F(13, True), fill=(255, 255, 255))
    d.text((16, 242), "Muhammad Zeeshan Ali, first foreigner aboard China's station  •  ALSO: two Chinese crew fly with Ali.", font=F(10), fill=(200, 210, 225))
    d.text((16, 255), "WHY IT MATTERS: China opens its station to the world; Pakistan reaches orbit.  [C]", font=F(10, True), fill=GOLD)
    # ---- hero cards ----
    hero_card(d, 608, 60, 1016, 160, "HERO 1  •  TRADE  •  NORTH AMERICA",
              "TRUMP'S NEW TARIFF SALVO",
              "14 partners  •  China 20% (40% if truce fails)  •  EU 15%",
              "WHY IT MATTERS: rewrites trade with every major partner.",
              "ALSO: hearing 25 Jan; Mexico, Norway spared for now.", "20%", RED)
    hero_card(d, 608, 168, 1016, 268, "HERO 2  •  MARKETS  •  EAST ASIA",
              "AI CHIP SELLOFF SINKS ASIA",
              "Kospi -6.16% to 4,697.51 • Samsung -9.87% • Hynix -11.05%",
              "WHY IT MATTERS: AI doubts now move whole markets.",
              "ALSO: S&P -2.2%, Nasdaq -3.2%; Japan, Taiwan slide too.", "-6.16%", RED)
    # ---- grid ----
    gx, gy, cw, ch, gap = 10, 272, 164, 41, 4
    overflow = []
    for i, (head, region, cert) in enumerate(STORIES):
        cx = gx + (i % 6) * (cw + gap)
        cy = gy + (i // 6) * (ch + gap)
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], 4, fill=CARD, outline=LINE)
        lines, ok = wrap(d, head, F(10), cw - 12, 2)
        if not ok:
            overflow.append((i + 1, head))
        for j, ln in enumerate(lines):
            d.text((cx + 6, cy + 3 + j * 12), ln, font=F(10), fill=INK)
        d.text((cx + 6, cy + ch - 12), region + "  ·  " + cert, font=F(8, True), fill=MUT)
    # ---- footer ----
    d.text((10, 630), "Sources: Reuters, AP, UN News, BBC, as reported 25 Nov 2026.  C = confirmed  •  R = reported  •  CL = claim.", font=F(8), fill=MUT)
    img.save("entry.png", optimize=True)
    print("stories:", 3 + len(STORIES), "regions:", len({r for _, r, _ in STORIES}))
    print("grid overflow (needs >2 lines):", overflow)
    print("size:", os.path.getsize("entry.png"), "bytes; dims:", img.size)

if __name__ == "__main__":
    main()
