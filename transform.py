#!/usr/bin/env python3
"""Transform borghei/Claude-Skills into a spec-compliant Claude plugin marketplace.

Usage: python3 transform.py <upstream_dir> <output_dir>
Re-run any time upstream updates, then commit and push the output repo.
"""
import json, re, shutil, sys
from pathlib import Path

def load_frontmatter_name(skill_md: Path):
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return None, text
    fm = m.group(1)
    nm = re.search(r"^name:\s*(.+)$", fm, re.M)
    return (nm.group(1).strip() if nm else None), text

def ensure_name(skill_md: Path, fallback: str):
    name, text = load_frontmatter_name(skill_md)
    if name:
        return name
    if text.startswith("---"):
        text = text.replace("---", f"---\nname: {fallback}", 1)
    else:
        text = f"---\nname: {fallback}\ndescription: {fallback}\n---\n" + text
    skill_md.write_text(text, encoding="utf-8")
    return fallback

def main(upstream: Path, out: Path):
    mp = json.load(open(upstream / ".claude-plugin" / "marketplace.json"))
    if out.exists():
        shutil.rmtree(out)
    (out / ".claude-plugin").mkdir(parents=True)
    plugins_out, report = [], []

    for entry in mp["plugins"]:
        pname = entry["name"]
        src = upstream / entry["source"].lstrip("./")
        if not src.is_dir():
            report.append(f"SKIP {pname}: source {src} missing"); continue
        pdir = out / "plugins" / pname
        skdir = pdir / "skills"
        skdir.mkdir(parents=True)
        # manifest: default skills/ layout, no custom paths
        manifest = {
            "name": pname,
            "description": entry.get("description", ""),
            "version": entry.get("version", "1.0.0"),
            "author": entry.get("author", {"name": "borghei"}),
            "repository": "https://github.com/borghei/Claude-Skills",
            "license": "MIT + Commons Clause",
        }
        (pdir / ".claude-plugin").mkdir()
        (pdir / ".claude-plugin" / "plugin.json").write_text(
            json.dumps(manifest, indent=2), encoding="utf-8")
        # collect every skill folder (any depth), flatten by basename
        seen = {}
        for smd in sorted(src.rglob("SKILL.md")):
            sfold = smd.parent
            # skip fixtures nested inside another skill's folder
            if any((anc / "SKILL.md").exists()
                   for anc in sfold.parents if src in anc.parents):
                continue
            base = sfold.name
            if base in seen:
                base = f"{sfold.parent.name}-{base}"  # collision guard
            seen[base] = sfold
            dest = skdir / base
            shutil.copytree(sfold, dest)
            ensure_name(dest / "SKILL.md", base)
        # domain docs: keep at plugin root, and drop CLAUDE.md into skills/
        # so intra-skill "../CLAUDE.md" links still resolve
        for doc in src.glob("*.md"):
            shutil.copy2(doc, pdir / doc.name)
            if doc.name == "CLAUDE.md":
                shutil.copy2(doc, skdir / "CLAUDE.md")
        plugins_out.append({
            "name": pname,
            "source": f"./plugins/{pname}",
            "description": entry.get("description", ""),
            "version": entry.get("version", "1.0.0"),
            "author": entry.get("author", {"name": "borghei"}),
            "category": entry.get("category", ""),
            "keywords": entry.get("keywords", []),
        })
        report.append(f"OK   {pname}: {len(seen)} skills")

    market = {
        "name": "brandon-claude-skills",
        "owner": {"name": "Brandon Lopez"},
        "description": ("Spec-compliant repack of borghei/Claude-Skills "
                        "(skills flattened into skills/ per plugin). "
                        "Rebuilt by transform.py; upstream: "
                        "https://github.com/borghei/Claude-Skills"),
        "plugins": plugins_out,
    }
    (out / ".claude-plugin" / "marketplace.json").write_text(
        json.dumps(market, indent=2), encoding="utf-8")
    for f in ("LICENSE",):
        if (upstream / f).exists():
            shutil.copy2(upstream / f, out / f)
    print("\n".join(report))
    print(f"TOTAL plugins: {len(plugins_out)}")

if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
