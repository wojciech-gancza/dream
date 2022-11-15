@echo off
REM DREAM starter - Windows version
REM -----------------------------------------------------------------
set START_LOCATION=work
REM -----------------------------------------------------------------
REM Take path of the this running script
set FACTORY_SOURCE=%~dp0
set FACTORY_DRIVE=%~d0
REM Look for subdirectory "py-code" in current directory and all subdirectories
set EXE_PATH=%FACTORY_SOURCE%
:try_again
if exist %FACTORY_DRIVE%%EXE_PATH%py-code\DREAM.py ( goto execute )
REM Cut the end of the path
set EXE_PATH=%EXE_PATH:~0,-1%
for %%i in (%EXE_PATH%) do (set EXE_PATH=%%~pi)
if not [%EXE_PATH%]==[\] ( goto try_again )
echo "ERROR: Cannot find program runner. Be sure that in one of subdirectory exist a folder 'py-code' with DREAM.py in it"
goto end_of_batch
:execute
%FACTORY_DRIVE%%EXE_PATH%py-code\DREAM.py %FACTORY_SOURCE% %START_LOCATION% 
:end_of_batch