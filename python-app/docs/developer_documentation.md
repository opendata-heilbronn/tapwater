---
title: Developer documentation
author: Gregor Schäfer, Benedikt Kurschakte, Florette Chamga, Simon Scheuermann, Rohan Ahmed
geometry: margin=2cm
version: 1.0
---

Status: Final

## Configure Tapwater application
At first you should configure the tapwater application before running it. 
This application is using a json-File for all custom configurations.

### Configuration
1. Go to the directory **config**
1. Copy the **example-config.json** and rename the copied file to **config.json**
1. Configure the config (see Variable description for more information)
    * For docker users: The **host** of every system is the name of the container, given in the **docker-compose.yml**.
    * Example: **"EMAIL_HOST": "mail"** or **"DATABASE_HOST": "db"** 

### Loading a custom configuration
It is also possible to load another custom configuration. Therefore use the following command and replace the path and filename:
```
export CONFIG_FILE=/Path/to/config/filename.json
```

### Variable description
* DEBUG: Accepted values (as Boolean)
    * **true** - Should not used for development, because Django doesn't deliver static content.
    * **false** - This value should be false on your production system.
* ALLOWED_HOSTS: This must be a JSON-List. 
    * The default value ["*"] allows all hosts for the application.
    * Adding more than one host to the application ["*", "127.0.0.1"]
* SECRET_KEY: The default value **false** allows the application to create an random string on each start. Otherwise you can add your own secret key.
    * Example: '4wjz%d7pc5=28r+uyupw%os88s^!7dt3ks9g-!_9yg5f_9^_ve'
* DATABASE_ENGINE: **django.db.backends.postgresql_psycopg2** or **django.db.backends.sqlite3**.
* DATABASE_NAME: Name of the database.
* DATABASE_USER: User for the database.
* DATABASE_PASSWORD: Password for the database.
* DATABASE_HOST: Host address of the database. It's per default configured for **localhost**.
* DATABASE_PORT: Postgres requires a Port for the configuration, which is per default **5432** (as Integer).
* TIME_ZONE: **UTC**
* DEFAULT_FROM_EMAIL: This is the default parameter for the sender address.
    * Example: user@localhost
* EMAIL_USE_SSL: Accepted values (as Boolean)
    * **false**
    * **true**
* EMAIL_USE_TLS: Accepted values (as Boolean)
    * **false**
    * **true**
* EMAIL_HOST: Host address of the database. It's per default configured for **localhost**.
* EMAIL_USER: User for the smtp server.
* EMAIL_PASSWORD: Password for the smtp server,
* EMAIL_PORT: Port for the smtp server. It's per default **25** (as Integer)
* GOOGLE_JAVASCRIPT_API_KEY: Your Google Maps JavaScript API key (for autocomplete function).
* GOOGLE_GEO_API_KEY: Your Google Maps Geocoding API key.
* HERE_MAPS_GEO_APP_CODE: Your Here Maps Geo code.
* HERE_MAPS_GEO_APP_ID: Your Here Maps App id.
* USE_GOOGLE_API: Accepted values (as Boolean)
    * **true** - If you want to use Google for geocoding
    * **false** - If you want to use Here Maps for geocoding

**HINT**: One of the given GEO API's is required for the autocompletion and localization. The API-Key's could be found in the wiki of HHN. 

### Running production system on localhost
Configure the **run_production.sh** in the main directory.

Replace this:
```
gunicorn --workers=1 wasser.wsgi:WSGI_APPLICATION -b :8000
```
with:
```
gunicorn --workers=1 wasser.wsgi:WSGI_APPLICATION -b 127.0.0.1:8000
```

The given address in front of the port is the important difference.

## Production environment without Docker

### Requirements
1. Ubuntu Server

### Build and run
1. ```yes "yes" | ./build_production.sh``` 
1. Start postgres: ```/etc/init.d/postgresql start```
1. Add postgres path to ```~/.profile```
    ```
    PATH=$PATH:/usr/lib/postgresql/{version}/bin
    export PATH
    ```
1. ```. ~/.profile```
1. Run as postgres: ```su - postgres```
1. Create user: ```createuser -P -d nutzername``` 
1. Create database: ```createdb -O nutzername datenbank```
1. Exit postgres: ```exit```
1. Reconfigure your **settings.py** with your database configuration. Database is now "localhost" instead of "db"
1. ```./run_production.sh```

### Configure
1. Set workers in **run_production.sh** to your max limit


## Production environment with Docker

### Requirements
1. Docker
1. Docker-Compose

### Build and run
1. ```docker-compose build```
1. ```docker-compose run web python manage.py makemigrations```
1. ```docker-compose run web python manage.py migrate```
1. ```docker-compose run web python manage.py loaddata fixtures/admin.json fixtures/tapwater.json```
1. ```docker-compose run web python manage.py compilemessages```
1. ```docker-compose -f docker-compose-prod.yml up``` 

### Configure VM
1. Setting Docker VM CPU's to max
1. docker exec -it <:CONTAINER_ID:> bash
 1. ```grep processor /proc/cpuinfo | wc -l``
 1. Edit ```/etc/nginx/nginx.conf```
 1. Set ```worker_processes``` to number of grep-Command
1. Restart containers

## Configure Docker with multiple containers
To generate more containers of this web project, you have to add them to the **docker-compose-prod.yml**.

Replace the following code: 
```
web:
    build: .
    container_name: wasser_web
    command: gunicorn wasser.wsgi:WSGI_APPLICATION -b :8000
    volumes:
      - .:/code
    expose:
          - "8000"
    depends_on:
      - db
```
with:

```
web_a:
    build: .
    container_name: wasser_web
    command: gunicorn wasser.wsgi:WSGI_APPLICATION -b :8000
    volumes:
      - .:/code
    expose:
          - "8000"
    depends_on:
      - db
web_b:
    build: .
    container_name: wasser_web
    command: gunicorn wasser.wsgi:WSGI_APPLICATION -b :8000
    volumes:
      - .:/code
    expose:
          - "8001"
    depends_on:
      - db
```

You also can add gunicorn workers to the project. See the **run_production.sh**.

## Build and run development with Docker
1. ```docker-compose build```
1. ```docker-compose run web python manage.py makemigrations```
1. ```docker-compose run web python manage.py migrate```
1. ```docker-compose run web python manage.py loaddata fixtures/admin.json fixtures/tapwater.json```
1. ```docker-compose run web python manage.py loaddata fixtures/selenium.json```
1. ```docker-compose run web python manage.py compilemessages```
1. ```docker-compose up```

### Build and run development with Docker and SSL Server
(Relevant for working with geolocation services which are sometimes only allowed from secure origins...)

1. Add 'django-sslserver' to the requirements.txt
1. Add 'sslserver' to the INSTALLED_APPS in the settings.py file.
1. ```docker-compose build```
1. ```docker-compose run web python manage.py makemigrations```
1. ```docker-compose run web python manage.py migrate```
1. ```docker-compose run web python manage.py loaddata fixtures/admin.json fixtures/tapwater.json```
1. ```docker-compose run web python manage.py loaddata fixtures/selenium.json```
1. ```docker-compose run web python manage.py compilemessages```
1. ```docker-compose -f docker-compose-dev-ssl.yml up```

The application is now running on port 9000 and can be loaded in the browser by https://localhost:9000 or the IP address can be used.
SSL Warnings given by the browser can be ignored or skipped for development.
