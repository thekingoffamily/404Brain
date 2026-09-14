@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
title 404Brain - RUN AND INSTALL

set "NEED_NODE=20.18.2"
set "TOOLS_DIR=%CD%\.tools"
set "NODE_HOME=%TOOLS_DIR%\node-v%NEED_NODE%-win-x64"
set "NODE_ZIP=%TOOLS_DIR%\node-v%NEED_NODE%-win-x64.zip"
set "NODE_URL=https://nodejs.org/dist/v%NEED_NODE%/node-v%NEED_NODE%-win-x64.zip"

echo.
echo  ========================================
echo   404Brain - lazy install + run
echo  ========================================
echo.
echo  Folder: %CD%
echo.

REM Soft warn on spaces
set "_P=%CD%"
set "_NOSPACE=%_P: =%"
if /I not "%_NOSPACE%"=="%_P%" (
  echo [!] WARNING: path has spaces. Build may fail.
  echo     Better: C:\dev\404Brain
  timeout /t 3 >nul
)

REM --- Ensure Node 20 for THIS script (keep your system Node 23 untouched) ---
call :ENSURE_NODE20
if errorlevel 1 exit /b 1

echo [ok] Using Node:
call node -v
call npm -v
echo     PATH tip: system Node can stay 23 - this bat uses portable Node 20.
echo.

REM Fresh install if node_modules was built with wrong Node
if exist "node_modules\" (
  if exist ".tools\.need_reinstall" (
    echo [..] Removing node_modules built with wrong Node...
    rmdir /s /q node_modules 2>nul
    del /f /q ".tools\.need_reinstall" 2>nul
  )
)

if not exist "node_modules\" (
  echo [..] npm install  (first time = long)
  call npm install
  if errorlevel 1 (
    echo.
    echo [!] npm install failed ^(native build^).
    echo     Open Visual Studio Installer - Modify VS 2022:
    echo       Workloads: Desktop development with C++
    echo                  Node.js build tools
    echo       Individual: MSVC v143 Spectre-mitigated libs
    echo                   C++ ATL with Spectre Mitigations
    echo                   C++ MFC with Spectre Mitigations
    echo     Then: rmdir /s /q node_modules ^& RUN_AND_INSTALL.bat
    echo     See BUILD.ru.md
    pause
    exit /b 1
  )
) else (
  echo [ok] node_modules present - skip npm install
)

echo.
set NODE_OPTIONS=--max-old-space-size=8192
echo [..] npm run compile
call npm run compile
if errorlevel 1 (
  echo [!] compile failed. See BUILD.ru.md
  pause
  exit /b 1
)

echo.
if not exist "src\vs\workbench\contrib\brain\browser\react\out\" (
  echo [..] npm run buildreact
  call npm run buildreact
) else (
  echo [ok] react/out present
)

echo.
echo [..] launching 404Brain...
call ".\scripts\code.bat" --user-data-dir ".\.tmp\user-data" --extensions-dir ".\.tmp\extensions" %*
set EXITCODE=%ERRORLEVEL%
echo Done. Exit code: %EXITCODE%
if not "%EXITCODE%"=="0" pause
endlocal & exit /b %EXITCODE%


:ENSURE_NODE20
REM If system node is already 20.x - use it
where node >nul 2>&1
if not errorlevel 1 (
  for /f "tokens=*" %%v in ('node -v 2^>nul') do set "SYSVER=%%v"
  echo !SYSVER! | findstr /R /C:"^v20\." >nul
  if not errorlevel 1 (
    echo [ok] System Node !SYSVER! is fine
    exit /b 0
  )
  echo [..] System Node is !SYSVER! - OK to keep it.
  echo     Build needs Node %NEED_NODE% ^(VS Code / Electron toolchain^).
  echo     Downloading portable Node %NEED_NODE% into .tools\ ...
  echo.>"%TOOLS_DIR%\.need_reinstall" 2>nul
)

if not exist "%NODE_HOME%\node.exe" (
  if not exist "%TOOLS_DIR%" mkdir "%TOOLS_DIR%"
  echo [..] Download: %NODE_URL%
  powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "try { Invoke-WebRequest -Uri '%NODE_URL%' -OutFile '%NODE_ZIP%' -UseBasicParsing } catch { exit 1 }"
  if errorlevel 1 (
    echo [!] Download failed. Check internet or install Node %NEED_NODE% manually.
    echo     %NODE_URL%
    pause
    exit /b 1
  )
  echo [..] Extracting...
  powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "Expand-Archive -Path '%NODE_ZIP%' -DestinationPath '%TOOLS_DIR%' -Force"
  if errorlevel 1 (
    echo [!] Extract failed.
    pause
    exit /b 1
  )
  del /f /q "%NODE_ZIP%" 2>nul
)

if not exist "%NODE_HOME%\node.exe" (
  echo [!] Portable Node not found at %NODE_HOME%
  pause
  exit /b 1
)

set "PATH=%NODE_HOME%;%PATH%"
echo [ok] Portable Node ready: %NODE_HOME%
exit /b 0
