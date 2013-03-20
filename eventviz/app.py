# -*- coding: utf-8 -*-

from flask import Flask

from eventviz import settings
from eventviz.views.main import main
from eventviz.views.timeline import timeline
from eventviz.views.search import search

app = Flask(__name__)
app.config.from_object(settings)
app.register_blueprint(main)
app.register_blueprint(timeline, url_prefix='/timeline')
app.register_blueprint(search, url_prefix='/search')

if __name__ == '__main__':
    app.run(debug=True)
