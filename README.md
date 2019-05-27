Install Django and project dependencies:

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

