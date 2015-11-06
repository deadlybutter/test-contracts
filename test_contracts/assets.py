# -*- coding: utf-8 -*-
from flask_assets import Bundle, Environment

css = Bundle(
    "css/bootstrap.min.css",
    "css/style.css",
    filters="cssmin",
    output="public/css/common.css"
)

js = Bundle(
    "js/jquery-2.1.4.min.js",
    "js/bootstrap.min.js",
    filters='jsmin',
    output="public/js/common.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
