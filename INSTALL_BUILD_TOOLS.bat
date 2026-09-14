@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title 404Brain - Install VS Build Tools

echo.
echo  ========================================
echo   404Brain - install C++ build tools
echo  ========================================
echo.
echo  npm install needs Visual C++ toolset + Spectre libs.
echo  This will install Visual Studio 2022 Build Tools
echo  ^(or modify them^) - needs Admin + internet + time.
echo.
pause

set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
set "SETUP=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\setup.exe"

set "ADD=--add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.NodeBuildTools --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 --add Microsoft.VisualStudio.Component.Windows11SDK.22621 --add Microsoft.VisualStudio.Component.VC.Runtimes.x86.x64.Spectre --add Microsoft.VisualStudio.Component.VC.ATL --add Microsoft.VisualStudio.Component.VC.ATLMFC --add Microsoft.VisualStudio.Component.VC.ATL.Spectre --add Microsoft.VisualStudio.Component.VC.MFC.Spectre --includeRecommended"

echo [..] Trying winget Build Tools...
where winget >nul 2>&1
if not errorlevel 1 (
  winget install --id Microsoft.VisualStudio.2022.BuildTools -e --accept-package-agreements --accept-source-agreements --override "--wait --passive %ADD%"
  if not errorlevel 1 goto DONE
  echo [!] winget install failed or already present - trying modify via setup.exe
)

if not exist "%SETUP%" (
  echo [!] Visual Studio Installer not found.
  echo     Download Build Tools:
  echo     https://aka.ms/vs/17/release/vs_BuildTools.exe
  start "" "https://aka.ms/vs/17/release/vs_BuildTools.exe"
  pause
  exit /b 1
)

REM Prefer modifying existing Build Tools 2022, else Community 2022
set "INSTALL_PATH="
if exist "%VSWHERE%" (
  for /f "usebackq tokens=*" %%i in (`"%VSWHERE%" -products Microsoft.VisualStudio.Product.BuildTools -version "[17.0,18.0)" -property installationPath`) do set "INSTALL_PATH=%%i"
  if not defined INSTALL_PATH (
    for /f "usebackq tokens=*" %%i in (`"%VSWHERE%" -products Microsoft.VisualStudio.Product.Community -version "[17.0,18.0)" -property installationPath`) do set "INSTALL_PATH=%%i"
  )
)

if defined INSTALL_PATH (
  echo [..] Modifying: %INSTALL_PATH%
  "%SETUP%" modify --installPath "%INSTALL_PATH%" --passive --wait %ADD%
) else (
  echo [..] No VS 2022 found - launching online Build Tools install...
  start "" "https://aka.ms/vs/17/release/vs_BuildTools.exe"
  echo.
  echo Install with workloads:
  echo   - Desktop development with C++
  echo   - Node.js build tools
  echo And Individual components Spectre libs / ATL / MFC Spectre.
  pause
  exit /b 1
)

REM Also patch Community if present ^(node-gyp sometimes prefers it^)
set "COMMUNITY_PATH="
if exist "%VSWHERE%" (
  for /f "usebackq tokens=*" %%i in (`"%VSWHERE%" -products Microsoft.VisualStudio.Product.Community -version "[17.0,18.0)" -property installationPath`) do set "COMMUNITY_PATH=%%i"
)
if defined COMMUNITY_PATH (
  if /I not "%COMMUNITY_PATH%"=="%INSTALL_PATH%" (
    echo [..] Also adding Spectre to Community: %COMMUNITY_PATH%
    "%SETUP%" modify --installPath "%COMMUNITY_PATH%" --passive --wait %ADD%
  )
)

:DONE
echo.
echo [ok] Installer finished. REBOOT recommended if Windows asks.
echo     Then:
echo       rmdir /s /q node_modules
echo       RUN_AND_INSTALL.bat
echo.
pause
endlocal
