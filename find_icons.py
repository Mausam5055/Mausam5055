import re

with open(r'd:\git_log.txt', 'r', encoding='utf-16') as f:
    content = f.read()

urls = re.findall(r'https://skillicons\.dev/icons\?i=[a-zA-Z0-9,]+(?:&[a-zA-Z0-9=]+)*', content)
unique_urls = set(urls)

for url in unique_urls:
    print(len(url), url)
