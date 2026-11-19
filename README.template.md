# Agent Skills

A public, searchable skill library for William's AI agents, devices, and anyone else who wants to browse or reuse them.

**[Open the visual catalog](https://williamlodge.github.io/agent-skills/)** · **[Machine-readable manifest](manifest.json)**

{{STATS}}

## Find a skill

The visual catalog provides instant search, platform filters, visible descriptions, source-folder links, and copy-ready install commands. On GitHub, use **Ctrl+F** (desktop) or your browser's **Find in page** (phone) to search the table below.

Each `SKILL.md` is the entry point. Keep its complete folder together so scripts, references, examples, and assets remain available.

## Import new skills

1. Create a ZIP containing a `skills/` folder, or an `all-skills/` folder with `shared-agents/`, `claude/`, and `kimi/` subfolders.
2. Open [`inbox/`](inbox/) and choose **Add file → Upload files**.
3. Upload the ZIP and commit it to `main`.

The **Import skill archive** action safely merges every ZIP in the inbox, rebuilds the visual catalog, this README, and `manifest.json`, commits the result, and removes the uploaded ZIP. Existing skills are preserved; matching folders are refreshed. No archived script is executed during import.

To rebuild without adding an archive, open **Actions → Import skill archive → Run workflow**.

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
docs/
├── catalog.template.html  # Edit the public page design here
└── index.html             # Generated; do not edit directly
inbox/                     # Upload new ZIP archives here
```

The same skill can appear in more than one platform folder. The catalog lists each skill once and shows every available platform. `manifest.json` retains all copies, including nested collections.

## Notes

- Skills may include instructions, scripts, references, examples, and binary assets; download the whole folder, not just `SKILL.md`.
- Some skills came from third-party collections. Their original notices remain in their folders; no additional license is granted by this repository.
- Review a skill before running its scripts, especially on a new device.
