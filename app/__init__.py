from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.debug = True

toolbar = DebugToolbarExtension(app)

from app import routes, models
