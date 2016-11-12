from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from konlpy.tag import Twitter as Nlp
from . import config as config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
nlp = Nlp()

from . import models, views
