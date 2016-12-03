from flask_bootstrap import Bootstrap
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_security import Security
from flask_assets import Environment

#from styles.models import User

# Setup flask cache
cache = Cache()

# init flask assets
assets_env = Environment()

# Bootstrap
bootstrap = Bootstrap()

# flask security
security = Security()

# flask sqlalchemy
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

debug_toolbar = DebugToolbarExtension()


# flask-social Mine
from shell.webinterface.plugin.social import Social
social = Social()

#login_manager = LoginManager()
#login_manager.login_view = "main.login"
#login_manager.login_message_category = "warning"


#@login_manager.user_loader
#def load_user(userid):
#    return User.query.get(userid)