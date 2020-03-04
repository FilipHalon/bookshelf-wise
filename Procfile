release: python ./bookshelfwise/manage.py migrate
web: gunicorn bookshelfwise.wsgi:application --log-file -