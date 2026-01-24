
import os
from datetime import datetime

def status_report(root: str, show_recent: int = 5) -> int:
    """Report on active tasks and knowledge base."""
    print("\n=== Status Report ===")

    # Count active tasks
    active_dir = os.path.join(root, "04_TASK_LOGS", "active")
    active_tasks: list[tuple[str, float]] = []
    if os.path.isdir(active_dir):
        for f in os.listdir(active_dir):
            if f.endswith(".md") and f != "README.md":
                fpath = os.path.join(active_dir, f)
                mtime = os.path.getmtime(fpath)
                active_tasks.append((f, mtime))

    active_tasks.sort(key=lambda x: x[1], reverse=True)

    # Count archived tasks
    archive_dir = os.path.join(root, "04_TASK_LOGS", "archive")
    archive_count = 0
    if os.path.isdir(archive_dir):
        for root_dir, dirs, files in os.walk(archive_dir):
            for f in files:
                if f.endswith(".md") and f != "README.md":
                    archive_count += 1

    # Count by type
    req_count = 0
    rule_count = 0
    cq_count = 0
    disc_count = 0

    for scan_dir in ["02_REQUIREMENTS/capabilities"]:
        req_path = os.path.join(root, scan_dir)
        if os.path.isdir(req_path):
            for f in os.listdir(req_path):
                if f.endswith(".md") and f != "README.md":
                    req_count += 1

    for scan_dir in ["02_REQUIREMENTS/invariants"]:
        rule_path = os.path.join(root, scan_dir)
        if os.path.isdir(rule_path):
            for f in os.listdir(rule_path):
                if f.endswith(".md") and f != "README.md":
                    rule_count += 1

    for scan_dir in ["02_REQUIREMENTS/competencies"]:
        cq_path = os.path.join(root, scan_dir)
        if os.path.isdir(cq_path):
            for f in os.listdir(cq_path):
                if f.endswith(".md") and f != "README.md":
                    cq_count += 1

    disc_path = os.path.join(root, "02_REQUIREMENTS", "discussions")
    if os.path.isdir(disc_path):
        for f in os.listdir(disc_path):
            if f.endswith(".md") and f != "README.md":
                disc_count += 1

    # Knowledge articles
    knowledge_dir = os.path.join(root, "98_KNOWLEDGE")
    knowledge_count = 0
    if os.path.isdir(knowledge_dir):
        for root_dir, dirs, files in os.walk(knowledge_dir):
            for f in files:
                if f.endswith(".md") and f != "README.md":
                    knowledge_count += 1

    print(f"\n  [Active RUN Tasks]: {len(active_tasks)}")
    if active_tasks and show_recent > 0:
        print(f"    Recent (top {min(show_recent, len(active_tasks))}):")
        for task, mtime in active_tasks[:show_recent]:
            dt = datetime.fromtimestamp(mtime)
            print(f"      - {task} (modified: {dt.strftime('%Y-%m-%d %H:%M')})")

    print(f"\n  [Archived Tasks]: {archive_count}")
    print(f"\n  [Authority Documents]:")
    print(f"    - Capabilities (REQ): {req_count}")
    print(f"    - Invariants (RULE): {rule_count}")
    print(f"    - Competencies (CQ): {cq_count}")
    print(f"    - Discussions: {disc_count}")
    print(f"\n  [Knowledge Articles]: {knowledge_count}")

    return 0


def list_runs(root: str, status_filter: str = None, limit: int = 20) -> int:
    """List RUN documents with optional status filtering.

    Args:
        root: Memory root directory
        status_filter: Filter by status (active, completed, failed, all)
        limit: Maximum number of RUNs to show

    Returns:
        0 on success
    """
    import re

    active_dir = os.path.join(root, "04_TASK_LOGS", "active")
    runs = []

    if not os.path.isdir(active_dir):
        print("No active directory found.")
        return 0

    # Parse RUN metadata
    status_re = re.compile(r'>\s*\*\*Status\*\*:\s*(\w+)', re.I)
    started_re = re.compile(r'>\s*\*\*Started\*\*:\s*([\d-]+)', re.I)
    git_re = re.compile(r'>\s*\*\*Git\*\*:\s*([^\n]+)', re.I)
    summary_re = re.compile(r'>\s*\*\*Summary\*\*:\s*([^\n]+)', re.I)

    for f in os.listdir(active_dir):
        if not f.endswith(".md") or f == "README.md":
            continue

        fpath = os.path.join(active_dir, f)
        try:
            with open(fpath, 'r', encoding='utf-8') as fp:
                text = fp.read()
        except:
            continue

        run_id = os.path.splitext(f)[0]

        # Extract metadata
        status_match = status_re.search(text)
        status = status_match.group(1) if status_match else "Unknown"

        started_match = started_re.search(text)
        started = started_match.group(1) if started_match else "N/A"

        git_match = git_re.search(text)
        git = git_match.group(1).strip() if git_match else "-"

        summary_match = summary_re.search(text)
        summary = summary_match.group(1).strip()[:40] if summary_match else "-"

        mtime = os.path.getmtime(fpath)

        runs.append({
            'id': run_id,
            'status': status,
            'started': started,
            'git': git[:12] if git != "-" else git,
            'summary': summary,
            'mtime': mtime
        })

    # Sort by modification time (most recent first)
    runs.sort(key=lambda x: x['mtime'], reverse=True)

    # Filter by status
    if status_filter and status_filter.lower() != 'all':
        filter_status = status_filter.lower()
        runs = [r for r in runs if r['status'].lower() == filter_status]

    # Limit results
    runs = runs[:limit]

    # Print results
    print(f"\n{'='*80}")
    print(f"RUN Documents" + (f" (Status: {status_filter})" if status_filter else " (All)"))
    print(f"{'='*80}")

    if not runs:
        print("No RUN documents found.")
        return 0

    # Table header
    print(f"{'Status':<12} {'Started':<12} {'Git':<14} {'RUN ID'}")
    print(f"{'-'*12} {'-'*12} {'-'*14} {'-'*40}")

    for run in runs:
        status_icon = {"active": "[*]", "completed": "[v]", "failed": "[X]"}.get(
            run['status'].lower(), "[ ]"
        )
        print(f"{status_icon} {run['status']:<8} {run['started']:<12} {run['git']:<14} {run['id']}")

    print(f"\nTotal: {len(runs)} RUN(s)")
    return 0
