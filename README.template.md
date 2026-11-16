# Agent Skills

A central, browsable skill library for William's AI agents and devices. Use the catalog below to find a skill, open its folder, and read its `SKILL.md` plus any supporting files.

{{STATS}}

## Find a skill

Use **Ctrl+F** (desktop) or your browser's **Find in page** (phone) to search the catalog by name, task, or platform. Select a skill name to open its folder. `SKILL.md` is the entry point; keep that folder's scripts, references, and assets with it.

For a machine-readable version, use [`manifest.json`](manifest.json). It contains every description, platform copy, folder path, and raw `SKILL.md` URL.

## Get the library on any device

### Windows, Mac, or Linux

```bash
git clone https://github.com/williamlodge/agent-skills.git
```

### Android with Termux

```bash
pkg install git
git clone https://github.com/williamlodge/agent-skills.git
```

## Download just one skill

From a local copy of this repository:

**Windows PowerShell:**

```powershell
.\get-skill.ps1 -Name pickeros-shipping-suggestions
```

**Mac, Linux, or Termux:**

```bash
bash get-skill.sh pickeros-shipping-suggestions
```

Both commands default to `shared-agents`, fall back to another available platform, and copy the complete skill folder into `skills/`. To request a specific platform or destination:

```powershell
.\get-skill.ps1 -Name pickeros-shipping-suggestions -Platform claude -Destination .\skills
```

```bash
bash get-skill.sh pickeros-shipping-suggestions claude ./skills
```

## Prompt for an AI agent

Copy this into an agent that can browse the web:

> Browse https://github.com/williamlodge/agent-skills and find the skill that matches my task. Read its SKILL.md first, download every supporting file in that skill folder, and then follow the skill. If several platform copies exist, prefer shared-agents, then the copy made for my agent.

## Skill catalog

{{CATALOG}}

## Folder layout

```text
all-skills/
├── shared-agents/   # Agent-neutral copies; default choice
├── claude/          # Claude-specific copies
└── kimi/            # Kimi-specific copies
```

The same skill can appear in more than one platform folder. The catalog lists each skill once and shows every available platform. `manifest.json` retains all copies, including nested collections.

## Add or refresh skills

Upload a new archive named `all-skills-20261116.zip` to the repository root. The **Import skill archive** GitHub Action safely unpacks it, rebuilds this catalog and `manifest.json`, commits the result, and removes the ZIP. No archived script is executed during import.

## Notes

- Skills may include instructions, scripts, references, examples, and binary assets; download the whole folder, not just `SKILL.md`.
- Some skills came from third-party collections. Their original notices remain in their folders; no additional license is granted by this repository.
- Review a skill before running its scripts, especially on a new device.
