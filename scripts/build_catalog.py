#!/usr/bin/env python3
"""Build the README catalog, machine manifest, and public browsing page."""

from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote
import html
import json
import yaml

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "all-skills"
DOCS = REPO / "docs"
REPO_URL = "https://github.com/williamlodge/agent-skills"
RAW_URL = "https://raw.githubusercontent.com/williamlodge/agent-skills/main"
PLATFORMS = ("shared-agents", "claude", "kimi")
LABELS = {"shared-agents": "Shared", "claude": "Claude", "kimi": "Kimi"}


def read_skill(path: Path) -> dict:
    relative = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    metadata = {}
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                metadata = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError:
                metadata = {}
    if not isinstance(metadata, dict):
        metadata = {}
    return {
        "name": str(metadata.get("name") or relative.parts[-2]).strip(),
        "description": " ".join(str(metadata.get("description") or "No description provided.").split()),
        "platform": relative.parts[0],
        "path": relative.parent.as_posix(),
        "skill_md": relative.as_posix(),
    }


def clean_description(value: str) -> str:
    return html.escape(value, quote=False).replace("|", "\\|")


def link(path: str) -> str:
    return quote(path, safe="/")


def platform_rank(platform: str) -> int:
    return PLATFORMS.index(platform) if platform in PLATFORMS else len(PLATFORMS)


def main() -> None:
    if not ROOT.is_dir():
        raise SystemExit("No all-skills directory found; import an archive first.")

    copies = [read_skill(path) for path in ROOT.rglob("SKILL.md")]
    if not copies:
        raise SystemExit("No SKILL.md files found.")

    grouped = defaultdict(list)
    for copy in copies:
        grouped[copy["name"]].append(copy)

    def rank(copy: dict) -> tuple:
        return (
            "/synced/" in f"/{copy['path']}/",
            platform_rank(copy["platform"]),
            copy["path"].count("/"),
            copy["path"],
        )

    skills = []
    table = ["| Skill | Description | Available for |", "|---|---|---|"]
    for name in sorted(grouped, key=str.casefold):
        entries = sorted(grouped[name], key=rank)
        primary = entries[0]
        platforms = sorted({entry["platform"] for entry in entries}, key=platform_rank)
        manifest_copies = []
        for entry in sorted(entries, key=lambda item: (platform_rank(item["platform"]), item["path"])):
            manifest_copies.append({
                "platform": entry["platform"],
                "path": entry["path"],
                "skill_md": entry["skill_md"],
                "raw_url": f"{RAW_URL}/all-skills/{link(entry['skill_md'])}",
            })
        folder_url = f"{REPO_URL}/tree/main/all-skills/{link(primary['path'])}"
        skills.append({
            "name": name,
            "description": primary["description"],
            "platforms": platforms,
            "primary_path": primary["path"],
            "primary_skill_md": primary["skill_md"],
            "primary_raw_url": f"{RAW_URL}/all-skills/{link(primary['skill_md'])}",
            "folder_url": folder_url,
            "copies": manifest_copies,
        })
        platform_text = ", ".join(LABELS.get(item, item) for item in platforms)
        table.append(f"| [{name}]({folder_url}) | {clean_description(primary['description'])} | {platform_text} |")

    all_files = [path for path in ROOT.rglob("*") if path.is_file()]
    size_mb = sum(path.stat().st_size for path in all_files) / 1_000_000
    counts = Counter(copy["platform"] for copy in copies)
    stats = (
        f"**{len(skills)} unique skills · {len(copies)} platform copies · "
        f"{len(all_files):,} files · {size_mb:.1f} MB unpacked**\n\n"
        f"Shared agents: {counts['shared-agents']} copies · "
        f"Claude: {counts['claude']} copies · Kimi: {counts['kimi']} copies."
    )

    template = (REPO / "README.template.md").read_text(encoding="utf-8")
    readme = template.replace("{{STATS}}", stats).replace("{{CATALOG}}", "\n".join(table))
    (REPO / "README.md").write_text(readme, encoding="utf-8")
    manifest = {
        "version": 1,
        "repository": REPO_URL,
        "default_branch": "main",
        "skill_count": len(skills),
        "copy_count": len(copies),
        "file_count": len(all_files),
        "skills": skills,
    }
    (REPO / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    page_template = (DOCS / "catalog.template.html").read_text(encoding="utf-8")
    browser_data = json.dumps(skills, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    replacements = {
        "{{SKILLS_JSON}}": browser_data,
        "{{SKILL_COUNT}}": str(len(skills)),
        "{{COPY_COUNT}}": str(len(copies)),
        "{{FILE_COUNT}}": f"{len(all_files):,}",
        "{{SIZE_MB}}": f"{size_mb:.1f}",
    }
    page = page_template
    for marker, value in replacements.items():
        page = page.replace(marker, value)
    (DOCS / "index.html").write_text(page, encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Cataloged {len(skills)} unique skills across {len(copies)} platform copies.")


if __name__ == "__main__":
    main()
