#!/usr/bin/env python3
"""Tel die woorde in elke boodskap en skryf leestyd (minute) in boodskappe/index.json.
Herhaalbaar: loop dit weer nadat jy 'n boodskap bygevoeg of verkort het."""
import re, json, os, collections

WPM = 180          # stadiger as gewone prosa — hierdie stukke is vol Skrif en pouses
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "boodskappe")

def woorde(pad):
    t = open(pad, encoding="utf-8").read()
    t = re.sub(r"^---\n.*?\n---\n", "", t, flags=re.S)     # front matter weg
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)           # notas weg
    t = re.sub(r"[#>*_`\[\]()|–—-]", " ", t)               # opmaak weg
    return len([w for w in t.split() if any(c.isalnum() for c in w)])

p = os.path.join(DIR, "index.json")
d = json.load(open(p, encoding="utf-8"), object_pairs_hook=collections.OrderedDict)

for m in d["messages"]:
    rt = {}
    for lang in ("af", "en"):
        f = os.path.join(DIR, "m", f"{m['id']}.{lang}.md")
        if os.path.exists(f):
            rt[lang] = max(1, round(woorde(f) / WPM))
    if rt:
        m["readingTime"] = rt
        print(f"  {m['id']:24s} " + "  ".join(f"{k}: {v} min" for k, v in rt.items()))

json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\nindex.json bygewerk ({WPM} woorde per minuut)")
