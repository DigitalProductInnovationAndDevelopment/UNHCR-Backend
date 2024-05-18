# chmod +x scripts/migrate_db.sh
# ./scripts/migrate_db.sh

# Clean and prepare the migration folder
folder_path="EndUserManager/migrations"
if [ -d "$folder_path" ]; then
    echo "Folder exists. Deleting..."
    rm -rf "$folder_path"
fi
mkdir -p "$folder_path"

# Apply database migrations
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --no-input
