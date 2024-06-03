# chmod +x scripts/migrate_db.sh
# ./scripts/migrate_db.sh

# Before running this script, check if you have a migratons folder in every app with an empty __init__.py file

# Apply database migrations
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --no-input
