#!/usr/bin/env python3
"""Tel die woorde in elke boodskap en artikel en skryf leestyd (minute) in
boodskappe/index.json en artikels/index.json.
Herhaalbaar: loop dit weer nadat jy 'n boodskap of artikel bygevoeg of verkort het."""
import re, json, os, collections

WPM = 180          # stadiger as gewone prosa — hierdie stukke is vol Skrif en pouses
ROOT = os.path.dirname(os.path.abspath(__file__))

def woorde(pad):
    t = open(pad, encoding="utf-8").read()
    t = re.sub(r"^---\n.*?\n---\n", "", t, flags=re.S)     # front matter weg
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)           # notas weg
    t = re.sub(r"^!\[.*$", "", t, flags=re.M)              # prentreëls tel nie
    t = re.sub(r"[#>*_`\[\]()|–—-]", " ", t)               # opmaak weg
    return len([w for w in t.split() if any(c.isalnum() for c in w)])

def werk(gids, lys, sub):
    p = os.path.join(ROOT, gids, "index.json")
    if not os.path.exists(p):
        return
    d = json.load(open(p, encoding="utf-8"), object_pairs_hook=collections.OrderedDict)
    for m in d[lys]:
        rt = {}
        for lang in ("af", "en"):
            f = os.path.join(ROOT, gids, sub, f"{m['id']}.{lang}.md")
            if os.path.exists(f):
                rt[lang] = max(1, round(woorde(f) / WPM))
        # 'n artikel in net een taal: wys dieselfde leestyd in die ander taal
        for lang in ("af", "en"):
            if lang not in rt and rt:
                rt[lang] = list(rt.values())[0]
        if rt:
            m["readingTime"] = rt
            print(f"  {m['id']:28s} " + "  ".join(f"{k}: {v} min" for k, v in rt.items()))
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{gids}/index.json bygewerk ({WPM} woorde per minuut)\n")

werk("boodskappe", "messages", "m")
werk("artikels", "articles", "a")
