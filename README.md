# Pydaemon

A cross-platform utilite allowing you to create daemons within your project in Python.
Daemons are called services within in the Pydaemon terminology.
Each service (or daemon) should be implemented as a class in `pydaemonlib/services` inheriting `Service` or `ServicePeriodical`.

`YesService` is already implemented in the source code to show you the example how to do it.

To start a service:

    $ python pydaemon.py start -n YesService     # to start YesService
    $ python pydaemon.py start -a                # to start all implemented services
    
To stop a service:

    $ python pydaemon.py stop -n YesService      # to stop YesService
    $ python pydaemon.py stop -a                 # to stop all implemented services
    
To restart a service:

    $ python pydaemon.py restart -n YesService   # to restart YesService
    $ python pydaemon.py restart -a              # to restart all implemented services
    
In Windows use `pydaemon.cmd` instead with the same arguments.
