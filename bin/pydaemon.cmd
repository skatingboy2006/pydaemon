@echo off
if "%1" == "start" (
    start /MIN "" python pydaemon %*
) else (
    python pydaemon %*
)
