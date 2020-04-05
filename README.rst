===============================
Task Office
===============================
Task Office - pet app with using Flask


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


Run Task Office
^^^^^^^^^^^^^^^^^^

To run the app use::

    $ cd <path_to_app_root>
    $ cp .env.example .env

    # run with flask wsgi:
        # install, run postgres, redis, actualize .env
        $ flask run --with-threads
        # type http://127.0.0.1:5000/ in browser

    # run with docker-compose:
        # install Docker, Docker Compose
            # https://docs.docker.com/v17.12/install/
            # https://docs.docker.com/compose/install/
        $ docker-compose up --build
        # type http://localhost/ in browser

Test user credentials::

        username: amigo@gmaill.com
        password: amigo1111


Run the following commands to create your app's
database tables and perform the initial migration ::

    flask db init
    flask db migrate
    flask db upgrade

Translations commands::

    https://pythonhosted.org/Flask-Babel/

    # Create(if not exists) map of translations
    pybabel extract -F babel.cfg -k lazy_gettext -o translations/messages.pot .

    # Init translations(if not exists)
    pybabel init -i messages.pot -d translations -l en
    pybabel init -i messages.pot -d translations -l uk
    pybabel init -i messages.pot -d translations -l ru

    # Update map and translations
    pybabel update -i translations/messages.pot -d translations

    # Compile translations
    pybabel compile -d translations


