# DT167G Group project VT2019

Twitter clone by Alexander Gillberg, Gustaf Holst, Michaela Hörnfeldt, Anders Jensen-Urstad, Zahra Zaree

## Installation

Python 3.6+ required, [virtualenv](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment) recommended.

After cloning this repository, `cd` into and and install Django and dependencies:

```
pip3 install -r requirements.txt
```

Do database migrations:

```
python3 manage.py makemigrations
python3 manage.py migrate
```

Assemble static files:

```
python3 manage.py collectstatic
```

Run development server:

```
python3 manage.py runserver
```

You should now be able to visit http://127.0.0.1:8000/ in your browser.

To access the administration backend, create an admin user:

```
python3 manage.py createsuperuser
```

You can then access the admin interface on http://127.0.0.1:8000/admin/