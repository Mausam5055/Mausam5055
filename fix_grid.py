import re

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Extract all skill icons
icons = re.findall(r'<img src="https://skillicons\.dev/icons\?i=[a-zA-Z0-9]+&theme=dark" />', content)

# Create 10-column table
lines = [
    "| | | | | | | | | | |",
    "|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|"
]

for i in range(0, len(icons), 10):
    chunk = icons[i:i+10]
    lines.append("| " + " | ".join(chunk) + " |")

table_str = "\n".join(lines)

# Find the start and end of the old table
start_idx = content.find("| | | | | |")
end_idx = content.find(">", start_idx) - 2 # right before the blockquote

new_content = content[:start_idx] + table_str + "\n\n" + content[end_idx:]

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Table reformatted to 5 columns.")
