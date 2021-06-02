web: gunicorn cybernatics_protetor.wsgi --log-file- --log-level debug
python manage.py collectstatic --noinput
manage.py migrate
