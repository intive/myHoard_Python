myHoard_Python
==============

### Prerequisites:

Requires the Pillow library
``http://pillow.readthedocs.org/en/latest/installation.html#linux-installation``

### Requirements:

 ``pip install -r requirements.txt``

#### Environment variable

``MYHOARD_SETTINGS_MODULE``

###### Values

``myhoard.settings.prod``

``myhoard.settings.dev``

``myhoard.settings.test``

### Run:

``python manage.py runserver``


# API
## create a new user
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"username": "krol.julian", "email": "krol.julian@mail.com", "password": "mort1234"}' http://localhost:5000/users/

## get token
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"username": "krol.julian", "password": "mort1234", "grant_type": "password"}' http://localhost:5000/oauth/token/

## get collections
curl -H "Accept: application/json" -H "Content-type: application/json" -H "Authorization: 192aac84-5a65-409b-901b-e10d9faa4509" -X GET http://localhost:5000/collections/

## create a new collection
curl -H "Accept: application/json" -H "Content-type: application/json" -H "Authorization: 192aac84-5a65-409b-901b-e10d9faa4509" -d '{"name": "Kolekcja testowa", "description": "Opis testowy"}' -X POST http://localhost:5000/collections/