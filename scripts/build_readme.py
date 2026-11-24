#!/usr/bin/env python3
"""Baut README.md aus README.template.md + profile.toml (keine Abhängigkeiten, Python 3.11+)."""
import tomllib
from pathlib import Path
from urllib.parse import quote, quote_plus

ROOT = Path(__file__).resolve().parent.parent
cfg = tomllib.loads((ROOT / "profile.toml").read_text(encoding="utf-8"))
h, user = cfg["header"], cfg["github"]["username"]
accent = h["accent"]


def gradient(colors):
    n = len(colors) - 1
    return ",".join(f"{round(i * 100 / n)}:{c}" for i, c in enumerate(colors))


def shield_label(text):
    # shields.io: "-" → "--", "_" → "__", Rest URL-kodieren
    return quote(text.replace("-", "--").replace("_", "__"), safe="")


grad = gradient(h["gradient"])
capsule = (
    "https://capsule-render.vercel.app/api?type=waving&height=200"
    f"&color={grad}&text={quote(h['name'])}&fontColor=ffffff&fontSize=60&fontAlignY=38"
    f"&desc={quote(h['subtitle'])}&descAlignY=58&descSize=16&animation=fadeIn"
)
typing = (
    "https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=20"
    f"&duration=3000&pause=1000&color={accent}&center=true&vCenter=true&width=680"
    f"&lines={';'.join(quote_plus(l) for l in h['typing'])}"
)
links = "\n".join(
    f'  <a href="{l["url"]}"><img src="https://img.shields.io/badge/{shield_label(l["label"])}-111111'
    f'?style=flat-square&logo={l["logo"]}&logoColor={accent}" /></a>'
    for l in h.get("links", [])
)

header = f"""<!-- Header -->
<p align="center">
  <img src="{capsule}" width="100%" />
</p>

<p align="center">
  <a href="https://github.com/{user}">
    <img src="{typing}" alt="Typing SVG" />
  </a>
</p>

<p align="center">
{links}
  <img src="https://komarev.com/ghpvc/?username={user}&color=111111&style=flat-square&label=views" />
</p>
"""

footer = f"""<!-- Footer -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=100&section=footer&color={grad}" width="100%" />
</p>
"""

def project_card(p):
    title = f'<a href="{p["url"]}">{p["name"]}</a>' if p.get("url") else p["name"]
    if p.get("emoji"):
        title = f'{p["emoji"]} {title}'
    lines = [
        "  <tr>",
        '    <td width="100%">',
        f"      <h3>{title}</h3>",
        f"      <p>{p['description']}</p>",
    ]
    items = p.get("items", [])
    if items:
        lines.append("      <p>")
        lines.append("<br>\n".join(f"        <b>{i['name']}</b> · {i['description']}" for i in items))
        lines.append("      </p>")
    badges = p.get("badges", [])
    if badges:
        lines.append("      <p>")
        lines += [
            f'        <img src="https://img.shields.io/badge/{shield_label(b["label"])}-111111'
            f'?style=flat-square&logo={b["logo"]}&logoColor={accent}" />'
            for b in badges
        ]
        lines.append("      </p>")
    lines += ["    </td>", "  </tr>"]
    return "\n".join(lines)


projects = "<table>\n" + "\n".join(project_card(p) for p in cfg.get("projects", [])) + "\n</table>\n"

tpl = (ROOT / "README.template.md").read_text(encoding="utf-8")
tpl = tpl.split("\n", 1)[1] if tpl.startswith("<!-- Diese Datei") else tpl
out = tpl.replace("{{HEADER}}\n", header + "\n").replace("{{FOOTER}}\n", footer).replace("{{PROJECTS}}\n", projects)
(ROOT / "README.md").write_text(out, encoding="utf-8")
print("README.md aktualisiert")
