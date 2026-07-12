import os
import re

file_path = 'profile-3d-contrib/profile-night-rainbow.svg'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The background rect looks something like <rect x="0" y="0" width="1280" height="850" fill="#0d1117"></rect>
# We will use regex to find the first rect with width="1280" and replace it entirely with our styled box.

content = re.sub(r'<rect x="0" y="0" width="1280" height="850" fill="[^"]+"></rect>',
                 r'<rect x="1" y="1" width="1278" height="848" fill="#0d1117" rx="15" stroke="#30363d" stroke-width="2"></rect>', 
                 content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
