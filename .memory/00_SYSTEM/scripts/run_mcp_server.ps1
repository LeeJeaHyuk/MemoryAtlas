$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$systemDir = Split-Path -Parent $scriptDir
$memoryDir = Split-Path -Parent $systemDir
$repoDir = Split-Path -Parent $memoryDir
$python = Join-Path $repoDir ".venv-mcp\\Scripts\\python.exe"
$server = Join-Path $memoryDir "00_SYSTEM\\mcp\\mcp_server.py"
& $python $server --stdio



