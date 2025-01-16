FROM postgres:15-alpine

# Copia el script de inicialización
COPY init.sql /docker-entrypoint-initdb.d/

# Argumentos de construcción desde el archivo .env
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB
ARG POSTGRES_PORT
ARG PGDATA

# Variables de entorno usando los argumentos
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_DB=$POSTGRES_DB
ENV POSTGRES_PORT=$POSTGRES_PORT
ENV PGDATA=$PGDATA

# # Opcional: Exponemos el puerto de PostgreSQL (ya se mapea en docker-compose)
# EXPOSE $POSTGRES_PORT