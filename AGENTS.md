# AGENTS.md

PhoneApp keeps its agent context in three places — read them in this order:

1. **[CLAUDE.md](CLAUDE.md)** — the canonical, always-loaded **map**: system overview, repo
   layout, and the Knowledge index ("for X, read Y"). **Start here.**
2. **[Knowledge/](Knowledge/)** — the **domain knowledge base**: one doc per component, each
   with `governs:` frontmatter naming the code it owns. Open the doc for what you're changing.
3. **Skills** — invokable **procedures**; see the skills index in CLAUDE.md. They live in
   `.claude/skills/` once the first one is earned. Always-follow rules live in CLAUDE.md;
   reference policy lives in `Knowledge/`.

Any agent (this harness or another) should read **CLAUDE.md first**. Keep code and `Knowledge/`
in sync with the deterministic, no-LLM rot-guard: `python3 scripts/check_knowledge.py`.
