# -*- coding: utf-8 -*-
from flask_assets import Bundle


css_all = Bundle(
    "libs/bootstrap/dist/css/bootstrap.css",
    "css/style.css",
    filters="cssmin",
    output="public/css/common.css"
)

js_all = Bundle(
    "libs/jQuery/dist/jquery.js",
    "libs/bootstrap/dist/js/bootstrap.min.js",
    #"js/plugins.js",
    filters='jsmin',
    output="public/js/common.js"
)
