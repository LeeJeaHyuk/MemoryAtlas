
from pathlib import Path

from core.config import (
    BOOTSTRAP_CONVENTIONS_TEMPLATE,
    BOOTSTRAP_GOALS_TEMPLATE,
    BOOTSTRAP_PROMPT_TEMPLATE,
    ROOT_DIR,
)

def bootstrap_init(dry_run: bool = False) -> None:
    """Create Bootstrap files for AI-driven project initialization.
    
    Context Bootstrapping (v2.4): AI가 사용자와 인터뷰를 통해
    프로젝트 헌법(CONVENTIONS, GOALS)을 작성하도록 유도하는 기능.
    
    Creates:
        - BOOTSTRAP_PROMPT.md: AI 킥오프 미팅 아젠다
        - 01_CONTEXT/CONVENTIONS.md: [TODO] 템플릿 (AI가 채움)
        - 01_CONTEXT/GOALS.md: [TODO] 템플릿 (AI가 채움)
    """
    bootstrap_dir = Path(ROOT_DIR)
    context_dir = bootstrap_dir / "01_CONTEXT"
    
    # Ensure base structure exists
    bootstrap_dir.mkdir(exist_ok=True)
    context_dir.mkdir(exist_ok=True)
    
    files_to_create = {
        bootstrap_dir / "BOOTSTRAP_PROMPT.md": BOOTSTRAP_PROMPT_TEMPLATE,
        context_dir / "CONVENTIONS.md": BOOTSTRAP_CONVENTIONS_TEMPLATE,
        context_dir / "GOALS.md": BOOTSTRAP_GOALS_TEMPLATE,
    }
    
    print("\n" + "=" * 60)
    print("🚀 Context Bootstrapping (v2.4)")
    print("=" * 60)
    
    for filepath, content in files_to_create.items():
        if filepath.exists():
            print(f"  [SKIP] {filepath} (already exists)")
            continue
        
        if dry_run:
            print(f"  [DRY-RUN] Would create: {filepath}")
        else:
            filepath.write_text(content, encoding="utf-8")
            print(f"  [CREATE] {filepath}")
    
    print("\n" + "-" * 60)
    print("📋 다음 단계:")
    print("   1. BOOTSTRAP_PROMPT.md를 AI 에이전트에게 전달하세요")
    print("   2. AI가 질문하면 프로젝트에 맞게 답변하세요")
    print("   3. AI가 CONVENTIONS.md와 GOALS.md를 완성합니다")
    print("   4. 완료 후 `python memory_manager.py --update`로 나머지 구조 생성")
    print("-" * 60 + "\n")
