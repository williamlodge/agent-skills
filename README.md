# Agent Skills

A central skill library for William's AI agents and devices: **295 unique skills**, with copies for shared agents, Claude, and Kimi.

## Finish the web-only setup

Two uploads remain because the connected GitHub session cannot write workflow files or binary archives directly.

### 1. Activate the automatic importer

1. Open [`import-skills.yml`](import-skills.yml).
2. Click the **pencil / Edit** icon.
3. In the filename box, replace `import-skills.yml` with `.github/workflows/import-skills.yml`.
4. Click **Commit changes**, then commit to `main`. This moves the file and activates the workflow.

### 2. Upload the skills archive

1. Return to the repository root and choose **Add file → Upload files**.
2. Drag in `all-skills-20261116.zip` without renaming it.
3. Click **Commit changes**.

The **Import skill archive** GitHub Action will then automatically:

1. Safely unpack all 4,891 skill files without executing archived code.
2. Replace this page with a searchable catalog of all 295 skill names and descriptions.
3. Publish `manifest.json` with raw download URLs for AI agents.
4. Commit the complete library and remove the uploaded ZIP.

After that action finishes, browse the catalog on this page or clone the repository:

```bash
git clone https://github.com/williamlodge/agent-skills.git
```

See [`README.template.md`](README.template.md) for the catalog and installation layout that will be published.
