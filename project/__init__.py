from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager
from flask_migrate import Migrate
#from flask_bootstrap import Bootstrap

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

#def create_app():
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#bootstrap = Bootstrap(app)

# db init
from .models import Callout
from .models import ResponseUnit
from .models import Path
from .models import Waypoint

db.init_app(app)
migrate = Migrate(app, db)

# blueprint for non-auth parts of app
from .callout_handling import callout_handling as callout_handling_blueprint
app.register_blueprint(callout_handling_blueprint)

from .pathfinding_handling import pathfinding_handling as pathfinding_handling_blueprint
app.register_blueprint(pathfinding_handling_blueprint)

from .response_unit_handling import response_unit_handling as response_unit_handling
app.register_blueprint(response_unit_handling)


