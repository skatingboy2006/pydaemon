# Pydaemon

A library for Python 3 that implements multiple daemons within your project in Python.

## Getting started

### 1. Installation

Download the source code from Github: https://github.com/fomalhaut88/pydaemon
Go into the downloaded directory and execute:

    sudo python3 setup.py install  # for linux
    
    python setup.py install  # for windows
    
### 2. Creating a daemon

Your daemons must be stored in the folder `daemons` in the root of your project. Each daemon should be implemented as a class inherited from `pydaemon.base_daemon.BaseDaemon` and stored in a separate file. There are some specialities regarding the names. The name of class must be in camel notation, and the appropriate file must have same name but in snake notation. For example, you are to develop a daemon called `hi_daemon`:

  1. In the folder `daemons` create a file `hi_daemon.py`
  2. Create the class `HiDaemon` inside the file:
  
    # daemons/hi_daemon.py
    from time import sleep
    from pydaemon.base_daemon import BaseDaemon
    
    class HiDaemon(BaseDaemon):
        def run(self):
            while True:
                print("hi")
                sleep(10)
                
  3. Check the daemon:
  
    $ pydaemon list
    hi_daemon          stopped                 ok
    
### 3. Running and stopping

If you wish to see the list of available daemons:

    $ pydaemon list
    hi_daemon          stopped                 ok
    
To run a daemon:

    $ pydaemon start -n hi_daemon
    
To stop:

    $ pydaemon stop -n hi_daemon
    
To restart:

    $ pydaemon restart -n hi_daemon
    
Pydaemon supports passing yaml-config to your daemon. It can be done this way:

    $ pydaemon start -n hi_daemon -c my/config.yaml
    
Parsed config data is available inside the daemon class through `self._config`.

### 4. Logging

With Pydaemon it is easy to manage your errors because it supports logging. Log information is being stored in:

    ~/.pydaemon/<project_name>/logs/<daemon_name>/
    
where `<project_name>` is the name of the folder where you keep the folder `daemons`.
