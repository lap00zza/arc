FROM postgres:alpine

COPY create_arc_db.sql /docker-entrypoint-initdb.d/

# The name of the default database in case
# no db is present.
# TODO: need proper initdb procedures
ENV POSTGRES_DB arc
