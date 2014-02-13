myHoard_Python
==============

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



#### Tree

```
.
├── myhoard
│   ├── apps
│   │   ├── auth
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── parsers.py
│   │   │   ├── tests.py
│   │   │   └── views.py
│   │   ├── collections
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── parsers.py
│   │   │   ├── tests.py
│   │   │   └── views.py
│   │   └── __init__.py
│   ├── media
│   ├── settings
│   │   ├── common.py
│   │   ├── dev.py
│   │   ├── __init__.py
│   │   ├── prod.py
│   │   └── test.py
│   ├── __init__.py
│   └── urls.py
├── LICENSE
├── manage.py
├── README.md
└── requirements.txt
```