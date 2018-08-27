import os
base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    ADMIN_PASSWORD = "password"
    SECRET_KEY = 'supersecret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(base_dir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
