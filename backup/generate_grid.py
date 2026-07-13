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

# New cloud, system design, and extra skills (25 icons). 
# Added a few more to reach 84 total icons so we can make a perfect 12x7 grid.
new_skills = [
    "azure", "grafana", "prometheus", "kubernetes", "linux", "nginx", "redis", "kafka", 
    "sqlite", "notion", "rust", "go", "cpp", "c", "sass", "powershell", "github", 
    "cloudflare", "windows", "raspberrypi", "vim", "postman", "webpack", "babel", "jest"
]

# Combine and remove duplicates while preserving order
all_skills = []
for s in skills + new_skills:
    if s not in all_skills:
        all_skills.append(s)
# Total is exactly 84 icons.

lines = ['<table>']
# 12 icons per row keeps them a great size while being wide enough to occupy left/right spaces on desktop!
# Using an HTML table with a non-breaking space spacer forces horizontal scrolling on mobile, preventing shrinking!
for i in range(0, len(all_skills), 12):
    row_skills = all_skills[i:i+12]
    lines.append("  <tr>")
    for s in row_skills:
        # The ultimate hack to prevent GitHub from shrinking cells on mobile: 
        # Add a string of non-breaking spaces in the very first row. This physically cannot shrink!
        spacer = '<br><sub>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</sub>' if i == 0 else ''
        lines.append(f'    <td width="80" align="center">\n      <img src="https://skillicons.dev/icons?i={s}&theme=dark" width="60" />{spacer}\n    </td>')
    
    # Pad just in case it doesn't divide evenly
    while len(row_skills) < 12:
        lines.append('    <td width="80" align="center">&nbsp;</td>')
        row_skills.append("")
    
    lines.append("  </tr>")

lines.append('</table>')

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
