release: python3 manage.py collectstatic --noinput
web: python3 manage.py migrate && gunicorn mysite.wsgi --timeout 600