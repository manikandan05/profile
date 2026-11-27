#!/usr/bin/env python3
"""Generates assets/hero-scene.svg: an original dusk illustration of a boy coding on a hill.

Run: python3 tools/make_scene.py
Animation uses only transform and opacity, and is switched off under prefers-reduced-motion.
"""
import pathlib
import random

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "hero-scene.svg"
random.seed(7)

# Stars (upper sky only)
stars = []
for i in range(70):
    x, y = random.randint(20, 1580), random.randint(10, 380)
    r = random.choice([1, 1, 1.4, 1.8])
    cls = ' class="tw" style="animation-delay:%.1fs"' % random.uniform(0, 6) if i % 3 == 0 else ""
    stars.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff6e0" opacity="{random.choice([0.5, 0.7, 0.9])}"{cls}/>')

# Fireflies
flies = []
for i in range(22):
    x, y = random.randint(620, 1560), random.randint(520, 760)
    d = random.uniform(0, 8)
    flies.append(
        f'<g class="ff" style="animation-delay:{d:.1f}s;animation-duration:{random.uniform(6, 11):.1f}s">'
        f'<circle cx="{x}" cy="{y}" r="9" fill="#ffe9a8" opacity="0.18"/>'
        f'<circle cx="{x}" cy="{y}" r="2.6" fill="#fff4c8"/></g>'
    )

# Code lines on the laptop screen: (x, y, width, colour)
code = [
    (8, 10, 34, "#ff8fb5"), (46, 10, 28, "#8fb7ff"),
    (14, 22, 52, "#7ee7a8"), (70, 22, 18, "#ffd479"),
    (14, 34, 24, "#8fb7ff"), (42, 34, 40, "#e8eefc"),
    (22, 46, 60, "#7ee7a8"),
    (22, 58, 30, "#ffd479"), (56, 58, 26, "#ff8fb5"),
    (14, 70, 44, "#8fb7ff"),
]
code_svg = []
for i, (x, y, w, c) in enumerate(code):
    code_svg.append(
        f'<rect class="ln" x="{x}" y="{y}" width="{w}" height="5" rx="2.5" fill="{c}" '
        f'style="animation-delay:{i * 0.55:.2f}s"/>'
    )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Illustration of a boy sitting on a hill at dusk, typing on a laptop where code is running">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#070b1f"/><stop offset="0.38" stop-color="#1a2760"/>
<stop offset="0.64" stop-color="#6d4a8f"/><stop offset="0.8" stop-color="#d9738a"/><stop offset="1" stop-color="#f6b070"/>
</linearGradient>
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
<stop offset="0" stop-color="#ffc98a" stop-opacity="0.75"/><stop offset="1" stop-color="#ffc98a" stop-opacity="0"/>
</radialGradient>
<radialGradient id="scr" cx="0.5" cy="0.5" r="0.5">
<stop offset="0" stop-color="#8fffd0" stop-opacity="0.55"/><stop offset="1" stop-color="#8fffd0" stop-opacity="0"/>
</radialGradient>
<g id="cloud">
<ellipse cx="0" cy="24" rx="132" ry="22" fill="#a77aa8"/>
<circle cx="-70" cy="6" r="32" fill="#f2cfda"/><circle cx="-18" cy="-14" r="46" fill="#f6d9e0"/>
<circle cx="46" cy="-2" r="38" fill="#f2cfda"/><circle cx="96" cy="12" r="26" fill="#eec3d3"/>
<circle cx="-28" cy="-24" r="30" fill="#fff0ec"/><circle cx="36" cy="-12" r="22" fill="#fff0ec"/>
</g>
</defs>
<style>
.tw{{animation:tw 5s ease-in-out infinite}}
.ff{{animation:ff 8s cubic-bezier(0.22,1,0.36,1) infinite;opacity:0}}
.ln{{transform-box:fill-box;transform-origin:left center;animation:type 7s cubic-bezier(0.22,1,0.36,1) infinite}}
.cur{{animation:blink 1s steps(2,jump-none) infinite}}
.pulse{{animation:pulse 3.2s ease-in-out infinite}}
.c1{{animation:drift 70s ease-in-out infinite alternate}}
.c2{{animation:drift 90s ease-in-out infinite alternate-reverse}}
.gl{{animation:rise 7s cubic-bezier(0.22,1,0.36,1) infinite;opacity:0}}
@keyframes tw{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
@keyframes ff{{0%{{opacity:0;transform:translate(0,0)}}20%{{opacity:1}}80%{{opacity:1}}100%{{opacity:0;transform:translate(26px,-60px)}}}}
@keyframes type{{0%{{transform:scaleX(0)}}18%,86%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}
@keyframes blink{{0%{{opacity:1}}100%{{opacity:0}}}}
@keyframes pulse{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}
@keyframes drift{{from{{transform:translateX(-30px)}}to{{transform:translateX(50px)}}}}
@keyframes rise{{0%{{opacity:0;transform:translateY(0)}}25%{{opacity:.9}}100%{{opacity:0;transform:translateY(-110px)}}}}
@media (prefers-reduced-motion:reduce){{.tw,.ff,.ln,.cur,.pulse,.c1,.c2,.gl{{animation:none}}.ff{{opacity:.7}}.gl{{opacity:.7}}}}
</style>

<rect width="1600" height="900" fill="url(#sky)"/>
{''.join(stars)}
<circle cx="1500" cy="150" r="92" fill="#fff1c9" opacity="0.12"/>
<circle cx="1500" cy="150" r="52" fill="#fff1c9" opacity="0.2"/>
<circle cx="1500" cy="150" r="34" fill="#fff6dc"/>
<circle cx="1512" cy="142" r="30" fill="#f4e3b8" opacity="0.55"/>

<g class="c1"><use href="#cloud" transform="translate(360 300) scale(1.1)"/></g>
<g class="c2"><use href="#cloud" transform="translate(980 420) scale(0.8)"/></g>
<g class="c1"><use href="#cloud" transform="translate(1440 330) scale(0.62)"/></g>

<ellipse cx="900" cy="690" rx="760" ry="150" fill="url(#glow)"/>

<path d="M0 640 C160 590 300 610 460 600 C640 590 760 640 960 620 C1160 600 1380 590 1600 630 L1600 900 L0 900Z" fill="#6a4f93"/>
<path d="M0 690 C200 640 360 676 560 654 C760 632 940 690 1160 660 C1340 636 1480 650 1600 676 L1600 900 L0 900Z" fill="#43467f"/>

<g fill="#ffd98a"><rect x="610" y="650" width="6" height="8" rx="1"/><rect x="626" y="652" width="6" height="8" rx="1"/><rect x="760" y="662" width="6" height="8" rx="1"/></g>
<path d="M600 662 L620 640 L644 662Z M752 672 L772 650 L792 672Z" fill="#2c2d5c"/>
<rect x="602" y="660" width="40" height="20" fill="#2c2d5c"/><rect x="754" y="670" width="36" height="20" fill="#2c2d5c"/>

<path d="M0 740 C240 700 480 730 720 716 C960 702 1120 740 1360 724 C1480 716 1560 722 1600 730 L1600 900 L0 900Z" fill="#1f3a63"/>

<g>
<rect x="906" y="590" width="22" height="150" rx="8" fill="#1a2b3d"/>
<circle cx="860" cy="560" r="78" fill="#10343a"/><circle cx="960" cy="548" r="86" fill="#10343a"/>
<circle cx="910" cy="486" r="92" fill="#10343a"/><circle cx="820" cy="610" r="56" fill="#10343a"/>
<circle cx="1002" cy="610" r="60" fill="#10343a"/>
<circle cx="880" cy="470" r="58" fill="#17504a"/><circle cx="950" cy="520" r="44" fill="#17504a"/>
<circle cx="846" cy="548" r="34" fill="#17504a"/>
<path d="M870 700 Q910 640 950 700" fill="none" stroke="#0a2024" stroke-width="3"/>
</g>

<path d="M560 900 L560 790 C760 742 1000 716 1260 712 C1420 710 1520 746 1600 770 L1600 900Z" fill="#12302f"/>
<path d="M560 800 C760 756 1000 730 1260 728 C1420 726 1520 758 1600 782" fill="none" stroke="#2a6a55" stroke-width="5" opacity="0.7"/>
<path d="M0 860 C300 820 700 850 1000 836 C1300 822 1500 846 1600 850 L1600 900 L0 900Z" fill="#000000"/>

<g class="pulse"><ellipse cx="1130" cy="640" rx="190" ry="130" fill="url(#scr)"/></g>

<g>
<rect x="1000" y="676" width="150" height="46" rx="6" fill="#7a5640"/>
<rect x="1000" y="676" width="150" height="9" rx="4" fill="#a37a58"/>
<ellipse cx="1124" cy="703" rx="12" ry="8" fill="none" stroke="#5a3c2c" stroke-width="2"/>

<path d="M1010 672 L1166 672 L1180 681 L1026 681Z" fill="#d6dcec"/>
<path d="M1026 681 L1180 681 L1180 685 L1026 685Z" fill="#9aa3bd"/>
<g transform="translate(1030 556) skewY(-6.5)">
<rect x="0" y="0" width="122" height="112" rx="5" fill="#1a1f36"/>
<rect x="5" y="5" width="112" height="102" rx="3" fill="#0b1626"/>
<g transform="translate(6 6)">
<rect x="0" y="0" width="110" height="8" fill="#14233a"/>
<circle cx="7" cy="4" r="1.8" fill="#ff7b7b"/><circle cx="13" cy="4" r="1.8" fill="#ffd479"/><circle cx="19" cy="4" r="1.8" fill="#7ee7a8"/>
{''.join(code_svg)}
<rect class="cur" x="52" y="82" width="5" height="9" fill="#e8eefc"/>
<rect x="8" y="82" width="38" height="9" rx="2" fill="#12311f"/><text x="12" y="89.5" font-family="ui-monospace,Menlo,monospace" font-size="7" fill="#7ee7a8">running</text>
<circle class="pulse" cx="100" cy="86" r="3.2" fill="#7ee7a8"/>
</g>
</g>
</g>

<g font-family="ui-monospace,Menlo,monospace" font-size="22" fill="#9ef0c0">
<text class="gl" x="1060" y="540" style="animation-delay:0s">{{ }}</text>
<text class="gl" x="1110" y="520" style="animation-delay:1.8s">&lt;/&gt;</text>
<text class="gl" x="1150" y="548" style="animation-delay:3.6s">01</text>
<text class="gl" x="1090" y="560" style="animation-delay:5.2s">;</text>
</g>

<g>
<path d="M1340 704 C1318 702 1262 700 1240 694" fill="none" stroke="#2f3d73" stroke-width="24" stroke-linecap="round"/>
<path d="M1240 694 C1236 718 1262 722 1296 718" fill="none" stroke="#263262" stroke-width="20" stroke-linecap="round"/>
<ellipse cx="1236" cy="698" rx="11" ry="9" fill="#efe9db"/>
<path d="M1352 706 C1366 668 1350 628 1316 606 C1296 594 1276 604 1276 624 C1278 652 1296 676 1298 706Z" fill="#d9573f"/>
<path d="M1280 624 C1282 650 1298 676 1300 700 L1310 700 C1306 672 1292 646 1290 616Z" fill="#f08a5d" opacity="0.8"/>
<path d="M1302 628 C1270 650 1218 662 1186 666" fill="none" stroke="#d9573f" stroke-width="15" stroke-linecap="round"/>
<path d="M1302 628 C1270 650 1218 662 1186 666" fill="none" stroke="#f08a5d" stroke-width="4" stroke-linecap="round" opacity="0.7" transform="translate(0 -4)"/>
<circle cx="1182" cy="667" r="7.5" fill="#f4c9a0"/>
<rect x="1288" y="592" width="12" height="16" rx="5" fill="#f4c9a0"/>
<circle cx="1290" cy="568" r="26" fill="#f4c9a0"/>
<path d="M1264 574 C1258 538 1286 526 1312 538 C1330 548 1328 574 1318 592 C1314 574 1304 560 1290 556 C1278 556 1268 564 1264 574Z" fill="#2a1b1b"/>
<path d="M1296 534 C1290 520 1300 512 1308 508 C1304 518 1306 526 1306 536Z" fill="#2a1b1b"/>
<path d="M1264 574 C1262 560 1270 550 1280 548 C1276 556 1274 566 1276 576Z" fill="#3a2626"/>
<ellipse cx="1274" cy="580" rx="5" ry="3.4" fill="#f09a8a" opacity="0.7"/>
<circle cx="1275" cy="570" r="2.6" fill="#1a1010"/><circle cx="1276" cy="569" r="0.9" fill="#ffffff"/>
<path d="M1264 584 q4 3 8 1" fill="none" stroke="#a5604f" stroke-width="1.6" stroke-linecap="round"/>
<path d="M1262 576 l-5 3 l5 1" fill="none" stroke="#d9a07e" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
<ellipse cx="1310" cy="580" rx="5" ry="7" fill="#e8b88f"/>
</g>

<g fill="#0a2326">
<path d="M1500 860 l-5 -30 l9 24 l6 -26 l3 32Z"/><path d="M1380 862 l-4 -22 l8 18 l4 -20 l2 24Z"/><path d="M1060 858 l-4 -24 l8 20 l5 -22 l2 26Z"/>
</g>
{''.join(flies)}
</svg>
'''
OUT.write_text(svg)
print("wrote", OUT, len(svg), "bytes")
