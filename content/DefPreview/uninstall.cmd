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
set "CURRENT_ASSOC="
set "OLD_ASSOC="
for /f "tokens=1,* delims==" %%A in ('assoc .def 2^>nul') do set "CURRENT_ASSOC=%%B"
for /f "tokens=2,*" %%A in ('"%SystemRoot%\System32\reg.exe" query "HKCR\.def" /v "DefPreviewBackup" 2^>nul ^| findstr /R "REG_"') do set "OLD_ASSOC=%%B"
rem Also support backups made by the previous installer version.
if not defined OLD_ASSOC for /f "tokens=3,*" %%A in ('"%SystemRoot%\System32\reg.exe" query "HKCR\.def" /v "DefPreview Backup" 2^>nul ^| findstr /R "REG_"') do set "OLD_ASSOC=%%B"

set "FAILED=0"
if /i "%CURRENT_ASSOC%"=="DefPreview.Def" (
    if defined OLD_ASSOC (
        "%SystemRoot%\System32\reg.exe" add "HKCR\.def" /ve /t REG_SZ /d "%OLD_ASSOC%" /f >nul
    ) else (
        "%SystemRoot%\System32\reg.exe" delete "HKCR\.def" /ve /f >nul 2>&1
    )
    if errorlevel 1 set "FAILED=1"
)

"%SystemRoot%\System32\reg.exe" delete "HKCR\.def" /v "DefPreviewBackup" /f >nul 2>&1
"%SystemRoot%\System32\reg.exe" delete "HKCR\.def" /v "DefPreview Backup" /f >nul 2>&1
"%SystemRoot%\System32\reg.exe" query "HKCR\DefPreview.Def" >nul 2>&1
if not errorlevel 1 (
    "%SystemRoot%\System32\reg.exe" delete "HKCR\DefPreview.Def" /f >nul
    if errorlevel 1 set "FAILED=1"
)

echo.
if "%FAILED%"=="0" (
    echo DefPreview file association was removed successfully.
    if defined OLD_ASSOC echo The previous .def association was restored.
) else (
    echo ERROR: The .def file association could not be removed completely.
)

pause
exit /b %FAILED%
