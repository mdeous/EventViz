# -*- coding: utf-8 -*-

from flask import Flask

from eventviz import settings
from eventviz.views.main import main
from eventviz.views.timeline import timeline

app = Flask(__name__)
app.config.from_object(settings)
app.register_blueprint(main)
app.register_blueprint(timeline, url_prefix='/timeline')

if __name__ == '__main__':
    app.run(debug=True)
