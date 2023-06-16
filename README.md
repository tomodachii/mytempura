# mytempura

- cp .env.template .env
- poetry install
- docker compose up -d
- poetry shell
- ./manage.py migrate
- ./manage.py compilemessages
### Test:

coverage run --source='.' manage.py test --no-input && coverage html && coverage report --skip-covered

### DB Design:

./db.vuerd.json

### Celery:

celery -A main worker --beat -l info

### branch naming Convention

https://dev.to/couchcamote/git-branching-name-convention-cch

https://dev.to/i5han3/git-commit-message-convention-that-you-can-follow-1709

upgrade postgres in docker compose
https://betterprogramming.pub/how-to-upgrade-your-postgresql-version-using-docker-d1e81dbbbdf9
```
docker-compose exec {service_name} pg_dumpall -U {postgres_user} > dump.sql
```
Connect to the container's bash terminal
```
docker-compose exec {service_name} bash
```
Now we run the import command
```
psql -U {postgres_user} -d {default_postgres_database} < {mapped_volume_folder_path}/dump.sql
```
We may encounter this error
```
User "postgres" does not have a valid SCRAM secret.
```
 resetting the password for the "postgres" user using the following command:
```  
docker-compose exec db psql -U postgres -c "ALTER USER postgres WITH PASSWORD 'new_password';"
```

celery get task metadata
```
https://stackoverflow.com/a/20551949
```
Export requirement.txt
```
poetry export --without-hashes -f requirements.txt --output requirements.txt
```

### docker-compose.yml explaination
```
worker:
    build: .
    command: watchmedo auto-restart --recursive -p '*.py' -- python -m celery -A main worker --beat -l info
    environment:
      - REDIS_CACHING_HOST=cache
      - REDIS_CACHING_PORT=${REDIS_CACHING_PORT}
    volumes:
      - .:/code
    depends_on:
      - cache
```
The environment variables declared in the docker-compose.yml file will override the values specified in the .env file. 
-> in the updated configuration, the environment variables REDIS_CACHING_HOST=cache and REDIS_CACHING_PORT=6379 will take precedence over the values specified in the .env file.

Regarding the connectivity issue, when you run your application locally on your host machine, services like Redis or PostgreSQL typically run on 127.0.0.1 (localhost) because they are running directly on your host machine. However, within a Docker network created by Docker Compose, each service gets its own isolated network stack, and the service names can be used as hostnames to communicate between services.

In the case of this worker service, it is running within the Docker network created by Docker Compose, and the Redis service is also running within the same network. So, the worker service can access the Redis service using the service name "cache" as the hostname because Docker Compose sets up internal DNS resolution for service names.

-> In the worker service configuration, specifying REDIS_CACHING_HOST=cache means that the worker will connect to the Redis service using the hostname "cache" within the Docker network, rather than trying to connect to 127.0.0.1, which would refer to the worker container itself.

# Multiple language support
First time run:
```
./manage.py makemessages -l vi
./manage.py makemessages -l en
```

This project support multiple language using i18n
Everywhen there are new updates in models -> Things to do:

- Define a verbose_name and verbose_name_plural in new model's Meta.

```
class newModel(ModelBase):
    class Meta:
        db_table = 'backend_new_model'
        ordering = ['pk']
        verbose_name = _('new model')
        verbose_name_plural = _('new models')
```

- Define a verbose_name in new model's fields

```
new_field = models.CharField(max_length=256, verbose_name=_('new field'))
```

> verbose_name and verbose_name plural should be in lowercase for consistency
> and separator '\_' should be replaced by ' ' (space)

- Update .po files

```
django-admin makemessages --all
```

- Provide the corresponding translation to the defined verbose_name model and fields by editting .po files

```
vdbc.be
└── locale
    └── <language> # ex: vi, en ...
        └── LC_MESSAGES
            └── django.po
```

- Upload the .po file to `https://poeditor.com/` or edit the .po file with the following syntax

```
#: backend/models/<new_model>.py:11
msgid <verbose_name> #"city"
msgstr <translation> #"thành phố"
```

- Generate .mo files

```
django-admin compilemessages
```