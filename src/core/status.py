
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
    disc_count = 0

    for scan_dir in ["02_REQUIREMENTS/features"]:
        req_path = os.path.join(root, scan_dir)
        if os.path.isdir(req_path):
            for f in os.listdir(req_path):
                if f.endswith(".md") and f != "README.md":
                    req_count += 1

    for scan_dir in ["02_REQUIREMENTS/business_rules"]:
        rule_path = os.path.join(root, scan_dir)
        if os.path.isdir(rule_path):
            for f in os.listdir(rule_path):
                if f.endswith(".md") and f != "README.md":
                    rule_count += 1

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
    print(f"    - Feature REQs: {req_count}")
    print(f"    - Business RULEs: {rule_count}")
    print(f"    - Discussions: {disc_count}")
    print(f"\n  [Knowledge Articles]: {knowledge_count}")

    return 0
