===============================
Task Office
===============================
Task Office - pet app with using Flask


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


Run Task Office
^^^^^^^^^^^^^^^^^^
Before running shell commands, set the ``FLASK_APP`` and ``FLASK_DEBUG``
environment variables ::

    export FLASK_APP=<path_to>/entry.py
    export FLASK_DEBUG=1


Run the following commands to create your app's
database tables and perform the initial migration ::

    flask db init
    flask db migrate
    flask db upgrade

To run the web application use::

    flask run --with-threads

Features
--------

* TODO
