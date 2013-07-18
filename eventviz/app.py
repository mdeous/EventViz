# -*- coding: utf-8 -*-

from flask import Flask

import eventviz
from eventviz import settings
from eventviz.assets import setup_assets
from eventviz.db import setup_indexes
from eventviz.views.main import main
from eventviz.views.timeline import timeline
from eventviz.views.search import search

app = Flask(__name__)
app.config.from_object(settings)
app.register_blueprint(main)
app.register_blueprint(timeline, url_prefix='/timeline')
app.register_blueprint(search, url_prefix='/search')

setup_assets(app)

setup_indexes()

@app.context_processor
def current_project():
    return {'current_project': eventviz.project}


if __name__ == '__main__':
    app.run(debug=settings.DEBUG)
