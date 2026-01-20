
from core.config import CURRENT_VERSION, ROOT_DIR
from core.migrate import is_v1_structure, migrate_v1_to_v2
from utils.fs import (
    create_missing_docs,
    ensure_structure,
    read_version,
    update_system_templates,
    update_tooling,
    write_version,
)

def init_or_update(dry_run: bool = False, force_migrate: bool = False) -> None:
    """Initialize or update the memory system."""
    installed_version = read_version(ROOT_DIR)
    print(
        f"Checking Memory System: Installed({installed_version}) "
        f"vs Current({CURRENT_VERSION})"
    )

    needs_migration = force_migrate or (
        installed_version.startswith("1.") and is_v1_structure(ROOT_DIR)
    )

    if needs_migration:
        print("\n[!] Detected v1.x structure. Migration required.")
        migrate_v1_to_v2(ROOT_DIR, dry_run=dry_run)

    ensure_structure(ROOT_DIR)
    create_missing_docs(ROOT_DIR, dry_run=dry_run)
    update_system_templates(ROOT_DIR, dry_run=dry_run)
    update_tooling(ROOT_DIR, dry_run=dry_run)

    if installed_version != CURRENT_VERSION:
        write_version(ROOT_DIR, dry_run=dry_run)
        if dry_run:
            print(f"\nWould update to v{CURRENT_VERSION}")
        else:
            print(f"\n[OK] Updated to v{CURRENT_VERSION}")
    else:
        print("\n[OK] Already up to date.")


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================
