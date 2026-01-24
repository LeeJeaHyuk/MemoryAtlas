
import os
import shutil

from core.config import LEGACY_DIRS_TO_ARCHIVE, MIGRATION_MAP_V1, MIGRATION_MAP_V2_TO_V3
from utils.fs import safe_move


def migrate_v1_to_v2(root: str, dry_run: bool = False) -> None:
    """Migrate from v1.x structure to v2.x structure."""
    archive_dir = os.path.join(root, "99_ARCHIVE", "v1_migration")
    print("\n=== Migrating v1.x -> v2.x ===")

    for old_rel, new_rel in MIGRATION_MAP_V1.items():
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


def migrate_v2_to_v3(root: str, dry_run: bool = False) -> None:
    """Migrate from v2.x structure to v3.0 structure (capabilities & invariants)."""
    print("\n=== Migrating v2.x -> v3.0 (Capabilities & Invariants) ===")
    
    migrated = False
    for old_rel, new_rel in MIGRATION_MAP_V2_TO_V3.items():
        old_path = os.path.join(root, old_rel)
        new_path = os.path.join(root, new_rel)
        
        if not os.path.exists(old_path):
            continue
        
        if not os.path.isdir(old_path):
            continue
        
        # Move all files from old to new (merge if target exists)
        files_moved = 0
        for item in os.listdir(old_path):
            src = os.path.join(old_path, item)
            dst = os.path.join(new_path, item)
            
            if os.path.exists(dst):
                if dry_run:
                    print(f"  - Would skip (exists): {old_rel}/{item}")
                else:
                    print(f"  ! Skipped (exists): {old_rel}/{item}")
                continue
            
            if dry_run:
                print(f"  - Would move: {old_rel}/{item} -> {new_rel}/{item}")
                files_moved += 1
            else:
                # Ensure target directory exists (only when actually moving)
                os.makedirs(new_path, exist_ok=True)
                shutil.move(src, dst)
                print(f"  * Moved: {old_rel}/{item} -> {new_rel}/{item}")
                files_moved += 1
        
        # Remove old directory if empty or only README.md remains
        if not dry_run and os.path.exists(old_path):
            remaining = os.listdir(old_path)
            if not remaining:
                os.rmdir(old_path)
                print(f"  * Removed empty: {old_rel}/")
            elif remaining == ["README.md"]:
                # README.md will be regenerated in new folder, safe to delete
                os.remove(os.path.join(old_path, "README.md"))
                os.rmdir(old_path)
                print(f"  * Removed old: {old_rel}/ (README.md only)")
            else:
                print(f"  ! Old folder not empty: {old_rel}/ ({len(remaining)} items remain)")
        
        if files_moved > 0:
            migrated = True
    
    if not migrated and not dry_run:
        print("  (No v2.x files to migrate)")


def is_v1_structure(root: str) -> bool:
    """Check if the current structure is v1.x"""
    v1_markers = [
        os.path.join(root, "02_SERVICES"),
        os.path.join(root, "03_MANAGEMENT"),
        os.path.join(root, "90_TOOLING"),
    ]
    return any(os.path.exists(m) for m in v1_markers)


def is_v2_structure(root: str) -> bool:
    """Check if the current structure is v2.x (has features/business_rules)"""
    v2_markers = [
        os.path.join(root, "02_REQUIREMENTS", "features"),
        os.path.join(root, "02_REQUIREMENTS", "business_rules"),
    ]
    return any(os.path.exists(m) for m in v2_markers)
