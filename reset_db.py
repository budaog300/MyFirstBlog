import os
import django
from django.db import connection
from django.apps import apps

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testsite.settings")
django.setup()

app = apps.get_app_config('shopapp')

with connection.cursor() as cursor:
    # Disable foreign key checks
    cursor.execute('PRAGMA foreign_keys = OFF;')

    # Drop all tables from the app
    for model in app.get_models():
        table = model._meta.db_table
        print(f'Dropping table {table}')
        cursor.execute(f'DROP TABLE IF EXISTS "{table}";')

    # Additionally, clear entries in django_content_type related to the app
    app_label = app.label
    cursor.execute(f'DELETE FROM django_content_type WHERE app_label = "{app_label}";')
    cursor.execute('DELETE FROM auth_permission WHERE content_type_id NOT IN (SELECT id FROM django_content_type);')
    # Drop the django_migrations table
    cursor.execute('DROP TABLE IF EXISTS django_migrations;')

    # Enable foreign key checks
    cursor.execute('PRAGMA foreign_keys = ON;')
