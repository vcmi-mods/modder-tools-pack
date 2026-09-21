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
echo Removing VCMIExtract context-menu commands...
set "FAILED=0"
call :remove_extension .lod
call :remove_extension .pac
call :remove_extension .snd
call :remove_extension .vid
call :remove_extension .pak
call :remove_extension .def
call :remove_extension .d32
call :remove_extension .pcx
call :remove_extension .p32

echo.
if "%FAILED%"=="0" (
    echo VCMIExtract context-menu commands were removed successfully.
) else (
    echo ERROR: One or more registry entries could not be removed.
)

pause
exit /b %FAILED%

:remove_extension
"%SystemRoot%\System32\reg.exe" query "HKCR\SystemFileAssociations\%~1\shell\VCMIExtract" >nul 2>&1
if errorlevel 1 goto :eof
"%SystemRoot%\System32\reg.exe" delete "HKCR\SystemFileAssociations\%~1\shell\VCMIExtract" /f >nul
if errorlevel 1 set "FAILED=1"
goto :eof
