def make_line(y, key, val, max_len=62):
    prefix = f'. {key}: '
    suffix = f' {val}'
    dots = max_len - len(prefix) - len(suffix)
    if '&#x1F1EE;&#x1F1F3;' in val: dots += 13
    if '🏆' in val: dots += 1
    return f'<tspan x=\"390\" y=\"{y}\" class=\"cc\">. </tspan><tspan class=\"key\">{key}</tspan>:<tspan class=\"cc\"> ' + '.'*dots + f' </tspan><tspan class=\"value\">{val}</tspan>'

def make_header(y, title, max_len=62):
    prefix = f'- {title} '
    dashes = max_len - len(prefix)
    return f'<tspan x=\"390\" y=\"{y}\">- {title} </tspan><tspan class=\"cc\">' + '-'*dashes + '</tspan>'

y = 50
out = []
out.append(make_line(y, 'OS', 'Windows 11, Android, Linux')); y+=20
out.append(make_line(y, 'Location', 'Assam, India &#x1F1EE;&#x1F1F3;')); y+=20
out.append(make_line(y, 'University', 'VIT Bhopal University')); y+=20
out.append(make_line(y, 'IDE', 'VSCode 1.96.0, Cursor AI')); y+=40

out.append(make_line(y, 'Languages.Programming', 'Python, Java, JavaScript, C++')); y+=20
out.append(make_line(y, 'Languages.Web', 'HTML, CSS, React, Node.js')); y+=20
out.append(make_line(y, 'Languages.Data', 'SQL, MongoDB, JSON, YAML')); y+=40

out.append(make_line(y, 'Interests.Dev', 'Full-Stack, AI/ML, Open Source')); y+=20
out.append(make_line(y, 'Interests.Tech', 'Cloud Computing, Emerging Tech')); y+=40

out.append(make_line(y, 'Bio', "Learn to remove 'L' 🏆")); y+=20

out.append(make_header(y, 'Contact')); y+=20
out.append(make_line(y, 'Email.Personal', 'rikikumkar@gmail.com')); y+=20
out.append(make_line(y, 'Portfolio', 'mausam04.vercel.app')); y+=20
out.append(make_line(y, 'LinkedIn', 'mausam-kar')); y+=20
out.append(make_line(y, 'GitHub', 'Mausam5055')); y+=40

out.append(make_header(y, 'GitHub Stats')); y+=20

def make_stat_line(y, k1, v1, k2, v2, len1=31, len2=29):
    p1 = f'. {k1}: '; s1 = f' {v1}'
    # if {stats} is present we approximate its len to 2 digits for Repos, 3 for Stars, etc.
    # Repos is ~ 79 -> len=2. "{stats['repos']}" string is 16 chars. 16 - 2 = 14 to subtract from dots calculation?
    # No, python formatting happens at runtime. So the script that generates the SVG will format it!
    # Wait, the SVG has literal "{stats['repos']}" string which is formatted later. So we should just hardcode the dots.
    pass

# Hardcoding stats lines
out.append(f'<tspan x=\"390\" y=\"{y}\" class=\"cc\">. </tspan><tspan class=\"key\">Repos</tspan>:<tspan class=\"cc\"> ...... </tspan><tspan class=\"value\">{{str(stats[\"repos\"]).rjust(3)}} {{Contributed: --}}</tspan> <tspan class=\"cc\">| </tspan><tspan class=\"key\">Stars</tspan>:<tspan class=\"cc\"> ......... </tspan><tspan class=\"value\">{{str(stats[\"stars\"]).rjust(4)}}</tspan>'); y+=20
out.append(f'<tspan x=\"390\" y=\"{y}\" class=\"cc\">. </tspan><tspan class=\"key\">Commits</tspan>:<tspan class=\"cc\"> ................... </tspan><tspan class=\"value\">--</tspan> <tspan class=\"cc\">| </tspan><tspan class=\"key\">Followers</tspan>:<tspan class=\"cc\"> ..... </tspan><tspan class=\"value\">{{str(stats[\"followers\"]).rjust(4)}}</tspan>'); y+=20
out.append(f'<tspan x=\"390\" y=\"{y}\" class=\"cc\">. </tspan><tspan class=\"key\">Lines of Code on GitHub</tspan>:<tspan class=\"cc\">. </tspan><tspan class=\"value\">--</tspan> ( <tspan class=\"addColor\">--</tspan><tspan class=\"addColor\">++</tspan>, <tspan class=\"cc\"> </tspan><tspan class=\"delColor\">--</tspan><tspan class=\"delColor\">--</tspan> )')

with open("output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
