cd bookshelfwise
release: python manage.py migrate
web: gunicorn bookshelfwise.wsgi:application --log-file -