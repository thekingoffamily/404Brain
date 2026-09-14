@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title 404Brain - RUN AND INSTALL

echo.
echo  ========================================
echo   404Brain - lazy install + run
echo  ========================================
echo.
echo  Folder: %CD%
echo.

REM Soft warn only if path really contains spaces
set "_P=%CD%"
set "_NOSPACE=%_P: =%"
if /I not "%_NOSPACE%"=="%_P%" (
  echo [!] WARNING: path has spaces. Build may fail.
  echo     Better move to e.g. C:\dev\404Brain
  echo     Continuing anyway in 3 sec...
  timeout /t 3 >nul
)

REM --- Node MUST be 20.x (project .nvmrc = 20.18.2). Node 23 WILL break native modules. ---
where node >nul 2>&1
if errorlevel 1 (
  echo [!] Node.js not found.
  goto NEED_NODE20
)

for /f "tokens=*" %%v in ('node -v') do set NODEVER=%%v
echo [..] Node %NODEVER%

echo %NODEVER% | findstr /R /C:"^v20\." >nul
if errorlevel 1 (
  echo.
  echo [!] WRONG Node version: %NODEVER%
  echo     404Brain needs Node v20.18.2  ^(see .nvmrc^)
  echo     Your Node 23/22/21 breaks @vscode/deviceid and other native builds.
  echo.
  goto NEED_NODE20
)

echo [ok] Node %NODEVER% is 20.x
echo.

REM --- npm install ---
if not exist "node_modules\" (
  echo [..] npm install  (first time = long)
  call npm install
  if errorlevel 1 (
    echo.
    echo [!] npm install failed.
    echo.
    echo     1^) Node must be 20.18.2 ^(you have that if you got here^)
    echo     2^) Visual Studio 2022 Community - open Installer and enable:
    echo        Workloads: Desktop development with C++
    echo                   Node.js build tools
    echo        Individual: MSVC v143 Spectre-mitigated libs ^(x64/x86^)
    echo                    C++ ATL with Spectre Mitigations
    echo                    C++ MFC with Spectre Mitigations
    echo     3^) Then delete node_modules and try again:
    echo        rmdir /s /q node_modules
    echo        RUN_AND_INSTALL.bat
    echo.
    echo     Details: BUILD.ru.md
    pause
    exit /b 1
  )
) else (
  echo [ok] node_modules already there - skip npm install
  echo     ^(delete node_modules to force reinstall^)
)
echo.

set NODE_OPTIONS=--max-old-space-size=8192
echo [..] npm run compile  (first time = several minutes)
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
  if errorlevel 1 echo [!] buildreact failed - continuing anyway
) else (
  echo [ok] react/out present - skip buildreact
)
echo.

echo [..] launching 404Brain...
call ".\scripts\code.bat" --user-data-dir ".\.tmp\user-data" --extensions-dir ".\.tmp\extensions" %*
set EXITCODE=%ERRORLEVEL%
echo.
echo Done. Exit code: %EXITCODE%
if not "%EXITCODE%"=="0" pause
endlocal & exit /b %EXITCODE%

:NEED_NODE20
echo.
echo     FIX NOW:
echo     1. Uninstall Node 23 from Settings - Apps  OR keep it but switch default
echo     2. Install Node 20.18.2 LTS:
echo        https://nodejs.org/dist/v20.18.2/node-v20.18.2-x64.msi
echo     3. Close ALL terminals / Cursor terminals
echo     4. Open NEW cmd and check:  node -v
echo        Must print: v20.18.2
echo     5. In repo folder:
echo        rmdir /s /q node_modules
echo        RUN_AND_INSTALL.bat
echo.
echo     Or via winget ^(if available^):
echo        winget install OpenJS.NodeJS.LTS --version 20.18.2
echo.
start "" "https://nodejs.org/dist/v20.18.2/node-v20.18.2-x64.msi"
pause
exit /b 1
