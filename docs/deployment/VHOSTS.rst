Apache + mod-wsgi configuration
===============================

An example Apache2 vhost configuration follows::

    WSGIDaemonProcess openklant-<target> threads=5 maximum-requests=1000 user=<user> group=staff
    WSGIRestrictStdout Off

    <VirtualHost *:80>
        ServerName my.domain.name

        ErrorLog "/srv/sites/openklant/log/apache2/error.log"
        CustomLog "/srv/sites/openklant/log/apache2/access.log" common

        WSGIProcessGroup openklant-<target>

        Alias /media "/srv/sites/openklant/media/"
        Alias /static "/srv/sites/openklant/static/"

        WSGIScriptAlias / "/srv/sites/openklant/src/openklant/wsgi/wsgi_<target>.py"
    </VirtualHost>


Nginx + uwsgi + supervisor configuration
========================================

Supervisor/uwsgi:
-----------------

.. code::

    [program:uwsgi-openklant-<target>]
    user = <user>
    command = /srv/sites/openklant/env/bin/uwsgi --socket 127.0.0.1:8001 --wsgi-file /srv/sites/openklant/src/openklant/wsgi/wsgi_<target>.py
    home = /srv/sites/openklant/env
    master = true
    processes = 8
    harakiri = 600
    autostart = true
    autorestart = true
    stderr_logfile = /srv/sites/openklant/log/uwsgi_err.log
    stdout_logfile = /srv/sites/openklant/log/uwsgi_out.log
    stopsignal = QUIT

Nginx
-----

.. code::

    upstream django_openklant_<target> {
      ip_hash;
      server 127.0.0.1:8001;
    }

    server {
      listen :80;
      server_name  my.domain.name;

      access_log /srv/sites/openklant/log/nginx-access.log;
      error_log /srv/sites/openklant/log/nginx-error.log;

      location /500.html {
        root /srv/sites/openklant/src/openklant/templates/;
      }
      error_page 500 502 503 504 /500.html;

      location /static/ {
        alias /srv/sites/openklant/static/;
        expires 30d;
      }

      location /media/ {
        alias /srv/sites/openklant/media/;
        expires 30d;
      }

      location / {
        uwsgi_pass django_openklant_<target>;
      }
    }
