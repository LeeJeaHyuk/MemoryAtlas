
import os
import shutil

from core.config import CURRENT_VERSION, DIRS, DOC_TEMPLATES, SYSTEM_TEMPLATES, UPDATABLE_READMES

def write_file(path: str, content: str, dry_run: bool = False) -> None:
    """Write content to file, creating parent directories if needed."""
    if dry_run:
        return
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def read_text(path: str) -> str:
    """Read text from file with error handling."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def safe_move(src: str, dest: str, dry_run: bool = False) -> bool:
    """Safely move file/directory."""
    if not os.path.exists(src):
        return False
    if dry_run:
        return True
    dest_dir = os.path.dirname(dest)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    if os.path.exists(dest):
        return False
    try:
        shutil.move(src, dest)
        return True
    except Exception as e:
        print(f"  ! Failed to move {src}: {e}")
        return False

def ensure_structure(root: str) -> None:
    """Ensure all required directories exist."""
    for folder in DIRS:
        os.makedirs(os.path.join(root, folder), exist_ok=True)

def create_missing_docs(root: str, dry_run: bool = False) -> None:
    """Create missing template documents."""
    for rel_path, content in DOC_TEMPLATES.items():
        path = os.path.join(root, rel_path)
        if os.path.exists(path):
            continue
        if dry_run:
            print(f"  - Would create doc: {rel_path}")
            continue
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        write_file(path, content)
        print(f"  + Created doc: {rel_path}")

def update_system_templates(root: str, dry_run: bool = False) -> None:
    """Update system-managed template files."""
    for rel_path, content in SYSTEM_TEMPLATES.items():
        path = os.path.join(root, rel_path)
        if dry_run:
            print(f"  - Would update system file: {rel_path}")
            continue
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        write_file(path, content)
        print(f"  * Updated system file: {rel_path}")


def update_readme_files(root: str, dry_run: bool = False) -> None:
    """Update README files that are system-managed."""
    for rel_path in UPDATABLE_READMES:
        if rel_path not in DOC_TEMPLATES:
            continue
        path = os.path.join(root, rel_path)
        content = DOC_TEMPLATES[rel_path]
        if dry_run:
            print(f"  - Would update readme: {rel_path}")
            continue
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        write_file(path, content)
        print(f"  * Updated readme: {rel_path}")

def update_tooling(root: str, dry_run: bool = False) -> None:
    """Copy current script to system scripts directory."""
    src = os.path.abspath(__file__)
    dest = os.path.join(root, "00_SYSTEM", "scripts", "memory_manager.py")
    dest_dir = os.path.dirname(dest)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    if os.path.abspath(src) != os.path.abspath(dest):
        if dry_run:
            print(f"  - Would update tool: {dest}")
            return
        shutil.copyfile(src, dest)
        print(f"  * Updated tool: 00_SYSTEM/scripts/memory_manager.py")

def read_version(root: str) -> str:
    """Read installed version from VERSION file."""
    version_file = os.path.join(root, "VERSION")
    if not os.path.exists(version_file):
        return "0.0.0"
    with open(version_file, "r", encoding="utf-8") as f:
        return f.read().strip()

def write_version(root: str, dry_run: bool = False) -> None:
    """Write current version to VERSION file."""
    version_file = os.path.join(root, "VERSION")
    if dry_run:
        print(f"  - Would update version to: {CURRENT_VERSION}")
        return
    write_file(version_file, CURRENT_VERSION)
