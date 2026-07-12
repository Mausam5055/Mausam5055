"""
Silhouette-only ASCII art generator for GitHub README SVG.
Approach: THRESHOLD — dark pixels (person's body) → characters,
           bright pixels (background) → pure SPACE (blank).
Result: clean body outline, blank rest.
"""
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import html, os, urllib.request

# ── Download profile picture ───────────────────────────────────────────────────
IMG_URL  = "https://avatars.githubusercontent.com/u/104557109?v=4"
IMG_PATH = r"d:\Mausam5055\profile_pic.jpg"
if not os.path.exists(IMG_PATH):
    urllib.request.urlretrieve(IMG_URL, IMG_PATH)
    print("Downloaded profile picture")

# ── ASCII grid dimensions ──────────────────────────────────────────────────────
# SVG: x=15..~375 → ~40 chars wide,  y=30..510 step=20 → 25 lines
W, H = 40, 25

# ── Threshold settings ────────────────────────────────────────────────────────
# pixels with brightness < THRESHOLD  →  body  →  gets a char
# pixels with brightness >= THRESHOLD →  background  →  pure space
THRESHOLD = 155      # tune: raise to capture more skin/face, lower to tighten

# Chars used ONLY for the person zone  (dense=very dark, light=slightly dark)
BODY_RAMP = "$@#%&W*o+="   # 10 chars


def build_ascii(img_path, width, height):
    img = Image.open(img_path).convert("L")
    iw, ih = img.size

    # 1. Crop — skip noisy venue ceiling (top 12%) and trim 3% sides/bottom
    img = img.crop((int(iw * 0.03), int(ih * 0.12),
                    int(iw * 0.97), int(ih * 0.98)))

    # 2. Median filter first — kills point-noise (chair legs, lights, etc.)
    img = img.filter(ImageFilter.MedianFilter(size=3))

    # 3. Heavy Gaussian blur — merges background details into smooth bright mass
    img = img.filter(ImageFilter.GaussianBlur(radius=5))

    # 4. Autocontrast — dark shirt stretches to near-0, bright bg to near-255
    img = ImageOps.autocontrast(img, cutoff=2)

    # 5. Extra contrast + darken — sharpens person vs background boundary
    img = ImageEnhance.Contrast(img).enhance(2.8)
    img = ImageEnhance.Brightness(img).enhance(0.78)

    # 6. Resize to grid (each pixel → one ASCII char, no duplicate rows)
    img = img.resize((width, height), Image.LANCZOS)

    # 7. Threshold map
    px       = img.load()
    ramp_len = len(BODY_RAMP) - 1
    rows     = []
    for y in range(height):
        row = ""
        for x in range(width):
            b = px[x, y]
            if b < THRESHOLD:
                # Scale 0..THRESHOLD-1  →  BODY_RAMP index
                idx  = int(b / THRESHOLD * ramp_len)
                row += BODY_RAMP[idx]
            else:
                row += " "   # background = blank
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

    # Terminal preview
    print(f"Preview ({len(lines)} lines x {len(lines[0])} chars)\n")
    sep = "+" + "-" * len(lines[0]) + "+"
    print(sep)
    for ln in lines:
        print("|" + ln + "|")
    print(sep)

    # Count how many rows have any body chars (sanity check)
    filled = sum(1 for ln in lines if ln.strip())
    print(f"\n{filled}/{len(lines)} rows contain body chars")

    # Write SVGs
    for dark, fname in [(True,  r"d:\Mausam5055\dark_mode.svg"),
                        (False, r"d:\Mausam5055\light_mode.svg")]:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(make_svg(lines, dark=dark))
        mode = "dark" if dark else "light"
        print(f"✓ Written {mode}_mode.svg")

    if os.path.exists(IMG_PATH):
        os.remove(IMG_PATH)
    print("Done!")
