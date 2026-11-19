# Agent Skills

A public, searchable skill library with visible descriptions, source links, install commands, and a repeatable ZIP importer.

## Finish the initial import

The importer and catalog generator are ready. The skill archive itself is uploaded through GitHub's web interface so its binary files remain intact.

1. Open [`inbox/`](inbox/).
2. Choose **Add file → Upload files**.
3. Upload `skills.zip` and commit it to `main`.
4. Open **Actions** and wait for **Import skill archive** to show a green checkmark.

The action safely merges the archive into `all-skills/shared-agents/`, builds the README catalog, `manifest.json`, and `docs/index.html`, commits those files, and removes the ZIP. It does not execute archived scripts.

## Enable the public catalog

After the import succeeds:

1. Open **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Select **main** and **/docs**, then click **Save**.

GitHub will publish the catalog at:

**https://williamlodge.github.io/agent-skills/**

## Add more skills later

Upload another ZIP to [`inbox/`](inbox/). New skills are merged without deleting unrelated existing skills. The catalog and manifest rebuild automatically after every import.

See [`README.template.md`](README.template.md) for the generated catalog layout and [`inbox/README.md`](inbox/README.md) for accepted ZIP structures.
