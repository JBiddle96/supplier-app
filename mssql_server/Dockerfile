# FROM mcr.microsoft.com/mssql/server:2022-latest
FROM mcr.microsoft.com/mssql/server:2022-CU11-ubuntu-22.04
USER root

# Create a config directory
RUN mkdir -p /usr/config
WORKDIR /usr/config

# Bundle config source
COPY . /usr/config

# Grant permissions for to our scripts to be executable
RUN chmod +x /usr/config/entrypoint.sh
RUN chmod +x /usr/config/configure-db.sh

ENTRYPOINT ["./entrypoint.sh"]