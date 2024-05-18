# chmod +x scripts/install_packages.sh
# ./scripts/install_packages.sh
echo "Installing packages.."

source scripts/install_packages.sh
# Activate virtual environment based on the operating system
if [ "$(uname)" == "Darwin" ] || [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    echo "Detected Unix-based system"
    source venv/bin/activate
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ] || [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    echo "Detected Windows system"
    source venv/Scripts/activate
else
    echo "Unsupported operating system"
    exit 1
fi

echo "Creating local database.."
chmod +x scripts/create_local_db.sh
./scripts/create_local_db.sh

echo "Executing migrations.."
chmod +x scripts/migrate_db.sh
./scripts/migrate_db.sh

python manage.py runserver 127.0.0.1:8000 --insecure