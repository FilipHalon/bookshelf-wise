release: python ./bookshelfwise/manage.py migrate
web: gunicorn --pythonpath bookshelfwise bookshelfwise.wsgi