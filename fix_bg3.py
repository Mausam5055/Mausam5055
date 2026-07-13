import glob
import re

for f in glob.glob('profile-3d-contrib/*.svg'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace for dark theme (currently #0d1117 in local files due to previous sed)
    content = re.sub(
        r'<rect x="0" y="0" width="1280" height="850" fill="#0d1117"></rect>',
        r'<rect x="0" y="0" width="1280" height="850" fill="#161b22" rx="15" stroke="#616e7f" stroke-width="2"></rect>',
        content
    )
    
    # Replace for light theme
    content = re.sub(
        r'<rect x="0" y="0" width="1280" height="850" fill="#ffffff"></rect>',
        r'<rect x="0" y="0" width="1280" height="850" fill="#f6f8fa" rx="15" stroke="#c2cfde" stroke-width="2"></rect>',
        content
    )
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Done")
