
import os
from pathlib import Path
from typing import List

from core.config import ROOT_DIR

REVERSE_PROMPT_TEMPLATE = """# 🧩 Partial Reverse Engineering Request

> **Focus Area**: `{focus_path}`

## 1. Instructions
당신은 현재 거대한 시스템의 **일부 모듈(`{focus_path}`)**만을 보고 있습니다.
전체 시스템을 다 알지 못하므로, 모르는 부분은 섣불리 가정하지 말고 **현재 코드 내의 로직에만 집중**하세요.

## 2. Existing Knowledge (Context)
현재 프로젝트에는 이미 다음 문서들이 정의되어 있습니다. 
**기존 규칙을 준수하고, 중복된 문서를 생성하지 마세요.**

### Existing Rules (Business Rules)
{existing_rules}

### Existing Features (Requirements)
{existing_reqs}

## 3. Analysis Strategy
1. **Local Rules**: 이 모듈 내부에서만 쓰이는 규칙은 `RULE-[DOMAIN]-XXX`로 정의하세요.
2. **Global Rules**: 프로젝트 전반에 쓰일 것 같은 규칙이 보이면, `RULE-CORE-XXX`로 제안하되 "확인 필요"라고 메모하세요.
3. **Features**: 각 주요 기능을 `REQ-[DOMAIN]-XXX`로 정의하세요.

---

## 4. Target Code
(아래 코드는 `{focus_path}` 경로의 파일들입니다.)

{code_content}
"""

def get_file_list(directory: str) -> List[str]:
    """Get list of markdown files in a directory (without extension)."""
    if not os.path.exists(directory):
        return ["(None)"]
    
    files = [
        f for f in os.listdir(directory) 
        if f.endswith(".md") and f != "README.md"
    ]
    return [os.path.splitext(f)[0] for f in sorted(files)] or ["(None)"]

def read_code_files(root: str, focus_subpath: str) -> str:
    """Read code files from the focus path."""
    target_path = os.path.join(root, focus_subpath)
    
    if not os.path.exists(target_path):
        return f"Error: Path '{target_path}' does not exist."

    code_content = []
    
    # If it's a file
    if os.path.isfile(target_path):
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                code_content.append(f"### `{focus_subpath}`\n```python\n{f.read()}\n```")
        except Exception as e:
            code_content.append(f"Error reading {target_path}: {e}")
            
    # If it's a directory
    elif os.path.isdir(target_path):
        for dirpath, _, filenames in os.walk(target_path):
            for name in sorted(filenames):
                # Simple filter: only python files, skip hidden/cache
                if not name.endswith(".py") or name.startswith("__"):
                    continue
                    
                full_path = os.path.join(dirpath, name)
                rel_path = os.path.relpath(full_path, root)
                
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        code_content.append(f"### `{rel_path}`\n```python\n{content}\n```")
                except Exception as e:
                    code_content.append(f"Error reading {rel_path}: {e}")
    
    if not code_content:
        return "(No Python files found in this path)"
        
    return "\n\n".join(code_content)

def generate_reverse_prompt(root: str, focus_path: str) -> None:
    """Generate the reverse engineering prompt."""
    print(f"\n🔍 Generating Reverse Engineering Prompt...")
    print(f"   Focus: {focus_path}")
    
    # 1. Scan Context
    # root is ".memory" folder
    rules_dir = os.path.join(root, "02_REQUIREMENTS", "invariants")
    reqs_dir = os.path.join(root, "02_REQUIREMENTS", "capabilities")
    
    existing_rules = get_file_list(rules_dir)
    existing_reqs = get_file_list(reqs_dir)
    
    print(f"   Context: Found {len(existing_rules)} invariants and {len(existing_reqs)} capabilities.")
    
    # 2. Read Target Code
    # Assuming root is relative ".memory", project root is current dir or parent of absolute root
    # Since we run from project root, we can just use focus_path relative to CWD, 
    # or derive project_root from root if it is absolute.
    # Let's derive safely:
    if os.path.isabs(root):
        project_root = os.path.dirname(root)
    else:
        project_root = "." # Assuming running from root
        
    code_content = read_code_files(project_root, focus_path)
    
    # 3. Generate Prompt
    prompt = REVERSE_PROMPT_TEMPLATE.format(
        focus_path=focus_path,
        existing_rules="- " + "\n- ".join(existing_rules),
        existing_reqs="- " + "\n- ".join(existing_reqs),
        code_content=code_content
    )
    
    output_path = os.path.join(root, "00_REVERSE_PROMPT.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(prompt)
        
    print(f"✅ Generated: {output_path}")
    print("📋 Next Step: Copy the content of 00_REVERSE_PROMPT.md to your AI Agent.\n")
