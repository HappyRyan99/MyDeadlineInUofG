echo "prepare python env"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "prepare VUE env"
cd frontend
npm ci
npm run build
cd ..
echo "prepare collectstatic"
python manage.py collectstatic
echo "Done !!!"