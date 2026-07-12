"""
ASCII art generator — works with a WHITE-background removed image.
Since background = white (brightness ~255), a simple threshold works perfectly:
  - bright white pixels (>230) → SPACE  (blank background)
  - dark/colored pixels (<=230) → ASCII char from BODY_RAMP
"""
from PIL import Image, ImageEnhance, ImageFilter
import sys, html, os, urllib.request, json

# ── INPUT: path to the background-removed image (white bg) ────────────────────
# Save your background-removed image into d:\Mausam5055\ and set the name here
IMG_PATH = r"d:\Mausam5055\profile_nobg.png"   # ← change filename if needed

if not os.path.exists(IMG_PATH):
    print(f"ERROR: Image not found at {IMG_PATH}")
    print("Please save your background-removed image there and re-run.")
    sys.exit(1)

# ── ASCII grid ────────────────────────────────────────────────────────────────
W, H = 44, 26

# Dense → sparse (dark shirt/hair → dense, medium skin → lighter)
BODY_RAMP = "$@#%&W*o+="

# Pixels brighter than this = white background → space
BG_THRESHOLD = 235


def build_ascii(img_path, width, height):
    img = Image.open(img_path).convert("RGBA")

    # If image has transparency, composite onto white background first
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    img = Image.alpha_composite(bg, img).convert("RGB")

    # Grayscale
    gray = img.convert("L")

    # Boost contrast so dark shirt = very dark, white bg = very bright
    gray = ImageEnhance.Contrast(gray).enhance(1.8)

    # Resize directly to grid
    gray = gray.resize((width, height), Image.LANCZOS)

    # Light sharpen
    gray = gray.filter(ImageFilter.UnsharpMask(radius=1, percent=100, threshold=2))

    px       = gray.load()
    ramp_len = len(BODY_RAMP) - 1
    rows     = []

    for y in range(height):
        row = ""
        for x in range(width):
            b = px[x, y]
            if b > BG_THRESHOLD:
                row += " "                            # white background → blank
            else:
                # 0 (black shirt) → '$',  ~BG_THRESHOLD (skin edge) → '='
                idx  = int(b / BG_THRESHOLD * ramp_len)
                row += BODY_RAMP[idx]
        rows.append(html.escape(row))
    return rows


def get_github_stats(username="Mausam5055"):
    stats = {"repos": "79", "followers": "21", "stars": "0"}
    try:
        # Fetch user stats
        req = urllib.request.Request(f"https://api.github.com/users/{username}", headers={"User-Agent": "Mozilla/5.0"})
        user_data = json.loads(urllib.request.urlopen(req).read())
        stats["repos"] = str(user_data.get("public_repos", stats["repos"]))
        stats["followers"] = str(user_data.get("followers", stats["followers"]))
        
        # Fetch stars across all repos
        req2 = urllib.request.Request(f"https://api.github.com/users/{username}/repos?per_page=100", headers={"User-Agent": "Mozilla/5.0"})
        repos_data = json.loads(urllib.request.urlopen(req2).read())
        stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
        stats["stars"] = str(stars)
    except Exception as e:
        print("Failed to fetch stats, using defaults:", e)
    return stats

def make_svg(ascii_lines, stats, dark=True):
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
<tspan x="390" y="30">mausam@github</tspan> <tspan class="cc">----------------------------------------------------</tspan>
<tspan x="390" y="50"  class="cc">. </tspan><tspan class="key">OS</tspan>:<tspan x="960" text-anchor="end" class="value">Windows 11, Android, Linux</tspan>
<tspan x="390" y="70"  class="cc">. </tspan><tspan class="key">Location</tspan>:<tspan x="960" text-anchor="end" class="value">Assam, India &#x1F1EE;&#x1F1F3;</tspan>
<tspan x="390" y="90"  class="cc">. </tspan><tspan class="key">University</tspan>:<tspan x="960" text-anchor="end" class="value">VIT Bhopal University</tspan>
<tspan x="390" y="110" class="cc">. </tspan><tspan class="key">IDE</tspan>:<tspan x="960" text-anchor="end" class="value">VSCode 1.96.0, Cursor AI</tspan>
<tspan x="390" y="130" class="cc">. </tspan>
<tspan x="390" y="150" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Programming</tspan>:<tspan x="960" text-anchor="end" class="value">Python, Java, JavaScript, C++</tspan>
<tspan x="390" y="170" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Web</tspan>:<tspan x="960" text-anchor="end" class="value">HTML, CSS, React, Node.js</tspan>
<tspan x="390" y="190" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Data</tspan>:<tspan x="960" text-anchor="end" class="value">SQL, MongoDB, JSON, YAML</tspan>
<tspan x="390" y="210" class="cc">. </tspan>
<tspan x="390" y="230" class="cc">. </tspan><tspan class="key">Interests</tspan>.<tspan class="key">Dev</tspan>:<tspan x="960" text-anchor="end" class="value">Full-Stack, AI/ML, Open Source</tspan>
<tspan x="390" y="250" class="cc">. </tspan><tspan class="key">Interests</tspan>.<tspan class="key">Tech</tspan>:<tspan x="960" text-anchor="end" class="value">Cloud Computing, Emerging Tech</tspan>
<tspan x="390" y="270" class="cc">. </tspan>
<tspan x="390" y="290" class="cc">. </tspan><tspan class="key">Bio</tspan>:<tspan x="960" text-anchor="end" class="value">Learn to remove &apos;L&apos; &#x1F3C6;</tspan>
<tspan x="390" y="310" class="key">Contact</tspan> <tspan class="cc">----------------------------------------------------------</tspan>
<tspan x="390" y="330" class="cc">. </tspan><tspan class="key">Email</tspan>.<tspan class="key">Personal</tspan>:<tspan x="960" text-anchor="end" class="value">rikikumkar@gmail.com</tspan>
<tspan x="390" y="350" class="cc">. </tspan><tspan class="key">Portfolio</tspan>:<tspan x="960" text-anchor="end" class="value">mausam04.vercel.app</tspan>
<tspan x="390" y="370" class="cc">. </tspan><tspan class="key">LinkedIn</tspan>:<tspan x="960" text-anchor="end" class="value">mausam-kar</tspan>
<tspan x="390" y="390" class="cc">. </tspan><tspan class="key">GitHub</tspan>:<tspan x="960" text-anchor="end" class="value">Mausam5055</tspan>
<tspan x="390" y="410" class="cc">. </tspan>
<tspan x="390" y="450" class="key">GitHub Stats</tspan> <tspan class="cc">-----------------------------------------------------</tspan>
<tspan x="390" y="470" class="cc">. </tspan><tspan class="key">Repos</tspan>:<tspan x="960" text-anchor="end" class="value">{stats['repos']}</tspan>
<tspan x="390" y="490" class="cc">. </tspan><tspan class="key">Stars</tspan>:<tspan x="960" text-anchor="end" class="value">{stats['stars']}</tspan>
<tspan x="390" y="510" class="cc">. </tspan><tspan class="key">Followers</tspan>:<tspan x="960" text-anchor="end" class="value">{stats['followers']}</tspan>
</text>
</svg>"""


if __name__ == "__main__":
    print(f"Loading {IMG_PATH} …")
    lines = build_ascii(IMG_PATH, W, H)

    sep = "+" + "-" * W + "+"
    print(f"\nPreview ({H} lines x {W} chars):")
    print(sep)
    for ln in lines:
        print("|" + ln + "|")
    print(sep)

    blank = sum(1 for ln in lines if not ln.strip())
    print(f"\nBlank rows: {blank}/{H}")

    print("\nFetching GitHub Stats...")
    stats = get_github_stats()
    print(f"Stats loaded: {stats}")

    for dark, fname in [(True,  r"d:\Mausam5055\dark_mode.svg"),
                        (False, r"d:\Mausam5055\light_mode.svg")]:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(make_svg(lines, stats, dark=dark))
        print(f"✓ {fname}")

    print("Done!")
