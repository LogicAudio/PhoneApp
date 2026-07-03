#!/usr/bin/env python3
"""LoWS knowledge rot-guard (Plan 12.5) — deterministic, ZERO LLM tokens.

Keeps the Knowledge/ base honest and in sync with the code. Three jobs:

  HARD (non-zero exit on failure):
    1. Link integrity   — every relative markdown link in the doc set resolves to a real file/dir.
    2. Frontmatter      — every Knowledge/ doc has valid frontmatter (name/type/governs/read_when)
                          and every `governs:` path actually exists in the repo.
    3. Bug hygiene      — Bugs/ files are NNN_snake_topic.md with unique numbers; every OPEN bug
                          (Bugs/ root) has a Description heading and is listed in Bugs/README.md.

  ADVISORY (warn, never blocks — keeps friction low so it never nags on doc-only tweaks):
    3a. Orphans         — Knowledge/ docs not reachable from CLAUDE.md's index.
    3b. Stale strings   — retired-term drift signals, read from Knowledge/_meta/stale_signals.txt.
    3c. Code↔doc drift  — (with --staged) a governed code file is staged but its doc is not.
    3d. Hygiene notes   — a `type: rules` doc with empty governs; scratch .md files at repo root.

Usage:
    python3 scripts/check_knowledge.py            # full scan; HARD checks gate the exit code
    python3 scripts/check_knowledge.py --staged   # also run the drift check vs git-staged files
    python3 scripts/check_knowledge.py --quiet     # only print problems
    python3 scripts/check_knowledge.py --strict    # advisory findings also fail the exit code

Wired into scripts/verify.sh and (advisory) scripts/hooks/pre-commit.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Doc roots we link-check. Only the ones that exist are scanned (handles the mid-migration tree).
ROOT_FILES = ["CLAUDE.md", "AGENTS.md", "README.md"]
DOC_DIRS = ["Knowledge", ".claude/skills", "Plans"]

# Frontmatter is required only here (the canonical knowledge base). _archive is exempt.
FRONTMATTER_ROOT = "Knowledge"
FRONTMATTER_EXEMPT_NAMES = {"README.md"}
VALID_TYPES = {"rules", "runbook", "architecture", "index", "reference"}
REQUIRED_KEYS = ("name", "type", "governs", "read_when")

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")  # inline links; skips ![images]
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)

# Advisory stale-signal denylist, checked line-by-line in NORMATIVE docs only (Knowledge/, CLAUDE.md,
# Documentation/, Rules/) — never in Plans/ (roadmap legitimately describes what to fix) or _archive/.
# The signals live in a DATA file (coexistence spec §8) so this engine stays byte-identical across
# repos: Knowledge/_meta/stale_signals.txt, one `trigger | context | negatable | why` per line,
# " | " (space-pipe-space) separated so regex alternation (a|b) stays intact; missing file = empty set.
# "negatable" signals are skipped when the same line carries a negation/modernization cue (NEG) —
# so "no OpenClaw" and "script.js is now modular js/" don't false-positive.
NEG = re.compile(
    r"\b(no|without|not|non|never|drop|dropp|remov|delete|self-host|native|instead|former|"
    r"legacy|was|used to|no longer|modular|split|migrat)\b|js/|~~|✗|❌|→",
    re.I,
)
STALE_SIGNALS_FILE = "Knowledge/_meta/stale_signals.txt"


def load_stale_signals():
    """Parse the stale-signal data file → [(trigger_re, context_re|None, negatable, why)]."""
    path = REPO / STALE_SIGNALS_FILE
    signals = []
    if not path.exists():
        return signals
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [f.strip() for f in line.split(" | ")]
        trigger, context = parts[0], (parts[1] if len(parts) > 1 and parts[1] else None)
        negatable = len(parts) > 2 and parts[2].lower() in ("yes", "y", "true", "1")
        why = parts[3] if len(parts) > 3 and parts[3] else parts[0]
        try:
            signals.append((re.compile(trigger, re.I),
                            re.compile(context, re.I) if context else None, negatable, why))
        except re.error as exc:
            print(f"⚠️  {STALE_SIGNALS_FILE}: bad regex {trigger!r} ({exc}) — line skipped",
                  file=sys.stderr)
    return signals


STALE_SIGNALS = load_stale_signals()


def in_stale_scope(p: Path) -> bool:
    """Stale-signal checks apply to normative docs only — not roadmap (Plans/) or archives."""
    if "_archive" in p.parts:
        return False
    if p == REPO / "CLAUDE.md":
        return True
    for d in ("Knowledge", "Documentation", "Rules"):
        try:
            p.relative_to(REPO / d)
            return True
        except ValueError:
            continue
    return False


# ── tiny frontmatter parser (stdlib only; we control the format) ──────────────────────────────
def parse_frontmatter(text: str):
    """Return (meta_dict, body) or (None, text) if no leading --- block."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    block = text[3:end].strip("\n")
    body = text[end + 4:]
    meta: dict = {}
    key = None
    for raw in block.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith(("  - ", "- ", "    - ")):  # block-list item
            if key:
                meta.setdefault(key, [])
                if isinstance(meta[key], list):
                    meta[key].append(line.split("-", 1)[1].strip())
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            key = k.strip()
            v = v.strip()
            if v == "":
                meta[key] = []                       # block list follows
            elif v.startswith("[") and v.endswith("]"):
                inner = v[1:-1].strip()
                meta[key] = [x.strip() for x in inner.split(",") if x.strip()]
            else:
                meta[key] = v
    return meta, body


def iter_docs():
    """All .md files in the scanned doc set that currently exist."""
    seen = set()
    for f in ROOT_FILES:
        p = REPO / f
        if p.exists():
            seen.add(p)
    for d in DOC_DIRS:
        base = REPO / d
        if base.is_dir():
            for p in base.rglob("*.md"):
                seen.add(p)
    return sorted(seen)


def strip_code(text: str) -> str:
    return FENCE_RE.sub("", text)


# ── checks ────────────────────────────────────────────────────────────────────────────────────
def check_links(docs):
    """HARD: relative links resolve. Returns list of error strings."""
    errors = []
    for p in docs:
        text = strip_code(p.read_text(encoding="utf-8", errors="ignore"))
        for m in LINK_RE.finditer(text):
            href = m.group(1).split()[0].strip()      # drop optional "title"
            target = href.split("#")[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "#", "tel:")):
                continue
            resolved = (p.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{p.relative_to(REPO)} → broken link: {href}")
    return errors


def check_frontmatter(docs):
    """HARD: Knowledge/ docs have valid frontmatter + governs paths exist."""
    errors = []
    kroot = REPO / FRONTMATTER_ROOT
    for p in docs:
        try:
            p.relative_to(kroot)
        except ValueError:
            continue
        if "_archive" in p.parts or p.name in FRONTMATTER_EXEMPT_NAMES:
            continue
        rel = p.relative_to(REPO)
        if not KEBAB_RE.match(p.name):
            errors.append(f"{rel} → Knowledge doc filename must be kebab-case.md")
        meta, _ = parse_frontmatter(p.read_text(encoding="utf-8", errors="ignore"))
        if meta is None:
            errors.append(f"{rel} → missing YAML frontmatter")
            continue
        for k in REQUIRED_KEYS:
            if k not in meta:
                errors.append(f"{rel} → frontmatter missing '{k}'")
        if isinstance(meta.get("name"), str) and meta["name"] != p.stem:
            errors.append(f"{rel} → frontmatter name '{meta['name']}' != filename stem '{p.stem}'")
        if meta.get("type") and meta["type"] not in VALID_TYPES:
            errors.append(f"{rel} → invalid type '{meta['type']}' (allowed: {sorted(VALID_TYPES)})")
        for gv in meta.get("governs", []) or []:
            if gv in ("-", "none", "None"):
                continue
            # governs entries may be exact paths or globs; require at least one match.
            matches = list(REPO.glob(gv)) if any(c in gv for c in "*?[") else [REPO / gv]
            if not any(mp.exists() for mp in matches):
                errors.append(f"{rel} → governs path not found: {gv}")
    return errors


BUG_NAME_RE = re.compile(r"^\d{3}_[a-z0-9]+(_[a-z0-9]+)*\.md$")
PLAN_NAME_RE = re.compile(r"^\d{2}_[a-z0-9]+(_[a-z0-9]+)*\.md$")
KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.md$")
ROOT_MD_ALLOWLIST = {"README.md", "CLAUDE.md", "AGENTS.md"}


def check_collection_names():
    """HARD: numbered-collection filenames (Plans/) match NN_snake_topic.md (spec §4)."""
    errors = []
    proot = REPO / "Plans"
    if proot.is_dir():
        for p in sorted(proot.glob("*.md")):
            if p.name in ("README.md", "CHANGELOG.md"):
                continue
            if not PLAN_NAME_RE.match(p.name):
                errors.append(f"{p.relative_to(REPO)} → plan filename must match NN_snake_topic.md")
    return errors


def check_hygiene(docs):
    """ADVISORY: rules docs without governs (drift check can't see them); root scratch files."""
    warns = []
    kroot = REPO / FRONTMATTER_ROOT
    for p in docs:
        try:
            p.relative_to(kroot)
        except ValueError:
            continue
        if "_archive" in p.parts or p.name in FRONTMATTER_EXEMPT_NAMES:
            continue
        meta, _ = parse_frontmatter(p.read_text(encoding="utf-8", errors="ignore"))
        if meta and meta.get("type") == "rules" and not [g for g in (meta.get("governs") or [])
                                                         if g not in ("-", "none", "None")]:
            warns.append(f"{p.relative_to(REPO)} → type:rules with empty governs — drift check can't protect it")
    for p in sorted(REPO.glob("*.md")):
        if p.name not in ROOT_MD_ALLOWLIST:
            warns.append(f"{p.name} → scratch .md at repo root — debug/repro notes belong in Tests/ (invariant)")
    return warns


def check_bugs():
    """HARD: bug-collection hygiene (coexistence spec §7) — filename pattern, unique numbers,
    open bugs carry a Description and are listed on the Bugs/README.md front page."""
    errors = []
    broot = REPO / "Bugs"
    if not broot.is_dir():
        return errors
    seen_nums: dict[str, list[str]] = {}
    open_bugs, all_bugs = [], []
    for p in sorted(broot.rglob("*.md")):
        if p.name == "README.md":
            continue
        all_bugs.append(p)
        if p.parent == broot:
            open_bugs.append(p)
    for p in all_bugs:
        rel = p.relative_to(REPO)
        if not BUG_NAME_RE.match(p.name):
            errors.append(f"{rel} → bug filename must match NNN_snake_topic.md")
        else:
            seen_nums.setdefault(p.name[:3], []).append(str(rel))
    for num, files in seen_nums.items():
        if len(files) > 1:
            errors.append(f"duplicate bug number {num}: {', '.join(files)}")
    readme = broot / "README.md"
    readme_text = readme.read_text(encoding="utf-8", errors="ignore") if readme.exists() else ""
    for p in open_bugs:
        rel = p.relative_to(REPO)
        if "## Description" not in p.read_text(encoding="utf-8", errors="ignore"):
            errors.append(f"{rel} → open bug missing '## Description' heading")
        if p.name not in readme_text:
            errors.append(f"{rel} → open bug not listed in Bugs/README.md")
    return errors


def governs_map(docs):
    """code path/glob → [doc rel paths], from Knowledge/ frontmatter."""
    mp: dict[str, list[str]] = {}
    kroot = REPO / FRONTMATTER_ROOT
    for p in docs:
        try:
            p.relative_to(kroot)
        except ValueError:
            continue
        meta, _ = parse_frontmatter(p.read_text(encoding="utf-8", errors="ignore"))
        if not meta:
            continue
        for gv in meta.get("governs", []) or []:
            if gv in ("-", "none", "None"):
                continue
            mp.setdefault(gv, []).append(str(p.relative_to(REPO)))
    return mp


def check_orphans(docs):
    """ADVISORY: Knowledge/ docs unreachable from CLAUDE.md."""
    claude = REPO / "CLAUDE.md"
    if not claude.exists():
        return []
    reachable = set()
    frontier = [claude]
    docset = set(docs)
    while frontier:
        cur = frontier.pop()
        if cur in reachable:
            continue
        reachable.add(cur)
        if cur.suffix != ".md" or not cur.exists():
            continue
        text = strip_code(cur.read_text(encoding="utf-8", errors="ignore"))
        for m in LINK_RE.finditer(text):
            target = m.group(1).split()[0].split("#")[0].strip()
            if not target or target.startswith(("http", "mailto", "#")):
                continue
            nxt = (cur.parent / target).resolve()
            if nxt in docset and nxt not in reachable:
                frontier.append(nxt)
    warns = []
    kroot = REPO / FRONTMATTER_ROOT
    for p in docs:
        try:
            p.relative_to(kroot)
        except ValueError:
            continue
        if "_archive" in p.parts or p.name in FRONTMATTER_EXEMPT_NAMES:
            continue
        if p not in reachable:
            warns.append(f"{p.relative_to(REPO)} → not reachable from CLAUDE.md index")
    return warns


def check_stale(docs):
    """ADVISORY: known drift signals in NORMATIVE docs, line-by-line + negation-aware."""
    warns = []
    for p in docs:
        if not in_stale_scope(p):
            continue
        lines = strip_code(p.read_text(encoding="utf-8", errors="ignore")).splitlines()
        for i, line in enumerate(lines):
            window = line + " " + (lines[i - 1] if i else "")  # span wrapped prose (prev line) for negation
            for trigger, context, negatable, why in STALE_SIGNALS:
                if not trigger.search(line):
                    continue
                if context and not context.search(line):
                    continue
                if negatable and NEG.search(window):
                    continue
                warns.append(f"{p.relative_to(REPO)} → stale signal: {why}")
                break  # one finding per line is enough
    return warns


def check_drift(docs):
    """ADVISORY (--staged): governed code staged without its doc."""
    try:
        out = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=REPO, capture_output=True, text=True, check=True,
        ).stdout
    except Exception:
        return []
    staged = {line.strip() for line in out.splitlines() if line.strip()}
    if not staged:
        return []
    mp = governs_map(docs)
    warns = []
    for gv, owner_docs in mp.items():
        is_glob = any(c in gv for c in "*?[")
        governed_staged = [
            s for s in staged
            if (is_glob and Path(s).match(gv)) or (not is_glob and s == gv)
        ]
        if governed_staged and not any(d in staged for d in owner_docs):
            warns.append(
                f"changed {', '.join(sorted(governed_staged))} but its doc(s) "
                f"{owner_docs} not staged — update the knowledge?"
            )
    return warns


def main(argv):
    staged = "--staged" in argv
    quiet = "--quiet" in argv
    strict = "--strict" in argv
    docs = iter_docs()

    hard = check_links(docs) + check_frontmatter(docs) + check_bugs() + check_collection_names()
    advisory = check_orphans(docs) + check_stale(docs) + check_hygiene(docs)
    if staged:
        advisory += check_drift(docs)

    if not quiet:
        print(f"📚 check_knowledge: scanned {len(docs)} docs across {FRONTMATTER_ROOT}/, "
              f".claude/skills/, Plans/, root")

    if hard:
        print(f"\n❌ {len(hard)} HARD issue(s):")
        for e in hard:
            print(f"   • {e}")
    elif not quiet:
        print("✅ HARD checks pass — links resolve, frontmatter valid, governs paths exist, bugs hygienic.")

    if advisory:
        print(f"\n⚠️  {len(advisory)} advisory note(s):")
        for w in advisory:
            print(f"   • {w}")

    failed = bool(hard) or (strict and bool(advisory))
    if not failed and not quiet:
        print("\n✅ knowledge base healthy.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
