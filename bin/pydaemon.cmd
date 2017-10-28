@echo off
if "%1" == "start" (
    start /MIN "" python pydaemon.py %*
) else (
    python pydaemon.py %*
)
