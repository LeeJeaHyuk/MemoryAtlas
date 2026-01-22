# System Management

> [!CAUTION]
> ## SYSTEM-MANAGED FOLDER
>
> 이 폴더는 `memory_manager.py`에 의해 **자동 관리**됩니다.
>
> ### Overwrite Policy
> - **AGENT_RULES.md**: 시스템 업데이트 시 덮어쓰기됨
> - **scripts/**: 시스템 업데이트 시 덮어쓰기됨
> - **mcp/**: auto-generated MCP definitions (overwritten on update)
> - 사용자/에이전트 수정 -> 다음 업데이트에서 원복
>
> ### For Customization
> 커스텀 규칙이 필요하면 `01_PROJECT_CONTEXT/01_CONVENTIONS.md`에 작성하세요.

## MCP Auto-Launch

- STDIO clients can auto-spawn the MCP server using the configured command.
- This means the server does not need to be running manually in the background.
- HTTP mode still requires a long-running server process.
- Use `python memory_manager.py --bootstrap-mcp --target <client> --os <windows|unix>` to generate MCP bootstrap prompts and templates.
- Validate with `python memory_manager.py --mcp-check --target <client>`.

## Version Info

- **Manager Version**: 3.3.0
- **Template Version**: 3.3