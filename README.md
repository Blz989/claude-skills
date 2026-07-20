# brandon-claude-skills

Spec-compliant repack of [borghei/Claude-Skills](https://github.com/borghei/Claude-Skills)
for use as a Claude plugin marketplace (claude.ai web, desktop, Claude Code).

Why: upstream declares `"skills": "./"` with skills nested in category folders,
which the claude.ai web loader rejects (shows "no skills or agents").
This repo flattens every skill to `plugins/<plugin>/skills/<name>/SKILL.md`.

## Refresh from upstream
```
git clone --depth 1 https://github.com/borghei/Claude-Skills.git /tmp/upstream
python3 transform.py /tmp/upstream .
git add -A && git commit -m "sync upstream" && git push
```

Upstream license: MIT + Commons Clause (see LICENSE). Internal/personal use only; do not resell.
