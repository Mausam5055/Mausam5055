import urllib.request, json, re

def get_repo_details(username, repo_name):
    commits = 0
    loc = 0
    try:
        # Get commits
        req = urllib.request.Request(f"https://api.github.com/repos/{username}/{repo_name}/commits?per_page=1", headers={"User-Agent": "Mozilla"})
        with urllib.request.urlopen(req) as resp:
            link = resp.getheader('Link')
            if link:
                match = re.search(r'page=(\d+)>; rel="last"', link)
                if match: commits = int(match.group(1))
            else:
                commits = len(json.loads(resp.read()))
                
        # Get languages (LOC proxy)
        req2 = urllib.request.Request(f"https://api.github.com/repos/{username}/{repo_name}/languages", headers={"User-Agent": "Mozilla"})
        with urllib.request.urlopen(req2) as resp2:
            langs = json.loads(resp2.read())
            loc = sum(langs.values()) // 30  # Roughly 30 bytes per line
            
    except Exception as e:
        print(f"Error fetching {repo_name}: {e}")
        
    return commits, loc

print(get_repo_details("Mausam5055", "Campus-Sync"))
