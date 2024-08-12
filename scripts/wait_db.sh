#!/bin/sh

while ! nc -z db 3306 ; do
    echo "Waiting for the Database Server"
    sleep 3
done

python manage.py makemigrations
python manage.py migrate

# If DB is empty, open these commands to insert fixture data to DB
echo "Inserting fixture data.."
chmod +x scripts/create_fixture_data.sh
./scripts/create_fixture_data.sh

# If DB is empty, open these commands to insert dummy data to DB
echo "Inserting dummy data.."
chmod +x scripts/create_dummy_data.sh
./scripts/create_dummy_data.sh

# Start the Django development server with debugpy enabled for debugging
python -m debugpy --listen 0.0.0.0:3000 manage.py runserver 0.0.0.0:8000
# python manage.py runserver 0.0.0.0:8000
