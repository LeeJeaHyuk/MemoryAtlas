
import re

# regex from automation.py (modified)
def extract_section_regex(heading):
    return re.compile(rf"^##\s+{re.escape(heading)}(?:.*)?$", re.M)

def extract_brief_section_regex(heading):
    return re.compile(rf"^##\s*(?:\d+\.)?\s*{re.escape(heading)}(?:.*)?$", re.M)

# Test content
run_content = """
# [RUN-BRIEF-GEN-001-step-01] Execution for BRIEF-GEN-001

> **ID**: RUN-BRIEF-GEN-001-step-01

## Objective (목표)
Execute the requirements.

## Scope (범위)
Implement changes.

## Output (결과물)
- Implemented features
"""

brief_content = """
# [BRIEF-GEN-001] Request: ...

## 1. Intent Summary (의도 요약)
My intent.

## 2. Affected Artifacts (영향받는 문서)
- Modify: REQ-001
"""

# Test RUN extraction
pattern_obj = extract_section_regex("Objective")
match_obj = pattern_obj.search(run_content)
print(f"RUN Objective match: {bool(match_obj)}")
if match_obj:
    print(f"Matched: {match_obj.group()}")

pattern_out = extract_section_regex("Output")
match_out = pattern_out.search(run_content)
print(f"RUN Output match: {bool(match_out)}")


# Test Brief extraction
pattern_intent = extract_brief_section_regex("Intent Summary")
match_intent = pattern_intent.search(brief_content)
print(f"Brief Intent match: {bool(match_intent)}")
if match_intent:
    print(f"Matched: {match_intent.group()}")

pattern_aff = extract_brief_section_regex("Affected Artifacts")
match_aff = pattern_aff.search(brief_content)
print(f"Brief Affected match: {bool(match_aff)}")
