@echo off
set VW_ACTSCRIPT_PATH=%TEMP%\vw-%1.cmd
if EXIST %VW_ACTSCRIPT_PATH% del %VW_ACTSCRIPT_PATH%
python %~dp0\vw-script.py %*
IF EXIST %VW_ACTSCRIPT_PATH% call %VW_ACTSCRIPT_PATH%