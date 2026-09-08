# Strome van Lewe · Bible resources

Bible resources for Strome van Lewe Gemeente, Boshof. Static HTML — no build step, no framework, no dependencies. Every page is a single file you can open and edit.

Live: **[stromevanlewe.github.io](https://stromevanlewe.github.io)**

---

## Structure

```
index.html                      Landing page (logo embedded, no external assets)
assets/
  hero.jpg                      Linocut tree of life — the landing page artwork
  logo.png                      Church logo, transparent (not used by the pages)
bibleplans/3-month-plan/
  index.html                    90-day reading plan, 1 Sep – 30 Nov 2026
studies/offence/
  index.html                    "Om Aanstoot te Neem" — 8-session study
  leiersgids/
    index.html                  Leader's guide — how to lead, and the source discussions
    s1/ … s8/index.html         One page per session: the session as the group sees it,
                                with the leader's notes and answers woven in
boodskappe/
  index.html                    Message archive — list, search, four filters, reader
  index.json                    Index of every message + the tag dictionary
  m/
    2026-09-06-hendrik.af.md    Message body, Afrikaans
    2026-09-06-hendrik.en.md    Message body, English
kidschurch/lessons/offence/     KidsChurch material for the teachers (from Sept 2026)
inligting/                      Working notes — the placement guide. Public, like everything else.
```

**Folder names are lower case and must stay that way.** See Deployment notes.

**Everything in this repository is served publicly**, including anything in `inligting/`. There is no private area. Keep anything you would not want a stranger to read off the repo entirely.

---

## The offence study

Eight sessions on offence, bilingual (Afrikaans / English), built for members to work through alone during the week and then discuss together in the Community Group.

| | Session | Key verse |
|---|---|---|
| **What it is** | 1. Die strik / The trap | Luke 17:1 |
| | 2. Die wortel / The root | Hebrews 12:15 |
| **The gospel** | 3. Die aanstoot van die Kruis / The offence of the Cross | 1 Corinthians 1:23 |
| | 4. Aanstoot teenoor Jesus self / Offence at Jesus Himself | Matthew 11:6 |
| **His example** | 5. Seer sonder aanstoot / Hurt without offence | 1 Peter 2:23 |
| **What to do** | 6. Gaan na jou broer / Go to your brother | Matthew 18:15 |
| | 7. Vergewe soos jy vergewe is / Forgive as you were forgiven | Colossians 3:13 |
| | 8. Leef vry / Living free | Psalm 119:165 |

Each session has: key verse in five translations · plain-language summary · teaching · a story · extra verses with paraphrases · one practical step · personal questions · separate group questions · a prayer.

Plus a step-by-step self-check ("Sit my voet in die strik?" / "Is my foot in the trap?") reachable from every session. It opens on the Galatians 5 mirror, asks for a name, then puts six questions one screen at a time and names which of sessions 5, 6 or 7 to start at. Nothing is scored and nothing is stored — not even in the browser.

**Navigation:** sessions are `#s1` … `#s8` in the URL.

**Language:** the page opens in Afrikaans. Add `?lang=en` for a direct English link, e.g. `/studies/offence/?lang=en#s3`.

### Editing the study

All eight sessions live in one readable `DATA` object near the top of `studies/offence/index.html`, before the rendering code. Change the text there and save — nothing to rebuild.

Scripture references written in the body text are **linked automatically**. If the verse is explained elsewhere in the study, the link jumps to that session; otherwise it opens bible.com in whichever translation the reader has selected. You don't have to write the links.

---

## The message archive

`boodskappe/` holds sermons and messages, built so that a message stays findable years later by speaker, series, year, Scripture, tag or free-text search.

**Two kinds of file.** `index.json` holds everything structured — who, when, which series, which texts, which tags. The message itself is plain Markdown in `m/`, one file per language. The page renders the Markdown at runtime with the same typography as the study, so what you write is what ships. Adding a message never touches code.

### Adding a message

1. Write the two Markdown files as `m/<id>.af.md` and `m/<id>.en.md`. Keep the id in the pattern **date-speaker** (`2026-09-13-dawid`) — it sorts itself and still makes sense in three years.
2. Add one entry at the top of `"messages"` in `index.json`. The `id` must match the file names exactly; that field causes more errors than all the others together.
3. Validate the JSON at [jsonlint.com](https://jsonlint.com) before pushing. Ten seconds, and it names the broken line.

### Fields worth knowing

| Field | Notes |
|---|---|
| `texts` | `{af, en, osis}` — the `osis` code (`GAL.5.17`) builds the bible.com link |
| `tags` | keys only, e.g. `["aanstoot", "vergifnis"]` |
| `related` | pointers to a study session or another message; renders as a named link |
| `media` | `{audio, video}` — a direct `.mp3`/`.m4a` gets a player; video becomes a button. Leave out what doesn't exist |

**The tag dictionary.** `tagname` at the top of `index.json` maps each tag key to its Afrikaans and English display name, so `vergifnis` shows as *forgiveness* in English and the search box finds a message in either language. A tag that isn't in the dictionary simply displays as written — nothing breaks. Add a new tag there once and it is right forever.

**Write each message to stand alone.** Never refer inside the body to "the study", a session number, "Sunday", or a recent series — a reader in three years has none of that context. Pointers belong in `related`, where they become a named, clickable link. Keep it to two or three; more and they stop meaning anything.

**The landing page reads this file.** The "Nuutste / Latest" card on the home page is built from the newest entry in `index.json`. Add a message and the home page updates itself — don't edit the card by hand.

---

## Bible translation IDs (YouVersion)

| Abbrev | Translation | ID |
|---|---|---|
| AFR83 | Afrikaans 1983 | **6** |
| AFR53 | Afrikaans 1933/1953 | **5** |
| NLV | Nuwe Lewende Vertaling | **117** |
| ESV | English Standard Version | 59 |
| NIV | New International Version | 111 |

⚠ Earlier versions of this site used ID **2** for AFR83. That is wrong — **ID 2 is ABA (Bybel vir almal)**, a simplified paraphrase. All AFR83 links were pointing at the wrong Bible.

All eight key verses were verified word for word against each translation before publishing.

---

## The leader's guide

`studies/offence/leiersgids/` is **not linked from anywhere on the site.** Leaders are given the address directly. It is not secret — everything in the repo is public — but a member who reads the answers first gets less out of the study.

**One page per session**, so a leader in training can be sent `…/leiersgids/s5/` and nothing else. Each page is the session exactly as the group sees it, with the leader material set apart in green: what the session is doing and where it goes wrong, a note under each home question, an answer under each group question, and one restart question at the end. There is a print button on every page.

The index page holds the front matter — how to lead, the shape of an evening, the safety guidance, the three limits, and the three discussions about Andrew Selley's material that a leader may be asked about.

**It is generated, not hand-written.** `leiersgids-EN.md` and `leiersgids-AF.md` are the source. `parse_guide.py` turns them into `guide.json`, and `build_guide.py` builds the nine pages from `template.html` + `data.json` + `guide.json`. So the session content can never drift from the study — both come from the same data. Edit the markdown, run the two scripts, upload the folder.

Verses quoted only in the guide are verified in AFR83 and ESV and live in `leader-verses.json`. Each one is marked in the text as *(in the session)* or *(only in this guide)* so a leader knows what is on the members' screens.

---

## Deployment notes

**The host is GitHub Pages, and the repository is the account's user site.** Because it is named `stromevanlewe.github.io`, its contents serve at the root of that address rather than in a subfolder. Netlify is no longer in use.

**Case sensitivity.** GitHub Pages resolves paths case-sensitively. A link to `BiblePlans/` will 404 where the folder is `bibleplans/`. Keep every folder and file name lower case.

**Relative links.** Every link in the site is relative — `./boodskappe/`, `../../`. Absolute paths beginning with `/` would work now that the site sits at the root, but relative links keep the whole site portable: it can be renamed, moved into a subfolder, or opened locally without anything breaking. Keep them relative.

**`?lang=en` goes before the `#`.** `./boodskappe/?lang=en#/2026-09-06-hendrik` works; putting the query after the hash makes it part of the fragment and the page never sees it.

**Renaming the repository changes the address.** GitHub redirects the old URL for a while afterwards, but not forever. Since the link has been shared with the congregation, treat the name as fixed.

---

## Scripture copyright

Quotations are used with acknowledgement:

- **AFR83** © 1983 Bybelgenootskap van Suid-Afrika
- **AFR53** © 1933, 1953 Bybelgenootskap van Suid-Afrika
- **NLV** © 2006 Christelike Uitgewersmaatskappy
- **ESV** © 2001 Crossway
- **NIV** © 1973, 1978, 1984, 2011 Biblica, Inc.

Key verses are quoted in full; extra verses are given as paraphrases with a link to the text.

---

## Still to come

- KidsChurch lessons — see the note below before the second lesson goes up
- Further landing-page sections: KidsChurch · Vir die huis · Hulpbronne vir leiers

### A note on the KidsChurch structure

`kidschurch/lessons/offence/` currently mirrors `studies/offence/` — one folder per theme, one page inside it. That shape suits a study that is written once and revisited.

Lessons behave differently: they arrive weekly and accumulate for years, which is the same shape as `boodskappe/`. Before the second or third lesson goes up, it is worth deciding whether lessons should follow the archive pattern instead — one `index.json` plus a markdown file per lesson, searchable by date, theme, age group and teacher. Changing that after thirty lesson folders exist is expensive; changing it after two is not.
