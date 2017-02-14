# run app
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata fixtures/admin.json fixtures/tapwater.json
python3 manage.py compilemessages
gunicorn --workers=1 wasser.wsgi:WSGI_APPLICATION -b :8000