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
pushd "%~dp0" || exit /b 1

if exist "%SystemRoot%\SysWOW64\" (
    set "TOOL=%CD%\x64\def2json.exe"
    echo Detected 64-bit Windows. Installing the x64 version...
) else (
    set "TOOL=%CD%\x86\def2json.exe"
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
call :install_menu .def
call :install_item .def 001_extract "Extract PNG + JSON" "" "%SystemRoot%\System32\shell32.dll,-231"
call :install_item .def 002_onlyconfig "Create JSON config only" "--onlyconfig" "%SystemRoot%\System32\shell32.dll,-174"
call :install_item .def 003_ignorefilename "Extract with sequential frame names" "--ignorefilename" "%SystemRoot%\System32\shell32.dll,-246"
call :install_item .def 004_ignoregroup "Extract all frames as group 0" "--ignoregroup" "%SystemRoot%\System32\shell32.dll,-274"
call :install_item .def 005_ignoreboth "Sequential names + group 0" "--ignorefilename --ignoregroup" "%SystemRoot%\System32\shell32.dll,-241"
call :install_item .def 006_mergeshadow "Extract with merged shadows" "--mergeshadow" "%SystemRoot%\System32\shell32.dll,-243"
call :install_item .def 007_overlay "Extract and generate overlays" "--overlay" "%SystemRoot%\System32\shell32.dll,-255"
call :install_item .def 008_template "Extract + create VCMI template" "--vcmi-template" "%SystemRoot%\System32\shell32.dll,-242"
call :install_item .def 009_maskonly "Create VCMI template only" "--vcmi-template --maskonly" "%SystemRoot%\System32\shell32.dll,-16775"
call :install_item .def 010_template_names "Sequential names + VCMI template" "--ignorefilename --vcmi-template" "%SystemRoot%\System32\shell32.dll,-16767"
call :install_item .def 011_template_group "Group 0 + VCMI template" "--ignoregroup --vcmi-template" "%SystemRoot%\System32\shell32.dll,-16769"
call :install_help .def 012_help

call :install_menu .d32
call :install_item .d32 001_extract "Extract PNG + JSON" "" "%SystemRoot%\System32\shell32.dll,-231"
call :install_item .d32 002_onlyconfig "Create JSON config only" "--onlyconfig" "%SystemRoot%\System32\shell32.dll,-174"
call :install_item .d32 003_ignorefilename "Extract with sequential frame names" "--ignorefilename" "%SystemRoot%\System32\shell32.dll,-246"
call :install_item .d32 004_ignoregroup "Extract all frames as group 0" "--ignoregroup" "%SystemRoot%\System32\shell32.dll,-274"
call :install_item .d32 005_ignoreboth "Sequential names + group 0" "--ignorefilename --ignoregroup" "%SystemRoot%\System32\shell32.dll,-241"
call :install_item .d32 006_mergeshadow "Extract with merged shadows" "--mergeshadow" "%SystemRoot%\System32\shell32.dll,-243"
call :install_item .d32 007_overlay "Extract and generate overlays" "--overlay" "%SystemRoot%\System32\shell32.dll,-255"
call :install_item .d32 008_template "Extract + create VCMI template" "--vcmi-template" "%SystemRoot%\System32\shell32.dll,-242"
call :install_item .d32 009_maskonly "Create VCMI template only" "--vcmi-template --maskonly" "%SystemRoot%\System32\shell32.dll,-16775"
call :install_item .d32 010_template_names "Sequential names + VCMI template" "--ignorefilename --vcmi-template" "%SystemRoot%\System32\shell32.dll,-16767"
call :install_item .d32 011_template_group "Group 0 + VCMI template" "--ignoregroup --vcmi-template" "%SystemRoot%\System32\shell32.dll,-16769"
call :install_help .d32 012_help

echo.
if "%FAILED%"=="0" (
    echo DEF2JSON context menus were installed successfully.
) else (
    echo ERROR: One or more registry entries could not be installed.
)

popd
pause
rem This installer runs in its own elevated cmd.exe window. Terminate that
rem process explicitly so execution can never fall through into subroutines.
set "RESULT=%FAILED%"
endlocal & exit %RESULT%

:install_menu
set "MENUKEY=HKCR\SystemFileAssociations\%~1\shell\DEF2JSON"
"%SystemRoot%\System32\reg.exe" add "%MENUKEY%" /v "MUIVerb" /t REG_SZ /d "DEF2JSON" /f >nul
if errorlevel 1 set "FAILED=1"
rem A cascading menu must not have a default value on its parent key.
"%SystemRoot%\System32\reg.exe" delete "%MENUKEY%" /ve /f >nul 2>&1
"%SystemRoot%\System32\reg.exe" add "%MENUKEY%" /v "SubCommands" /t REG_SZ /d "" /f >nul
if errorlevel 1 set "FAILED=1"
"%SystemRoot%\System32\reg.exe" add "%MENUKEY%" /v "Icon" /t REG_SZ /d "%SystemRoot%\System32\shell32.dll,-51380" /f >nul
if errorlevel 1 set "FAILED=1"
goto :eof

:install_item
set "ITEMKEY=HKCR\SystemFileAssociations\%~1\shell\DEF2JSON\shell\%~2"
set "DISPLAY=%~3"
if not "%~4"=="" set "DISPLAY=%~3	[%~4]"
"%SystemRoot%\System32\reg.exe" add "%ITEMKEY%" /v "MUIVerb" /t REG_SZ /d "%DISPLAY%" /f >nul
if errorlevel 1 set "FAILED=1"
"%SystemRoot%\System32\reg.exe" delete "%ITEMKEY%" /ve /f >nul 2>&1
"%SystemRoot%\System32\reg.exe" add "%ITEMKEY%" /v "Icon" /t REG_SZ /d "%~5" /f >nul
if errorlevel 1 set "FAILED=1"
"%SystemRoot%\System32\reg.exe" add "%ITEMKEY%\command" /ve /t REG_SZ /d "\"%TOOL%\" \"%%1\" %~4" /f >nul
if errorlevel 1 set "FAILED=1"
goto :eof

:install_help
set "ITEMKEY=HKCR\SystemFileAssociations\%~1\shell\DEF2JSON\shell\%~2"
"%SystemRoot%\System32\reg.exe" add "%ITEMKEY%" /v "MUIVerb" /t REG_SZ /d "Show command-line help	[--help]" /f >nul
if errorlevel 1 set "FAILED=1"
"%SystemRoot%\System32\reg.exe" delete "%ITEMKEY%" /ve /f >nul 2>&1
"%SystemRoot%\System32\reg.exe" add "%ITEMKEY%" /v "Icon" /t REG_SZ /d "%SystemRoot%\System32\shell32.dll,-263" /f >nul
if errorlevel 1 set "FAILED=1"
"%SystemRoot%\System32\reg.exe" add "%ITEMKEY%\command" /ve /t REG_SZ /d "cmd.exe /k \"\"%TOOL%\" --help\"" /f >nul
if errorlevel 1 set "FAILED=1"
goto :eof
