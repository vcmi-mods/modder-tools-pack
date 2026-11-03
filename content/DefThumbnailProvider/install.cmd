@echo off
setlocal EnableExtensions

rem Check administrator access (compatible with Windows XP through Windows 11).
"%SystemRoot%\System32\cacls.exe" "%SystemRoot%\System32\config\system" >nul 2>&1
if not errorlevel 1 goto elevated

echo Requesting administrator privileges...
call :elevate
exit /b

:elevate
set "ELEVATE_VBS=%TEMP%\DefThumbnailProvider_elevate_%RANDOM%.vbs"
>"%ELEVATE_VBS%" echo Set UAC = CreateObject^("Shell.Application"^)
>>"%ELEVATE_VBS%" echo UAC.ShellExecute "%~f0", "", "%~dp0", "runas", 1
"%SystemRoot%\System32\cscript.exe" //NoLogo "%ELEVATE_VBS%"
del /q "%ELEVATE_VBS%" >nul 2>&1
goto :eof

:elevated

pushd "%~dp0" || exit /b 1

rem SysWOW64 exists only on 64-bit Windows. Install the native provider.
if exist "%SystemRoot%\SysWOW64\" (
    set "DLL=%CD%\x64\DefThumbnailProvider.dll"
    set "REGSVR=%SystemRoot%\System32\regsvr32.exe"
    echo Detected 64-bit Windows. Installing the x64 thumbnail provider...
) else (
    set "DLL=%CD%\x86\DefThumbnailProvider.dll"
    set "REGSVR=%SystemRoot%\System32\regsvr32.exe"
    echo Detected 32-bit Windows. Installing the x86 thumbnail provider...
)

if not exist "%DLL%" (
    echo.
    echo ERROR: File not found:
    echo "%DLL%"
    popd
    pause
    exit /b 1
)

"%REGSVR%" /n /i:machine "%DLL%" /s
set "RESULT=%ERRORLEVEL%"

echo.
if "%RESULT%"=="0" (
    echo Installation completed successfully.
) else (
    echo ERROR: Installation failed with code %RESULT%.
)

popd
pause
exit /b %RESULT%
