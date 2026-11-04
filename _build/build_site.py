"""Static site builder for the Rally Lab GitHub Pages site.

Fragments live in _build/pages/*.html. First line is a meta comment:
    <!--meta {"kind": "lab", "session": 1, "n": 4} -->
    <!--meta {"kind": "page", "out": "index.html", "title": "...", "theme": "home", "nav": "home"} -->

Shorthands expanded inside fragments:
    <prompt where="Copilot Chat">text with [[placeholders]]</prompt>
    <file href="{{root}}data/x.xlsx" ext="xlsx" title="Name" desc="What it is"/>
    {{root}} -> relative path to site root
Run: python _build/build_site.py
"""
import html
import json
import re
import zipfile
from pathlib import Path

import story as S
import concepts as C

ROOT = Path(__file__).resolve().parents[1]
PAGES = Path(__file__).resolve().parent / "pages"

LABS = {
    1: [
        dict(n=1, title="The AI Investigation Begins", short="Investigation Plan", tools=["Copilot Chat"], mins=10,
             sub="Grounded vs. general answers, picking the right Copilot tool, and building an investigation plan.",
             output="A clear investigation plan"),
        dict(n=2, title="Follow the Evidence", short="The Missing Approval", tools=["Outlook", "Teams"], mins=25,
             sub="Reconstruct a disputed approval from fragmented emails and a meeting, and catch a flawed AI recap.",
             output="Decision timeline, outstanding-commitments report, follow-up email"),
        dict(n=3, title="Researcher: Is the Promotion Really Ready?", short="Readiness Brief", tools=["Researcher"], mins=25,
             sub="Run a multi-source, cited investigation and stress-test its conclusions.",
             output="Promotional-readiness investigation brief"),
        dict(n=4, title="The Giveaway Mystery", short="Reconciliation", tools=["Analyst", "Copilot in Excel"], mins=45,
             sub="Reconcile two workbooks full of planted discrepancies, then build and verify an exception report.",
             output="Reconciliation findings, verified exception workbook, operational risk summary"),
        dict(n=5, title="The Evidence Room: Make the Call", short="Make the Call", tools=["Copilot Chat"], mins=15,
             sub="Separate facts from estimates, prioritize risk, and defend a go / conditional / delay decision.",
             output="Promotional-readiness scorecard and prioritized action plan"),
    ],
    2: [
        dict(n=1, title="The Plot Twist", short="Plot Twist", tools=["Copilot Chat"], mins=10,
             sub="Four overnight changes. Which assumptions and recommendations no longer hold?",
             output="Updated list of business questions to resolve"),
        dict(n=2, title="The Promotional Weekend Command Center", short="Notebook", tools=["Copilot Notebooks"], mins=20,
             sub="Build a grounded project knowledge hub and find the limits of what it knows.",
             output="Reusable project knowledge workspace and readiness briefing"),
        dict(n=3, title="Build the Readiness Coach", short="Agent Builder", tools=["Agent Builder"], mins=30,
             sub="Turn a good interaction into a reusable agent, then try to break it.",
             output="Tested readiness agent, reusable instructions and test cases"),
        dict(n=4, title="Game-Day Promotion Simulator", short="Simulator", tools=["Copilot Pages"], mins=30,
             sub="Prompt your way to an interactive scenario calculator and survive the Budget Surprise.",
             output="Working planning prototype with visible assumptions and validated math"),
        dict(n=5, title="Pitch the Revised Promotion Plan", short="Executive Story", tools=["PowerPoint", "Word"], mins=20,
             sub="Turn evidence into a three-slide storyline and a decision brief, then face a skeptical executive.",
             output="Executive decision brief and three-slide presentation"),
        dict(n=6, title="Keep the Momentum Going", short="Scheduled Prompts", tools=["Scheduled Prompts"], mins=10,
             sub="Put recurring status checks on autopilot and pick your next workflow.",
             output="Recurring prompt and practical implementation idea"),
    ],
}
SESSION_NAME = {1: "Game 1 · The Investigation", 2: "Game 2 · The Innovation Lab"}

BALL_SVG = """<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="29" fill="#fff" stroke="#E7E0CF" stroke-width="2"/><path d="M14 10c8 7 11 15 11 22s-3 15-11 22M50 10c-8 7-11 15-11 22s3 15 11 22" fill="none" stroke="#C6011F" stroke-width="2.4"/><g stroke="#C6011F" stroke-width="2" stroke-linecap="round"><path d="M17 15l4-2M20 20l4-1.5M22 26l4-.8M22.5 32h4M22 38l4 .8M20 44l4 1.5M17 49l4 2M47 15l-4-2M44 20l-4-1.5M42 26l-4-.8M41.5 32h-4M42 38l-4 .8M44 44l-4 1.5M47 49l-4 2"/></g></svg>"""


def esc(s):
    return html.escape(s, quote=True)


def rel_root(out):
    depth = out.count("/")
    return "../" * depth


def expand(frag, root):
    def prompt(m):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        body = m.group(2).strip("\n")
        body = esc(body)
        body = re.sub(r"\[\[(.+?)\]\]", r'<span class="ph">[\1]</span>', body)
        where = esc(attrs.get("where", "Copilot Chat"))
        hint = ""
        if re.search(r"(^|\s)/(0\d_|Rally_|My_)", m.group(2)):
            hint = '<div class="p-hint">📎 <b>Attach the files first.</b> Pasted, the <code>/FileName</code> text is just a label. To link a file, type <kbd>/</kbd> and pick it, or attach it with <b>+</b>.</div>' 
        return (f'<div class="prompt"><div class="p-head"><span class="where">{where}</span>'
                f'<button class="copy-btn" type="button">Copy</button></div><pre>{body}</pre>{hint}</div>')
    frag = re.sub(r"<prompt([^>]*)>(.*?)</prompt>", prompt, frag, flags=re.S)

    def filetag(m):
        a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        return (f'<a class="file" href="{a["href"]}" download><span class="ext {a.get("ext","")}">{a.get("ext","").upper()}</span>'
                f'<span><b>{a.get("title","")}</b><span>{a.get("desc","")}</span></span></a>')
    frag = re.sub(r"<file([^>]*)/>", filetag, frag)
    return frag.replace("{{root}}", root)


def nav(root, active):
    items = [("home", "Home", "index.html"), ("s1", "Game 1: Investigation", "session-1/index.html"),
             ("s2", "Game 2: Innovation Lab", "session-2/index.html"), ("case", "Case File", "case-file.html"),
             ("dugout", "Dugout Guide", "resources.html")]
    act = ' class="active"'
    links = "".join(f'<a href="{root}{h}"{act if k == active else ""}>{t}</a>' for k, t, h in items)
    return f"""<header class="topbar"><div class="wrap">
<a class="brand" href="{root}index.html">{BALL_SVG}<span class="word">Rally Lab</span><span class="tag">Microsoft 365 Copilot<br>Level 2</span></a>
<button class="nav-toggle" type="button" aria-label="Menu">Menu</button>
<nav class="nav">{links}</nav></div></header>"""


FOOTER = """<footer class="footer"><div class="wrap">
<div><b>Rally Lab</b><br>Enhancing Productivity with Microsoft 365 Copilot - Level 2<br>Investigate, Innovate, and Make Smarter Decisions</div>
<div style="max-width:520px">All people, sponsors, numbers, emails and documents in these labs are <b style="font-size:inherit;letter-spacing:0;text-transform:none">fictional</b> training material
created for this workshop. Copilot features and menu names vary by license, tenant settings and release - your screen may differ slightly.</div>
</div></footer>"""


def head(title, root):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | Rally Lab - Copilot Level 2</title>
<meta name="description" content="Baseball-themed hands-on labs for Microsoft 365 Copilot Level 2: Researcher, Analyst, Excel, Notebooks, Agent Builder, Pages.">
<link rel="icon" href="data:image/svg+xml,{BALL_SVG.replace('"', "'").replace('#', '%23').replace('<svg ', "<svg xmlns='http://www.w3.org/2000/svg' ")}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Oswald:wght@400;500;600&family=Yellowtail&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/site.css"><script>document.documentElement.classList.add("js")</script></head>"""


def page_wrap(out, title, theme, active, body, data_page="", data_lab=""):
    root = rel_root(out)
    attrs = f' class="theme-{theme}"'
    if data_page:
        attrs += f' data-page="{data_page}"'
    if data_lab:
        attrs += f' data-lab="{data_lab}"'
    return (head(title, root) + f"<body{attrs}>" + nav(root, active) + "<main>" + expand(body, root) + "</main>"
            + FOOTER + f'<script src="{root}assets/js/site.js"></script></body></html>')


def scoreboard(sessions=(1, 2), root=""):
    max_inn = 6
    th = "".join(f"<th>{i}</th>" for i in range(1, max_inn + 1))
    rows = ""
    for s in sessions:
        cells = ""
        for i in range(1, max_inn + 1):
            if i <= len(LABS[s]):
                cells += f'<td data-lab-cell="s{s}-l{i}"><a href="{root}session-{s}/lab-{i}.html" title="{esc(LABS[s][i-1]["title"])}">0</a></td>'
            else:
                cells += '<td style="opacity:.35">-</td>'
        team = "GAME 1 · INVESTIGATE" if s == 1 else "GAME 2 · INNOVATE"
        rows += f'<tr data-row="{s}"><td class="team">{team}</td>{cells}<td class="total" data-r>0</td><td data-h>0</td><td data-e>0</td></tr>'
    return f"""<div class="scoreboard" data-session="{','.join(map(str, sessions))}">
<div class="sb-title"><span>Rally Lab · Your Progress</span><span>● Live</span></div>
<table><thead><tr><th></th>{th}<th>R</th><th>H</th><th>E</th></tr></thead><tbody>{rows}</tbody></table>
<div class="sb-foot"><span>R = labs complete · H = steps done · E = AI errors caught</span><button type="button" data-reset>Reset</button></div></div>"""


LETTERS = "ABCDE"


def shot_html(lid, c):
    sh = c["shot"]
    opts = "".join(f'<button type="button" class="opt" data-correct="{1 if i == sh["a"] else 0}"><span class="l">{LETTERS[i]}</span>{esc(o)}</button>'
                   for i, o in enumerate(sh["opts"]))
    return f"""<section id="call-your-shot" data-toc="Call your shot"><div class="shot" data-key="shot:{lid}">
<div class="shot-head"><span class="shot-badge">☝ Call your shot</span><span>Predict before you play. Wrong guesses teach the most.</span></div>
<h3>{esc(sh['q'])}</h3><div class="opts">{opts}</div>
<div class="shot-why" hidden><b class="verdict"></b> {sh['why']}</div></div></section>"""


def drill_html(lid, d):
    cats = d["cats"]
    items = ""
    for i, (quote, who, ans, why) in enumerate(d["items"]):
        btns = "".join(f'<button type="button" data-cat="{esc(c)}">{esc(c)}</button>' for c in cats)
        items += f"""<div class="sort-item" data-answer="{esc(ans)}"><div class="sort-q"><blockquote>{esc(quote)}</blockquote><cite>{esc(who)}</cite></div>
<div class="sort-btns">{btns}</div><div class="sort-fb" hidden><b></b> {esc(why)}</div></div>"""
    return f"""<section id="drill" data-toc="Bullpen drill"><h2><span class="base"></span>Bullpen drill: {esc(d['title'])}</h2>
<p class="lead">{esc(d['intro'])}</p><div class="sorter" data-key="drill:{lid}">
<div class="sort-top"><span class="sort-time">⏱ 2-minute drill · optional if you're short on time</span><span class="sort-score" aria-live="polite">0 / {len(d['items'])} sorted</span><button type="button" class="sort-reset">Reset drill</button></div>
{items}<div class="sort-done" hidden></div></div></section>"""


def postgame_html(lid, c):
    cards = "".join(f'<div class="concept"><span class="c-num">{i + 1}</span><h4>{t}</h4><p>{b}</p></div>' for i, (t, b) in enumerate(c["concepts"]))
    ex = c["extra"]
    return f"""<section id="extra-innings" data-toc="Extra innings"><h2><span class="base"></span>Extra innings: {esc(ex['title'])}</h2>
<div class="extra-card"><span class="extra-tag">Stretch at-bat · optional</span><p>{esc(ex['text'])}</p>
<prompt where="{esc(ex['where'])}">{ex['prompt']}</prompt></div></section>
<section id="postgame" data-toc="Postgame takeaways"><div class="postgame">
<div class="pg-head"><span>🎙 Postgame press conference</span><span>Big Idea #{c['no']} of 11</span></div>
<div class="big-idea"><span class="bi-kick">The big idea</span><h3>{esc(c['title'])}</h3><p>{c['idea']}</p></div>
<div class="concepts">{cards}</div>
<div class="transfer"><h4>📎 Take it to your desk</h4><p>The same move, ready for your real work. Copy it now and use it this week.</p>
<prompt where="Copilot Chat · your work">{c['transfer']}</prompt></div></div></section>"""


def stretch_html(st):
    return f"""<section id="stretch" data-toc="7th-inning stretch"><div class="stretch"><div class="st-head"><span class="st-badge">🎵 {esc(st['title'])}</span><span>{esc(st['time'])} · stand up, then type</span></div>
<prompt where="{esc(st['where'])}">{st['prompt']}</prompt>
<div class="st-ump"><b>Then umpire it.</b> {esc(st['ump'].replace('Umpire it. ', ''))}<label><input type="checkbox" class="track" data-key="{st['key']}"> I caught it</label></div></div></section>"""


def inject(frag, lid):
    c = C.LAB_CONCEPTS.get(lid)
    if not c:
        return frag
    i = frag.index("</section>") + len("</section>")
    frag = frag[:i] + "\n" + (stretch_html(c["stretch"]) if c.get("stretch") else "") + shot_html(lid, c) + frag[i:]
    if c.get("drill"):
        for anchor in ('<section id="challenge"', '<section id="scorecard"', '<section id="verify"', '<section id="ump"'):
            if anchor in frag:
                j = frag.index(anchor)
                frag = frag[:j] + drill_html(lid, c["drill"]) + "\n" + frag[j:]
                break
    anchor = '<section id="finale"' if '<section id="finale"' in frag else '<section id="dugout"'
    j = frag.index(anchor)
    return frag[:j] + postgame_html(lid, c) + "\n" + frag[j:]


def bases_svg(s, n):
    total = len(LABS[s])
    return f'''<div class="hero-path" data-session="{s}" aria-label="Session progress">
<svg viewBox="0 0 120 120" aria-hidden="true"><path d="M60 106 L104 62 L60 18 L16 62 Z" fill="none" stroke="rgba(255,255,255,.25)" stroke-width="2" stroke-dasharray="4 4"/>
{''.join(f'<rect class="hp-base" data-lab-dot="s{s}-l{k}" x="-7" y="-7" width="14" height="14" transform="translate({x} {y}) rotate(45)"{" data-current" if k == n else ""}/>' for k, (x, y) in enumerate(PATH[total], start=1))}
</svg><small>{SESSION_NAME[s].split(" · ")[0]} base path</small></div>'''


PATH = {5: [(60, 106), (104, 62), (60, 18), (16, 62), (60, 62)], 6: [(60, 106), (104, 62), (82, 40), (60, 18), (16, 62), (60, 62)]}


def build_lab(meta, frag):
    s, n = meta["session"], meta["n"]
    lab = LABS[s][n - 1]
    labs = LABS[s]
    out = f"session-{s}/lab-{n}.html"
    root = rel_root(out)
    lid = f"s{s}-l{n}"
    c = C.LAB_CONCEPTS.get(lid, {})
    frag = inject(frag, lid)
    tools = "".join(f'<span class="chip tool">{esc(t)}</span>' for t in lab["tools"])
    idea_chip = f'<span class="chip idea">💡 Big Idea #{c["no"]}: {esc(c["title"])}</span>' if c else ""
    hero = f"""<section class="lab-hero"><div class="hero-num" aria-hidden="true">{n}</div><div class="wrap">
<div class="crumbs"><a href="{root}index.html">Rally Lab</a> / <a href="index.html">{SESSION_NAME[s]}</a> / Inning {n}</div>
<div class="row"><div class="inning-badge"><div><small>Inning</small><b>{n}</b><small>of {len(labs)}</small></div></div>
<div class="hero-text"><h1>{esc(lab['title'])}</h1><p class="sub">{esc(lab['sub'])}</p>
<div class="chips">{tools}<span class="chip">⏱ {lab['mins']} minutes</span><span class="chip">📋 Output: {esc(lab['output'])}</span>{idea_chip}</div></div>
{bases_svg(s, n)}</div></div></section>"""
    lineup = '<nav class="lineup-nav" aria-label="Innings"><div class="wrap"><span class="lbl">' + ("Game 1" if s == 1 else "Game 2") + " lineup</span>"
    for l in labs:
        cur = " current" if l["n"] == n else ""
        lineup += f'<a class="{cur.strip()}" data-lab-link="s{s}-l{l["n"]}" href="lab-{l["n"]}.html"><span class="n">{l["n"]}</span>{esc(l["short"])}</a>'
    lineup += '<span class="lineup-progress"><i style="width:0%"></i></span></div></nav>'
    toc = "".join(f'<a href="#{i}">{esc(t)}</a>' for i, t in re.findall(r'<section id="([^"]+)" data-toc="([^"]+)"', frag))
    prev_ = f'<a class="prev" href="lab-{n-1}.html"><small>← Previous inning</small><b>{esc(labs[n-2]["title"])}</b></a>' if n > 1 else f'<a class="prev" href="index.html"><small>← Back to</small><b>{SESSION_NAME[s]}</b></a>'
    if n < len(labs):
        next_ = f'<a class="next" href="lab-{n+1}.html"><small>Next inning →</small><b>{esc(labs[n]["title"])}</b></a>'
    elif s == 1:
        next_ = f'<a class="next" href="{root}session-2/index.html"><small>Next game →</small><b>{SESSION_NAME[2]}</b></a>'
    else:
        next_ = f'<a class="next" href="{root}resources.html"><small>Take it home →</small><b>Dugout Guide & Toolkit</b></a>'
    body = hero + lineup + f"""<div class="lab-body"><div class="wrap lab-grid"><aside class="toc"><b>In this inning</b>{toc}</aside>
<div class="lab-content">{frag}
<div class="complete-bar"><div><b class="cb-title">Inning {n} in the books?</b><p>Log it on the scoreboard. Your progress is saved in this browser.</p></div><button class="btn" type="button" data-complete>Mark inning complete</button></div>
<div class="pager">{prev_}{next_}</div></div></div></div>"""
    return out, page_wrap(out, f"Inning {n}: {lab['title']}", f"s{s}", f"s{s}", body, data_page=lid, data_lab=lid)


def playbook_html(root=""):
    cards = ""
    for lid, c in C.LAB_CONCEPTS.items():
        s, n = lid[1], lid.split("-l")[1]
        cards += f"""<a class="bcard g{s}" href="{root}session-{s}/lab-{n}.html#postgame"><div class="bc-inner">
<div class="bc-front"><span class="bc-num">#{c['no']}</span><span class="bc-game">Game {s} · Inning {n}</span><span class="bc-flip">hover to flip ↻</span><div class="bc-band"><h4>{esc(c['title'])}</h4><span class="bc-tool">{esc(c['tool'])}</span></div></div>
<div class="bc-back"><span class="bc-num">#{c['no']}</span><p>{c['idea']}</p><span class="bc-go">Open the inning →</span></div></div></a>"""
    return f'<div class="playbook">{cards}</div>'


def lab_rows(s):
    rows = ""
    for l in LABS[s]:
        tools = " · ".join(l["tools"])
        rows += f"""<a class="lab-row" data-lab-link="s{s}-l{l['n']}" href="lab-{l['n']}.html"><div class="inn"><small>INNING</small>{l['n']}</div>
<div><h3>{esc(l['title'])}</h3><p>{esc(l['sub'])}</p></div><div class="right">{l['mins']} min<br><span class="tag {'red' if s == 1 else 'blue'}">{esc(tools)}</span></div></a>"""
    return f'<div class="lab-list">{rows}</div>'


def case_file():
    people = {c[0]: c for c in S.CAST}
    emails = ""
    for eid, when, frm, to, cc, subj, body, notes in S.EMAILS:
        ini = people[frm][3]
        ext = " ext" if frm == "Ryan Castellano" else ""
        b = "".join(f"<p>{esc(p)}</p>" for p in body)
        cc_s = f" · cc {esc(', '.join(cc))}" if cc else ""
        emails += f"""<article class="email" id="{eid}"><div class="e-top"><div class="avatar{ext}">{ini}</div>
<div><div class="e-subj">{esc(subj)}</div><div class="e-meta"><b>{esc(frm)}</b> → {esc(', '.join(to))}{cc_s} · {esc(when)}</div></div><span class="e-id">{eid}</span></div>
<div class="e-body">{b}</div></article>"""
    m = S.TRANSCRIPT_META
    lines = ""
    for ts, who, text in S.TRANSCRIPT:
        lines += f'<div class="chat-line"><span class="ts">{ts}</span><div class="avatar">{people[who][3]}</div><div><b>{esc(who)}</b><p>{esc(text)}</p></div></div>'
    recap = "".join(f"<li>{esc(c)}</li>" for c, _, _ in S.RECAP)
    roster = ""
    for name, role, desc, ini in S.CAST:
        ext = " ext" if name == "Ryan Castellano" else ""
        roster += f'<div class="player{ext}"><div class="num">{ini}</div><div><b>{esc(name)}</b><span>{esc(role)}</span><span>{esc(desc)}</span></div></div>'
    ops = "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td></tr>" for a, b in S.OPS_RULES)
    sp = "".join(f"<tr><td><b>{esc(a[0])}</b></td><td>{esc(a[1])}</td><td>{esc(a[2])}</td><td>{esc(a[3])}</td><td>{esc(a[5])}</td></tr>" for a in S.SPONSORS)
    body = f"""
<section class="session-hero" style="background:linear-gradient(160deg,#16161A,#3B2A12)"><div class="wrap">
<span class="kicker" style="color:var(--gold)">Exhibit room · All evidence is fictional</span>
<h1>The Case File</h1>
<p>Everything the Task Force has to work with: 16 emails, one Teams huddle (with an auto-generated recap you should not trust), the
event plan, sponsor terms, operating rules and four Excel workbooks. Download the kit, or read the evidence right here.</p>
<div class="meta-row" style="display:flex;gap:10px;flex-wrap:wrap;margin-top:18px"><a class="btn" href="data/Session1_Lab_Kit.zip" download>⬇ Session 1 kit (.zip)</a>
<a class="btn gold" href="data/Session2_Lab_Kit.zip" download>⬇ Session 2 kit (.zip)</a></div></div></section>
<section class="band tight"><div class="wrap">
<span class="kicker">The roster</span><h2>Who's who</h2><div class="roster">{roster}</div></div></section>
<section class="band paper"><div class="wrap">
<div class="section-head"><span class="kicker">Exhibit A · 01_Email_Thread_Export.docx</span><h2>The email trail</h2>
<p>Sixteen messages from May 10 to June 15, 2027. Read them in order and you can watch a conditional "looks good to me" turn into "it's approved."</p></div>
<div class="wrap-narrow" style="padding:0"><div class="timeline">{emails}</div></div></div></section>
<section class="band"><div class="wrap two-col">
<div><span class="kicker">Exhibit B · 02_Teams_Ops_Huddle_Transcript.docx</span><h2>{esc(m['title'])}</h2>
<p class="muted">{esc(m['when'])} · Organizer {esc(m['organizer'])} · Not present: {esc(', '.join(m['absent']))}</p>
<div class="card">{lines}</div></div>
<div><span class="kicker">Exhibit B2 · same file</span><h2>The auto-generated recap</h2>
<div class="callout warn"><b class="t">Do not trust - verify</b><p>This recap was generated automatically and never reviewed. Compare every line with the transcript.</p></div>
<div class="card"><ul>{recap}</ul></div></div></div></section>
<section class="band paper"><div class="wrap">
<div class="section-head"><span class="kicker">Exhibits C - D</span><h2>Plans, contracts &amp; rules</h2></div>
<h3>Sponsor commitments (04_Sponsor_Requirements_Summary.docx)</h3>
<div class="table-wrap"><table class="data"><thead><tr><th>Sponsor</th><th>Promotion</th><th>Contract status</th><th>Fee</th><th>Make-good</th></tr></thead><tbody>{sp}</tbody></table></div>
<h3 style="margin-top:30px">Operations playbook (05_Operations_Playbook_Giveaway_Rules.docx)</h3>
<div class="table-wrap"><table class="data"><tbody>{ops}</tbody></table></div></div></section>
<section class="band paper" id="glossary"><div class="wrap"><div class="section-head"><span class="kicker">Scorebook abbreviations</span><h2>Glossary</h2>
<p>The front-office shorthand used throughout the labs.</p></div><div class="gloss">{gloss_html()}</div></div></section>
<section class="band"><div class="wrap"><div class="section-head"><span class="kicker">All files</span><h2>Equipment room</h2></div>
{downloads_html()}</div></section>"""
    return "case-file.html", page_wrap("case-file.html", "Case File", "home", "case", body)


GLOSSARY = [
    ("Make-good", "The credit or replacement a sponsor receives when we deliver less than the contract guarantees."),
    ("UOM · EA · CS", "Unit of measure. EA = each (one unit); CS = case. Convert cases to units with the Item Master case pack."),
    ("Case pack", "Units per case, e.g. 24 bobbleheads per case, 100 towels per case."),
    ("PO", "Purchase order. No PO means nothing has been ordered from the vendor."),
    ("STM", "Season Ticket Member. STM-only items need their own scan lane."),
    ("Redline", "A marked-up counter-proposal to a contract. Not an agreement until both sides sign."),
    ("Countersigned", "Signed by both parties. Only then is an amendment in force."),
    ("Lock date", "The date after which no new promotional items may be added (June 4 for Rally Weekend)."),
    ("Distributable", "Units that can actually go to fans: delivered quantity minus damaged units, on time for the game."),
    ("Net contribution", "Attendance × (margin − variable cost) + sponsorship − promotional costs − fixed costs."),
    ("Per cap", "Revenue per fan through the gates (e.g., merchandise per cap)."),
    ("Tolerance", "The allowed difference between plan and actual (±1% per gate) before it counts as an exception."),
]


def gloss_html():
    return "".join(f'<div class="g-row"><b>{esc(t)}</b><span>{esc(d)}</span></div>' for t, d in GLOSSARY)


DL = {
    1: [
        ("01_Email_Thread_Export.docx", "docx", "Email thread export", "16 emails, May 10 - Jun 15"),
        ("02_Teams_Ops_Huddle_Transcript.docx", "docx", "Teams huddle transcript", "Transcript + unverified recap"),
        ("03_Event_Plan_v3_Riverfront_Rally_Weekend.docx", "docx", "Event Plan v3", "Locked June 4"),
        ("04_Sponsor_Requirements_Summary.docx", "docx", "Sponsor requirements", "Guarantees & make-goods"),
        ("05_Operations_Playbook_Giveaway_Rules.docx", "docx", "Ops playbook", "Reconciliation & approval rules"),
        ("Promo_Allocations_Requests.xlsx", "xlsx", "Promo Allocations & Requests", "Marketing / Sponsorship master"),
        ("Warehouse_Fulfillment_Deliveries.xlsx", "xlsx", "Warehouse Fulfillment & Deliveries", "Logistics system export"),
        ("Promo_Attendance_History_2025_2026.xlsx", "xlsx", "Promo & Attendance History", "163 rows, two seasons"),
        ("Rally_Reconciliation_start.xlsx", "xlsx", "Reconciliation starter", "Inning 4 Part B: both tables in one workbook"),
    ],
    2: [
        ("06_Plot_Twist_Memo_June17.docx", "docx", "Plot Twist memo", "Four changes overnight"),
        ("07_Promotional_Readiness_Checklist.docx", "docx", "Readiness checklist", "Agent grounding"),
        ("08_Event_Standards.docx", "docx", "Event standards", "Agent grounding"),
        ("09_Task_Force_Findings_Session1.docx", "docx", "Session 1 findings", "Reference readiness assessment"),
        ("Rally_Weekend_Budget_Model.xlsx", "xlsx", "Budget model", "Simulator inputs"),
    ],
}


def downloads_html(sessions=(1, 2)):
    out = ""
    for s in sessions:
        files = "".join(
            f'<file href="{{{{root}}}}data/session-{s}/{f}" ext="{e}" title="{t}" desc="{d}"/>' for f, e, t, d in DL[s])
        out += f'<h3 style="margin-top:22px">{SESSION_NAME[s]}</h3><div class="files"><file href="{{{{root}}}}data/Session{s}_Lab_Kit.zip" ext="zip" title="Session {s} lab kit" desc="Every file below in one download"/>{files}</div>'
    return out


def make_zips():
    for s in (1, 2):
        z = ROOT / "data" / f"Session{s}_Lab_Kit.zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            for f, *_ in DL[s]:
                zf.write(ROOT / "data" / f"session-{s}" / f, f"Rally Weekend Task Force/{f}")
            if s == 2:  # session 2 also needs the core reference docs from session 1
                for f in ["03_Event_Plan_v3_Riverfront_Rally_Weekend.docx", "04_Sponsor_Requirements_Summary.docx",
                          "05_Operations_Playbook_Giveaway_Rules.docx", "Promo_Attendance_History_2025_2026.xlsx"]:
                    zf.write(ROOT / "data" / "session-1" / f, f"Rally Weekend Task Force/{f}")


def main():
    written = []
    for p in sorted(PAGES.glob("*.html")):
        txt = p.read_text()
        m = re.match(r"<!--meta (.*?)-->\s*", txt, flags=re.S)
        if not m:
            print("skip (no meta):", p.name)
            continue
        meta = json.loads(m.group(1))
        frag = txt[m.end():]
        frag = frag.replace("{{scoreboard}}", scoreboard(root=rel_root(meta.get("out", "x/y"))) if meta.get("kind") == "page" else scoreboard(root="../"))
        frag = frag.replace("{{labs1}}", lab_rows(1)).replace("{{labs2}}", lab_rows(2))
        frag = frag.replace("{{downloads1}}", downloads_html((1,))).replace("{{downloads2}}", downloads_html((2,)))
        frag = frag.replace("{{downloads}}", downloads_html())
        frag = frag.replace("{{playbook}}", playbook_html(rel_root(meta.get("out", "x/y"))))
        if meta["kind"] == "lab":
            out, doc = build_lab(meta, frag)
        else:
            out = meta["out"]
            doc = page_wrap(out, meta["title"], meta.get("theme", "home"), meta.get("nav", ""), frag,
                            data_page=meta.get("page", ""))
        (ROOT / out).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / out).write_text(doc)
        written.append(out)
    out, doc = case_file()
    (ROOT / out).write_text(doc)
    written.append(out)
    make_zips()
    (ROOT / ".nojekyll").write_text("")
    print("wrote:", ", ".join(written))


if __name__ == "__main__":
    main()
