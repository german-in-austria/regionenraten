## Regionenraten (Basierend auf iamDioeVr)

### 1. Start a PostgreSQL container
like this:
`docker run --name my-postgres -e POSTGRES_PASSWORD=passwort -e POSTGRES_USER=user -e POSTGRES_DB=personendb postgres`

Use ` -p 5432:5432` to expose a port for easy access through a GUI like pgAdmin.

### 2. Start the "Regionenraten" App with a container-link and an exposed port
`docker run -p 3333:80 --env-file=.env --link my-postgres:postgres dioe/regionenraten:stage`

### 3. Setup the App/Database
run these commands from inside the container:
 - `python3.5 /home/docker/code/app/manage.py makemigrations`
 - `python3.5 /home/docker/code/app/manage.py migrate auth`
 - `python3.5 /home/docker/code/app/manage.py migrate`
 - `python3.5 /home/docker/code/app/manage.py createsuperuser`


#### Environment Variables
If none of these are specified, it will fall back to an internal SQLite DB.
Put these into a `.env` file for convenient access.

| Variable              | Example                                      |
|-----------------------|----------------------------------------------|
| REGIONENRATEN_DB          | `django.db.backends.postgresql_psycopg2` |
| REGIONENRATEN_DB_NAME     | `regionenratendb`                        |
| REGIONENRATEN_DB_USER     | `user`                                   |
| REGIONENRATEN_DB_PASSWORD | `passwort`                               |
| REGIONENRATEN_DB_PORT     | `5432`                                   |
| REGIONENRATEN_DB_HOST     | `postgres`                               |
| REGIONENRATEN_STATIC_ROOT | `/static`                                |


### Sonstiges
 - `/admin/` Admin
 - `/updateaudio/` Audiodateien in Datenbank eintragen
