import glob
import re

for f in glob.glob('profile-3d-contrib/*.svg'):
    content = open(f, encoding='utf-8').read()
    match = re.search(r'fill="([^"]+)"', content)
    bg = match.group(1) if match else None
    print(f, bg)
