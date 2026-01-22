
import os
import re
from typing import Optional

from core.config import *
from utils.fs import read_text, read_version

def iter_md_files(root: str, dirs: list[str]) -> list[str]:
    """Iterate over markdown files in specified directories."""
    files = []
    for base in dirs:
        base_path = os.path.join(root, base)
        if not os.path.isdir(base_path):
            continue
        for dirpath, _, filenames in os.walk(base_path):
            for name in filenames:
                if name.lower().endswith(".md"):
                    files.append(os.path.join(dirpath, name))
    return files

def get_doc_type(path: str) -> str:
    """Determine document type from path."""
    if "capabilities" in path:
        return "capabilities"
    if "invariants" in path:
        return "invariants"
    if "decisions" in path:
        return "decisions"
    if "discussions" in path:
        return "discussions"
    if "active" in path and "RUN-" in os.path.basename(path):
        return "runs"
    return "default"

def check_structure(root: str) -> int:
    """Validate directory structure and required files."""
    issues = 0
    if not os.path.isdir(root):
        print(f"! Missing root directory: {root}")
        return 1

    for folder in DIRS:
        path = os.path.join(root, folder)
        if not os.path.isdir(path):
            print(f"! Missing directory: {folder}")
            issues += 1

    required_files = set(DOC_TEMPLATES.keys())
    required_files.add("VERSION")
    required_files.update(SYSTEM_TEMPLATES.keys())

    for rel_path in sorted(required_files):
        path = os.path.join(root, rel_path)
        if not os.path.exists(path):
            print(f"! Missing file: {rel_path}")
            issues += 1

    installed_version = read_version(root)
    if installed_version != CURRENT_VERSION:
        print(
            f"! Version mismatch: installed {installed_version} "
            f"vs current {CURRENT_VERSION}"
        )
        issues += 1

    print(f"\nStructure check: {issues} issue(s)")
    return issues

def check_mcp(root: str, target: Optional[str] = None) -> int:
    """Validate MCP bootstrap outputs (templates and scripts)."""
    issues = 0
    mcp_dir = os.path.join(root, "00_SYSTEM", "mcp")
    templates_dir = os.path.join(mcp_dir, "templates")
    scripts_dir = os.path.join(root, "00_SYSTEM", "scripts")

    required_files = [
        os.path.join(mcp_dir, "README.md"),
        os.path.join(mcp_dir, "mcp_server.py"),
    ]
    for path in required_files:
        if not os.path.exists(path):
            rel = os.path.relpath(path, root)
            print(f"! Missing MCP file: {rel}")
            issues += 1

    if not os.path.isdir(templates_dir):
        print("! Missing MCP templates directory: 00_SYSTEM/mcp/templates")
        issues += 1
    else:
        if target:
            template_path = os.path.join(templates_dir, f"{target}.mcp.json")
            if not os.path.exists(template_path):
                rel = os.path.relpath(template_path, root)
                print(f"! Missing MCP template for target: {rel}")
                issues += 1
        else:
            templates = [f for f in os.listdir(templates_dir) if f.endswith(".json")]
            if not templates:
                print("! No MCP templates found in 00_SYSTEM/mcp/templates")
                issues += 1

    script_ps1 = os.path.join(scripts_dir, "run_mcp_server.ps1")
    script_sh = os.path.join(scripts_dir, "run_mcp_server.sh")
    if not os.path.exists(script_ps1):
        print("! Missing MCP run script: 00_SYSTEM/scripts/run_mcp_server.ps1")
        issues += 1
    if not os.path.exists(script_sh):
        print("! Missing MCP run script: 00_SYSTEM/scripts/run_mcp_server.sh")
        issues += 1

    print(f"MCP check: {issues} issue(s)")
    return issues

def lint_metadata(root: str) -> int:
    """Check metadata headers in documents."""
    issues = 0
    for path in iter_md_files(root, LINT_DIRS):
        name = os.path.basename(path)
        if name in LINT_SKIP_FILES:
            continue

        text = read_text(path)
        head = "\n".join(text.splitlines()[:40])

        doc_type = get_doc_type(path)
        required_fields = HEADER_FIELDS_BY_TYPE.get(
            doc_type, HEADER_FIELDS_BY_TYPE["default"]
        )

        missing = [field for field in required_fields if field not in head]
        if missing:
            rel_path = os.path.relpath(path, root)
            print(f"! Missing header fields in {rel_path}: {', '.join(missing)}")
            issues += 1

    print(f"Metadata lint: {issues} issue(s)")
    return issues

def iter_links(text: str) -> list[str]:
    """Extract markdown links from text, excluding code blocks."""
    links = []
    in_code = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for match in LINK_RE.finditer(line):
            links.append(match.group(1).strip())
    return links

def check_links(root: str, allow_absolute: bool = False) -> int:
    """Validate links in markdown documents."""
    issues = 0
    for path in iter_md_files(root, LINK_SCAN_DIRS):
        text = read_text(path)
        for target in iter_links(text):
            if not target:
                continue
            if target.startswith("#"):
                continue
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue

            clean = target.split("#", 1)[0].split("?", 1)[0].strip()
            if not clean:
                continue
            if clean.startswith("<") and clean.endswith(">"):
                clean = clean[1:-1].strip()

            is_absolute = os.path.isabs(clean) or re.match(r"^[A-Za-z]:", clean)
            if is_absolute:
                rel_path = os.path.relpath(path, root)
                if not allow_absolute:
                    print(f"! Absolute path link forbidden in {rel_path}: {target}")
                    issues += 1
                elif not os.path.exists(clean):
                    print(f"! Broken absolute link in {rel_path}: {target}")
                    issues += 1
                continue

            resolved = os.path.normpath(os.path.join(os.path.dirname(path), clean))
            if not os.path.exists(resolved):
                rel_path = os.path.relpath(path, root)
                print(f"! Broken link in {rel_path}: {target}")
                issues += 1

    print(f"Link check: {issues} issue(s)")
    return issues

def extract_id_from_filename(filename: str) -> Optional[str]:
    """Extract document ID from filename."""
    name = os.path.splitext(filename)[0]
    if REQ_ID_PATTERN.match(name):
        return name
    if RULE_ID_PATTERN.match(name):
        return name
    if DISC_ID_PATTERN.match(name):
        return name
    if RUN_ID_PATTERN.match(name):
        return name
    return None

def extract_meta_id(text: str) -> Optional[str]:
    """Extract document ID from **ID**: metadata line (authority source)."""
    match = META_ID_RE.search(text)
    if match:
        return match.group(1)
    return None

def parse_must_read(text: str) -> tuple[list[str], list[str], list[str]]:
    """Parse Must-Read and return (ids, invalid_links, disallowed_ids)."""
    match = MUST_READ_RE.search(text)
    if not match:
        return [], [], []

    refs = match.group(1).strip()
    ids: list[str] = []
    invalid_links: list[str] = []
    disallowed_ids: list[str] = []
    seen_ids: set[str] = set()
    seen_invalid: set[str] = set()
    seen_disallowed: set[str] = set()

    for link_match in MUST_READ_LINK_RE.finditer(refs):
        link_text = link_match.group(1).strip()
        if not link_text:
            if "<empty>" not in seen_invalid:
                invalid_links.append("<empty>")
                seen_invalid.add("<empty>")
            continue
        if MUST_READ_ANY_ID_RE.fullmatch(link_text):
            if MUST_READ_ALLOWED_ID_RE.fullmatch(link_text):
                if link_text not in seen_ids:
                    ids.append(link_text)
                    seen_ids.add(link_text)
            else:
                if link_text not in seen_disallowed:
                    disallowed_ids.append(link_text)
                    seen_disallowed.add(link_text)
        else:
            if link_text not in seen_invalid:
                invalid_links.append(link_text)
                seen_invalid.add(link_text)

    refs_without_links = MUST_READ_LINK_RE.sub(" ", refs)
    for id_match in MUST_READ_ANY_ID_RE.finditer(refs_without_links):
        candidate = id_match.group(0)
        if MUST_READ_ALLOWED_ID_RE.fullmatch(candidate):
            if candidate not in seen_ids:
                ids.append(candidate)
                seen_ids.add(candidate)
        else:
            if candidate not in seen_disallowed:
                disallowed_ids.append(candidate)
                seen_disallowed.add(candidate)

    return ids, invalid_links, disallowed_ids

def extract_must_read(text: str) -> list[str]:
    """Extract allowed Must-Read IDs from document."""
    ids, _, _ = parse_must_read(text)
    return ids

def extract_header_ids(
    text: str, patterns: Optional[list[re.Pattern]] = None
) -> list[str]:
    """Extract IDs from header lines (for sync validation)."""
    header_ids: list[str] = []
    scan_patterns = patterns or [REQ_HEADER_RE, RULE_HEADER_RE]
    for pattern in scan_patterns:
        for match in pattern.finditer(text):
            header_ids.append(match.group(1))
    return header_ids

def check_requirements(root: str) -> int:
    """Validate requirement documents with authority model."""
    issues = 0
    seen_ids: dict[str, str] = {}
    all_ids: set[str] = set()

    # First pass: collect all IDs
    for path in iter_md_files(root, REQ_SCAN_DIRS):
        text = read_text(path)
        meta_id = extract_meta_id(text)
        if meta_id:
            all_ids.add(meta_id)

    # Fix F: Collect DISC IDs so they can be referenced
    for path in iter_md_files(root, ["02_REQUIREMENTS/discussions"]):
        text = read_text(path)
        meta_id = extract_meta_id(text)
        if meta_id:
            all_ids.add(meta_id)

    # Also collect RULE IDs
    for path in iter_md_files(root, ["02_REQUIREMENTS/invariants"]):
        text = read_text(path)
        meta_id = extract_meta_id(text)
        if meta_id:
            all_ids.add(meta_id)

    # Also collect ADR IDs (v2.2.1: P0 fix - validate ADR references)
    for path in iter_md_files(root, ["03_TECH_SPECS/decisions"]):
        text = read_text(path)
        meta_id = extract_meta_id(text)
        if meta_id:
            all_ids.add(meta_id)
        else:
            # Fallback: extract ADR ID from filename (ADR-NNN-*.md)
            filename = os.path.basename(path)
            adr_match = re.match(r"(ADR-\d{3})", filename)
            if adr_match:
                all_ids.add(adr_match.group(1))

    # Second pass: validate
    for path in iter_md_files(root, REQ_SCAN_DIRS):
        text = read_text(path)
        rel_path = os.path.relpath(path, root)
        filename = os.path.basename(path)

        if filename == "README.md":
            continue

        # === AUTHORITY: Extract ID from **ID**: metadata ===
        meta_id = extract_meta_id(text)
        filename_id = extract_id_from_filename(filename)
        if (filename_id and filename_id.startswith("REQ-")) or (
            meta_id and meta_id.startswith("REQ-")
        ):
            expected_patterns = [REQ_HEADER_RE]
        elif (filename_id and filename_id.startswith("RULE-")) or (
            meta_id and meta_id.startswith("RULE-")
        ):
            expected_patterns = [RULE_HEADER_RE]
        else:
            expected_patterns = [REQ_HEADER_RE, RULE_HEADER_RE]

        header_ids = extract_header_ids(text, patterns=expected_patterns)
        header_ids_any = extract_header_ids(
            text, patterns=[REQ_HEADER_RE, RULE_HEADER_RE, DISC_HEADER_RE, RUN_HEADER_RE]
        )

        # --- Validation 1: **ID**: must exist ---
        if meta_id is None:
            print(f"! Missing **ID**: metadata in {rel_path}")
            print(f"    -> Add: > **ID**: REQ-DOMAIN-NNN or RULE-DOMAIN-NNN")
            issues += 1
            if filename_id:
                meta_id = filename_id

        # --- Validation 2: Filename format check ---
        if filename_id is None:
            print(f"! Invalid filename format in {rel_path}")
            print(f"    -> Expected: REQ-[DOMAIN]-[NNN].md or RULE-[DOMAIN]-[NNN].md")
            issues += 1

        # --- Validation 3: Filename must match **ID**: ---
        if meta_id and filename_id and meta_id != filename_id:
            print(f"! Filename does not match **ID**: in {rel_path}")
            print(f"    -> **ID**: {meta_id}")
            print(f"    -> Filename: {filename_id}")
            issues += 1

        # --- Validation 4: Header must match **ID**: ---
        if meta_id and header_ids:
            if meta_id not in header_ids:
                print(f"! Header does not match **ID**: in {rel_path}")
                print(f"    -> **ID**: {meta_id}")
                print(f"    -> Header(s): {', '.join(header_ids)}")
                issues += 1
        elif meta_id and not header_ids:
            if header_ids_any:
                print(f"! Header type mismatch in {rel_path}")
                print(f"    -> **ID**: {meta_id}")
                print(f"    -> Header(s): {', '.join(header_ids_any)}")
                issues += 1
            else:
                print(f"! Missing header with ID in {rel_path}")
                print(f"    -> Fix: Add header # [{meta_id}] Feature/Rule Name")
                issues += 1

        # --- Validation 5: Must-Read field exists (v2.2) ---
        must_read_match = MUST_READ_RE.search(text)
        must_read_ids, invalid_links, disallowed_ids = parse_must_read(text)
        if must_read_match is None:
            print(f"! Missing **Must-Read**: field in {rel_path}")
            print(f"    -> Add: > **Must-Read**: RULE-XXX-001, ADR-XXX")
            issues += 1
        else:
            if invalid_links:
                print(f"! Must-Read link text must be an ID in {rel_path}")
                print(f"    -> Invalid link text: {', '.join(invalid_links)}")
                issues += 1
            if disallowed_ids:
                print(f"! Must-Read allows only RULE/ADR IDs in {rel_path}")
                print(f"    -> Disallowed ID(s): {', '.join(disallowed_ids)}")
                issues += 1
            # Fix B: Fail if Must-Read is empty (but present)
            if not must_read_ids:
                print(f"! Empty **Must-Read**: list in {rel_path}")
                print(
                    f"    -> MUST specify at least one ID (or 'None' if genuinely none, though rare)"
                )
                issues += 1

        # --- Validation 6: Must-Read references exist (v2.2.1: includes ADR) ---
        for ref_id in must_read_ids:
            if ref_id and ref_id not in all_ids:
                print(f"! Must-Read reference not found in {rel_path}: {ref_id}")
                issues += 1

        # --- Validation 7: Duplicate ID check ---
        if meta_id:
            if meta_id in seen_ids:
                print(
                    f"! Duplicate ID {meta_id} in {rel_path} "
                    f"(also in {seen_ids[meta_id]})"
                )
                issues += 1
            else:
                seen_ids[meta_id] = rel_path

    print(f"Requirement check: {issues} issue(s)")
    return issues

def check_runs(root: str) -> int:
    """Validate RUN documents (Execution Unit model) with 3-way ID consistency."""
    issues = 0

    for path in iter_md_files(root, RUN_SCAN_DIRS):
        text = read_text(path)
        rel_path = os.path.relpath(path, root)
        filename = os.path.basename(path)

        if filename == "README.md":
            continue

        # === v2.2.1: 3-way ID consistency for RUN documents ===
        meta_id = extract_meta_id(text)
        filename_id = os.path.splitext(filename)[0]  # RUN ID is full filename
        header_match = RUN_HEADER_RE.search(text)
        header_id = header_match.group(1) if header_match else None

        # Check filename format
        if not RUN_ID_PATTERN.match(filename_id):
            print(f"! Invalid RUN filename format: {rel_path}")
            print(f"    -> Expected: RUN-REQ-[DOMAIN]-[NNN]-step-[NN].md")
            issues += 1

        # --- Validation: **ID**: must exist ---
        if meta_id is None:
            print(f"! Missing **ID**: metadata in {rel_path}")
            print(f"    -> Add: > **ID**: {filename_id}")
            issues += 1
            meta_id = filename_id  # Fallback for subsequent checks

        # --- Validation: Filename must match **ID**: ---
        if meta_id and meta_id != filename_id:
            print(f"! Filename does not match **ID**: in {rel_path}")
            print(f"    -> **ID**: {meta_id}")
            print(f"    -> Filename: {filename_id}")
            issues += 1

        # --- Validation: Header must match **ID**: ---
        if meta_id and header_id and meta_id != header_id:
            print(f"! Header does not match **ID**: in {rel_path}")
            print(f"    -> **ID**: {meta_id}")
            print(f"    -> Header: {header_id}")
            issues += 1
        elif meta_id and not header_id:
            print(f"! Missing header with ID in {rel_path}")
            print(f"    -> Fix: Add header # [{meta_id}] Step Description")
            issues += 1

        # Check required fields
        # Check required fields
        # Fix E: Use regex search instead of string containment
        if not RUN_INPUT_RE.search(text):
            print(f"! Missing **Input**: field in {rel_path}")
            issues += 1

        if not RUN_VERIFICATION_RE.search(text):
            print(f"! Missing **Verification**: field in {rel_path}")
            issues += 1

        # Check Output section exists
        # Fix D: RUN_OUTPUT_RE updated to support ### Output
        if not RUN_OUTPUT_RE.search(text):
            print(f"! Missing ## Output section in {rel_path}")
            issues += 1

    print(f"RUN document check: {issues} issue(s)")
    return issues

def check_discussions(root: str) -> int:
    """Validate DISCUSSION documents (3-way ID consistency)."""
    issues = 0
    # Fix F: Add DISC validation
    for path in iter_md_files(root, ["02_REQUIREMENTS/discussions"]):
        text = read_text(path)
        rel_path = os.path.relpath(path, root)
        filename = os.path.basename(path)

        if filename == "README.md":
            continue

        meta_id = extract_meta_id(text)
        filename_id = extract_id_from_filename(filename)
        header_ids = extract_header_ids(text, patterns=[DISC_HEADER_RE])

        # 1. **ID**: metadata existence
        if meta_id is None:
            print(f"! Missing **ID**: metadata in {rel_path}")
            issues += 1
            if filename_id:
                meta_id = filename_id

        # 2. Filename format
        if filename_id is None:
            print(f"! Invalid DISC filename format in {rel_path}")
            issues += 1

        # 3. Filename vs Meta ID
        if meta_id and filename_id and meta_id != filename_id:
            print(f"! Filename does not match **ID**: in {rel_path}")
            print(f"    -> **ID**: {meta_id}")
            print(f"    -> Filename: {filename_id}")
            issues += 1

        # 4. Header vs Meta ID
        if meta_id and header_ids:
            if meta_id not in header_ids:
                print(f"! Header does not match **ID**: in {rel_path}")
                print(f"    -> **ID**: {meta_id}")
                print(f"    -> Header(s): {', '.join(header_ids)}")
                issues += 1
        elif meta_id and not header_ids:
            print(f"! Missing header with ID in {rel_path}")
            print(f"    -> Fix: Add header # [{meta_id}] Discussion Title")
            issues += 1

    print(f"Discussion check: {issues} issue(s)")
    return issues

def doctor(root: str, allow_absolute_links: bool = False) -> int:
    """Run all checks at once."""
    print("\n" + "=" * 60)
    print("  MemoryAtlas Doctor - Full System Check")
    print("=" * 60)

    total_issues = 0

    print("\n[1/6] Structure Check")
    print("-" * 40)
    total_issues += check_structure(root)

    print("\n[2/6] Metadata Lint")
    print("-" * 40)
    total_issues += lint_metadata(root)

    print("\n[3/6] Link Validation")
    print("-" * 40)
    total_issues += check_links(root, allow_absolute=allow_absolute_links)

    print("\n[4/6] Requirement Validation (Authority)")
    print("-" * 40)
    total_issues += check_requirements(root)

    print("\n[5/6] RUN Document Validation (Execution)")
    print("-" * 40)
    total_issues += check_runs(root)

    print("\n[6/6] Discussion Validation (Reference)")
    print("-" * 40)
    total_issues += check_discussions(root)

    print("\n" + "=" * 60)
    if total_issues == 0:
        print("  [OK] All checks passed!")
    else:
        print(f"  [!] Total issues found: {total_issues}")
    print("=" * 60)

    return total_issues


# ============================================================================
# MAIN
# ============================================================================
