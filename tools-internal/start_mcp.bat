@echo off
REM Start MCP Ecosystem - double-click to run
cd /d "E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal"
mkdir logs 2>nul

echo Starting MCP Ecosystem...
echo.

echo [1/5] System Server (9876)
start /B python agent_mcp_server.py > logs\system.log 2>&1
timeout /t 2 /nobreak >nul

echo [2/5] Memory Server (9877)
start /B python mcp_memory_server.py > logs\memory.log 2>&1
timeout /t 2 /nobreak >nul

echo [3/5] Search Server (9878)
start /B python mcp_search_server.py > logs\search.log 2>&1
timeout /t 2 /nobreak >nul

echo [4/5] LLM Server (9879)
start /B python mcp_llm_server.py > logs\llm.log 2>&1
timeout /t 3 /nobreak >nul

echo [5/5] API Gateway (9001)
start /B python api_gateway.py > logs\gateway.log 2>&1
timeout /t 2 /nobreak >nul

echo.
echo === MCP Ecosystem Started! ===
echo  System: http://127.0.0.1:9876
echo  Memory: http://127.0.0.1:9877
echo  Search: http://127.0.0.1:9878
echo  LLM:    http://127.0.0.1:9879
echo  Gateway: http://127.0.0.1:9001
echo.
echo Logs: tools-internal\logs\
echo.
