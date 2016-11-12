import os

CSRF_ENABLED = True
SECRET_KEY = "random-string"
migration_directory = "migrations"
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://dbuser:dbpasswd@db/dbname'
SQLALCHEMY_TRACK_MODIFICATIONS = False
debug = False
