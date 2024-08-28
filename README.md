# PII Supplier Masking App

This app uses [marimo](https://marimo.io/), a python notebook library, to build an app for interacting with PII supplier masking data. The app provides edit, add and delete functionality, allowing a user to modify the supplier masking data via a straightforward interface.

## Running the App via Docker
The app and a Microsoft SQL server containing mock data can be spun up using [Docker](https://www.docker.com/). Ensure that Docker and docker-compose is installed and the Docker daemon is running on your system. On Windows, installing and running [Docker Desktop](https://www.docker.com/products/docker-desktop/) is the easiest way to do this. Once installed, invoke
```
docker compose up
```
in the root directory of this repo to build and run the containers, then navigate to http://localhost:8080 to view the app. 

## Development

To modify the app, you'll need to first setup your python environment. The easiest way to do this on Windows is via the following commands:
```
cd .\app\
py -m venv .venv
.venv\Scripts\activate

pip install .
```
Then, start the marimo server in edit mode with the command
```
marimo edit pii_supplier_masking_app.py
```
A prompt will appear, linking to the app in "edit" mode. See the [marimo docs](https://docs.marimo.io/) for guidance on how to modify the behaviour of the app.

To connect to the SQL server, you'll first need to ensure the ODBC 18 drivers are installed. These can be found [here](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16). 

This app uses environment variables specified in a `.env` file to configure database credentials and table names. A working example is provided in this repo, however they can be modified to suit your use case. Currently, the app expects three SQL tables,
1. MASKING_TABLE - The table containing the masking data, including the supplier, it's type and the masking fields. Values with NULL for the SupplierID are presumed to indicate default values.
2. SUPPLIER_ID_TABLE - The table listing all available suppliers. This is used when adding new suppliers to the masking table to infer the available options
3. SUPPLIER_TYPE_ID_TABLE - The table mapping type ID's to their names. This is used to populate the SupplierType column in the masking table.

The synthetic data in the Microsoft SQL server is uploaded via the commands in `mssql_server/setupl.sql`. To customise the database strucutre and data, edit this file, then remove and rebuild the container.