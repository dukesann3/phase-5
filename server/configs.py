from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_caching import Cache

cache_config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social_media.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
app.secret_key = '''b'\_5#y2L\"F4Q8z\n\xec]/\''''

db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)
db.init_app(app)
api = Api(app)
bcrypt = Bcrypt(app)

app.config.from_mapping(cache_config)
cache = Cache(app)
