# Skill import inbox

Upload one or more `.zip` archives to this folder using **Add file → Upload files**.

Accepted layouts:

- `skills/` — imported into `all-skills/shared-agents/`
- `all-skills/` — preserves its `shared-agents/`, `claude/`, and `kimi/` structure
- A bare collection of skill folders containing `SKILL.md` files — imported into `all-skills/shared-agents/`

The **Import skill archive** workflow merges the files without deleting unrelated existing skills, rebuilds the public catalog and `manifest.json`, and removes the ZIP after a successful import.

Do not upload secrets or private code. This repository and its catalog are public. Review third-party skills before running their scripts.
