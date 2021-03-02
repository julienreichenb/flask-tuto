from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

## Register DB ##
# Credentials & Specs
POSTGRES = {
    'user': 'postgres',
    'pw': 'root',
    'db': 'FlaskBlog',
    'host': '127.0.0.1',
    'port': '5432'
}
# Registering the DB with the ORM
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCBHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

## Register Login Manager ##
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

## Register Blueprints : MUST BE AFTER DB ! ##
from blog.core.views import core
from blog.users.views import users
from blog.posts.views import posts
from blog.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(error_pages)

