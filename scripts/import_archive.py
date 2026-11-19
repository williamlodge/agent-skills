#!/usr/bin/env python3
"""Safely merge uploaded skill archives without executing archived code."""

from pathlib import Path, PurePosixPath
from zipfile import ZipFile
import shutil
import stat
import tempfile

REPO = Path(__file__).resolve().parents[1]
INBOX = REPO / "inbox"
LEGACY_ARCHIVE = REPO / "all-skills-20261116.zip"
TARGET = REPO / "all-skills"
MAX_UNPACKED_BYTES = 1_000_000_000


def pending_archives() -> list[Path]:
    archives = sorted(INBOX.glob("*.zip")) if INBOX.is_dir() else []
    if LEGACY_ARCHIVE.is_file():
        archives.append(LEGACY_ARCHIVE)
    return archives


def validate_archive(archive: ZipFile) -> None:
    total_size = 0
    for info in archive.infolist():
        path = PurePosixPath(info.filename)
        mode = info.external_attr >> 16
        if path.is_absolute() or ".." in path.parts:
            raise SystemExit(f"Unsafe archive path: {info.filename}")
        if stat.S_ISLNK(mode):
            raise SystemExit(f"Symbolic links are not allowed: {info.filename}")
        total_size += info.file_size
        if total_size > MAX_UNPACKED_BYTES:
            raise SystemExit("Archive exceeds the 1 GB unpacked import limit.")


def import_one(archive_path: Path) -> None:
    temp = Path(tempfile.mkdtemp(prefix=".skill-import-", dir=REPO))
    try:
        with ZipFile(archive_path) as archive:
            validate_archive(archive)
            archive.extractall(temp)

        if (temp / "all-skills").is_dir():
            source = temp / "all-skills"
            destination = TARGET
        elif (temp / "skills").is_dir():
            source = temp / "skills"
            destination = TARGET / "shared-agents"
        elif any(temp.rglob("SKILL.md")):
            source = temp
            destination = TARGET / "shared-agents"
        else:
            raise SystemExit(f"{archive_path.name} contains no SKILL.md files.")

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, destination, dirs_exist_ok=True)
        archive_path.unlink()
        imported = sum(1 for path in source.rglob("*") if path.is_file())
        print(f"Merged {imported} files from {archive_path.name}.")
    finally:
        shutil.rmtree(temp, ignore_errors=True)


def main() -> None:
    archives = pending_archives()
    if not archives:
        print("No ZIP archives waiting in inbox; rebuilding the existing catalog only.")
        return
    for archive_path in archives:
        import_one(archive_path)


if __name__ == "__main__":
    main()
