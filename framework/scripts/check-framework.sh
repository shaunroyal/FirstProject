#!/bin/sh
# check-framework.sh: validate the AI-assisted repo framework files.
#
# Usage: sh framework/scripts/check-framework.sh [options]
#   --root DIR              repo root (default: two levels above this script)
#   --latest X.Y.Z          latest framework release, used for the version-drift check
#   --max-minor-behind N    allowed minor versions behind --latest (default: 2)
#   --strict                treat version drift as a failure instead of a warning
#   -h, --help              show this help
#
# Exit codes: 0 = passed (warnings allowed), 1 = one or more checks failed, 2 = usage error.
# POSIX sh only. Needs: awk, grep, sed, find, cut, tr, mktemp (busybox is enough).

set -u

ROOT=""
LATEST=""
MAX_MINOR_BEHIND=2
STRICT=0
FAILS=0
WARNS=0

usage() { sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; }

while [ $# -gt 0 ]; do
  case "$1" in
    --root) [ $# -ge 2 ] || { echo "--root needs a value" >&2; exit 2; }; ROOT=$2; shift 2 ;;
    --latest) [ $# -ge 2 ] || { echo "--latest needs a value" >&2; exit 2; }; LATEST=$2; shift 2 ;;
    --max-minor-behind) [ $# -ge 2 ] || { echo "--max-minor-behind needs a value" >&2; exit 2; }; MAX_MINOR_BEHIND=$2; shift 2 ;;
    --strict) STRICT=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if [ -z "$ROOT" ]; then
  ROOT=$(cd "$(dirname "$0")/../.." && pwd) || exit 2
fi
[ -d "$ROOT" ] || { echo "Root not found: $ROOT" >&2; exit 2; }
case "$MAX_MINOR_BEHIND" in ''|*[!0-9]*) echo "--max-minor-behind must be a whole number" >&2; exit 2 ;; esac

TMP=$(mktemp "${TMPDIR:-/tmp}/check-framework.XXXXXX") || exit 2
trap 'rm -f "$TMP"' EXIT INT TERM

pass() { printf 'PASS  %s\n' "$1"; }
warn() { printf 'WARN  %s\n' "$1"; WARNS=$((WARNS + 1)); }
fail() { printf 'FAIL  %s\n' "$1"; FAILS=$((FAILS + 1)); }
section() { printf '\n== %s\n' "$1"; }
rel() { printf '%s' "${1#"$ROOT"/}"; }

# Value of a top-level "key: value" line in .ai-framework.yml (quotes and trailing comments removed).
yml_value() {
  awk -v key="$1" -v q="'" '
    { sub(/\r$/, "") }
    index($0, key ":") == 1 {
      v = substr($0, length(key) + 2)
      sub(/[[:space:]]+#.*$/, "", v)
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", v)
      gsub("^[\"" q "]|[\"" q "]$", "", v)
      print v
      exit
    }' "$ROOT/.ai-framework.yml"
}

# 0 if the file starts with a closed YAML frontmatter block.
has_frontmatter() {
  awk '
    { sub(/\r$/, "") }
    NR == 1 { if ($0 != "---") exit 1; next }
    $0 == "---" { found = 1; exit }
    END { exit found ? 0 : 1 }' "$1"
}

# Value of a frontmatter key (quotes removed). Empty if absent.
fm_value() {
  awk -v key="$2" -v q="'" '
    { sub(/\r$/, "") }
    NR == 1 { if ($0 != "---") exit; next }
    $0 == "---" { exit }
    index($0, key ":") == 1 {
      v = substr($0, length(key) + 2)
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", v)
      gsub("^[\"" q "]|[\"" q "]$", "", v)
      print v
      exit
    }' "$1"
}

is_semver() { printf '%s' "$1" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$'; }

printf 'Framework check: %s\n' "$ROOT"

# ---------------------------------------------------------------------------
section "Required files"
for f in AGENTS.md README.md .ai-framework.yml docs/constitution.md \
         .github/pull_request_template.md .github/copilot-instructions.md framework/WORKFLOW.md; do
  if [ -f "$ROOT/$f" ]; then pass "$f exists"; else fail "$f is missing"; fi
done

if [ ! -f "$ROOT/.ai-framework.yml" ]; then
  printf '\nResult: FAILED (%s failure(s), %s warning(s)). .ai-framework.yml is required for the remaining checks.\n' "$FAILS" "$WARNS"
  exit 1
fi

TEMPLATE_MODE=$(yml_value template_mode)
VERSION=$(yml_value framework_version)
case "$TEMPLATE_MODE" in
  true) printf '\nMode: template repo (template_mode: true)\n' ;;
  false) printf '\nMode: project repo (template_mode: false)\n' ;;
  *) fail ".ai-framework.yml: template_mode must be true or false (found '$TEMPLATE_MODE')"; TEMPLATE_MODE=false ;;
esac

# ---------------------------------------------------------------------------
section "Framework version"
if [ -z "$VERSION" ]; then
  fail ".ai-framework.yml: framework_version is missing"
elif ! is_semver "$VERSION"; then
  fail ".ai-framework.yml: framework_version '$VERSION' is not X.Y.Z"
else
  pass "framework_version is $VERSION"
  if [ -n "$LATEST" ]; then
    if ! is_semver "$LATEST"; then
      fail "--latest '$LATEST' is not X.Y.Z"
    else
      cur_major=$(echo "$VERSION" | cut -d. -f1); cur_minor=$(echo "$VERSION" | cut -d. -f2)
      lat_major=$(echo "$LATEST" | cut -d. -f1); lat_minor=$(echo "$LATEST" | cut -d. -f2)
      drift=""
      if [ "$cur_major" -lt "$lat_major" ]; then
        drift="a major version behind ($VERSION < $LATEST)"
      elif [ "$cur_major" -eq "$lat_major" ] && [ $((lat_minor - cur_minor)) -gt "$MAX_MINOR_BEHIND" ]; then
        drift="$((lat_minor - cur_minor)) minor versions behind $LATEST (limit $MAX_MINOR_BEHIND)"
      fi
      if [ -n "$drift" ]; then
        if [ "$STRICT" -eq 1 ]; then fail "framework is $drift. Run /sync-framework"
        else warn "framework is $drift. Run /sync-framework"; fi
      else
        pass "within $MAX_MINOR_BEHIND minor versions of $LATEST"
      fi
    fi
  fi
fi

# ---------------------------------------------------------------------------
section "Ownership lists"
for key in framework_owned project_owned; do
  if grep -Eq "^[[:space:]]+$key:" "$ROOT/.ai-framework.yml"; then pass "ownership.$key defined"
  else fail ".ai-framework.yml: ownership.$key is missing"; fi
done

# ---------------------------------------------------------------------------
section "Placeholders in project context files"
if [ "$TEMPLATE_MODE" = "true" ]; then
  pass "skipped in template mode"
else
  : > "$TMP"
  for f in AGENTS.md README.md CHANGELOG.md docs/constitution.md docs/architecture.md \
           .github/CODEOWNERS .github/pull_request_template.md .ai-framework.yml; do
    [ -f "$ROOT/$f" ] && printf '%s\n' "$ROOT/$f" >> "$TMP"
  done
  if [ -d "$ROOT/.github/instructions/project" ]; then
    find "$ROOT/.github/instructions/project" -type f -name '*.md' >> "$TMP"
  fi
  found=0
  while IFS= read -r f; do
    hits=$(grep -n '<FILL:' "$f" | cut -d: -f1 | tr '\n' ' ')
    if [ -n "$hits" ]; then fail "$(rel "$f"): unfilled <FILL: ...> on line(s) $hits"; found=1; fi
  done < "$TMP"
  [ "$found" -eq 0 ] && pass "no <FILL: ...> tokens left"
  if [ -f "$ROOT/README.md" ] && grep -q 'template-only:start' "$ROOT/README.md"; then
    fail "README.md still contains the template-only section. Run /start-project"
  fi
fi

# ---------------------------------------------------------------------------
section "Skills (.github/skills/<name>/SKILL.md)"
count=0
for d in "$ROOT"/.github/skills/*/; do
  [ -d "$d" ] || continue
  dir=${d%/}; name=${dir##*/}; f="$dir/SKILL.md"
  count=$((count + 1))
  if [ ! -f "$f" ]; then fail "$(rel "$dir"): missing SKILL.md"; continue; fi
  if ! has_frontmatter "$f"; then fail "$(rel "$f"): missing or unclosed frontmatter"; continue; fi
  fm_name=$(fm_value "$f" name)
  desc=$(fm_value "$f" description)
  ok=1
  if ! printf '%s' "$fm_name" | grep -Eq '^[a-z0-9-]{1,64}$'; then
    fail "$(rel "$f"): name '$fm_name' must be 1-64 lowercase letters, digits or hyphens"; ok=0
  elif [ "$fm_name" != "$name" ]; then
    fail "$(rel "$f"): name '$fm_name' must match folder '$name'"; ok=0
  fi
  if [ -z "$desc" ]; then fail "$(rel "$f"): description is missing"; ok=0
  elif [ "${#desc}" -gt 1024 ]; then fail "$(rel "$f"): description is over 1024 characters"; ok=0; fi
  [ "$ok" -eq 1 ] && pass "$(rel "$f")"
done
[ "$count" -eq 0 ] && fail "no skills found in .github/skills/"

# ---------------------------------------------------------------------------
section "Prompt files and custom agents"
count=0
for f in "$ROOT"/.github/prompts/*.prompt.md "$ROOT"/.github/agents/*.agent.md; do
  [ -f "$f" ] || continue
  count=$((count + 1))
  if ! has_frontmatter "$f"; then fail "$(rel "$f"): missing or unclosed frontmatter"
  elif [ -z "$(fm_value "$f" description)" ]; then fail "$(rel "$f"): description is missing"
  else pass "$(rel "$f")"; fi
done
[ "$count" -eq 0 ] && pass "none present"

# ---------------------------------------------------------------------------
section "Scoped instructions (*.instructions.md)"
: > "$TMP"
for d in "$ROOT/.github/instructions" "$ROOT/framework/catalogue"; do
  [ -d "$d" ] && find "$d" -type f -name '*.instructions.md' >> "$TMP"
done
count=0
while IFS= read -r f; do
  count=$((count + 1))
  if ! has_frontmatter "$f"; then fail "$(rel "$f"): missing or unclosed frontmatter"; continue; fi
  desc=$(fm_value "$f" description); apply=$(fm_value "$f" applyTo)
  case "$f" in
    "$ROOT"/framework/catalogue/*|"$ROOT"/.github/instructions/catalogue/*)
      if [ -z "$desc" ] || [ -z "$apply" ]; then fail "$(rel "$f"): catalogue files need description and applyTo"; continue; fi ;;
    *)
      if [ -z "$desc" ] && [ -z "$apply" ]; then fail "$(rel "$f"): needs description and/or applyTo"; continue; fi ;;
  esac
  pass "$(rel "$f")"
done < "$TMP"
[ "$count" -eq 0 ] && warn "no *.instructions.md files found"

# ---------------------------------------------------------------------------
section "Stack catalogue"
if [ "$TEMPLATE_MODE" = "true" ]; then
  for d in "$ROOT"/framework/catalogue/*/; do
    [ -d "$d" ] || continue
    stack=${d%/}; stack=${stack##*/}
    n=$(find "$d" -maxdepth 1 -type f -name '*.instructions.md' | wc -l | tr -d ' ')
    if [ ! -f "$d/README.md" ]; then fail "catalogue/$stack: missing README.md"
    elif ! grep -q '^Use when:' "$d/README.md"; then fail "catalogue/$stack/README.md: missing 'Use when:' line"
    elif [ "$n" -eq 0 ]; then fail "catalogue/$stack: no *.instructions.md files"
    else pass "catalogue/$stack ($n instruction files)"; fi
  done
else
  stacks=$(yml_value stacks | tr -d '[]' | tr ',' ' ')
  if [ -z "$(printf '%s' "$stacks" | tr -d ' ')" ]; then
    warn ".ai-framework.yml: no stacks installed (expected at least 'generic')"
  fi
  for stack in $stacks; do
    inst="$ROOT/.github/instructions/catalogue/$stack"
    src="$ROOT/framework/catalogue/$stack"
    if [ ! -d "$inst" ]; then fail "stack '$stack' listed but .github/instructions/catalogue/$stack/ is missing"; continue; fi
    pass "stack '$stack' installed"
    if [ -d "$src" ]; then
      for s in "$src"/*.instructions.md; do
        [ -f "$s" ] || continue
        t="$inst/${s##*/}"
        if [ ! -f "$t" ]; then warn "stack '$stack': ${s##*/} not installed. Run /sync-framework"
        elif ! cmp -s "$s" "$t"; then warn "stack '$stack': ${s##*/} differs from framework/catalogue (local edits to a framework-owned file?)"; fi
      done
    fi
  done
fi

# ---------------------------------------------------------------------------
section "Secret scan"
: > "$TMP"
if command -v git >/dev/null 2>&1 && git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git -C "$ROOT" ls-files -co --exclude-standard | sed "s|^|$ROOT/|" > "$TMP"
else
  find "$ROOT" -type d \( -name .git -o -name node_modules -o -name .terraform -o -name .venv \) -prune -o -type f -print > "$TMP"
fi
SELF="$ROOT/framework/scripts/check-framework.sh"
pk='-----BEGIN [A-Z ]*PRIVATE'' KEY-----'
patterns="AKIA[0-9A-Z]{16}|$pk|gh[pousr]_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{40,}|xox[abprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35}|\"private_key_id\"[[:space:]]*:"
found=0
while IFS= read -r f; do
  [ -f "$f" ] || continue
  [ "$f" = "$SELF" ] && continue
  hits=$(grep -I -n -E "$patterns" "$f" 2>/dev/null | cut -d: -f1 | tr '\n' ' ')
  if [ -n "$hits" ]; then fail "$(rel "$f"): possible secret on line(s) $hits"; found=1; fi
done < "$TMP"
[ "$found" -eq 0 ] && pass "no common secret patterns found"

# ---------------------------------------------------------------------------
printf '\n'
if [ "$FAILS" -gt 0 ]; then
  printf 'Result: FAILED (%s failure(s), %s warning(s))\n' "$FAILS" "$WARNS"
  exit 1
fi
printf 'Result: PASSED (%s warning(s))\n' "$WARNS"
exit 0
