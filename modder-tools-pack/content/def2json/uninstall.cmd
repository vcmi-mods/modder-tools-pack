@echo off
setlocal EnableExtensions

rem Check administrator access (compatible with Windows XP through Windows 11).
"%SystemRoot%\System32\cacls.exe" "%SystemRoot%\System32\config\system" >nul 2>&1
if not errorlevel 1 goto elevated

echo Requesting administrator privileges...
call :elevate
exit /b

:elevate
set "ELEVATE_VBS=%TEMP%\DEF2JSON_elevate_%RANDOM%.vbs"
>"%ELEVATE_VBS%" echo Set UAC = CreateObject^("Shell.Application"^)
>>"%ELEVATE_VBS%" echo UAC.ShellExecute "%~f0", "", "%~dp0", "runas", 1
"%SystemRoot%\System32\cscript.exe" //NoLogo "%ELEVATE_VBS%"
del /q "%ELEVATE_VBS%" >nul 2>&1
goto :eof

:elevated
echo Removing DEF2JSON context menus...
set "FAILED=0"
call :remove_menu .def
call :remove_menu .d32

echo.
if "%FAILED%"=="0" (
    echo DEF2JSON context menus were removed successfully.
) else (
    echo ERROR: One or more registry entries could not be removed.
)

pause
exit /b %FAILED%

:remove_menu
set "MENUKEY=HKCR\SystemFileAssociations\%~1\shell\DEF2JSON"
"%SystemRoot%\System32\reg.exe" query "%MENUKEY%" >nul 2>&1
if errorlevel 1 goto :eof
"%SystemRoot%\System32\reg.exe" delete "%MENUKEY%" /f >nul
if errorlevel 1 set "FAILED=1"
goto :eof
