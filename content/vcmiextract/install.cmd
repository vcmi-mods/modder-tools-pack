@echo off
setlocal EnableExtensions

rem Check administrator access (compatible with Windows XP through Windows 11).
"%SystemRoot%\System32\cacls.exe" "%SystemRoot%\System32\config\system" >nul 2>&1
if not errorlevel 1 goto elevated

echo Requesting administrator privileges...
call :elevate
exit /b

:elevate
set "ELEVATE_VBS=%TEMP%\VCMIExtract_elevate_%RANDOM%.vbs"
>"%ELEVATE_VBS%" echo Set UAC = CreateObject^("Shell.Application"^)
>>"%ELEVATE_VBS%" echo UAC.ShellExecute "%~f0", "", "%~dp0", "runas", 1
"%SystemRoot%\System32\cscript.exe" //NoLogo "%ELEVATE_VBS%"
del /q "%ELEVATE_VBS%" >nul 2>&1
goto :eof

:elevated
pushd "%~dp0" || exit /b 1

if exist "%SystemRoot%\SysWOW64\" (
    set "TOOL=%CD%\x64\vcmiextract.exe"
    echo Detected 64-bit Windows. Installing the x64 version...
) else (
    set "TOOL=%CD%\x86\vcmiextract.exe"
    echo Detected 32-bit Windows. Installing the x86 version...
)

if not exist "%TOOL%" (
    echo.
    echo ERROR: File not found:
    echo "%TOOL%"
    popd
    pause
    exit /b 1
)

set "FAILED=0"
call :install_extension .lod
call :install_extension .pac
call :install_extension .snd
call :install_extension .vid
call :install_extension .pak
call :install_extension .def
call :install_extension .d32
call :install_extension .pcx
call :install_extension .p32

echo.
if "%FAILED%"=="0" (
    echo VCMIExtract context-menu commands were installed successfully.
) else (
    echo ERROR: One or more registry entries could not be installed.
)

popd
pause
exit /b %FAILED%

:install_extension
"%SystemRoot%\System32\reg.exe" add "HKCR\SystemFileAssociations\%~1\shell\VCMIExtract" /ve /t REG_SZ /d "Extract using VCMIExtract" /f >nul
if errorlevel 1 set "FAILED=1"
"%SystemRoot%\System32\reg.exe" add "HKCR\SystemFileAssociations\%~1\shell\VCMIExtract" /v "Icon" /t REG_SZ /d "shell32.dll,45" /f >nul
if errorlevel 1 set "FAILED=1"
"%SystemRoot%\System32\reg.exe" add "HKCR\SystemFileAssociations\%~1\shell\VCMIExtract\command" /ve /t REG_SZ /d "\"%TOOL%\" \"%%1\"" /f >nul
if errorlevel 1 set "FAILED=1"
goto :eof
