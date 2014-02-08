myHoard_Python
==============

### Requirements:

 ``pip install -r requirements.txt``

### Run:

``python manage.py runserver --settings=dev``

#### Run parameters

``--settings=dev``
``--settings=prod``
``--settings=test``

#### tree

```
.
├── my_hoard
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
│   ├── templates
│   │   └── apps
│   │       ├── auth
│   │       └── collections
│   ├── __init__.py
│   └── urls.py
├── LICENSE
├── manage.py
├── README.md
└── requirements.txt
```