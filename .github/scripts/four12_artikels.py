#!/usr/bin/env python3
"""Lees Four12 se artikelvoer en skryf four12-artikels.json.

Net die standaardbiblioteek. Word deur .github/workflows/four12-video.yml geroep.
Voer: https://four12global.com/?feed=rss2&post_type=articles
"""
import json, pathlib, sys, datetime, html, re
import xml.etree.ElementTree as ET

VOER   = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "artikels.xml")
UIT    = pathlib.Path("four12-artikels.json")
HOEVEEL = 4                     # 1 uitgelig + 3 in die lys

NS = {"dc": "http://purl.org/dc/elements/1.1/"}
MND = ["Januarie","Februarie","Maart","April","Mei","Junie",
       "Julie","Augustus","September","Oktober","November","Desember"]

def skoon(t):
    if not t: return ""
    t = re.sub(r"<[^>]+>", " ", t)          # enige HTML uit die opsomming
    t = html.unescape(t)
    return " ".join(t.split())

def datum_af(pub):
    # "Tue, 29 Sep 2026 09:56:54 +0000"
    try:
        d = datetime.datetime.strptime(pub[:25].strip(), "%a, %d %b %Y %H:%M:%S")
    except Exception:
        return ""
    return "%d %s %d" % (d.day, MND[d.month - 1], d.year)

def main():
    if not VOER.exists():
        sys.exit("Kry nie %s nie" % VOER)
    try:
        wortel = ET.parse(VOER).getroot()
    except ET.ParseError as e:
        sys.exit("Die voer is nie geldige XML nie: %s" % e)

    items = wortel.findall("./channel/item")
    if not items:
        sys.exit("Die voer het geen items nie — niks geskryf nie.")

    # Loop deur ALLES en neem die eerste HOEVEEL egte artikels. Vat ek net
    # items[:HOEVEEL], stoot een vennootbladsy 'n artikel uit die lys.
    uit = []
    for it in items:
        if len(uit) >= HOEVEEL:
            break
        def t(p):
            k = it.find(p, NS)
            return (k.text or "").strip() if k is not None and k.text else ""
        titel = skoon(t("title"))
        skakel = t("link")
        if not titel or not skakel:
            continue
        # net regte artikels — nie vennootbladsye of konferensies nie
        if "/articles/" not in skakel:
            continue
        pub = t("pubDate")
        uit.append({
            "titel": titel,
            "skakel": skakel,
            "opsom": skoon(t("description")),
            "datum": datum_af(pub),
            "sorteer": pub[:16],
        })

    if not uit:
        sys.exit("Geen bruikbare artikels in die voer nie — niks geskryf nie.")

    data = {
        "artikels": uit,
        "opgedateer": datetime.datetime.now(datetime.timezone.utc)
                        .replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }
    nuut = json.dumps(data, ensure_ascii=False, indent=1) + "\n"

    if UIT.exists():
        try:
            ou = json.loads(UIT.read_text(encoding="utf-8"))
            if [a.get("skakel") for a in ou.get("artikels", [])] == [a["skakel"] for a in uit]:
                print("Dieselfde %d artikels — niks verander nie." % len(uit))
                return
        except Exception:
            pass
    UIT.write_text(nuut, encoding="utf-8")
    print("Geskryf: %d artikels, nuutste = %s" % (len(uit), uit[0]["titel"]))

if __name__ == "__main__":
    main()
