# recreate database
python manage.py makemigrations deadlinemain
# init DB
python manage.py migrate
python populate.py

cd frontend
npm ci
npm run build
cd ..

python manage.py collectstatic
