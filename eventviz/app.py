# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.assets import Bundle, Environment

import eventviz
from eventviz import settings
from eventviz.views.main import main
from eventviz.views.timeline import timeline
from eventviz.views.search import search

app = Flask(__name__)
app.config.from_object(settings)
app.register_blueprint(main)
app.register_blueprint(timeline, url_prefix='/timeline')
app.register_blueprint(search, url_prefix='/search')

@app.context_processor
def current_project():
    return {'current_project': eventviz.project}

assets = Environment(app)

js_all = Bundle(
    'js/jquery-1.9.1.js', 'js/jquery.tablesorter.js', 'js/bootstrap.js',
    filters='yui_js', output='js/eventviz.min.js'
)
js_timeline = Bundle(
    'js/timeline.js', 'js/eventviz-timeline.js',
    filters='jsmin', output='js/timeline.min.js'
)
css_all = Bundle(
    'css/bootstrap.css', 'css/bootstrap-responsive.css', 'css/eventviz.css',
    filters='yui_css', output='css/eventviz.min.css'
)
css_timeline = Bundle('css/timeline.css', filters='cssmin', output='css/timeline.min.css')
assets.register('js_all', js_all)
assets.register('js_timeline', js_timeline)
assets.register('css_all', css_all)
assets.register('css_timeline', css_timeline)

if __name__ == '__main__':
    app.run(debug=True)
