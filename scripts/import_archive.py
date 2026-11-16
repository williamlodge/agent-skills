#!/usr/bin/env python3
"""Safely unpack the uploaded skill archive without running any archived code."""

from pathlib import Path, PurePosixPath
from zipfile import ZipFile
import shutil
import tempfile

REPO = Path(__file__).resolve().parents[1]
ARCHIVE = REPO / "all-skills-20261116.zip"
TARGET = REPO / "all-skills"


def main() -> None:
    if not ARCHIVE.is_file():
        raise SystemExit(
            "Missing all-skills-20261116.zip. Upload it to the repository root, "
            "then run this workflow again."
        )

    with ZipFile(ARCHIVE) as archive:
        for info in archive.infolist():
            path = PurePosixPath(info.filename)
            if path.is_absolute() or ".." in path.parts:
                raise SystemExit(f"Unsafe archive path: {info.filename}")
            if not path.parts or path.parts[0] != "all-skills":
                raise SystemExit(f"Unexpected archive path: {info.filename}")

        temp_name = tempfile.mkdtemp(prefix=".skill-import-", dir=REPO)
        temp = Path(temp_name)
        try:
            archive.extractall(temp)
            extracted = temp / "all-skills"
            if not extracted.is_dir():
                raise SystemExit("The ZIP did not contain an all-skills directory.")
            if TARGET.exists():
                shutil.rmtree(TARGET)
            shutil.move(str(extracted), str(TARGET))
        finally:
            shutil.rmtree(temp, ignore_errors=True)

    ARCHIVE.unlink()
    print(f"Imported {sum(1 for path in TARGET.rglob('*') if path.is_file())} files.")


if __name__ == "__main__":
    main()
