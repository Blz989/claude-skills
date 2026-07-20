#!/usr/bin/env bash
# Fails loudly if any plugin's skills/ layout would confuse the strict claude.ai web loader.
# Rule derived from observed loader behavior: it registers exactly the immediate
# subdirectories of skills/. A registered folder MUST carry its own SKILL.md.
set -e
root="$(cd "$(dirname "$0")" && pwd)"
fail=0
for p in "$root"/plugins/*/; do
  name=$(basename "$p")
  [ -d "$p/skills" ] || { echo "FAIL $name: no skills/ dir"; fail=1; continue; }
  for d in "$p"/skills/*/; do
    if [ ! -f "$d/SKILL.md" ]; then
      echo "FAIL $name: skills/$(basename "$d")/ has no SKILL.md (would register as an empty/ghost skill)"; fail=1
    fi
  done

  # link integrity within this plugin
  if [ -d "$p/reference" ]; then
    stale=$(grep -rhoE '(execution|discovery|strategy-frameworks|gtm|career)/[a-z0-9-]+' "$p"/skills/*/SKILL.md "$p"/reference/*/REFERENCE.md 2>/dev/null | wc -l | tr -d ' ')
    [ "$stale" = 0 ] || { echo "FAIL $name: $stale stale category-prefixed cross-link(s) (e.g. execution/foo/)"; fail=1; }
  fi

  # mangled run-commands: `<name>`scripts/ (rewrite artifact)
  if grep -rqE '`[a-z0-9-]+`/?scripts/' "$p"/skills/*/SKILL.md 2>/dev/null; then
    echo "FAIL $name: backtick glued to scripts/ path in a run-command"; fail=1
  fi
  reg=$(find "$p/skills" -maxdepth 1 -mindepth 1 -type d | wc -l | tr -d ' ')
  printf "OK   %-30s %s registered skill(s)\n" "$name" "$reg"
done
if [ "$fail" = 0 ]; then echo "ALL PLUGINS PASS"; else echo "REGRESSIONS FOUND"; exit 1; fi
