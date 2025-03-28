FROM postgres:15

COPY init.sql /docker-entrypoint-initdb.d/
COPY select.sql /docker-entrypoint-initdb.d/

USER postgres 