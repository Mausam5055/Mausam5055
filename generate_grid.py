import re

# Base skills from the previous version (59 unique)
skills = [
    "html", "css", "js", "ts", "react", "threejs", "p5js", "express", "vite", "vercel",
    "tailwind", "bootstrap", "firebase", "supabase", "mysql", "java", "figma", "obsidian", "prisma", "vue",
    "python", "pytorch", "rabbitmq", "spring", "solidjs", "vscode", "discord", "gitlab", "cs", "angular",
    "arduino", "bash", "bun", "codepen", "django", "docker", "dotnet", "flask", "gcp", "git",
    "pinia", "graphql", "md", "matlab", "mui", "mongodb", "netlify", "nextjs", "nodejs",
    "npm", "postgres", "opencv", "r", "ubuntu", "aws", "svelte", "solidity", "tensorflow", "terraform"
]

# New cloud, system design, and extra skills (21 icons). 
# Pandas and Numpy were replaced with Sass and Powershell because they weren't loading.
new_skills = [
    "azure", "grafana", "prometheus", "kubernetes", "linux", "nginx", "redis", "kafka", 
    "sqlite", "notion", "rust", "go", "cpp", "c", "sass", "powershell", "github", 
    "cloudflare", "windows", "raspberrypi", "vim"
]

# Combine and remove duplicates while preserving order
all_skills = []
for s in skills + new_skills:
    if s not in all_skills:
        all_skills.append(s)
# Total is exactly 80 icons.

lines = []
# Changed to 16 icons per row to stretch the table wider and occupy left/right spaces!
for i in range(0, len(all_skills), 16):
    row_skills = all_skills[i:i+16]
    cells = [f'<img src="https://skillicons.dev/icons?i={s}&theme=dark" />' for s in row_skills]
    # Pad just in case it doesn't divide evenly
    while len(cells) < 16:
        cells.append("&nbsp;")
    lines.append("| " + " | ".join(cells) + " |")
    
    # After the first row, add the markdown header separator
    if i == 0:
        lines.append("|" + "|".join([":---:"] * 16) + "|")

table_str = "\n".join(lines)

with open(r'd:\Mausam5055\README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the start of the Skills section
start_match = re.search(r'## 💀 Skills &amp; Stacks\s+<div align="center">\s+', content)
if start_match:
    start_idx = start_match.end()
    # Find the end of the Skills section
    end_idx = content.find("</div>", start_idx)
    new_content = content[:start_idx] + table_str + "\n\n> *Yes... I'm pretty comfortable with every language and library on this list.*\n\n" + content[end_idx:]
    with open(r'd:\Mausam5055\README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Updated README.md")
else:
    print("Could not find the Skills section in README.md")
