# Choose a python version that you know works with your application
FROM python:3.9-slim-bullseye

RUN apt-get -y update 
RUN apt-get -y install curl 

# Install database drivers
RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc
RUN curl https://packages.microsoft.com/config/debian/11/prod.list | tee /etc/apt/sources.list.d/mssql-release.list
RUN apt-get -y update 
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18
RUN export PATH="$PATH:/opt/mssql-tools18/bin"
RUN apt-get install -y unixodbc-dev
RUN apt-get install -y libgssapi-krb5-2

# Install python requirements
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_HOME='/usr/local'

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app
COPY --link pyproject.toml .
COPY --link poetry.lock .
RUN poetry install

# You may copy more files like csv, images, data
COPY --link ./pii_supplier_masking_app.py .

EXPOSE 8080

# Create a non-root user and switch to it
RUN useradd -m user1
USER user1

CMD [ "marimo", "run", "pii_supplier_masking_app.py", "-p", "8080", "--host", "0.0.0.0"  ]
# CMD ["tail", "-f", "/dev/null"]