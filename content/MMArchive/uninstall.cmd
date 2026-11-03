@echo off
setlocal EnableExtensions

rem Check administrator access (compatible with Windows XP through Windows 11).
"%SystemRoot%\System32\cacls.exe" "%SystemRoot%\System32\config\system" >nul 2>&1
if not errorlevel 1 goto elevated

echo Requesting administrator privileges...
call :elevate
exit /b

:elevate
set "ELEVATE_VBS=%TEMP%\MMArchive_elevate_%RANDOM%.vbs"
>"%ELEVATE_VBS%" echo Set UAC = CreateObject^("Shell.Application"^)
>>"%ELEVATE_VBS%" echo UAC.ShellExecute "%~f0", "", "%~dp0", "runas", 1
"%SystemRoot%\System32\cscript.exe" //NoLogo "%ELEVATE_VBS%"
del /q "%ELEVATE_VBS%" >nul 2>&1
goto :eof

:elevated
set "FAILED=0"
call :unassociate .lod MMArchive.Lod
call :unassociate .lwd MMArchive.Lwd
call :unassociate .snd MMArchive.Snd
call :unassociate .vid MMArchive.Vid
call :unassociate .pac MMArchive.Pac

echo.
if "%FAILED%"=="0" (
    echo MMArchive file associations were removed successfully.
) else (
    echo ERROR: One or more file associations could not be removed.
)

pause
set "RESULT=%FAILED%"
endlocal & exit %RESULT%

:unassociate
set "EXT=%~1"
set "PROGID=%~2"
set "CURRENT_ASSOC="
set "OLD_ASSOC="
for /f "tokens=1,* delims==" %%A in ('assoc %EXT% 2^>nul') do set "CURRENT_ASSOC=%%B"
for /f "tokens=3,*" %%A in ('%SystemRoot%\System32\reg.exe query "HKCR\%EXT%" /v "MMArchive Backup" 2^>nul ^| findstr /R "REG_"') do set "OLD_ASSOC=%%B"

if /i "%CURRENT_ASSOC%"=="%PROGID%" (
    if defined OLD_ASSOC (
        "%SystemRoot%\System32\reg.exe" add "HKCR\%EXT%" /ve /t REG_SZ /d "%OLD_ASSOC%" /f >nul
    ) else (
        "%SystemRoot%\System32\reg.exe" delete "HKCR\%EXT%" /ve /f >nul 2>&1
    )
    if errorlevel 1 set "FAILED=1"
)

"%SystemRoot%\System32\reg.exe" delete "HKCR\%EXT%" /v "MMArchive Backup" /f >nul 2>&1
"%SystemRoot%\System32\reg.exe" query "HKCR\%PROGID%" >nul 2>&1
if not errorlevel 1 (
    "%SystemRoot%\System32\reg.exe" delete "HKCR\%PROGID%" /f >nul
    if errorlevel 1 set "FAILED=1"
)
goto :eof
