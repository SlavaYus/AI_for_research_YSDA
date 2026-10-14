@echo off
REM MCP server "research" (OpenAlex, Wikidata) - Windows shim, mirrors bin/research-mcp.
setlocal
set "REPO=%~dp0.."
set "PY=%REPO%\.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
"%PY%" "%REPO%\src\research_mcp.py" %*
endlocal
