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
pushd "%~dp0" || exit /b 1
set "TOOL=%CD%\MMArchive.exe"

if not exist "%TOOL%" (
    echo.
    echo ERROR: File not found:
    echo "%TOOL%"
    popd
    pause
    exit /b 1
)

set "FAILED=0"
call :associate .lod MMArchive.Lod "MMArchive LOD archive"
call :associate .lwd MMArchive.Lwd "MMArchive LWD archive"
call :associate .snd MMArchive.Snd "MMArchive sound archive"
call :associate .vid MMArchive.Vid "MMArchive video archive"
call :associate .pac MMArchive.Pac "MMArchive PAC archive"

echo.
if "%FAILED%"=="0" (
    echo MMArchive file associations were installed successfully.
    echo Double-clicking a LOD, LWD, SND, VID or PAC file will now open it in MMArchive.
) else (
    echo ERROR: One or more file associations could not be installed.
)

popd
pause
set "RESULT=%FAILED%"
endlocal & exit %RESULT%

:associate
set "EXT=%~1"
set "PROGID=%~2"
set "DESCRIPTION=%~3"
set "OLD_ASSOC="
for /f "tokens=1,* delims==" %%A in ('assoc %EXT% 2^>nul') do set "OLD_ASSOC=%%B"
if defined OLD_ASSOC if /i not "%OLD_ASSOC%"=="%PROGID%" (
    "%SystemRoot%\System32\reg.exe" add "HKCR\%EXT%" /v "MMArchive Backup" /t REG_SZ /d "%OLD_ASSOC%" /f >nul
    if errorlevel 1 set "FAILED=1"
)
"%SystemRoot%\System32\reg.exe" add "HKCR\%PROGID%" /ve /t REG_SZ /d "%DESCRIPTION%" /f >nul
if errorlevel 1 set "FAILED=1"
"%SystemRoot%\System32\reg.exe" add "HKCR\%PROGID%\DefaultIcon" /ve /t REG_SZ /d "\"%TOOL%\",0" /f >nul
if errorlevel 1 set "FAILED=1"
"%SystemRoot%\System32\reg.exe" add "HKCR\%PROGID%\shell\open\command" /ve /t REG_SZ /d "\"%TOOL%\" \"%%1\"" /f >nul
if errorlevel 1 set "FAILED=1"
"%SystemRoot%\System32\reg.exe" add "HKCR\%EXT%" /ve /t REG_SZ /d "%PROGID%" /f >nul
if errorlevel 1 set "FAILED=1"
goto :eof
