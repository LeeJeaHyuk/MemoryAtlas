import sys
import os
sys.path.append(os.path.join(os.getcwd(), "src"))
from core.automation import Automator

def run_intake():
    auto = Automator()
    description = "간단한 동작의 경우 실행 문서(RUN)를 작성하지 않고 바로 요구사항 단계에서 실행할 수 있도록 하는 옵션 추가 요청 (Fast-track Execution)"
    brief_path = auto.intake(description, domain="MCP")
    print(f"Created Brief: {brief_path}")

if __name__ == "__main__":
    run_intake()
