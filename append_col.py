import re

langs = [
    ("C#", "30h 15m"),
    ("PHP", "12h 40m"),
    ("Ruby", "8h 22m"),
    ("Rust", "7h 10m"),
    ("Dart", "5h 05m"),
    ("Swift", "4h 12m"),
    ("Kotlin", "3h 50m"),
    ("Scala", "2h 30m"),
    ("Elixir", "1h 45m"),
    ("Lua", "1h 20m"),
    ("Obj-C", "45m")
]

def append_3rd_col(match, lang_idx):
    lang_name, time_str = langs[lang_idx]
    
    time_str_padded = f"{time_str:>8}"
    num_dots = 15 - len(lang_name)
    dots_str = "." * num_dots
    
    col3 = f'    <tspan class="cc">|    </tspan><tspan class="key">{lang_name}</tspan>:<tspan class="cc"> {dots_str} </tspan><tspan class="value">{time_str_padded}</tspan>'
    
    # We replace </tspan> with </tspan> + col3
    return "</tspan>" + col3

for filename in ['hackatime_dark_v1.svg', 'hackatime_light_v1.svg']:
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    idx = 0
    for i, line in enumerate(lines):
        if 'class="value"' in line and '|' in line and not 'col3' in line:
            # Replaces the last </tspan> before the newline
            line = re.sub(r'</tspan>(\r?\n)$', lambda m: append_3rd_col(m, idx) + m.group(1), line)
            lines[i] = line
            idx += 1
            
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(lines)

print("Done!")
