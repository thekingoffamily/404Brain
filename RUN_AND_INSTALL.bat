@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title 404Brain - RUN AND INSTALL

echo.
echo  ========================================
echo   404Brain — lazy install + run
echo  ========================================
echo.

REM --- path with spaces is poison for this codebase ---
echo %CD% | findstr /C:" " >nul
if not errorlevel 1 (
  echo [!] Path has SPACES. Move the repo to a path without spaces.
  echo     Example: C:\dev\404Brain
  echo.
  pause
  exit /b 1
)

REM --- Node ---
where node >nul 2>&1
if errorlevel 1 (
  echo [!] Node.js not found. Install Node 20.18.2 then re-run.
  echo     https://nodejs.org/
  echo.
  pause
  exit /b 1
)

for /f "tokens=*" %%v in ('node -v') do set NODEVER=%%v
echo [ok] Node %NODEVER%  (want v20.18.2 — see .nvmrc)
echo.

REM --- npm install ---
if not exist "node_modules\" (
  echo [..] npm install  (first time = long, go make coffee)
  call npm install
  if errorlevel 1 (
    echo [!] npm install failed.
    echo     Windows: need VS 2022 with C++ + Node.js build tools. See BUILD.md
    pause
    exit /b 1
  )
) else (
  echo [ok] node_modules already there — skip npm install
  echo     (delete node_modules folder to force reinstall)
)
echo.

REM --- compile once (no watch window needed) ---
set NODE_OPTIONS=--max-old-space-size=8192
echo [..] npm run compile  (first time = several minutes)
call npm run compile
if errorlevel 1 (
  echo [!] compile failed. See BUILD.md / BUILD.ru.md
  pause
  exit /b 1
)
echo.

REM --- React UI bundle if missing ---
if not exist "src\vs\workbench\contrib\brain\browser\react\out\" (
  echo [..] npm run buildreact
  call npm run buildreact
  if errorlevel 1 (
    echo [!] buildreact failed — continuing anyway
  )
) else (
  echo [ok] react/out present — skip buildreact
)
echo.

REM --- launch ---
echo [..] launching 404Brain...
echo     data: .tmp\user-data
echo.
call ".\scripts\code.bat" --user-data-dir ".\.tmp\user-data" --extensions-dir ".\.tmp\extensions" %*
set EXITCODE=%ERRORLEVEL%

echo.
echo Done. Exit code: %EXITCODE%
if not "%EXITCODE%"=="0" pause
endlocal & exit /b %EXITCODE%
