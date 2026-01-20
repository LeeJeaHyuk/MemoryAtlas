
import os
import shutil

from core.config import LEGACY_DIRS_TO_ARCHIVE, MIGRATION_MAP
from utils.fs import safe_move

def migrate_v1_to_v2(root: str, dry_run: bool = False) -> None:
    """Migrate from v1.x structure to v2.x structure."""
    archive_dir = os.path.join(root, "99_ARCHIVE", "v1_migration")
    print("\n=== Migrating v1.x -> v2.x ===")

    for old_rel, new_rel in MIGRATION_MAP.items():
        old_path = os.path.join(root, old_rel)
        if not os.path.exists(old_path):
            continue

        if new_rel is None:
            archive_path = os.path.join(archive_dir, old_rel)
            if dry_run:
                print(f"  - Would archive: {old_rel}")
            else:
                if safe_move(old_path, archive_path):
                    print(f"  * Archived: {old_rel}")
        else:
            new_path = os.path.join(root, new_rel)
            if dry_run:
                print(f"  - Would move: {old_rel} -> {new_rel}")
            else:
                if safe_move(old_path, new_path):
                    print(f"  * Moved: {old_rel} -> {new_rel}")

    for legacy_dir in LEGACY_DIRS_TO_ARCHIVE:
        legacy_path = os.path.join(root, legacy_dir)
        if os.path.isdir(legacy_path):
            archive_path = os.path.join(archive_dir, legacy_dir)
            if dry_run:
                print(f"  - Would archive directory: {legacy_dir}")
            else:
                if not os.path.exists(archive_path):
                    shutil.move(legacy_path, archive_path)
                    print(f"  * Archived and removed: {legacy_dir}")
                else:
                    shutil.rmtree(legacy_path)
                    print(f"  * Removed legacy (already archived): {legacy_dir}")

def is_v1_structure(root: str) -> bool:
    """Check if the current structure is v1.x"""
    v1_markers = [
        os.path.join(root, "02_SERVICES"),
        os.path.join(root, "03_MANAGEMENT"),
        os.path.join(root, "90_TOOLING"),
    ]
    return any(os.path.exists(m) for m in v1_markers)
