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

REM --- Prefer VS 2022 Build Tools with Spectre ^(Community often lacks Spectre^) ---
call :ENSURE_VCTOOLS
if errorlevel 1 (
  echo [!] C++ / Spectre not ready. Run INSTALL_BUILD_TOOLS.bat first.
  set /p OPENBT=Open INSTALL_BUILD_TOOLS.bat now? [Y/N]: 
  if /I "!OPENBT!"=="Y" call "%~dp0INSTALL_BUILD_TOOLS.bat"
  pause
  exit /b 1
)

REM Need ~8+ GB free on C: for node-gyp / MSBuild PDBs
for /f "tokens=3" %%a in ('dir /-c C:\ 2^>nul ^| findstr /C:"bytes free"') do set "FREEBYTES=%%a"
if defined FREEBYTES (
  set /a FREEGBapprox=!FREEBYTES:~0,-9! 2>nul
  if defined FREEGBapprox if !FREEGBapprox! LSS 6 (
    echo [!] C: has only ~!FREEGBapprox! GB free. Native build needs ~8+ GB.
    echo     Free space ^(Docker cache, Android, .gradle, Recycle Bin^), then retry.
    echo     Biggest usual hog: %%LOCALAPPDATA%%\Docker
    pause
    exit /b 1
  )
)

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
    echo [!] npm install failed ^(native C++ build^).
    echo     Often: disk full ^(LNK1201 / No space left on device^).
    echo     Check free space on C:, then:
    echo       rmdir /s /q node_modules
    echo       RUN_AND_INSTALL.bat
    echo     If tools missing: INSTALL_BUILD_TOOLS.bat
    echo.
    set /p OPENBT=Open INSTALL_BUILD_TOOLS.bat now? [Y/N]: 
    if /I "!OPENBT!"=="Y" call "%~dp0INSTALL_BUILD_TOOLS.bat"
    pause
    exit /b 1
  )
) else (
  echo [ok] node_modules present - skip npm install
)

echo.
set NODE_OPTIONS=--max-old-space-size=8192

REM compile imports gitignored react/out/*.js — build those first
if not exist "src\vs\workbench\contrib\brain\browser\react\out\" (
  echo [..] npm run buildreact
  call npm run buildreact
  if errorlevel 1 (
    echo [!] buildreact failed. See BUILD.ru.md
    pause
    exit /b 1
  )
) else (
  echo [ok] react/out present
)

echo.
echo [..] npm run compile
call npm run compile
if errorlevel 1 (
  echo [!] compile failed. See BUILD.ru.md
  pause
  exit /b 1
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


:ENSURE_VCTOOLS
set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
set "VS_PATH="
set "VCVARS="

REM Prefer Build Tools 2022, then Community 2022
if exist "%VSWHERE%" (
  for /f "usebackq tokens=*" %%i in (`"%VSWHERE%" -products Microsoft.VisualStudio.Product.BuildTools -version "[17.0,18.0)" -property installationPath`) do set "VS_PATH=%%i"
  if not defined VS_PATH (
    for /f "usebackq tokens=*" %%i in (`"%VSWHERE%" -products Microsoft.VisualStudio.Product.Community -version "[17.0,18.0)" -property installationPath`) do set "VS_PATH=%%i"
  )
)

if not defined VS_PATH (
  if exist "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" (
    set "VS_PATH=%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools"
  ) else if exist "%ProgramFiles%\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" (
    set "VS_PATH=%ProgramFiles%\Microsoft Visual Studio\2022\Community"
  )
)

if not defined VS_PATH (
  echo [!] Visual Studio 2022 C++ tools not found
  exit /b 1
)

set "VCVARS=!VS_PATH!\VC\Auxiliary\Build\vcvars64.bat"
if not exist "!VCVARS!" (
  echo [!] vcvars64.bat missing under !VS_PATH!
  exit /b 1
)

REM Spectre libs required by @vscode/* native modules
set "HAS_SPECTRE=0"
for /d %%D in ("!VS_PATH!\VC\Tools\MSVC\*") do (
  if exist "%%~D\lib\spectre\x64\" set "HAS_SPECTRE=1"
)
if "!HAS_SPECTRE!"=="0" (
  echo [!] Spectre-mitigated libs missing under !VS_PATH!
  echo     Run INSTALL_BUILD_TOOLS.bat ^(adds Spectre / ATL / MFC^)
  exit /b 1
)

echo [ok] VS C++: !VS_PATH!
echo [..] Loading vcvars64...
call "!VCVARS!" >nul
if errorlevel 1 (
  echo [!] vcvars64 failed
  exit /b 1
)
set "GYP_MSVS_VERSION=2022"
set "npm_config_msvs_version=2022"
where cl >nul 2>&1
if errorlevel 1 (
  echo [!] cl.exe not on PATH after vcvars64
  exit /b 1
)
echo [ok] cl.exe ready ^(Spectre OK^)
exit /b 0
