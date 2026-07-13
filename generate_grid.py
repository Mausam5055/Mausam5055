import re

# Base skills from the previous version
skills = [
    "html", "css", "js", "ts", "react", "threejs", "p5js", "express", "vite", "vercel",
    "tailwind", "bootstrap", "firebase", "supabase", "mysql", "java", "figma", "obsidian", "prisma", "vue",
    "python", "pytorch", "rabbitmq", "spring", "solidjs", "vscode", "discord", "gitlab", "cs", "angular",
    "arduino", "bash", "bun", "codepen", "django", "docker", "dotnet", "flask", "gcp", "git",
    "pinia", "graphql", "md", "matlab", "mui", "mongodb", "netlify", "nextjs", "nodejs",
    "npm", "postgres", "opencv", "r", "ubuntu", "aws", "svelte", "solidity", "tensorflow", "terraform"
]

# New cloud, system design, and extra skills (around 20)
new_skills = [
    "azure", "grafana", "prometheus", "kubernetes", "linux", "nginx", "redis", "kafka", 
    "sqlite", "notion", "rust", "go", "cpp", "c", "pandas", "numpy", "github", 
    "cloudflare", "windows", "raspberrypi", "vim"
]

# Combine and remove duplicates while preserving order
all_skills = []
for s in skills + new_skills:
    if s not in all_skills:
        all_skills.append(s)

# Create a single image URL using skillicons.dev with all icons
icons_list = ",".join(all_skills)
# Use perline=12 for a nice grid layout that fits well on GitHub profiles
table_str = f'<a href="https://skillicons.dev">\n  <img src="https://skillicons.dev/icons?i={icons_list}&theme=dark&perline=12" />\n</a>'

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
