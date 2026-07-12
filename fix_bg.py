import os
file_path = 'profile-3d-contrib/profile-night-rainbow.svg'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the first <rect> fill which is the background
content = content.replace('fill="#00000f"', 'fill="#0d1117"')
content = content.replace('fill="#161b22"', 'fill="#0d1117"')
content = content.replace('fill="#010409"', 'fill="#0d1117"')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
