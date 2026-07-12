"""
Silhouette-only ASCII art generator for GitHub README SVG.
Dark pixels (person's body) → characters. Bright background → pure SPACE.
"""
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import html, os, urllib.request

IMG_URL  = "https://avatars.githubusercontent.com/u/104557109?v=4"
IMG_PATH = r"d:\Mausam5055\profile_pic.jpg"
if not os.path.exists(IMG_PATH):
    urllib.request.urlretrieve(IMG_URL, IMG_PATH)

# Grid: SVG x=15..375 → ~38 chars wide max; keep 32 so there's clear padding
W, H = 32, 22

# Threshold: pixels < THRESHOLD → body char, >= THRESHOLD → space
THRESHOLD = 130
BODY_RAMP = "$@#%&W*o+="   # dense→light, 10 chars


def build_ascii(img_path, width, height):
    img = Image.open(img_path).convert("L")
    iw, ih = img.size

    # Crop: start from 30% down (skips noisy dark ceiling + hair-vs-bg ambiguity)
    # tight sides (18% each) to remove dark venue walls
    img = img.crop((int(iw * 0.22), int(ih * 0.30),
                    int(iw * 0.78), int(ih * 0.98)))

    # Median filter → kills point noise
    img = img.filter(ImageFilter.MedianFilter(size=3))

    # Heavy Gaussian blur → blends background into uniform bright mass
    img = img.filter(ImageFilter.GaussianBlur(radius=5))

    # Stretch histogram so dark shirt = 0, bright bg = 255
    img = ImageOps.autocontrast(img, cutoff=2)

    # Boost contrast + darken to sharpen person vs background
    img = ImageEnhance.Contrast(img).enhance(2.8)
    img = ImageEnhance.Brightness(img).enhance(0.78)

    # Resize to grid
    img = img.resize((width, height), Image.LANCZOS)

    # Threshold map: dark = body char, bright = space
    px       = img.load()
    ramp_len = len(BODY_RAMP) - 1
    rows     = []
    for y in range(height):
        row = ""
        for x in range(width):
            b = px[x, y]
            if b < THRESHOLD:
                idx  = int(b / THRESHOLD * ramp_len)
                row += BODY_RAMP[idx]
            else:
                row += " "
        rows.append(html.escape(row))
    return rows


def make_svg(ascii_lines, dark=True):
    bg    = "#161b22" if dark else "#f6f8fa"
    fg    = "#c9d1d9" if dark else "#24292f"
    key_c = "#ffa657" if dark else "#953800"
    val_c = "#a5d6ff" if dark else "#0a3069"
    add_c = "#3fb950" if dark else "#1a7f37"
    del_c = "#f85149" if dark else "#cf222e"
    cc_c  = "#616e7f" if dark else "#c2cfde"

    tspans = "\n".join(
        f'<tspan x="15" y="{30 + i * 20}">{ln}</tspan>'
        for i, ln in enumerate(ascii_lines)
    )

    return f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="985px" height="530px" font-size="16px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key   {{fill: {key_c};}}
.value {{fill: {val_c};}}
.addColor {{fill: {add_c};}}
.delColor {{fill: {del_c};}}
.cc    {{fill: {cc_c};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="985px" height="530px" fill="{bg}" rx="15"/>
<text x="15" y="30" fill="{fg}">
{tspans}
</text>
<text x="390" y="30" fill="{fg}">
<tspan x="390" y="30">mausam@github</tspan> -———————————————————————————————————————————-—-
<tspan x="390" y="50"  class="cc">. </tspan><tspan class="key">OS</tspan>:<tspan class="cc"> ........................ </tspan><tspan class="value">Windows 11, Android, Linux</tspan>
<tspan x="390" y="70"  class="cc">. </tspan><tspan class="key">Location</tspan>:<tspan class="cc"> .................... </tspan><tspan class="value">Assam, India &#x1F1EE;&#x1F1F3;</tspan>
<tspan x="390" y="90"  class="cc">. </tspan><tspan class="key">University</tspan>:<tspan class="cc"> .................. </tspan><tspan class="value">VIT Bhopal University</tspan>
<tspan x="390" y="110" class="cc">. </tspan><tspan class="key">IDE</tspan>:<tspan class="cc"> ....................... </tspan><tspan class="value">VSCode 1.96.0, Cursor AI</tspan>
<tspan x="390" y="130" class="cc">. </tspan>
<tspan x="390" y="150" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Programming</tspan>:<tspan class="cc"> ..... </tspan><tspan class="value">Python, Java, JavaScript, C++</tspan>
<tspan x="390" y="170" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Web</tspan>:<tspan class="cc"> .............. </tspan><tspan class="value">HTML, CSS, React, Node.js</tspan>
<tspan x="390" y="190" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Data</tspan>:<tspan class="cc"> ............. </tspan><tspan class="value">SQL, MongoDB, JSON, YAML</tspan>
<tspan x="390" y="210" class="cc">. </tspan>
<tspan x="390" y="230" class="cc">. </tspan><tspan class="key">Interests</tspan>.<tspan class="key">Dev</tspan>:<tspan class="cc"> .............. </tspan><tspan class="value">Full-Stack, AI/ML, Open Source</tspan>
<tspan x="390" y="250" class="cc">. </tspan><tspan class="key">Interests</tspan>.<tspan class="key">Tech</tspan>:<tspan class="cc"> ............. </tspan><tspan class="value">Cloud Computing, Emerging Tech</tspan>
<tspan x="390" y="270" class="cc">. </tspan>
<tspan x="390" y="290" class="cc">. </tspan><tspan class="key">Bio</tspan>:<tspan class="cc"> ..................... </tspan><tspan class="value">Learn to remove &apos;L&apos; &#x1F3C6;</tspan>
<tspan x="390" y="310">- Contact</tspan> -——————————————————————————————————————————————-—-
<tspan x="390" y="330" class="cc">. </tspan><tspan class="key">Email</tspan>.<tspan class="key">Personal</tspan>:<tspan class="cc"> ..................... </tspan><tspan class="value">rikikumkar@gmail.com</tspan>
<tspan x="390" y="350" class="cc">. </tspan><tspan class="key">Portfolio</tspan>:<tspan class="cc"> ............................ </tspan><tspan class="value">mausam04.vercel.app</tspan>
<tspan x="390" y="370" class="cc">. </tspan><tspan class="key">LinkedIn</tspan>:<tspan class="cc"> ............................. </tspan><tspan class="value">mausam-kar</tspan>
<tspan x="390" y="390" class="cc">. </tspan><tspan class="key">GitHub</tspan>:<tspan class="cc"> ............................... </tspan><tspan class="value">Mausam5055</tspan>
<tspan x="390" y="410" class="cc">. </tspan>
<tspan x="390" y="450">- GitHub Stats</tspan> -—————————————————————————————————————————-—-
<tspan x="390" y="470" class="cc">. </tspan><tspan class="key">Repos</tspan>:<tspan class="cc" id="repo_data_dots"> ........ </tspan><tspan class="value" id="repo_data">79</tspan> {{<tspan class="key">Contributed</tspan>: <tspan class="value" id="contrib_data">--</tspan>}} | <tspan class="key">Stars</tspan>:<tspan class="cc" id="star_data_dots"> ....... </tspan><tspan class="value" id="star_data">--</tspan>
<tspan x="390" y="490" class="cc">. </tspan><tspan class="key">Commits</tspan>:<tspan class="cc" id="commit_data_dots"> .................... </tspan><tspan class="value" id="commit_data">--</tspan> | <tspan class="key">Followers</tspan>:<tspan class="cc" id="follower_data_dots"> ....... </tspan><tspan class="value" id="follower_data">21</tspan>
<tspan x="390" y="510" class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:<tspan class="cc" id="loc_data_dots">. </tspan><tspan class="value" id="loc_data">--</tspan> ( <tspan class="addColor" id="loc_add">--</tspan><tspan class="addColor">++</tspan>, <tspan id="loc_del_dots"> </tspan><tspan class="delColor" id="loc_del">--</tspan><tspan class="delColor">--</tspan> )
</text>
</svg>"""


if __name__ == "__main__":
    lines = build_ascii(IMG_PATH, W, H)

    sep = "+" + "-" * W + "+"
    print(sep)
    for ln in lines:
        print("|" + ln + "|")
    print(sep)

    blank_rows = sum(1 for ln in lines if not ln.strip())
    print(f"\n{blank_rows} fully-blank rows / {len(lines)} total")

    for dark, fname in [(True,  r"d:\Mausam5055\dark_mode.svg"),
                        (False, r"d:\Mausam5055\light_mode.svg")]:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(make_svg(lines, dark=dark))
        print(f"✓ {fname}")

    if os.path.exists(IMG_PATH):
        os.remove(IMG_PATH)
    print("Done!")
