# -*- coding: utf-8 -*-

import sys, os, pwd

project = "Styles"

# Use instance folder, instead of env variables.
# specify dev/production config
#os.environ['%s_APP_CONFIG' % project.upper()] = ''
# http://code.google.com/p/modwsgi/wiki/ApplicationIssues#User_HOME_Environment_Variable
#os.environ['HOME'] = pwd.getpwuid(os.getuid()).pw_dir

BASE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__))
)
# activate virtualenv
#activate_this = os.path.join(BASE_DIR, "env/bin/activate_this.py")
#execfile(activate_this, dict(__file__=activate_this))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# give wsgi the "application"
from shell import create_app

# default to dev config because no one should use this in
# production anyway
env = os.environ.get('STYLES_ENV', 'dev')
application = create_app('shell.webinterface.settings.%sConfig' % env.capitalize(), env=env)

if __name__ == '__main__':
    application.run()