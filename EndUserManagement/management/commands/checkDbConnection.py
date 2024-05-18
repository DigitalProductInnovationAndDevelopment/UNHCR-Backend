import os
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Custom command to check if there is a working DB connection. (python manage.py checkDbConnection)"

    def handle(self, *args, **options):
        try:
            isMySQL = os.environ.get("MYSQL_ACTIVE", None)
            if not isMySQL:
                raise Exception(
                    "MYSQL_ACTIVE environment variable is not defined!! Make sure that dotenv Python \
                                package is installed and MYSQL_ACTIVE is present in environment variables."
                )
            dbDetails = connection.get_connection_params()
            db = dbDetails["database"] if "database" in dbDetails else ""
            print(f"Target Database: {str(db)}")
            # Perform a simple query to check database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                row = cursor.fetchone()
                if row:
                    print("Database connection is working!")
                else:
                    print("Error: Database connection is not working!")
        except Exception as e:
            print("Error: An error occurred while checking database connection: ", e)
