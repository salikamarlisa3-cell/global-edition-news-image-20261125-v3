#!/usr/bin/env python3
"""Poster builder for the Global Edition of Wednesday 25 Nov 2026.

Emits poster.svg (a build artifact) from the verified story table
below; generate.mjs renders it to entry.png and main.ts delivers that
PNG to the judge unchanged. Sources for every story: SOURCES.md.
Data note: 16 stories were refreshed against Just Security's Early
Edition of 25 Nov 2026 itself (tags marked "via JS"); where it
superseded an earlier wire claim (stories 9, 20, 30) the newer
account is the one printed here.
"""
from xml.sax.saxutils import escape as esc

# region name | bar colour | stories as "headline ~ outlet" lines
DATA = """
NORTH AMERICA|#1f5fa6
Dow tops 50,000 for first time, +0.85% to 50,018.70 ~ Investopedia
Nvidia falls 5.86% a day after +31% surge ~ Reuters
US consumer confidence jumps to 103.3 in November ~ Reuters
USTR to announce higher tariffs on China, EU + 14 ~ AP via JS
Senate panel probes Vance role in Vitol oil deal ~ Reuters via JS
Court finds Huawei guilty of conspiracy, bank fraud ~ BBC via JS
Rep. Jimmy Gomez to resign after ethics finding ~ NYT via JS
Sullivan concedes Alaska Senate race to Peltola ~ NYT via JS
Abrego Garcia leaves US for Spain, 'leaving happy' ~ NYT via JS
LATIN AMERICA & CARIBBEAN|#2e8b57
Mexico to try 'El Chapo Isidro' despite US request ~ Reuters
Bolsonaro in ICU with bowel obstruction, stable ~ Al Jazeera
Brazil lifts 2027 inflation forecast to 4.5% ~ MercoPress
Argentina economy shrank 1.2% y/y in September ~ Rio Times
WHO chief: lift US fuel blockade on Cuba ~ Reuters via JS
Drone attack on Colombia police base hurts civilians ~ Al Jazeera
Peru dengue outbreak: 45 dead, 20,000+ cases ~ Rio Times
EUROPE|#5b4fa6
Lukashenko proposes flying with Zelenskiy to Moscow ~ Reuters
Moscow accuses Estonia of acts on verge of war ~ Al Jazeera
Russian strike on Odesa kills 2, injures 3 ~ Reuters via JS
Libya vows retaliation over drone hit on Russian ship ~ AP via JS
NATO's Rutte: alliance will defend in space too ~ BBC via JS
Poland: peace deal won't end Russian sabotage ~ Politico via JS
Putin: retaliation for refinery strikes 'inevitable' ~ Reuters via JS
Europe launches 36 satellites for Amazon's Kuiper ~ Bloomberg
Merz accuses Russia of escalating threats to Europe ~ Reuters via JS
MIDDLE EAST & NORTH AFRICA|#b3541e
Israel kills Hamas security chief Abuelouf + family ~ Reuters via JS
Israeli strike kills UNRWA worker at Jabalia well ~ Reuters via JS
Eisenkot clinches first coalition agreement ~ Reuters
Iran VP: US blockade does not worry Tehran ~ Reuters via JS
IRGC: two tankers hit mines in Hormuz, ablaze ~ Reuters via JS
Houthi strike on Riyadh tower injures 11 ~ NYT via JS
Houthis claim Ras Tanura refinery attack ~ Reuters via JS
Vance, Rubio meet Qatari PM at White House ~ AP via JS
SUB-SAHARAN AFRICA|#967014
Zambia opposition leader charged with treason ~ Reuters
Migrant boat capsizes off Senegal; ~175 missing ~ OkayAfrica
CAS reinstates Senegal as 2025 AFCON champions ~ PANA
Amnesty: Tigray shelling may be war crimes ~ Reuters via JS
DRC army hunts missing cargo plane ~ OkayAfrica
DRC to force foreign miners to open local units ~ OkayAfrica
Gavi to buy up to 1.5M experimental Ebola doses ~ OkayAfrica
RSF drone strikes kill 19 civilians in Sudan ~ Reuters via JS
ASIA-PACIFIC|#14828c
China investigates Politburo member Chen Jining ~ Reuters
Japan to pay full 2027 ICC contribution early ~ Reuters via JS
S. Korea offers $375k rewards vs AI exam cheats ~ WSJ via JS
Russian jets enter S. Korea air defence zone ~ AP via JS
Hasina plans return to Bangladesh on Dec 16 ~ Reuters via JS
Solomons + Australia sign treaty barring foreign base ~ NYT via JS
Singapore probes Megaspeed after US blacklisting ~ Reuters
China extends pause on US minerals curbs 2 months ~ SCMP
Hanoi gas blast kills 6, injures 10 at restaurant ~ World Now
GLOBAL: MARKETS, CULTURE & SPORT|#78285a
Champions League: Real Madrid 5-1 PSV; City 2-2 Napoli ~ SuperSport
Record quasar seen 630M years after the Big Bang ~ Reuters/AP
Titanium oxide found around young star Orion I ~ Phys.org
Pope Leo XIV laments COP31 failure to agree ~ AP via JS
Anthropic shares fall below IPO price in sell-off ~ Investopedia
Gold -2.7% to $3,552.80; oil up on Hormuz attacks ~ StockMktWatch
"""

LEADS = [
    (1, "Dow tops 50,000", "first time"), (30, "Hormuz tankers", "hit mines"),
    (20, "Libya vows", "retaliation"), (52, "Oldest quasar", "630M yrs after BB"),
    (47, "Solomons treaty", "no foreign base"), (41, "Sudan drones", "19 killed"),
    (19, "Odesa strike", "2 killed"), (9, "Abrego Garcia", "leaves US"),
    (35, "Senegal boat", "~175 missing"), (56, "Gold -2.7%", "$3,552.80"),
    (6, "Huawei guilty", "conspiracy"), (26, "Hamas chief", "killed"),
    (14, "Cuba blockade", "WHO warning"), (51, "Real Madrid 5-1", "Champions League"),
    (44, "AI exam cheats", "$375k rewards"), (2, "Nvidia -5.86%", "after +31% surge"),
]

WEATHER = ("WEATHER (Open-Meteo, 25 Nov 02:26 UTC) - New York 3C clear - "
           "Quito 13C overcast - London 5C overcast - Tokyo 11C clear - "
           "Sydney 21C overcast - Mumbai 24C clear - Singapore 29C drizzle - "
           "Sao Paulo 23C drizzle")

LEFT_OUT = [
    ("LEFT OUT & WHY - DATE CHECK", True),
    ("Held back: anything filed before 24 Nov 2026 UTC - an item is", False),
    ("only on this page if it belongs to the 25 Nov (Asia) cycle.", False),
    ("Where Just Security's Early Edition of 25 Nov superseded an", False),
    ("earlier wire claim (stories 9, 20, 30), this page prints the", False),
    ("newer account, not the first report.", False),
]

MAP = [
    "        ####  ##                                                        ",
    "      ############        #####   #######  ########                     ",
    "     ##############      ##################################  ####       ",
    "      ############        #####################################         ",
    "       #########           ##################################  ##       ",
    "        ######   #          ###############################             ",
    "         ####  ####          ################  ##########               ",
    "          ##  ######          ##############      ######                ",
    "              ######           ##########        ####  ##               ",
    "              #####             ########          ##                    ",
    "               ####              ######           ##   #                ",
    "               ###                ####            #  ####               ",
    "                ##                 ##                 #####             ",
    "                #                                      ######           ",
    "                                                         ####    #      ",
    "                                                          ##   ###      ",
    "                                                               ###      ",
    "                                                                #       ",
]
PIN_XY = [(13, 3), (17, 12), (47, 2), (54, 6), (50, 11), (66, 6), (36, 16)]
LEGEND = ["North America", "Latin America", "Europe", "Middle East & N. Africa",
          "Sub-Saharan Africa", "Asia-Pacific", "Global"]

INK, MUTE, RED = "#1a1a1e", "#605c54", "#b22222"


class Page:
    def __init__(self):
        self.parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1024" '
                      'height="1024" viewBox="0 0 1024 1024">',
                      '<rect width="1024" height="1024" fill="#f7f3ea"/>']

    def t(self, x, y, s, size, fill=INK, bold=False, mid=False):
        b = ' font-weight="bold"' if bold else ""
        a = ' text-anchor="middle"' if mid else ""
        self.parts.append(
            '<text x="%d" y="%d" font-family="DejaVu Sans, sans-serif" '
            'font-size="%d" fill="%s"%s%s>%s</text>'
            % (x, y, size, fill, b, a, esc(s)))

    def r(self, x, y, w, h, fill=None, stroke=None):
        f = 'fill="%s"' % fill if fill else 'fill="none"'
        s = ' stroke="%s"' % stroke if stroke else ""
        self.parts.append('<rect x="%d" y="%d" width="%d" height="%d" %s%s/>'
                          % (x, y, w, h, f, s))

    def c(self, cx, cy, rad, fill):
        self.parts.append('<circle cx="%d" cy="%d" r="%d" fill="%s"/>'
                          % (cx, cy, rad, fill))

    def save(self, path):
        self.parts.append("</svg>")
        with open(path, "w") as fh:
            fh.write("\n".join(self.parts) + "\n")


def parse(data):
    regions, cur = [], None
    for raw in data.strip().split("\n"):
        line = raw.strip()
        if "|" in line and "~" not in line:
            name, color = line.split("|")
            cur = (name, color, [])
            regions.append(cur)
        elif line:
            head, tag = line.split(" ~ ")
            cur[2].append((head, tag))
    return regions


def main():
    regions = parse(DATA)
    p = Page()
    p.t(24, 42, "THE WORLD IN ONE DAY", 34, bold=True)
    p.t(24, 64, "Global Edition - Wednesday 25 November 2026 - 56 stories - "
                "7 regions - every story sourced", 13, fill=MUTE)
    p.r(24, 70, 976, 3, fill=RED)
    for ri, row in enumerate(MAP):
        for ci, ch in enumerate(row):
            if ch == "#":
                p.c(26 + ci * 10, 86 + ri * 6, 2, "#78766e")
    for n, (col, row) in enumerate(PIN_XY, start=1):
        x, y = 24 + col * 10, 84 + row * 6
        p.c(x, y, 8, RED)
        p.t(x, y + 4, str(n), 11, fill="#ffffff", bold=True, mid=True)
    p.t(776, 94, "REGIONS", 11, bold=True)
    for i, nm in enumerate(LEGEND):
        yy = 104 + i * 13
        p.c(780, yy - 3, 5, RED)
        p.t(780, yy, str(i + 1), 8, fill="#ffffff", bold=True, mid=True)
        p.t(790, yy, "%s - %d" % (nm, len(regions[i][2])), 10)

    p.t(24, 214, "FRONT PAGE - 16 LEADS", 11, fill=RED, bold=True)
    for i, (num, l1, l2) in enumerate(LEADS):
        x = 24 + (i % 8) * 122
        y = 222 + (i // 8) * 40
        p.r(x, y, 116, 34, fill="#eee7d8", stroke=MUTE)
        p.t(x + 5, y + 22, str(num), 17, fill=RED, bold=True)
        p.t(x + 30, y + 14, l1, 9)
        p.t(x + 30, y + 25, l2, 9)

    def block(x, y, w, idx, first_no):
        name, color, stories = regions[idx]
        p.r(x, y, w, 19, fill=color)
        p.t(x + 6, y + 14, "%s - %d STORIES" % (name, len(stories)), 13,
            fill="#ffffff", bold=True)
        y += 24
        for j, (head, tag) in enumerate(stories):
            p.t(x + 2, y + 11, "%d. %s - %s" % (first_no + j, head, tag), 12)
            y += 15
        return y + 6

    y = block(24, 302, 476, 0, 1)
    y = block(24, y, 476, 1, 10)
    y = block(24, y, 476, 2, 17)
    p.r(24, y + 2, 476, 12 + len(LEFT_OUT) * 13, stroke=RED)
    for i, (ln, bold) in enumerate(LEFT_OUT):
        p.t(30, y + 17 + i * 13, ln, 11 if bold else 10,
            fill=RED if bold else INK, bold=bold)
    y2 = block(524, 302, 476, 3, 26)
    y2 = block(524, y2, 476, 4, 34)
    y2 = block(524, y2, 476, 5, 42)
    y2 = block(524, y2, 476, 6, 51)

    p.r(24, 926, 976, 1, fill=MUTE)
    p.t(24, 946, "BY THE NUMBERS - 56 stories - 7 regions - 16 leads - "
                 "25+ outlets - 1 news day", 11, bold=True)
    cut = WEATHER.rindex(" - ", 0, 118)
    p.t(24, 968, WEATHER[:cut], 11)
    p.t(24, 982, WEATHER[cut + 3:], 11)
    p.t(24, 1006, "Sources: Just Security Early Edition (25 Nov 2026), "
                  "Reuters, AP, NYT, BBC, Al Jazeera + more - full list "
                  "in SOURCES.md", 10, fill=MUTE)
    p.save("poster.svg")
    print("poster.svg written")


if __name__ == "__main__":
    main()
