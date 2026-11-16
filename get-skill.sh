#!/usr/bin/env bash
set -euo pipefail

NAME="${1:-}"
PLATFORM="${2:-}"
DESTINATION="${3:-$PWD/skills}"
MANIFEST_URL="https://raw.githubusercontent.com/williamlodge/agent-skills/main/manifest.json"
REPO_URL="https://github.com/williamlodge/agent-skills.git"

if [[ -z "$NAME" ]]; then
  echo "Usage: bash get-skill.sh <skill-name> [platform] [destination]" >&2
  exit 2
fi
for command_name in git python3; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Missing required command: $command_name" >&2
    exit 2
  fi
done

TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

python3 - "$NAME" "$PLATFORM" "$MANIFEST_URL" "$TEMP_DIR/skill-path" <<'PY'
import json
from pathlib import Path
import sys
from urllib.request import urlopen

name, platform, manifest_url, output = sys.argv[1:]
with urlopen(manifest_url, timeout=30) as response:
    manifest = json.load(response)
skill = next((item for item in manifest["skills"] if item["name"] == name), None)
if skill is None:
    raise SystemExit(f"Skill not found: {name}. Search the repository catalog for the exact name.")
if platform:
    copy = next((item for item in skill["copies"] if item["platform"] == platform), None)
    if copy is None:
        available = ", ".join(skill["platforms"])
        raise SystemExit(f"{name} is not available for {platform}. Available: {available}")
else:
    copy = next((item for item in skill["copies"] if item["platform"] == "shared-agents"), None)
    if copy is None:
        copy = next(item for item in skill["copies"] if item["path"] == skill["primary_path"])
Path(output).write_text(copy["path"], encoding="utf-8")
PY

SKILL_PATH="$(cat "$TEMP_DIR/skill-path")"
TARGET="$DESTINATION/$NAME"
if [[ -e "$TARGET" ]]; then
  echo "Destination already exists; refusing to overwrite: $TARGET" >&2
  exit 3
fi

git clone --quiet --depth 1 --filter=blob:none --sparse "$REPO_URL" "$TEMP_DIR/repository"
git -C "$TEMP_DIR/repository" sparse-checkout set "all-skills/$SKILL_PATH"
mkdir -p "$DESTINATION"
cp -R "$TEMP_DIR/repository/all-skills/$SKILL_PATH" "$TARGET"
printf 'Installed %s to %s\n' "$NAME" "$TARGET"
