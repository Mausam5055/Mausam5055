"""
ASCII art generator — works with a WHITE-background removed image.
Since background = white (brightness ~255), a simple threshold works perfectly:
  - bright white pixels (>230) → SPACE  (blank background)
  - dark/colored pixels (<=230) → ASCII char from BODY_RAMP
"""
from PIL import Image, ImageEnhance, ImageFilter
import sys, html, os, urllib.request, json, random, textwrap

QUOTES = [
    ("Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "Martin Fowler"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Experience is the name everyone gives to their mistakes.", "Oscar Wilde"),
    ("Java is to JavaScript what car is to Carpet.", "Chris Heilmann"),
    ("Sometimes it pays to stay in bed on Monday, rather than spending the rest of the week debugging Monday's code.", "Dan Salomon"),
    ("Perfection is achieved not when there is nothing more to add, but rather when there is nothing more to take away.", "Antoine de Saint-Exupery"),
    ("Code is like humor. When you have to explain it, it's bad.", "Cory House"),
    ("Fix the cause, not the symptom.", "Steve Maguire"),
    ("Optimism is an occupational hazard of programming: feedback is the treatment.", "Kent Beck"),
    ("Simplicity is the soul of efficiency.", "Austin Freeman"),
    ("Before software can be reusable it first has to be usable.", "Ralph Johnson"),
    ("Make it work, make it right, make it fast.", "Kent Beck")
]

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
    stats = {"repos": "79", "followers": "21", "stars": "0", "commits": "--"}
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
        
        # Fetch total commits
        req3 = urllib.request.Request(f"https://api.github.com/search/commits?q=author:{username}&per_page=1", headers={"Accept": "application/vnd.github.cloak-preview", "User-Agent": "Mozilla/5.0"})
        commits_data = json.loads(urllib.request.urlopen(req3).read())
        if "total_count" in commits_data:
            stats["commits"] = f"{commits_data['total_count']:,}"
    except Exception as e:
        print("Failed to fetch stats, using defaults:", e)
    return stats

def get_top_repos(username="Mausam5055", limit=4):
    try:
        req = urllib.request.Request(f"https://api.github.com/users/{username}/repos?sort=pushed&per_page=30", headers={"User-Agent": "Mozilla/5.0"})
        repos = json.loads(urllib.request.urlopen(req).read())
        # Filter out forks and the profile README repo itself
        repos = [r for r in repos if not r.get("fork") and r.get("name").lower() != username.lower()]
        return repos[:limit]
    except Exception as e:
        print("Failed to fetch repos for projects:", e)
        return []

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
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="1030px" height="530px" font-size="16px">
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
<rect width="1030px" height="530px" fill="{bg}" rx="15"/>
<text x="15" y="30" fill="{fg}">
{tspans}
</text>
<text x="390" y="30" fill="{fg}">
<tspan x="390" y="30">mausam@github</tspan> <tspan class="cc">----------------------------------------------------</tspan>
<tspan x="390" y="50" class="cc">. </tspan><tspan class="key">OS</tspan>:<tspan class="cc"> ............................. </tspan><tspan class="value">Windows 11, Android, Linux</tspan>
<tspan x="390" y="70" class="cc">. </tspan><tspan class="key">Location</tspan>:<tspan class="cc"> ............................... </tspan><tspan class="value">Assam, India &#x1F1EE;&#x1F1F3;</tspan>
<tspan x="390" y="90" class="cc">. </tspan><tspan class="key">University</tspan>:<tspan class="cc"> .......................... </tspan><tspan class="value">VIT Bhopal University</tspan>
<tspan x="390" y="110" class="cc">. </tspan><tspan class="key">IDE</tspan>:<tspan class="cc"> .............................. </tspan><tspan class="value">VSCode 1.96.0, Cursor AI</tspan>
<tspan x="390" y="130" class="cc">. </tspan>
<tspan x="390" y="150" class="cc">. </tspan><tspan class="key">Languages.Programming</tspan>:<tspan class="cc"> ....... </tspan><tspan class="value">Python, Java, JavaScript, C++</tspan>
<tspan x="390" y="170" class="cc">. </tspan><tspan class="key">Languages.Web</tspan>:<tspan class="cc"> ................... </tspan><tspan class="value">HTML, CSS, React, Node.js</tspan>
<tspan x="390" y="190" class="cc">. </tspan><tspan class="key">Languages.Data</tspan>:<tspan class="cc"> ................... </tspan><tspan class="value">SQL, MongoDB, JSON, YAML</tspan>
<tspan x="390" y="210" class="cc">. </tspan>
<tspan x="390" y="230" class="cc">. </tspan><tspan class="key">Interests.Dev</tspan>:<tspan class="cc"> .............. </tspan><tspan class="value">Full-Stack, AI/ML, Open Source</tspan>
<tspan x="390" y="250" class="cc">. </tspan><tspan class="key">Interests.Tech</tspan>:<tspan class="cc"> ............. </tspan><tspan class="value">Cloud Computing, Emerging Tech</tspan>
<tspan x="390" y="270" class="cc">. </tspan>
<tspan x="390" y="290" class="cc">. </tspan><tspan class="key">Bio</tspan>:<tspan class="cc"> .................................. </tspan><tspan class="value">Learn to remove &apos;L&apos; &#x1F3C6;</tspan>
<tspan x="390" y="310">- Contact </tspan><tspan class="cc">----------------------------------------------------</tspan>
<tspan x="390" y="330" class="cc">. </tspan><tspan class="key">Email.Personal</tspan>:<tspan class="cc"> ....................... </tspan><tspan class="value">rikikumkar@gmail.com</tspan>
<tspan x="390" y="350" class="cc">. </tspan><tspan class="key">Portfolio</tspan>:<tspan class="cc"> ............................. </tspan><tspan class="value">mausam04.vercel.app</tspan>
<tspan x="390" y="370" class="cc">. </tspan><tspan class="key">LinkedIn</tspan>:<tspan class="cc"> ....................................... </tspan><tspan class="value">mausam-kar</tspan>
<tspan x="390" y="390" class="cc">. </tspan><tspan class="key">GitHub</tspan>:<tspan class="cc"> ......................................... </tspan><tspan class="value">Mausam5055</tspan>
<tspan x="390" y="410" class="cc">. </tspan>
<tspan x="390" y="450">- GitHub Stats </tspan><tspan class="cc">-----------------------------------------------</tspan>
<tspan x="390" y="470" class="cc">. </tspan><tspan class="key">Repos</tspan>:<tspan class="cc"> ...... </tspan><tspan class="value">{str(stats["repos"]).rjust(3)} {{Contributed: 24}}</tspan> <tspan class="cc">| </tspan><tspan class="key">Stars</tspan>:<tspan class="cc"> ......... </tspan><tspan class="value">{str(stats["stars"]).rjust(4)}</tspan>
<tspan x="390" y="490" class="cc">. </tspan><tspan class="key">Commits</tspan>:<tspan class="cc"> ................. </tspan><tspan class="value">{str(stats["commits"]).rjust(4)}</tspan> <tspan class="cc">| </tspan><tspan class="key">Followers</tspan>:<tspan class="cc"> ..... </tspan><tspan class="value">{str(stats["followers"]).rjust(4)}</tspan>
<tspan x="390" y="510" class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:<tspan class="cc">. </tspan><tspan class="value">446,276</tspan> ( <tspan class="addColor">523,178</tspan><tspan class="addColor">++</tspan>, <tspan class="cc"> </tspan><tspan class="delColor">76,902</tspan><tspan class="delColor">--</tspan> )
</text>
</svg>"""

def make_quote_svg(dark=True):
    bg    = "#161b22" if dark else "#f6f8fa"
    fg    = "#c9d1d9" if dark else "#24292f"
    key_c = "#ffa657" if dark else "#953800"
    val_c = "#a5d6ff" if dark else "#0a3069"
    cc_c  = "#616e7f" if dark else "#c2cfde"

    quote_text, quote_author = random.choice(QUOTES)
    wrapped_quote = textwrap.wrap(f'"{quote_text}"', width=80)
    
    quote_tspans = f'<tspan x="20" y="30" class="key">mausam@github</tspan> <tspan class="cc">---[ Random Dev Quote ]---------------------------------------</tspan>\n'
    y_pos = 60
    for line in wrapped_quote:
        quote_tspans += f'<tspan x="20" y="{y_pos}" class="value">{html.escape(line)}</tspan>\n'
        y_pos += 24
    
    author_str = f"- {quote_author}".rjust(80)
    quote_tspans += f'<tspan x="20" y="{y_pos + 10}" class="key">{html.escape(author_str)}</tspan>\n'
    
    total_height = y_pos + 40

    return f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="800px" height="{total_height}px" font-size="16px">
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
.cc    {{fill: {cc_c};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="800px" height="{total_height}px" fill="{bg}" rx="10" stroke="{cc_c}" stroke-width="1"/>
<text x="20" y="30" fill="{fg}">
{quote_tspans}
</text>
</svg>"""

def make_hackatime_svg(dark=True):
    bg    = "#161b22" if dark else "#f6f8fa"
    fg    = "#c9d1d9" if dark else "#24292f"
    key_c = "#ffa657" if dark else "#953800"
    val_c = "#a5d6ff" if dark else "#0a3069"
    cc_c  = "#616e7f" if dark else "#c2cfde"

    stats_col1 = [
        ("TypeScript", "75h 55m"), ("Text", "33h 44m"), ("Other", "9h 12m"),
        ("Markdown", "5h 50m"), ("Shell", "1h 54m"), ("SQL", "1h 12m"),
        ("Batchfile", "26m"), ("TOML", "21m"), ("XML", "14m"),
        ("PowerShell", "10m"), ("Java", "4m")
    ]
    stats_col2 = [
        ("Python", "42h 58m"), ("JavaScript", "14h 39m"), ("JSON", "6h 24m"),
        ("CSS", "3h 46m"), ("INI", "1h 17m"), ("JSX", "28m"),
        ("HTML", "23m"), ("YAML", "20m"), ("C++", "11m"),
        ("Go", "6m"), ("Docker", "2m")
    ]

    tspans = f'<tspan x="20" y="30" class="key">mausam@github</tspan> <tspan class="cc">---[ Hackatime Stats ]----------------------------------------</tspan>\n'
    
    y_pos = 60
    for i in range(len(stats_col1)):
        k1, v1 = stats_col1[i]
        k2, v2 = stats_col2[i] if i < len(stats_col2) else ("", "")
        
        line = f'<tspan x="20" y="{y_pos}" class="cc">. </tspan><tspan class="key">{html.escape(k1)}</tspan>:<tspan class="cc"> {"." * (15 - len(k1))} </tspan><tspan class="value">{v1.rjust(8)}</tspan>    <tspan class="cc">|    </tspan>'
        if k2:
            line += f'<tspan class="key">{html.escape(k2)}</tspan>:<tspan class="cc"> {"." * (15 - len(k2))} </tspan><tspan class="value">{v2.rjust(8)}</tspan>\n'
        else:
            line += '\n'
        tspans += line
        y_pos += 24

    total_height = y_pos + 20

    return f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="550px" height="{total_height}px" font-size="16px">
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
.cc    {{fill: {cc_c};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="550px" height="{total_height}px" fill="{bg}" rx="10" stroke="{cc_c}" stroke-width="1"/>
<text x="20" y="30" fill="{fg}">
{tspans}
</text>
</svg>"""

def make_about_svg(dark=True):
    bg    = "#161b22" if dark else "#f6f8fa"
    fg    = "#c9d1d9" if dark else "#24292f"
    key_c = "#ffa657" if dark else "#953800"
    val_c = "#a5d6ff" if dark else "#0a3069"
    cc_c  = "#616e7f" if dark else "#c2cfde"

    paragraphs = [
        "Tech-focused engineer passionate about building scalable, high-performance systems and modern web experiences. I work across the stack — from crafting smooth, interactive UIs using GSAP and modern frontend tools to designing robust backend systems powered by Go, Node.js, PostgreSQL, and distributed architectures.",
        "",
        "With strong foundations in system design, DBMS, and DevOps, I’ve built and experimented with microservices, cloud deployments, and automation workflows that solve real-world problems at scale. I’m particularly interested in AI/ML, backend infrastructure, and intelligent systems, constantly exploring how these domains intersect to create efficient and resilient products.",
        "",
        "Technical Focus:",
        " • Full-Stack Development (React, Node.js, Tailwind)",
        " • Backend & Distributed Systems (Go, Redis, Microservices)",
        " • Web Animations & Modern UI (GSAP, Lenis)",
        " • AI/ML, NLP, Python",
        " • System Design & Databases",
        "",
        "Currently diving deeper into cloud computing (AWS/GCP), DevOps, and advanced analytics, aiming to build production-grade systems that are scalable, efficient, and reliable.",
        "",
        "I enjoy hackathons, open-source, and experimental projects that push me beyond comfort zones — combining creativity with solid engineering principles."
    ]

    tspans = f'<tspan x="20" y="30" class="key">mausam@github</tspan> <tspan class="cc">---[ About Me ]-----------------------------------------------</tspan>\n'
    
    y_pos = 60
    for p in paragraphs:
        if not p.strip():
            y_pos += 20
            continue
        
        if p.startswith(" •"):
            wrapped = [p]
        elif p == "Technical Focus:":
            wrapped = [p]
        else:
            wrapped = textwrap.wrap(p, width=85)
            
        for line in wrapped:
            if line.startswith(" •"):
                tspans += f'<tspan x="20" y="{y_pos}" class="cc">. </tspan><tspan class="key">{html.escape(line)}</tspan>\n'
            elif line == "Technical Focus:":
                tspans += f'<tspan x="20" y="{y_pos}" class="cc">. </tspan><tspan class="key">{html.escape(line)}</tspan>\n'
            else:
                tspans += f'<tspan x="20" y="{y_pos}" class="cc">. </tspan><tspan class="value">{html.escape(line)}</tspan>\n'
            y_pos += 22

    total_height = y_pos + 20

    return f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="800px" height="{total_height}px" font-size="16px">
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
.cc    {{fill: {cc_c};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="800px" height="{total_height}px" fill="{bg}" rx="10" stroke="{cc_c}" stroke-width="1"/>
<text x="20" y="30" fill="{fg}">
{tspans}
</text>
</svg>"""

def make_projects_svg(repos, dark=True):
    bg    = "#161b22" if dark else "#f6f8fa"
    fg    = "#c9d1d9" if dark else "#24292f"
    key_c = "#ffa657" if dark else "#953800"
    val_c = "#a5d6ff" if dark else "#0a3069"
    add_c = "#3fb950" if dark else "#1a7f37"
    cc_c  = "#616e7f" if dark else "#c2cfde"

    tspans = f'<tspan x="20" y="30" class="key">mausam@github</tspan> <tspan class="cc">---[ Top Projects &amp; Repositories ]----------------------</tspan>\n'
    
    y_pos = 60
    
    if not repos:
        tspans += f'<tspan x="20" y="{y_pos}" class="cc">. </tspan><tspan class="value">No public repositories found.</tspan>\n'
        y_pos += 24
    else:
        for repo in repos:
            name = repo.get("name", "Unknown")
            desc = repo.get("description", "") or "No description provided."
            lang = repo.get("language", "") or "Unknown"
            stars = repo.get("stargazers_count", 0)
            forks = repo.get("forks_count", 0)
            size_kb = repo.get("size", 0)
            size_mb = round(size_kb / 1024, 1) if size_kb > 1024 else f"{size_kb}KB"
            size_str = f"{size_mb}MB" if isinstance(size_mb, float) else size_mb
            
            wrapped_desc = textwrap.wrap(desc, width=70)
            
            tspans += f'<tspan x="20" y="{y_pos}" class="cc">. </tspan><tspan class="add">📦 {html.escape(name)}</tspan>\n'
            y_pos += 22
            
            for line in wrapped_desc:
                tspans += f'<tspan x="20" y="{y_pos}" class="cc">.    </tspan><tspan class="value">{html.escape(line)}</tspan>\n'
                y_pos += 22
                
            stats_line = f"🌟 {stars} Stars  |  🍴 {forks} Forks  |  📏 {size_str}  |  💻 {lang}"
            tspans += f'<tspan x="20" y="{y_pos}" class="cc">.    </tspan><tspan class="key">{html.escape(stats_line)}</tspan>\n'
            y_pos += 30

    total_height = max(y_pos + 10, 200)

    return f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="800px" height="{total_height}px" font-size="16px">
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
.add   {{fill: {add_c};}}
.cc    {{fill: {cc_c};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="800px" height="{total_height}px" fill="{bg}" rx="10" stroke="{cc_c}" stroke-width="1"/>
<text x="20" y="30" fill="{fg}">
{tspans}
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

    for dark, fname in [(True,  r"d:\Mausam5055\dark_mode_v5.svg"),
                        (False, r"d:\Mausam5055\light_mode_v5.svg")]:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(make_svg(lines, stats, dark=dark))
        print(f"✓ {fname}")
        
    for dark, fname in [(True,  r"d:\Mausam5055\quote_dark_v1.svg"),
                        (False, r"d:\Mausam5055\quote_light_v1.svg")]:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(make_quote_svg(dark=dark))
        print(f"✓ {fname}")
        
    for dark, fname in [(True,  r"d:\Mausam5055\hackatime_dark_v1.svg"),
                        (False, r"d:\Mausam5055\hackatime_light_v1.svg")]:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(make_hackatime_svg(dark=dark))
        print(f"✓ {fname}")
        
    for dark, fname in [(True,  r"d:\Mausam5055\about_dark_v1.svg"),
                        (False, r"d:\Mausam5055\about_light_v1.svg")]:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(make_about_svg(dark=dark))
        print(f"✓ {fname}")
        
    print("\nFetching Top Repos...")
    top_repos = get_top_repos()
    for dark, fname in [(True,  r"d:\Mausam5055\projects_dark_v1.svg"),
                        (False, r"d:\Mausam5055\projects_light_v1.svg")]:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(make_projects_svg(top_repos, dark=dark))
        print(f"✓ {fname}")

    print("Done!")
