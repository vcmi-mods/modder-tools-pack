@echo off
setlocal EnableExtensions

rem Check administrator access (compatible with Windows XP through Windows 11).
"%SystemRoot%\System32\cacls.exe" "%SystemRoot%\System32\config\system" >nul 2>&1
if not errorlevel 1 goto elevated

echo Requesting administrator privileges...
call :elevate
exit /b

:elevate
set "ELEVATE_VBS=%TEMP%\DefPreview_elevate_%RANDOM%.vbs"
>"%ELEVATE_VBS%" echo Set UAC = CreateObject^("Shell.Application"^)
>>"%ELEVATE_VBS%" echo UAC.ShellExecute "%~f0", "", "%~dp0", "runas", 1
"%SystemRoot%\System32\cscript.exe" //NoLogo "%ELEVATE_VBS%"
del /q "%ELEVATE_VBS%" >nul 2>&1
goto :eof

:elevated
pushd "%~dp0" || exit /b 1
set "TOOL=%CD%\DefPreview.exe"

if not exist "%TOOL%" (
    echo.
    echo ERROR: File not found:
    echo "%TOOL%"
    popd
    pause
    exit /b 1
)

rem Preserve the previous default .def association for uninstall.
set "OLD_ASSOC="
for /f "tokens=1,* delims==" %%A in ('assoc .def 2^>nul') do set "OLD_ASSOC=%%B"
if defined OLD_ASSOC if /i not "%OLD_ASSOC%"=="DefPreview.Def" (
    "%SystemRoot%\System32\reg.exe" add "HKCR\.def" /v "DefPreviewBackup" /t REG_SZ /d "%OLD_ASSOC%" /f >nul
)

set "FAILED=0"
"%SystemRoot%\System32\reg.exe" add "HKCR\DefPreview.Def" /ve /t REG_SZ /d "Heroes III DEF file" /f >nul
if errorlevel 1 set "FAILED=1"
"%SystemRoot%\System32\reg.exe" add "HKCR\DefPreview.Def\DefaultIcon" /ve /t REG_SZ /d "\"%TOOL%\",0" /f >nul
if errorlevel 1 set "FAILED=1"
"%SystemRoot%\System32\reg.exe" add "HKCR\DefPreview.Def\shell\open\command" /ve /t REG_SZ /d "\"%TOOL%\" \"%%1\"" /f >nul
if errorlevel 1 set "FAILED=1"
"%SystemRoot%\System32\reg.exe" add "HKCR\.def" /ve /t REG_SZ /d "DefPreview.Def" /f >nul
if errorlevel 1 set "FAILED=1"

echo.
if "%FAILED%"=="0" (
    echo DefPreview was associated with .def files successfully.
    echo Double-clicking a .def file will now open it in DefPreview.
) else (
    echo ERROR: The .def file association could not be installed completely.
)

popd
pause
exit /b %FAILED%
