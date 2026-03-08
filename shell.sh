# recreate database
python manage.py makemigrations deadlinemain
# init DB
python manage.py migrate
python populate.py
npm run build
python manage.py collectstatic