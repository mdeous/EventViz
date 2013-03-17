# -*- coding: utf-8 -*-

from flask import Flask

from eventviz import settings
from eventviz.views.main import main

app = Flask(__name__)
app.config.from_object(settings)
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
