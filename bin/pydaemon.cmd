@ECHO OFF

SET ScriptDir=%~dp0
SET ScriptDir=%ScriptDir:~0,-1%

IF "%1" == "start" (
    START /MIN "" PYTHON %ScriptDir%\pydaemon-script.py %*
    ECHO Daemon started
)

IF "%1" == "restart" (
    START /MIN "" PYTHON %ScriptDir%\pydaemon-script.py %*
    ECHO Daemon restarted
) 

IF "%1" == "stop" (
    START /MIN "" PYTHON %ScriptDir%\pydaemon-script.py %*
    ECHO Daemon stopped
)

IF "%1" == "list" (
    PYTHON %ScriptDir%\pydaemon-script.py %*
)
