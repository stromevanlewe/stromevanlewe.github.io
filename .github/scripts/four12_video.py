#!/usr/bin/env python3
"""Lees Four12 Global se YouTube-voer en skryf four12-video.json.

Gebruik net die standaardbiblioteek — geen pip, geen sleutel, geen derde party.
Word deur .github/workflows/four12-video.yml geroep.
"""
import json, pathlib, sys, datetime
import xml.etree.ElementTree as ET

VOER = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "voer.xml")
UIT  = pathlib.Path("four12-video.json")

NS = {
    "a":     "http://www.w3.org/2005/Atom",
    "yt":    "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}

def tekst(el, pad):
    k = el.find(pad, NS)
    return (k.text or "").strip() if k is not None and k.text else ""

def main():
    if not VOER.exists():
        sys.exit("Kry nie %s nie" % VOER)
    try:
        wortel = ET.parse(VOER).getroot()
    except ET.ParseError as e:
        sys.exit("Die voer is nie geldige XML nie: %s" % e)

    inskrywings = wortel.findall("a:entry", NS)
    if not inskrywings:
        sys.exit("Die voer het geen inskrywings nie — niks geskryf nie.")

    e = inskrywings[0]
    vid = tekst(e, "yt:videoId")
    titel = tekst(e, "a:title")
    if not vid or not titel:
        sys.exit("Die eerste inskrywing het geen videoId of titel nie — niks geskryf nie.")

    gepubliseer = tekst(e, "a:published")[:10]      # 2026-10-05T14:00:00+00:00 -> 2026-10-05
    kanaal = tekst(wortel, "a:title") or "Four12 Global"

    groep = e.find("media:group", NS)
    beskrywing = ""
    if groep is not None:
        beskrywing = tekst(groep, "media:description")
    # hou dit kort genoeg vir 'n kaart
    beskrywing = " ".join(beskrywing.split())
    if len(beskrywing) > 200:
        beskrywing = beskrywing[:197].rsplit(" ", 1)[0] + "…"

    data = {
        "id": vid,
        "titel": titel,
        "beskrywing": beskrywing,
        "skakel": "https://www.youtube.com/watch?v=" + vid,
        "duimnael": "https://i.ytimg.com/vi/%s/hqdefault.jpg" % vid,
        "gepubliseer": gepubliseer,
        "kanaal": kanaal,
        "opgedateer": datetime.datetime.now(datetime.timezone.utc)
                        .replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }

    nuut = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
    if UIT.exists():
        try:
            ou = json.loads(UIT.read_text(encoding="utf-8"))
            if ou.get("id") == vid:
                print("Dieselfde video (%s) — niks verander nie." % vid)
                return
        except Exception:
            pass
    UIT.write_text(nuut, encoding="utf-8")
    print("Geskryf: %s — %s (%s)" % (vid, titel, gepubliseer))

if __name__ == "__main__":
    main()
